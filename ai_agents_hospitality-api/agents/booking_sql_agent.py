import os
from sqlalchemy import create_engine, text

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from datetime import date
from sqlalchemy import text

from config.agent_config import get_agent_config


_sql_agent = None

_engine = None

def get_db_uri() -> str:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "bookings-db")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "bookings_db")
    return f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(get_db_uri(), pool_pre_ping=True)
    return _engine

def _get_sql_agent():
    global _sql_agent
    if _sql_agent is None:
        _sql_agent = create_booking_sql_agent()
    return _sql_agent

def create_booking_sql_agent():
    # LLM
    config = get_agent_config()

    if config.provider != "openai":
        raise ValueError("Booking SQL Agent requires provider='openai' (set it in agent_config.yaml)")

    llm = ChatOpenAI(
        model=config.model,
        temperature=config.temperature,
        api_key=config.api_key,
    )

    db = SQLDatabase.from_uri(get_db_uri())

    # Toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # System prompt (MUY importante)
    system_prompt = """
You are an analytics assistant for a hotel booking system.

The database has ONE table called "bookings" with columns:
- id
- hotel_name
- room_id
- room_type
- room_category
- check_in_date
- check_out_date
- total_nights
- guest_first_name
- guest_last_name
- guest_country
- guest_city
- meal_plan
- total_price

Rules:
- Always generate valid PostgreSQL SQL
- Use COUNT, SUM, GROUP BY when needed
- Dates are in YYYY-MM-DD format
- Never guess table or column names

"""

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        system_prompt=system_prompt,
        verbose=False
    )

    return agent

def calculate_occupancy_rate(engine, hotel_name: str, start_date: str, end_date: str, days: int) -> float:
    with engine.connect() as c:
        occupied_nights = c.execute(
            text("""
                SELECT COALESCE(SUM(
                    GREATEST(
                        0,
                        LEAST(check_out_date, CAST(:end_date AS date))
                        - GREATEST(check_in_date, CAST(:start_date AS date))
                    )
                ), 0)
                FROM bookings
                WHERE hotel_name = :hotel
                    AND check_out_date > CAST(:start_date AS date)
                    AND check_in_date < CAST(:end_date AS date)
                """),
                {"hotel": hotel_name, "start_date": start_date, "end_date": end_date},
        ).scalar()

        rooms = c.execute(
            text("""
                SELECT COUNT(DISTINCT room_id)
                FROM bookings
                WHERE hotel_name = :hotel
            """),
            {"hotel": hotel_name},
        ).scalar()

    if not rooms or rooms == 0 or days <= 0:
        return 0.0

    return round((float(occupied_nights) / (rooms * days)) * 100, 2)

def calculate_total_revenue(engine, hotel_name: str, start_date: str, end_date: str) -> float:
    start_d = date.fromisoformat(start_date)
    end_d = date.fromisoformat(end_date)

    with engine.connect() as c:
        revenue = c.execute(
            text("""
                SELECT COALESCE(SUM(
                    total_price * (
                        GREATEST(
                            0,
                            LEAST(check_out_date, :end_date)
                            - GREATEST(check_in_date, :start_date)
                        )::numeric
                        / NULLIF(total_nights, 0)
                    )
                ), 0)
                FROM bookings
                WHERE hotel_name = :hotel
                  AND check_out_date > :start_date
                  AND check_in_date < :end_date
            """),
            {
                "hotel": hotel_name,
                "start_date": start_d,
                "end_date": end_d,
            },
        ).scalar()

    return round(float(revenue or 0), 2)

def calculate_revpar(engine, hotel_name: str, start_date: str, end_date: str, days: int) -> float:

    total_revenue = calculate_total_revenue(engine, hotel_name, start_date, end_date)

    with engine.connect() as c:
        rooms = c.execute(
            text("""
                SELECT COUNT(DISTINCT room_id)
                FROM bookings
                WHERE hotel_name = :hotel
            """),
            {"hotel": hotel_name},
        ).scalar()

    if not rooms or rooms == 0 or days <= 0:
        return 0.0

    return round(total_revenue / (rooms * days), 2)

def kpi_occupancy_rate(hotel_name: str, start_date: str, end_date: str, days: int) -> float:
    return calculate_occupancy_rate(get_engine(), hotel_name, start_date, end_date, days)

def kpi_revpar(hotel_name: str, start_date: str, end_date: str, days: int) -> float:
    total_revenue = calculate_total_revenue(get_engine(), hotel_name, start_date, end_date)
    with get_engine().connect() as c:
        rooms = c.execute(
            text("""SELECT COUNT(DISTINCT room_id) FROM bookings WHERE hotel_name = :hotel"""),
            {"hotel": hotel_name},
        ).scalar()

    if not rooms or rooms == 0 or days <= 0:
        return 0.0

    return round(total_revenue / (rooms * days), 2)

def answer_booking_question_sql(question: str) -> str:
    agent = _get_sql_agent()
    result = agent.invoke({"input": question})

    if isinstance(result, dict) and "output" in result:
        return result["output"]
    return str(result)
