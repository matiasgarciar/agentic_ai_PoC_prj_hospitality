"""Module for writing booking data to output files in various formats (JSON, Excel, MD)."""

import json
import re
from io import TextIOWrapper
from typing import cast, Dict, List, Any
import pandas as pd

def generate_file_json_for_bookings(
    bookings: Dict[str, Any],
    hotel_key: str,
    hotel_name: str,
    output_path: str
) -> None:
    """Generate a JSON file containing booking data for a specific hotel.

    Args:
        bookings: Dictionary containing booking data with 'Bookings' key
        hotel_key: Unique identifier for the hotel
        hotel_name: Name of the hotel
        output_path: Directory path where the file will be saved

    Returns:
        None
    """
    filename = (
        f"{output_path}"
        f"{generate_hotel_bookings_filename(hotel_key, hotel_name)}.json"
    )
    print(f"filename JSON bookings: {filename}")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(bookings, cast(TextIOWrapper, file), indent=4, ensure_ascii=False)

def generate_file_excel_for_bookings(
    bookings: Dict[str, Any],
    hotel_key: str,
    hotel_name: str,
    output_path: str
) -> None:
    """Generate an Excel file containing booking data for a specific hotel.

    Args:
        bookings: Dictionary containing booking data with 'Bookings' key
        hotel_key: Unique identifier for the hotel
        hotel_name: Name of the hotel
        output_path: Directory path where the file will be saved

    Returns:
        None
    """
    df = pd.DataFrame(bookings["Bookings"])
    filename = (
        f"{output_path}"
        f"{generate_hotel_bookings_filename(hotel_key, hotel_name)}.xlsx"
    )
    df.to_excel(filename, index=False)

def generate_file_excel_all_bookings(booking_list, output_path):
    """Generate an Excel file with all booking data.
    
    Args:
        booking_list (list): List of booking dictionaries
        output_path (str): Path to write the Excel file
    """
    # Create a list to store all booking data
    all_bookings = []

    # Extract data from each booking
    for hotel_bookings in booking_list:
        hotel_name = hotel_bookings["HotelName"]
        for booking in hotel_bookings["Bookings"]:
            booking_data = {
                'Hotel Name': hotel_name,
                'Room ID': booking['RoomAssigned'],
                'Room Type': booking['RoomType'],
                'Room Category': booking['RoomCategory'],
                'Check-in Date': booking['CheckInDate'],
                'Check-out Date': booking['CheckOutDate'],
                'Guest First Name': booking['Guest']['FirstName'],
                'Guest Last Name': booking['Guest']['LastName'],
                'Guest Email': booking['Guest']['Email'],
                'Guest Phone': booking['Guest']['Phone'],
                'Guest Country': booking['Guest']['Country'],
                'Guest City': booking['Guest']['City'],
                'Guest Address': booking['Guest']['Address'],
                'Guest Zip Code': booking['Guest']['ZipCode'],
                'Meal Plan': booking['MealPlan'],
                'Total Price': booking['TotalPrice']
            }
            all_bookings.append(booking_data)

    # Create DataFrame and write to Excel
    df = pd.DataFrame(all_bookings)
    df.to_excel(output_path, index=False)
    print(f"Excel file with all bookings written to: {output_path}")

def generate_hotel_bookings_filename(hotel_key: str, hotel_name: str) -> str:
    """Generate a standardized filename for hotel booking data.

    Args:
        hotel_key: Unique identifier for the hotel
        hotel_name: Name of the hotel

    Returns:
        Formatted filename in the format 'hotel_{key}_{camelCaseName}_bookings'
    """
    # Convert hotel name to CamelCase and remove special characters
    camel_case_name = ''.join(
        word.capitalize() for word in re.findall(r'\w+', hotel_name)
    )
    # Generate the filename
    filename = f"hotel_{hotel_key}_{camel_case_name}_bookings"
    return filename

def generate_file_md_hotel_bookings(
    hotel_bookings_list: List[Dict[str, Any]],
    output_path: str
) -> None:
    """Generate a Markdown file containing booking data for multiple hotels.

    Creates a markdown table with booking details including guest information,
    check-in/out dates, room details, and pricing.

    Args:
        hotel_bookings_list: List of dictionaries containing booking data for
            multiple hotels. Each dict must have 'HotelName' and 'Bookings' keys
        output_path: Directory path where the file will be saved

    Returns:
        None
    """
    filename = f"{output_path}hotel_bookings.md"

    with open(filename, "w", encoding="utf-8") as file:
        for hotel_bookings in hotel_bookings_list:
            hotel_name = hotel_bookings["HotelName"]

            file.write(f"# HOTEL - Name: {hotel_name}\n\n")
            file.write("## Bookings\n\n")
            file.write(
                "| Country of Guest | City of Guest | Check-In Date | "
                "Check-Out Date | Room Assigned | Room Category | Room Type | "
                "Meal Plan | Total Price |\n"
            )
            file.write(
                "|------------------|---------------|---------------|"
                "----------------|---------------|---------------|-----------|"
                "-----------|-------------|\n"
            )

            for booking in hotel_bookings["Bookings"]:
                guest_country = booking["Guest"]["Country"]
                guest_city = booking["Guest"]["City"]
                file.write(
                    f"| {guest_country} | {guest_city} | "
                    f"{booking['CheckInDate']} | {booking['CheckOutDate']} | "
                    f"{booking['RoomAssigned']} | {booking['RoomCategory']} | "
                    f"{booking['RoomType']} | {booking['MealPlan']} | "
                    f"{booking['TotalPrice']} |\n"
                )
            file.write("\n---\n\n")
