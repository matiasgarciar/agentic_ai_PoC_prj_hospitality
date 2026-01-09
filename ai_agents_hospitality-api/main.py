"""
FastAPI application for hosting a WebSocket-based chat interface.

This module provides a FastAPI application that serves as a WebSocket server for real-time
communication. It includes endpoints for serving the main web interface
and handling WebSocket connections for chat interactions.

Exercise 0 Implementation:
- Uses LangChain agent with file context (3 hotels sample)
- Falls back to hardcoded responses if agent is unavailable
- Integrates with WebSocket API for real-time chat
"""

import json
import re
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from util.logger_config import logger
from util.configuration import settings, PROJECT_ROOT
from config.agent_config import get_agent_config
from agents.hotel_rag_agent import answer_hotel_question_rag

import asyncio

from datetime import date
import calendar
from agents.booking_sql_agent import (
    answer_booking_question_sql,
    kpi_occupancy_rate,
    kpi_revpar,
)


# Import Exercise 0 agent
EXERCISE_0_AVAILABLE = False
try:
    from agents.hotel_simple_agent import handle_hotel_query_simple, load_hotel_data
    # Try to load hotel data to verify everything is set up correctly
    try:
        load_hotel_data()
        EXERCISE_0_AVAILABLE = True
        logger.info("✅ Exercise 0 agent loaded successfully and hotel data verified")
    except Exception as e:
        logger.warning(f"Exercise 0 agent code loaded but data/files not ready: {e}")
        logger.warning("Will use hardcoded responses until hotel data is available")
        EXERCISE_0_AVAILABLE = False
except ImportError as e:
    logger.warning(f"Exercise 0 agent not available (ImportError): {e}")
    logger.warning("Using hardcoded responses. Install LangChain dependencies if needed.")
    EXERCISE_0_AVAILABLE = False
except Exception as e:
    logger.warning(f"Error loading Exercise 0 agent: {e}. Using hardcoded responses.")
    EXERCISE_0_AVAILABLE = False


# Hardcoded responses for demo queries
HARDCODED_RESPONSES = {
    "list the hotels in france": """Here are the hotels in France:

**Paris:**
- Grand Victoria
- Majestic Plaza
- Obsidian Tower

**Nice:**
- Imperial Crown
- Royal Sovereign""",
    
    "prices for triple premium rooms in paris": """Triple Premium Room prices in Paris:

**Grand Victoria:**
- Peak Season: €450/night
- Off Season: €320/night

**Majestic Plaza:**
- Peak Season: €480/night
- Off Season: €350/night

**Obsidian Tower:**
- Peak Season: €520/night
- Off Season: €380/night""",
    
    "compare the triple room prices at off season for room and breakfast at the hotels in nice": """Triple Room prices at Off Season with Room and Breakfast in Nice:

**Imperial Crown:**
- Standard Triple: €180/night + €25/person breakfast = €255/night total
- Premium Triple: €240/night + €25/person breakfast = €315/night total

**Royal Sovereign:**
- Standard Triple: €190/night + €25/person breakfast = €265/night total
- Premium Triple: €250/night + €25/person breakfast = €325/night total""",
    
    "lowest price for a standard sigle room in nice considering no meal plan": """Lowest price for Standard Single Room in Nice (No Meal Plan):

**Imperial Crown:** €80/night (Off Season)
**Royal Sovereign:** €85/night (Off Season)

The lowest price is at **Imperial Crown** with €80/night during off season.""",
    
    "hotels in paris the meal charge for half board": """Meal charges for Half Board in Paris hotels:

**Grand Victoria:** €45/person/day
**Majestic Plaza:** €50/person/day
**Obsidian Tower:** €55/person/day

*Half Board includes breakfast and dinner*""",
    
    "amount of rooms per type for hotels in paris": """Room distribution by type in Paris hotels:

**Grand Victoria:**
- Single: 30 rooms
- Double: 50 rooms
- Triple: 20 rooms

**Majestic Plaza:**
- Single: 25 rooms
- Double: 45 rooms
- Triple: 30 rooms

**Obsidian Tower:**
- Single: 40 rooms
- Double: 60 rooms
- Triple: 25 rooms""",
    
    "price of a double room standard category in g victoria for peak and off season": """Double Room Standard Category pricing at Grand Victoria:

**Peak Season:** €280/night
**Off Season:** €180/night

Difference: €100/night (35.7% discount in off season)""",
    
    "price for a premium triple room for obsidian tower next october 14th considering room and breakfast and 4 guests": """Price calculation for Premium Triple Room at Obsidian Tower (October 14th):

**Room Rate:** €380/night (Off Season - October)
**Breakfast:** €25/person × 4 guests = €100
**Total:** €480/night

*Note: October is considered off season, and the premium triple room can accommodate up to 4 guests.*"""
}



def find_matching_response(query: str) -> str:
    """
    Find a matching hardcoded response based on the query.
    Uses fuzzy matching to find similar queries.
    
    Args:
        query: User query string
        
    Returns:
        Matching response or default message
    """
    query_lower = query.lower().strip()
    
    # Try exact match first
    if query_lower in HARDCODED_RESPONSES:
        return HARDCODED_RESPONSES[query_lower]
    
    # Try partial matching
    for key, response in HARDCODED_RESPONSES.items():
        # Check if key words are present
        key_words = set(key.split())
        query_words = set(query_lower.split())
        
        # If 60% or more of the key words are in the query
        if len(key_words.intersection(query_words)) / len(key_words) >= 0.6:
            return response
    
    # Default response if no match
    return """I'm a demo API with hardcoded responses. 

Try asking questions about:
- Hotels in France
- Room prices in Paris or Nice
- Meal plans and charges
- Room availability

Example: "list the hotels in France" or "tell me the prices for triple premium rooms in Paris"

*This is a workshop starter - implement your LangChain agent here!*"""

HOTELS = ["Imperial Crown", "Grand Victoria", "Majestic Plaza", "Royal Sovereign", "Obsidian Tower"]

def extract_hotel(query: str):
    q = query.lower()
    for h in HOTELS:
        if h.lower() in q:
            return h
    return None

def parse_period(query: str):
    q = query.lower().strip()

    # Quarter: Q1 2025
    m = re.search(r"\bq([1-4])\s*(20\d{2})\b", q)
    if m:
        quarter = int(m.group(1))
        year = int(m.group(2))
        start_month = 1 + (quarter - 1) * 3
        end_month = start_month + 2
        start = date(year, start_month, 1)
        last_day = calendar.monthrange(year, end_month)[1]
        end = date(year, end_month, last_day)
        end = date.fromordinal(end.toordinal() + 1)  # +1 day => [start, end)
        days = (end - start).days
        return start, end, days

    # Month: January 2025
    months = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
    }
    for name, month in months.items():
        if name in q:
            y = re.search(r"\b(20\d{2})\b", q)
            if not y:
                return None
            year = int(y.group(1))
            start = date(year, month, 1)
            # next month
            if month == 12:
                end = date(year + 1, 1, 1)
            else:
                end = date(year, month + 1, 1)
            days = (end - start).days
            return start, end, days

    return None


async def handle_booking_query_sql(user_query: str) -> str:
    q = user_query.lower()

    wants_occupancy = "occupancy" in q
    wants_revpar = "revpar" in q

    if wants_occupancy or wants_revpar:
        period = parse_period(user_query)
        if not period:
            return "Please specify a period like 'January 2025' or 'Q1 2025'."

        start, end, days = period
        start_s = start.isoformat()
        end_s = end.isoformat()

        by_hotel = ("by hotel" in q) or ("across all hotels" in q) or ("all hotels" in q)

        if by_hotel:
            lines = []
            for h in HOTELS:
                if wants_occupancy:
                    val = kpi_occupancy_rate(h, start_s, end_s, days)
                    lines.append(f"{h}: {val:.2f}%")
                else:
                    val = kpi_revpar(h, start_s, end_s, days)
                    lines.append(f"{h}: {val:.2f}")
            title = "Occupancy rate" if wants_occupancy else "RevPAR"
            return f"{title} by hotel for {start_s} to {end_s}:\n" + "\n".join(lines)

        hotel = extract_hotel(user_query)
        if not hotel:
            return "Please specify the hotel name (e.g., Imperial Crown, Grand Victoria, Majestic Plaza, Royal Sovereign, Obsidian Tower)."

        if wants_occupancy:
            val = kpi_occupancy_rate(hotel, start_s, end_s, days)
            return f"Occupancy rate for {hotel} from {start_s} to {end_s}: {val:.2f}%"

        val = kpi_revpar(hotel, start_s, end_s, days)
        return f"RevPAR for {hotel} from {start_s} to {end_s}: {val:.2f}"

    # Non-KPI -> use SQL agent
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, answer_booking_question_sql, user_query)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown logic.
    """
    logger.info("Starting AI Hospitality API...")
    yield
    logger.info("Shutting down AI Hospitality API...")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))


@app.get("/")
async def get(request: Request):
    """
    Serve the main web interface.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered HTML template for the main interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{uuid}")
async def websocket_endpoint(websocket: WebSocket, uuid: str):
    """
    Handle WebSocket connections for real-time chat.

    This endpoint establishes a WebSocket connection and handles
    bidirectional communication between the client and the server.
    
    Uses Exercise 0 agent (LangChain with file context) if available,
    otherwise falls back to hardcoded responses.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        uuid (str): Unique identifier for the WebSocket connection.
    """
    await websocket.accept()
    logger.info("WebSocket connection opened for %s", uuid)

    try:
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                logger.info(f"Received from {uuid}: {data}")
                
                # Parse the query
                try:
                    message_data = json.loads(data)
                    user_query = message_data.get("content", data)
                except json.JSONDecodeError:
                    user_query = data
                
                # Select agent based on configuration
                try:
                    agent_config = get_agent_config()
                    logger.info(f"Routing with mode={agent_config.mode}")

                    if agent_config.mode == "sql":
                        logger.info(f"Using Exercise 2 (SQL) agent for query: {user_query[:100]}.")
                        response_content = await handle_booking_query_sql(user_query)

                    elif agent_config.mode == "rag":
                        logger.info(f"Using Exercise 1 (RAG) agent for query: {user_query[:100]}...")
                        response_content = answer_hotel_question_rag(user_query)

                    elif EXERCISE_0_AVAILABLE:
                        logger.info(f"Using Exercise 0 agent for query: {user_query[:100]}...")
                        response_content = await handle_hotel_query_simple(user_query)

                    else:
                        logger.warning("No agent available, falling back to hardcoded response")
                        response_content = find_matching_response(user_query)

                except Exception as e:
                    logger.error(f"❌ Error while processing query: {e}", exc_info=True)
                    logger.warning("Falling back to hardcoded response")
                    response_content = find_matching_response(user_query)

                # Send response back to client
                agent_message = {
                    "role": "assistant",
                    "content": response_content
                }
                
                await websocket.send_text(
                    f"JSONSTART{json.dumps(agent_message)}JSONEND"
                )
                logger.info(f"Sent response to {uuid}")
                
            except WebSocketDisconnect:
                logger.info("WebSocket connection closed for %s", uuid)
                break
            except (RuntimeError, ConnectionError) as e:
                logger.error(
                    "Error in WebSocket connection for %s: %s", 
                    uuid, str(e)
                )
                break
    except Exception as e:
        logger.error(
            "Unexpected error in WebSocket for %s: %s", 
            uuid, str(e)
        )
    finally:
        try:
            await websocket.close()
        except (RuntimeError, ConnectionError) as e:
            logger.error(
                "Error closing WebSocket for %s: %s", 
                uuid, str(e)
            )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
