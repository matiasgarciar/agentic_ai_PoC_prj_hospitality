"""Utility functions for generating parametric hotel and booking data."""

import random

import pandas as pd


def get_rooms_floors(config):
    """
    Generate random number of rooms and floors based on configuration.

    Args:
        config (dict): Configuration dictionary with min/max values for rooms and floors

    Returns:
        tuple: (number of rooms, number of floors)
    """
    num_rooms = random.randint(config["number"]["min"], config["number"]["max"])

    if num_rooms < 100:
        num_floors = min(
            random.randint(config["floors"]["min"], config["floors"]["max"]), 5)
    else:
        num_floors = random.randint(config["floors"]["min"],
                                    config["floors"]["max"])

    return num_rooms, num_floors


def get_room_type_weights(rooms_per_hotel_params):
    """
    Calculate weights for different room types based on configuration parameters.

    Args:
        rooms_per_hotel_params (dict): Parameters for room type distribution

    Returns:
        dict: Weights for each room type (1=single, 2=double, 3=triple)
    """
    room_types = {
        1: rooms_per_hotel_params['weight_single_rooms'],
        2: rooms_per_hotel_params['weight_double_rooms'],
        3: rooms_per_hotel_params['weight_triple_rooms']
    }

    weights = {}
    total_target = 1.0

    for room_type, data in room_types.items():
        min_weight = data['min'] / 100
        max_weight = data['max'] / 100
        weight = round(random.uniform(min_weight, max_weight), 2)
        weights[room_type] = weight

    # Verificar que weights es un diccionario
    assert isinstance(weights, dict), "weights debe ser un diccionario"

    total_weight = sum(weights.values())
    for room_type, _ in weights.items():
        weights[room_type] = round(weights[room_type] / total_weight, 2)

    total_weight = sum(weights.values())
    difference = total_target - total_weight

    while abs(difference) > 0.001:
        default_room_type = next(
            (room_type for room_type, data in room_types.items()
             if data.get('default', False)), None
        )
        if default_room_type:
            weights[default_room_type] += difference
            weights[default_room_type] = max(0, min(1, weights[default_room_type]))
        else:
            for room_type, _ in weights.items():
                weights[room_type] += difference / len(weights)
                weights[room_type] = max(0, min(1, weights[room_type]))

        total_weight = sum(weights.values())
        difference = total_target - total_weight

    return weights


def get_room_guests(room_type_weights):
    """
    Select a room type based on the provided weights.

    Args:
        room_type_weights (dict): Weights for each room type

    Returns:
        int: Selected room type (1=single, 2=double, 3=triple)
    """
    rand_num = random.random()
    cumulative_weight = 0

    for room_type, weight in room_type_weights.items():
        cumulative_weight += weight
        if rand_num < cumulative_weight:
            return room_type

    # Default return if no room type is selected (should never happen with proper weights)
    return 1  # Return single room as default


def get_room_type_name(guests):
    """
    Convert room type number to name.

    Args:
        guests (int): Room type number (1=single, 2=double, 3=triple)

    Returns:
        str: Room type name
    """
    translate_guest_room_type = {
        1: "Single",
        2: "Double",
        3: "Triple"
    }
    return translate_guest_room_type[guests]


def get_room_category_premium_weight(config):
    """
    Get random weight for premium room category.

    Args:
        config (dict): Configuration with min/max values for premium room weight

    Returns:
        float: Weight for premium room category (0-1)
    """
    return (random.randint(config["weight_premium_rooms"]["min"],
                           config["weight_premium_rooms"]["max"])) / 100


def get_room_category(room_category_premium_weight):
    """
    Select room category based on premium weight.

    Args:
        room_category_premium_weight (float): Weight for premium category (0-1)

    Returns:
        str: Selected room category ("Standard" or "Premium")
    """
    return random.choices(
        ["Standard", "Premium"],
        weights=[1 - room_category_premium_weight, room_category_premium_weight],
        k=1
    )[0]


def get_standard_low_season_prices(pricing_config):
    """
    Generate standard low season prices for different room types.

    Args:
        pricing_config (dict): Configuration with price ranges for each room type

    Returns:
        dict: Prices for each room type (1=single, 2=double, 3=triple)
    """
    single_price = random.randint(
        pricing_config["single_room_standard_low_season"]["min"],
        pricing_config["single_room_standard_low_season"]["max"]
    )
    double_price = random.randint(
        pricing_config["double_room_standard_low_season"]["min"],
        pricing_config["double_room_standard_low_season"]["max"]
    )
    triple_price = random.randint(
        pricing_config["triple_room_standard_low_season"]["min"],
        pricing_config["triple_room_standard_low_season"]["max"]
    )

    # Ensure price constraints
    double_price = max(float(double_price), single_price * 1.5)
    triple_price = max(float(triple_price), double_price * 1.5)

    return {
        1: single_price,
        2: double_price,
        3: triple_price,
    }


def get_premium_increase(pricing_config):
    """
    Get random premium price increase percentage.

    Args:
        pricing_config (dict): Configuration with min/max values for premium increase

    Returns:
        int: Premium price increase percentage
    """
    return random.randint(
        pricing_config["premium_price_increase_percentage"]["min"],
        pricing_config["premium_price_increase_percentage"]["max"]
    )


def get_high_season_increase(pricing_config):
    """
    Get random high season price increase percentage.

    Args:
        pricing_config (dict): Configuration with min/max values for high season increase

    Returns:
        int: High season price increase percentage
    """
    return random.randint(
        pricing_config["peak_season_price_increase_percentage"]["min"],
        pricing_config["peak_season_price_increase_percentage"]["max"]
    )


def get_category_price(category, base_price, premium_increase):
    """
    Calculate price based on room category and premium increase.

    Args:
        category (str): Room category ("Standard" or "Premium")
        base_price (float): Base price for the room
        premium_increase (int): Premium price increase percentage

    Returns:
        float: Calculated price
    """
    if category == "Premium":
        return round(base_price * (premium_increase / 100 + 1), 2)
    return base_price


def get_hotel_mealplan_weight(config):
    """
    Calculate weights for different meal plans based on configuration.

    Args:
        config (dict): Configuration with meal plan parameters

    Returns:
        dict: Weights for each meal plan
    """
    meal_plans = config['meal_plans_weight']
    pesos = {}
    total_target = 1.0  # El objetivo es que la suma de los pesos sea 1.0

    for plan, data in meal_plans.items():
        min_weight = data['min'] / 100
        max_weight = data['max'] / 100
        weight = round(random.uniform(min_weight, max_weight), 2)
        pesos[plan] = {'name': data['name'], 'weight': weight}

    # Normalizar los pesos para que sumen 1
    total_weight = sum(plan_data['weight'] for plan_data in pesos.values())
    for plan, plan_data in pesos.items():
        plan_data['weight'] = round(plan_data['weight'] / total_weight, 2)

    # Ajuste final (iterativo para evitar pesos negativos)
    total_weight = sum(plan_data['weight'] for plan_data in pesos.values())
    difference = total_target - total_weight

    while abs(difference) > 0.001:  # Tolerancia para evitar bucles infinitos por redondeo
        default_plan = next(
            (plan for plan, data in meal_plans.items()
             if data.get('default', False)), None
        )
        if default_plan:
            plan_data = pesos[default_plan]
            plan_data['weight'] += difference
            plan_data['weight'] = max(
                0.0, min(1.0, float(plan_data['weight']))
            )  # Rango 0-1
        else:
            # Distribuir la diferencia proporcionalmente (sin pesos negativos)
            for plan, plan_data in pesos.items():
                plan_data['weight'] += difference / len(pesos)
                plan_data['weight'] = max(
                    0.0, min(1.0, float(plan_data['weight']))
                )  # Rango 0-1

        total_weight = sum(plan_data['weight'] for plan_data in pesos.values())
        difference = total_target - total_weight

    return pesos


def get_meal_plan(pesos):
    """
    Select a meal plan based on the provided weights.

    Args:
        pesos (dict): Weights for each meal plan

    Returns:
        str: Selected meal plan name
    """
    rand_num = random.random()
    cumulative_weight = 0

    for _, data in pesos.items():
        cumulative_weight += data['weight']
        if rand_num < cumulative_weight:
            return data['name']

    # Default return if no meal plan is selected (should never happen with proper weights)
    return list(pesos.values())[0]['name']  # Return first meal plan as default


def get_work_travel():
    """
    Determine if the booking is for work travel.

    Returns:
        str: "Yes" or "No"
    """
    return random.choices(["Yes", "No"], weights=[30, 70], k=1)[0]


def get_free_cancellation():
    """
    Determine if the booking has free cancellation.

    Returns:
        str: "Yes" or "No"
    """
    return random.choices(["Yes", "No"], weights=[40, 60], k=1)[0]


def get_promotion():
    """
    Determine if the booking has a promotion.

    Returns:
        str: "Yes" or "No"
    """
    return random.choices(["Yes", "No"], weights=[20, 80], k=1)[0]


def get_non_refundable():
    """
    Determine if the booking is non-refundable.

    Returns:
        str: "Yes" or "No"
    """
    return random.choices(["Yes", "No"], weights=[30, 70], k=1)[0]


def get_cancellation_fee(non_refundable):
    """
    Get cancellation fee based on refund policy.

    Args:
        non_refundable (str): "Yes" or "No"

    Returns:
        str: Cancellation fee percentage or "N/A"
    """
    if non_refundable == "Yes":
        return "N/A"
    return random.choices(["15%", "25%", "35%"], weights=[20, 50, 30], k=1)[0]


def get_cancellation_status():
    """
    Determine if the booking is cancelled.

    Returns:
        str: "Cancelled" or "Active"
    """
    return random.choices(["Cancelled", "Active"], weights=[5, 95], k=1)[0]


def get_number_of_guests(room_type):
    """
    Determine number of guests based on room type.

    Args:
        room_type (int): Room type (1=single, 2=double, 3=triple)

    Returns:
        int: Number of guests
    """
    if room_type == 1:
        return 1
    if room_type == 2:
        return random.choices([1, 2], weights=[10, 90], k=1)[0]
    if room_type == 3:
        return random.choices([2, 3], weights=[10, 70], k=1)[0]

    # Default return if room_type is invalid
    return 1  # Return 1 guest as default


def get_extra_bed(room_type):
    """
    Determine if an extra bed is needed based on room type.

    Args:
        room_type (int): Room type (1=single, 2=double, 3=triple)

    Returns:
        str: "Yes", "No", or "N/A"
    """
    if room_type == 1:
        return "N/A"
    if room_type == 2:
        return random.choices(["Yes", "No"], weights=[5, 95], k=1)[0]
    if room_type == 3:
        return random.choices(["Yes", "No"], weights=[5, 95], k=1)[0]

    # Default return if room_type is invalid
    return "No"  # Return "No" as default


def get_meal_plan_prices(meal_plans_weight):
    """
    Calculate price multipliers for different meal plans.

    Args:
        meal_plans_weight (dict): Configuration for meal plans

    Returns:
        dict: Price multipliers for each meal plan
    """
    meal_plan_prices = {}
    for _, plan_data in meal_plans_weight.items():
        min_increase = plan_data["price_increase_percentage"]["min"]
        max_increase = plan_data["price_increase_percentage"]["max"]
        price_increase = random.randint(min_increase, max_increase)
        meal_plan_prices[plan_data["name"]] = round((price_increase/100)+1, 2)
    return meal_plan_prices


def get_total_price(booking, room, peak_season_months, hotel_synthetic_params):
    """
    Calculate total price for a booking.

    Args:
        booking (dict): Booking information
        room (dict): Room information
        peak_season_months (list): List of peak season months
        hotel_synthetic_params (dict): Hotel parameters

    Returns:
        float: Total price for the booking
    """
    # Initialize booking parameters
    booking_params = {
        'check_in': pd.Timestamp(booking["CheckInDate"]),
        'check_out': pd.Timestamp(booking["CheckOutDate"]),
        'num_guests': booking["NumberOfGuests"],
        'extra_bed': booking["ExtraBed"],
        'meal_plan': booking["MealPlan"],
        'promotion': booking["Promotion"]
    }

    # Initialize price parameters
    price_params = {
        'base_off': room["PriceOffSeason"],
        'base_peak': room["PricePeakSeason"],
        'room_type': room["Type"],
        'room_capacity': {"Single": 1, "Double": 2, "Triple": 3}
    }

    # Apply occupancy discount
    occupancy_discount = 1 - (hotel_synthetic_params["OccupancyBaseDiscountPercentage"] / 100)
    if price_params['room_type'] in price_params['room_capacity']:
        room_capacity = price_params['room_capacity'][price_params['room_type']]
        if booking_params['num_guests'] < room_capacity:
            price_params['base_off'] *= occupancy_discount
            price_params['base_peak'] *= occupancy_discount

    # Apply extra bed increase
    extra_bed_increase = 1 + (hotel_synthetic_params["ExtraBedChargePercentage"] / 100)
    if booking_params['extra_bed'] == "Yes":
        price_params['base_off'] *= extra_bed_increase
        price_params['base_peak'] *= extra_bed_increase

    # Apply meal plan increase
    meal_plan_increase = hotel_synthetic_params["MealPlanPrices"][booking_params['meal_plan']]
    price_params['base_off'] *= meal_plan_increase
    price_params['base_peak'] *= meal_plan_increase

    # Calculate total price
    total_price = 0
    current_date = booking_params['check_in']
    while current_date < booking_params['check_out']:
        is_peak_season = current_date.strftime("%B") in peak_season_months
        daily_price = price_params['base_peak'] if is_peak_season else price_params['base_off']
        total_price += daily_price
        current_date += pd.Timedelta(days=1)

    # Apply promotion discount
    if booking_params['promotion'] == "Yes":
        total_price *= (1 - (hotel_synthetic_params["PromotionPriceDiscount"] / 100))

    return round(total_price, 2)
