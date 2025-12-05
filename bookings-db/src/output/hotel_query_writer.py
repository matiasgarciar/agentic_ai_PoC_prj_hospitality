"""Module for writing hotel queries to output files."""

from typing import List

import pandas as pd

def generate_file_csv_for_queries_room_hotels(queries: List[str], output_path: str) -> None:
    """Generate a CSV file containing hotel room queries.

    Args:
        queries: List of query strings to write
        output_path: Path to save the CSV file
    """
    # Create a pandas DataFrame with the queries
    df = pd.DataFrame(queries, columns=["Query"])

    # Save the DataFrame to a CSV file
    filename = f"{output_path}hotel_room_queries.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
