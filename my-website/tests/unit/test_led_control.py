"""
Unit tests for LED control components.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the code-examples directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../code-examples/actuator-control'))

from basic_led import LEDController, simple_led_control


class TestLEDControl(unittest.TestCase):
    """Unit tests for LED control functions."""

    def test_led_controller_initialization(self):
        """Test LED controller initialization."""
        led = LEDController(simulation_mode=True)
        self.assertEqual(led.pin, 18)
        self.assertTrue(led.simulation_mode)
        self.assertFalse(led.led_state)

    def test_led_controller_initialization_custom_pin(self):
        """Test LED controller initialization with custom pin."""
        led = LEDController(pin=21, simulation_mode=True)
        self.assertEqual(led.pin, 21)
        self.assertTrue(led.simulation_mode)

    def test_led_turn_on_simulation(self):
        """Test turning LED on in simulation mode."""
        led = LEDController(simulation_mode=True)
        result = led.turn_on()
        self.assertTrue(result)
        self.assertTrue(led.led_state)

    def test_led_turn_off_simulation(self):
        """Test turning LED off in simulation mode."""
        led = LEDController(simulation_mode=True)
        led.turn_on()  # Turn on first
        result = led.turn_off()
        self.assertTrue(result)
        self.assertFalse(led.led_state)

    def test_led_set_state(self):
        """Test setting LED state directly."""
        led = LEDController(simulation_mode=True)

        # Set to on
        result = led.set_state(True)
        self.assertTrue(result)
        self.assertTrue(led.led_state)

        # Set to off
        result = led.set_state(False)
        self.assertTrue(result)
        self.assertFalse(led.led_state)

    def test_led_get_state(self):
        """Test getting LED state."""
        led = LEDController(simulation_mode=True)
        self.assertFalse(led.get_state())

        led.turn_on()
        self.assertTrue(led.get_state())

    def test_simple_led_control_on(self):
        """Test simple LED control function - ON."""
        result = simple_led_control(True, simulation_mode=True)
        self.assertTrue(result)

    def test_simple_led_control_off(self):
        """Test simple LED control function - OFF."""
        result = simple_led_control(False, simulation_mode=True)
        self.assertTrue(result)

    def test_simple_led_control_custom_pin(self):
        """Test simple LED control with custom pin."""
        result = simple_led_control(True, pin=22, simulation_mode=True)
        self.assertTrue(result)

    def test_led_blink_simulation(self):
        """Test LED blink function in simulation."""
        led = LEDController(simulation_mode=True)
        result = led.blink(duration=0.1, count=2)
        self.assertTrue(result)

    def test_led_fade_in_out_simulation(self):
        """Test LED fade in/out function in simulation."""
        led = LEDController(simulation_mode=True)
        result = led.fade_in_out(step_duration=0.01, steps=3)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()