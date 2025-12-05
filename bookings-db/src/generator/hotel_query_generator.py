"""Module for generating natural language queries about hotel rooms and bookings."""

import random
from itertools import combinations
from typing import List, Tuple, Dict, Optional


def get_random_hotel_filters(hotel_names: List[str], num_filters: int) -> List[str]:
    """
    Generate random hotel filters.

    Args:
        hotel_names (List[str]): List of hotel names
        num_filters (int): Number of filters to generate

    Returns:
        List[str]: List of hotel filters
    """
    hotel_filters = []
    for _ in range(num_filters):
        hotel_filters.append(f"'{random.choice(hotel_names)}'")
    return hotel_filters


def get_random_hotel_filters_multiple(
    hotel_names: List[str], num_filters: int
) -> List[str]:
    """
    Generate random multiple hotel filters.

    Args:
        hotel_names (List[str]): List of hotel names
        num_filters (int): Number of filters to generate

    Returns:
        List[str]: List of multiple hotel filters
    """
    hotel_filters = []
    for _ in range(num_filters):
        num_hotels = random.randint(2, 3)
        selected_hotels = random.sample(hotel_names, num_hotels)
        if num_hotels == 2:
            combined_hotels = f"'{selected_hotels[0]}' and '{selected_hotels[1]}'"
        else:
            combined_hotels = (
                f"'{selected_hotels[0]}', '{selected_hotels[1]}', and '{selected_hotels[2]}'"
            )
        hotel_filters.append(combined_hotels)
    return hotel_filters


def get_random_hotel_tuple_filters(
    hotel_names: List[str], num_filters: int
) -> List[Tuple[str, str]]:
    """
    Generate random hotel tuple filters.

    Args:
        hotel_names (List[str]): List of hotel names
        num_filters (int): Number of filters to generate

    Returns:
        List[Tuple[str, str]]: List of hotel tuple filters
    """
    hotel_filters = []
    hotel_tuples = list(combinations(hotel_names, 2))
    for _ in range(num_filters):
        selected_hotels = random.choice(hotel_tuples)
        hotel_filters.append(selected_hotels)
    return hotel_filters


def get_random_queries(p_queries: List[str], num_queries: int) -> List[str]:
    """
    Generate random queries from a pool of queries.

    Args:
        p_queries (List[str]): Pool of queries
        num_queries (int): Number of queries to generate

    Returns:
        List[str]: List of random queries
    """
    random_queries = []
    for _ in range(num_queries):
        random_queries.append(random.choice(p_queries))
    return random_queries


class HotelQueryGenerator:
    """Generator class for hotel queries."""

    _instance: Optional['HotelQueryGenerator'] = None

    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(HotelQueryGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self, queries_config: Dict):
        """
        Initialize the generator with configuration.

        Args:
            queries_config (Dict): Configuration dictionary

        Raises:
            ValueError: If required query lists are empty
        """
        if not hasattr(self, 'initialized'):
            self.hotels: List[str] = []
            room_queries = queries_config.get('room_queries', {})
            self.hotel_room_queries: List[str] = room_queries.get('hotel', [])
            self.hotel_compare_queries: List[str] = room_queries.get('hotel_compare', [])
            self.organization_room_queries: List[str] = room_queries.get('organization', [])
            self.num_queries: int = room_queries.get('number', 20)
            self.initialized = True

        if not self.hotel_room_queries:
            raise ValueError(
                "The list of hotel room queries is empty in the configuration file."
            )
        if not self.organization_room_queries:
            raise ValueError(
                "The list of organization room queries is empty in the configuration file."
            )

    def get_room_queries(self, hotel_names: Optional[List[str]] = None) -> List[str]:
        """
        Generate room queries.

        Args:
            hotel_names (Optional[List[str]]): List of hotel names

        Returns:
            List[str]: List of generated queries
        """
        queries = []

        # Calculate query distribution
        query_distribution = {
            'direct': int(self.num_queries * 0.50),
            'multiple': int(self.num_queries * 0.20),
            'compare': int(self.num_queries * 0.20),
            'org': min(int(self.num_queries * 0.15), 10)
        }

        # Generate direct hotel queries
        direct_queries = {
            'filters': get_random_hotel_filters(hotel_names, query_distribution['direct']),
            'templates': get_random_queries(self.hotel_room_queries, query_distribution['direct'])
        }
        for hotel, question in zip(direct_queries['filters'], direct_queries['templates']):
            queries.append(question.replace("{hotel_filter}", hotel))

        # Generate multiple hotel queries
        multiple_queries = {
            'filters': get_random_hotel_filters_multiple(hotel_names,
                                                         query_distribution['multiple']),
            'templates': get_random_queries(self.hotel_room_queries, query_distribution['multiple'])
        }
        for hotel, question in zip(multiple_queries['filters'], multiple_queries['templates']):
            queries.append(question.replace("{hotel_filter}", hotel))

        # Generate comparison queries
        compare_queries = {
            'filters': get_random_hotel_tuple_filters(hotel_names, query_distribution['compare']),
            'templates': get_random_queries(self.hotel_compare_queries,
                                            query_distribution['compare'])
        }
        for i in range(query_distribution['compare']):
            question = compare_queries['templates'][i].replace(
                "{hotel_filter_a}", compare_queries['filters'][i][0]
            ).replace("{hotel_filter_b}", compare_queries['filters'][i][1])
            queries.append(question)

        # Generate organization queries
        org_queries = get_random_queries(
            self.organization_room_queries, query_distribution['org']
        )
        queries.extend(org_queries)

        return queries


if __name__ == "__main__":
    t_hotel_names = [
        "Royal Sovereign", "Grand Victoria", "Imperial Crown",
        "Majestic Plaza", "Regal Chambers", "Sovereign Suites",
        "Chancellor's Retreat", "Ambassador's Residence"
    ]
    # Example configuration based on the provided YAML structure
    t_queries_config = {
        'room_queries': {
            'number': 30,
            'hotel': [
                "How many total rooms are there in {hotel_filter}?",
                "What is the number of floors in {hotel_filter}?",
                "How many rooms are available per floor in {hotel_filter}?",
                "How many individual rooms are there in {hotel_filter}?",
                "What is the distribution of rooms by type (individual, double, triple) "
                "on each floor in {hotel_filter}?",
                "What is the ratio of standard vs luxury rooms in {hotel_filter}?",
                "How many triple rooms are available on the top floor in {hotel_filter}?",
                "What is the most common room type in {hotel_filter}?",
                "How much is the surcharge for an extra bed in a standard room in "
                "{hotel_filter}?",
                "What is the difference in price between peak and low season for a "
                "single room in {hotel_filter}?",
                "What is the weekend occupancy target for July in {hotel_filter}?",
                "Does {hotel_filter} offer any special pricing for long stays?",
                "Is there a discount for early bookings in {hotel_filter}?",
                "Is there a surcharge for last-minute bookings in {hotel_filter}?",
                "Does {hotel_filter} have different prices for weekdays and weekends?",
                "Are there any additional fees for extra guests in {hotel_filter}?"
            ],
            'hotel_compare': [
                "What is the difference in the number of rooms between {hotel_filter_a} "
                "and {hotel_filter_b}?",
                "How does the number of floors compare between {hotel_filter_a} and "
                "{hotel_filter_b}?",
                "Which hotel has more rooms available per floor, {hotel_filter_a} or "
                "{hotel_filter_b}?",
                "What is the difference in the number of individual rooms between "
                "{hotel_filter_a} and {hotel_filter_b}?",
                "How does the distribution of room types (individual, double, triple) "
                "compare between {hotel_filter_a} and {hotel_filter_b}?",
                "Which hotel has a higher ratio of standard vs luxury rooms, "
                "{hotel_filter_a} or {hotel_filter_b}?",
                "How many more triple rooms are available on the top floor in "
                "{hotel_filter_a} compared to {hotel_filter_b}?",
                "Which hotel has more rooms with balconies or special views, "
                "{hotel_filter_a} or {hotel_filter_b}?",
                "Are there more rooms with special accessibility features in "
                "{hotel_filter_a} or {hotel_filter_b}?",
                "Which hotel has more rooms available for families, {hotel_filter_a} "
                "or {hotel_filter_b}?",
                "How do the prices for a luxury room in peak season compare between "
                "{hotel_filter_a} and {hotel_filter_b}?",
                "What is the price difference for a standard double room in peak "
                "season between {hotel_filter_a} and {hotel_filter_b}?",
                "Which hotel offers a better discount for early bookings, "
                "{hotel_filter_a} or {hotel_filter_b}?",
                "How does the surcharge for last-minute bookings compare between "
                "{hotel_filter_a} and {hotel_filter_b}?",
                "Which hotel has different prices for weekdays and weekends, "
                "{hotel_filter_a} or {hotel_filter_b}?",
                "Are there more additional fees for extra guests in {hotel_filter_a} "
                "or {hotel_filter_b}?"
            ],
            'organization': [
                "How many total rooms are there?",
                "What is the number of floors?",
                "How many rooms are available per floor?",
                "How many individual rooms are there?",
                "What is the distribution of rooms by type (individual, double, triple)?",
                "What is the ratio of standard vs luxury rooms?",
                "How many rooms have balconies or special views?",
                "How many rooms are available for families?",
                "Are there any connecting rooms for families or groups?",
                "How many rooms are available with ocean/city views?",
                "What is the price range for a standard double room in peak season?",
                "What is the minimum and maximum price range for a double room in "
                "low season?",
                "How much does a single room cost during peak season?",
                "What is the discount applied if there are fewer guests than the "
                "room capacity?",
                "What percentage increase does a luxury room have compared to a "
                "standard room?",
                "How much is the surcharge for an extra bed in a standard room?",
                "What is the difference in price between peak and low season for a "
                "single room?",
                "What is the weekend occupancy target for July?",
                "Does the organization offer any special pricing for long stays?",
                "Is there a discount for early bookings?",
                "Is there a surcharge for last-minute bookings?",
                "Does the organization have different prices for weekdays and weekends?",
                "Are there any additional fees for extra guests?"
            ]
        }
    }

    # Test the behavior of the HotelQueryGenerator class
    generator = HotelQueryGenerator(t_queries_config)

    try:
        res_queries = generator.get_room_queries(t_hotel_names)
        if res_queries:
            print("Room queries generated successfully.")
            for query in res_queries:
                print(query)
        else:
            print("No room queries generated.")
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error generating room queries: {e}")
