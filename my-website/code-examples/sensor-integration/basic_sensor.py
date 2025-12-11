

"""
Basic Sensor Reading Function

This module provides functions for reading from a temperature sensor.
It includes both real hardware and simulation modes for testing.
"""

import time
import random
from typing import Union, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_temperature_sensor(simulation_mode: bool = True, sensor_type: str = "DHT22") -> Union[float, None]:
    """
    Read temperature from a sensor.

    Args:
        simulation_mode: If True, return simulated values; if False, attempt real hardware read
        sensor_type: Type of sensor to read from

    Returns:
        Temperature in Celsius, or None if reading failed
    """
    if simulation_mode:
        # Simulate temperature reading with some randomness
        base_temp = 22.5  # Base room temperature
        variation = random.uniform(-2.0, 3.0)  # Random variation
        temperature = base_temp + variation
        logger.info(f"Simulated temperature reading: {temperature:.2f}°C")
        return round(temperature, 2)
    else:
        # Real hardware reading would go here
        try:
            # Example using Adafruit DHT sensor library (uncomment when hardware is available)
            # import adafruit_dht
            # import board
            #
            # if sensor_type == "DHT22":
            #     dht = adafruit_dht.DHT22(board.D4)
            # elif sensor_type == "DHT11":
            #     dht = adafruit_dht.DHT11(board.D4)
            #
            # temperature = dht.temperature
            # humidity = dht.humidity
            # logger.info(f"Real sensor reading - Temperature: {temperature}°C, Humidity: {humidity}%")
            # return temperature

            # For now, return a simulated value to indicate the function structure
            logger.warning("Real hardware mode selected but no hardware connected")
            return None

        except ImportError:
            logger.error("Required sensor libraries not installed")
            return None
        except Exception as e:
            logger.error(f"Error reading sensor: {e}")
            return None


def read_humidity_sensor(simulation_mode: bool = True, sensor_type: str = "DHT22") -> Union[float, None]:
    """
    Read humidity from a sensor.

    Args:
        simulation_mode: If True, return simulated values; if False, attempt real hardware read
        sensor_type: Type of sensor to read from

    Returns:
        Humidity percentage, or None if reading failed
    """
    if simulation_mode:
        # Simulate humidity reading with some randomness
        base_humidity = 45.0  # Base room humidity
        variation = random.uniform(-5.0, 5.0)  # Random variation
        humidity = max(0, min(100, base_humidity + variation))  # Clamp between 0-100%
        logger.info(f"Simulated humidity reading: {humidity:.2f}%")
        return round(humidity, 2)
    else:
        # Real hardware reading would go here
        try:
            # Similar to temperature, but for humidity
            logger.warning("Real hardware mode selected but no hardware connected")
            return None

        except ImportError:
            logger.error("Required sensor libraries not installed")
            return None
        except Exception as e:
            logger.error(f"Error reading sensor: {e}")
            return None


def read_multiple_sensors(simulation_mode: bool = True) -> Tuple[Union[float, None], Union[float, None]]:
    """
    Read both temperature and humidity sensors simultaneously.

    Args:
        simulation_mode: If True, return simulated values; if False, attempt real hardware read

    Returns:
        Tuple of (temperature, humidity) or (None, None) if reading failed
    """
    temp = read_temperature_sensor(simulation_mode)
    humidity = read_humidity_sensor(simulation_mode)
    return temp, humidity


def continuous_sensor_reading(interval: float = 2.0, duration: float = 60.0,
                             simulation_mode: bool = True) -> list:
    """
    Perform continuous sensor readings over a specified duration.

    Args:
        interval: Time between readings in seconds
        duration: Total duration to read in seconds
        simulation_mode: If True, use simulated values; if False, use real hardware

    Returns:
        List of (timestamp, temperature, humidity) tuples
    """
    readings = []
    start_time = time.time()

    logger.info(f"Starting continuous sensor reading for {duration} seconds")

    while time.time() - start_time < duration:
        timestamp = time.time()
        temp, humidity = read_multiple_sensors(simulation_mode)

        if temp is not None and humidity is not None:
            readings.append((timestamp, temp, humidity))
            logger.info(f"Reading: T={temp}°C, H={humidity}%")
        else:
            logger.warning("Failed to get sensor reading")

        time.sleep(interval)

    logger.info(f"Completed {len(readings)} readings")
    return readings


def validate_sensor_reading(temperature: Union[float, None],
                           humidity: Union[float, None]) -> bool:
    """
    Validate sensor readings to ensure they're within reasonable ranges.

    Args:
        temperature: Temperature reading in Celsius
        humidity: Humidity reading in percentage

    Returns:
        True if readings are valid, False otherwise
    """
    if temperature is None or humidity is None:
        return False

    # Check if temperature is in reasonable range (-50 to 80 Celsius)
    if not (-50 <= temperature <= 80):
        logger.warning(f"Temperature reading out of range: {temperature}°C")
        return False

    # Check if humidity is in reasonable range (0 to 100%)
    if not (0 <= humidity <= 100):
        logger.warning(f"Humidity reading out of range: {humidity}%")
        return False

    return True


if __name__ == "__main__":
    # Example usage
    print("Testing basic sensor reading functions...")

    # Test single reading
    temp = read_temperature_sensor(simulation_mode=True)
    print(f"Temperature: {temp}°C")

    humidity = read_humidity_sensor(simulation_mode=True)
    print(f"Humidity: {humidity}%")

    # Test multiple readings
    temp, humidity = read_multiple_sensors(simulation_mode=True)
    print(f"Multiple reading: T={temp}°C, H={humidity}%")

    # Validate readings
    is_valid = validate_sensor_reading(temp, humidity)
    print(f"Readings valid: {is_valid}")

    # Test continuous reading (for 10 seconds with 2-second intervals)
    print("\nStarting 10-second continuous reading...")
    readings = continuous_sensor_reading(interval=2.0, duration=10.0, simulation_mode=True)
    print(f"Collected {len(readings)} readings")