"""Module for generating synthetic hotel names, locations, and guest information."""

import os
import random
from typing import Dict, Tuple, Optional

import yaml
from faker import Faker


class HotelNameLocationGenerator:
    """Generator class for hotel names, locations and guest information."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(HotelNameLocationGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_path=None, config_filename="hotel_naming_location.yaml"):
        """Initialize the generator with configuration data."""
        if not hasattr(self, 'initialized'):
            self._state = {
                'current_hotel_index': 0,
                'existing_keys': set(),
                'existing_addresses': set()
            }
            self._load_hotel_naming_location(base_path, config_filename)
            self.initialized = True

    def _load_hotel_naming_location(self, base_path, config_filename) -> None:
        """
        Load hotel naming and location configuration from YAML file.

        Args:
            base_path (str): Base path for the configuration file
            config_filename (str): Name of the configuration file

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            RuntimeError: If there's an error reading the file
            ValueError: If hotel names list is empty
        """
        file_path = os.path.join(base_path, config_filename) if base_path else config_filename
        print(f"config Hotel Naming Location: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The configuration file '{file_path}' does not exist.")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)

                # hotel names
                name_list = [
                    name for name in config.get('hotel_names', [])
                    if "'" not in name
                ]
                self._hotel_names = name_list
                # hotel countries
                self._hotel_locations = config.get('hotel_location', [])
                # guest locations
                self._guest_locations = config.get('booking_guest_location', [])

                self.config_dict = config
        except (yaml.YAMLError, IOError) as e:
            raise RuntimeError(
                f"Failed to read the configuration file '{file_path}'"
            ) from e

        if not self._hotel_names:
            raise ValueError("The list of hotel names is empty in the configuration file.")

    def generate_hotel_name(self) -> Optional[str]:
        """
        Generate a unique hotel name.

        Returns:
            Optional[str]: A hotel name or None if no names are available
        """
        if not self._hotel_names:
            return None

        hotel_name = self._hotel_names[self._state['current_hotel_index']]
        self._state['current_hotel_index'] = (
            self._state['current_hotel_index'] + 1
        ) % len(self._hotel_names)
        return hotel_name

    def generate_hotel_key(self) -> str:
        """
        Generate a unique hotel key.

        Returns:
            str: A unique 4-digit hotel key
        """
        while True:
            key = str(random.randint(1, 9999)).zfill(4)
            if key not in self._state['existing_keys']:
                self._state['existing_keys'].add(key)
                return key

    def generate_address(self) -> Dict[str, str]:
        """
        Generate a unique hotel address.

        Returns:
            Dict[str, str]: Address information including country, city, zip code and street
        """
        fake = Faker()
        while True:
            country, city = self.generate_hotel_location()
            address = {
                "Country": country,
                "City": city,
                "ZipCode": fake.zipcode(),
                "Address": fake.street_address(),
            }
            address_tuple = tuple(address.values())
            if address_tuple not in self._state['existing_addresses']:
                self._state['existing_addresses'].add(address_tuple)
                return address

    def generate_hotel_location(self) -> Tuple[str, str]:
        """
        Generate a hotel location.

        Returns:
            Tuple[str, str]: Country and city for the hotel
        """
        country = random.choice(list(self._hotel_locations.keys()))
        city = random.choice(self._hotel_locations[country])
        return country, city

    def generate_guest_location(self) -> Tuple[str, str]:
        """
        Generate a guest location.

        Returns:
            Tuple[str, str]: Country and city for the guest
        """
        country = random.choice(list(self._guest_locations.keys()))
        city = random.choice(self._guest_locations[country])
        return country, city
