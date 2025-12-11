"""
Unit tests for sensor integration components.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the code-examples directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../code-examples/sensor-integration'))

from basic_sensor import read_temperature_sensor, read_humidity_sensor, read_multiple_sensors, validate_sensor_reading


class TestSensorIntegration(unittest.TestCase):
    """Unit tests for sensor integration functions."""

    def test_read_temperature_sensor_simulation(self):
        """Test reading temperature in simulation mode."""
        temp = read_temperature_sensor(simulation_mode=True)
        self.assertIsInstance(temp, float)
        self.assertGreaterEqual(temp, 20.0)  # Should be reasonable room temp
        self.assertLessEqual(temp, 27.0)    # Should be reasonable room temp

    def test_read_humidity_sensor_simulation(self):
        """Test reading humidity in simulation mode."""
        humidity = read_humidity_sensor(simulation_mode=True)
        self.assertIsInstance(humidity, float)
        self.assertGreaterEqual(humidity, 40.0)  # Should be reasonable humidity
        self.assertLessEqual(humidity, 60.0)    # Should be reasonable humidity

    def test_read_multiple_sensors_simulation(self):
        """Test reading multiple sensors simultaneously."""
        temp, humidity = read_multiple_sensors(simulation_mode=True)
        self.assertIsInstance(temp, float)
        self.assertIsInstance(humidity, float)
        self.assertIsNotNone(temp)
        self.assertIsNotNone(humidity)

    def test_validate_sensor_reading_valid(self):
        """Test validation of valid sensor readings."""
        result = validate_sensor_reading(25.0, 50.0)
        self.assertTrue(result)

    def test_validate_sensor_reading_invalid_temperature(self):
        """Test validation of invalid temperature reading."""
        result = validate_sensor_reading(100.0, 50.0)  # Too high
        self.assertFalse(result)

    def test_validate_sensor_reading_invalid_humidity(self):
        """Test validation of invalid humidity reading."""
        result = validate_sensor_reading(25.0, 120.0)  # Too high
        self.assertFalse(result)

    def test_validate_sensor_reading_none_values(self):
        """Test validation when one value is None."""
        result = validate_sensor_reading(None, 50.0)
        self.assertFalse(result)

        result = validate_sensor_reading(25.0, None)
        self.assertFalse(result)

    @patch('basic_sensor.random.uniform')
    def test_read_temperature_sensor_deterministic(self, mock_uniform):
        """Test temperature reading with deterministic values."""
        mock_uniform.return_value = 1.5  # Fixed variation
        temp = read_temperature_sensor(simulation_mode=True)
        expected = 22.5 + 1.5  # base_temp + variation
        self.assertEqual(temp, round(expected, 2))


if __name__ == '__main__':
    unittest.main()