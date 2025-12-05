
# DATA STRUCTURE DEFINITIONS

## HOTELS

The JSON files for hotels contain detailed information about each hotel, including its key, name, address, synthetic parameters for the booking generator, and rooms. Below is the structure and description of each field, along with examples.

### Structure

- **hotelkey**: A unique identifier for the hotel.
  - Example: `"1825"`

- **Name**: The name of the hotel.
  - Example: `"Hotel Rodriguez, Figueroa and Sanchez"`

- **Address**: An object containing the address details of the hotel.
  - **Country**: The country where the hotel is located.
    - Example: `"Burundi"`
  - **City**: The city where the hotel is located.
    - Example: `"Lake Joyside"`
  - **ZipCode**: The postal code of the hotel's location.
    - Example: `"11896"`
  - **Address**: The street address of the hotel.
    - Example: `"01338 Anna Stravenue Suite 379"`

- **SyntheticParams**: An object containing various synthetic parameters for the hotel.
  - **OccupancyPeakSeasonWeight**: The occupancy weight during peak season.
    - Example: `80`
  - **OccupancyOffSeasonWeight**: The occupancy weight during off-season.
    - Example: `36`
  - **OccupancyBaseDiscountPercentage**: The base discount percentage for occupancy.
    - Example: `21`
  - **ExtraBedChargePercentage**: The percentage charge for an extra bed.
    - Example: `30`
  - **MealPlanWeights**: An object containing the weights for different meal plans.
    - **room_only**: The weight for the "Room Only" meal plan.
      - **name**: The name of the meal plan.
        - Example: `"Room Only"`
      - **weight**: The weight of the meal plan.
        - Example: `0.12`
    - **room_and_breakfast**: The weight for the "Room and Breakfast" meal plan.
      - **name**: The name of the meal plan.
        - Example: `"Room and Breakfast"`
      - **weight**: The weight of the meal plan.
        - Example: `0.46`
    - **all_inclusive**: The weight for the "All Inclusive" meal plan.
      - **name**: The name of the meal plan.
        - Example: `"All Inclusive"`
      - **weight**: The weight of the meal plan.
        - Example: `0.06`
    - **half_board**: The weight for the "Half Board" meal plan.
      - **name**: The name of the meal plan.
        - Example: `"Half Board"`
      - **weight**: The weight of the meal plan.
        - Example: `0.12`
    - **full_board**: The weight for the "Full Board" meal plan.
      - **name**: The name of the meal plan.
        - Example: `"Full Board"`
      - **weight**: The weight of the meal plan.
        - Example: `0.24`
  - **MealPlanPrices**: An object containing the prices for different meal plans.
    - **Room Only**: The price multiplier for the "Room Only" meal plan.
      - Example: `1.0`
    - **Room and Breakfast**: The price multiplier for the "Room and Breakfast" meal plan.
      - Example: `1.19`
    - **All Inclusive**: The price multiplier for the "All Inclusive" meal plan.
      - Example: `2.1`
    - **Half Board**: The price multiplier for the "Half Board" meal plan.
      - Example: `1.45`
    - **Full Board**: The price multiplier for the "Full Board" meal plan.
      - Example: `1.5`
  - **PromotionPriceDiscount**: The discount percentage for promotional prices, if the booking type is `Promotion: "Yes"`.
    - Example: `13`

- **Rooms**: An array of objects, each representing a room in the hotel.
  - **RoomId**: A unique identifier for the room, composed of the floor number (two digits) and the room number on the floor, separated by a hyphen.
    - Example: `"01-001"`
  - **Category**: The category of the room.
    - Example: `"Standard"` or `"Premium"`
  - **Type**: The type of the room, expected guests
    - Example: `1`, `2`, `3`
  - **PriceOffSeason**: The daily price of the room during the off-season months.
    - Example: `74.0`
  - **PricePeakSeason**: The dailyprice of the room during the peak season months.
    - Example: `112.48`

### Example JSON

```json
{
    "hotelkey": "1825",
    "Name": "Hotel Rodriguez, Figueroa and Sanchez",
    "Address": {
        "Country": "Burundi",
        "City": "Lake Joyside",
        "ZipCode": "11896",
        "Address": "01338 Anna Stravenue Suite 379"
    },
    "SyntheticParams": {
        "OccupancyPeakSeasonWeight": 80,
        "OccupancyOffSeasonWeight": 36,
        "OccupancyBaseDiscountPercentage": 21,
        "ExtraBedChargePercentage": 30,
        "BookingYearStart": 2025,
        "BookingYearEnd": 2025,
        "MealPlanWeights": {
            "room_only": {
                "name": "Room Only",
                "weight": 0.12
            },
            "room_and_breakfast": {
                "name": "Room and Breakfast",
                "weight": 0.46
            },
            "all_inclusive": {
                "name": "All Inclusive",
                "weight": 0.06
            },
            "half_board": {
                "name": "Half Board",
                "weight": 0.12
            },
            "full_board": {
                "name": "Full Board",
                "weight": 0.24
            }
        },
        "MealPlanPrices": {
            "Room Only": 1.0,
            "Room and Breakfast": 1.19,
            "All Inclusive": 2.1,
            "Half Board": 1.45,
            "Full Board": 1.5
        },
        "PromotionPriceDiscount": 13
    },
    "Rooms": [
        {
            "RoomId": "01-001",
            "Category": "Standard",
            "Type": 1,
            "PriceOffSeason": 74.0,
            "PricePeakSeason": 112.48
        },
        {
            "RoomId": "01-002",
            "Category": "Premium",
            "Type": 2,
            "PriceOffSeason": 130.34,
            "PricePeakSeason": 170.11
        }
    ]
}