"""
Basic LED Control Function

This module provides functions for controlling an LED actuator.
It includes both real hardware and simulation modes for testing.
"""

import time
import logging
from typing import Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LEDController:
    """
    A class to control an LED actuator with both real hardware and simulation modes.
    """

    def __init__(self, pin: int = 18, simulation_mode: bool = True):
        """
        Initialize the LED controller.

        Args:
            pin: GPIO pin number for the LED (default 18 for Raspberry Pi)
            simulation_mode: If True, simulate hardware; if False, use real GPIO
        """
        self.pin = pin
        self.simulation_mode = simulation_mode
        self.led_state = False  # False = off, True = on

        if not simulation_mode:
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pin, GPIO.OUT)
                self.gpio = GPIO
                logger.info(f"Real LED controller initialized on pin {pin}")
            except ImportError:
                logger.warning("RPi.GPIO not available, switching to simulation mode")
                self.simulation_mode = True

        if simulation_mode:
            logger.info(f"Simulated LED controller initialized on pin {pin}")

    def turn_on(self) -> bool:
        """
        Turn the LED on.

        Returns:
            True if successful, False otherwise
        """
        if self.simulation_mode:
            self.led_state = True
            logger.info(f"LED turned ON (pin {self.pin}) - SIMULATION")
            return True
        else:
            try:
                self.gpio.output(self.pin, self.gpio.HIGH)
                self.led_state = True
                logger.info(f"LED turned ON (pin {self.pin}) - REAL HARDWARE")
                return True
            except Exception as e:
                logger.error(f"Error turning LED on: {e}")
                return False

    def turn_off(self) -> bool:
        """
        Turn the LED off.

        Returns:
            True if successful, False otherwise
        """
        if self.simulation_mode:
            self.led_state = False
            logger.info(f"LED turned OFF (pin {self.pin}) - SIMULATION")
            return True
        else:
            try:
                self.gpio.output(self.pin, self.gpio.LOW)
                self.led_state = False
                logger.info(f"LED turned OFF (pin {self.pin}) - REAL HARDWARE")
                return True
            except Exception as e:
                logger.error(f"Error turning LED off: {e}")
                return False

    def set_state(self, state: bool) -> bool:
        """
        Set the LED to a specific state.

        Args:
            state: True for on, False for off

        Returns:
            True if successful, False otherwise
        """
        if state:
            return self.turn_on()
        else:
            return self.turn_off()

    def get_state(self) -> bool:
        """
        Get the current state of the LED.

        Returns:
            Current state (True = on, False = off)
        """
        return self.led_state

    def blink(self, duration: float = 0.5, count: int = 3) -> bool:
        """
        Blink the LED for a specified duration and count.

        Args:
            duration: Time for each on/off cycle in seconds
            count: Number of blink cycles

        Returns:
            True if successful, False otherwise
        """
        success = True
        original_state = self.led_state

        for i in range(count):
            # Turn on
            if not self.turn_on():
                success = False
                break
            time.sleep(duration)

            # Turn off
            if not self.turn_off():
                success = False
                break
            time.sleep(duration)

        # Restore original state
        self.set_state(original_state)
        return success

    def fade_in_out(self, step_duration: float = 0.1, steps: int = 10) -> bool:
        """
        Simulate a fade in/out effect using PWM-like behavior (in simulation mode).

        Note: Real hardware implementation would require actual PWM control.

        Args:
            step_duration: Duration of each step in seconds
            steps: Number of steps in the fade sequence

        Returns:
            True if successful, False otherwise
        """
        if self.simulation_mode:
            # In simulation, just show the steps
            logger.info("Simulating LED fade in/out...")
            for i in range(steps):
                intensity = min(100, int((i / steps) * 100))
                logger.info(f"Fade step {i+1}/{steps}, intensity: {intensity}%")
                time.sleep(step_duration)

            for i in range(steps, 0, -1):
                intensity = min(100, int((i / steps) * 100))
                logger.info(f"Fade step {steps-i+1}/{steps} (reverse), intensity: {intensity}%")
                time.sleep(step_duration)

            return True
        else:
            # Real hardware implementation would use PWM
            logger.info("LED fade in/out (real hardware)...")
            try:
                # This would require setting up PWM on the GPIO pin
                # For now, just blink rapidly to simulate fading
                for i in range(steps):
                    self.gpio.output(self.pin, self.gpio.HIGH if i % 2 == 0 else self.gpio.LOW)
                    time.sleep(step_duration)
                return True
            except Exception as e:
                logger.error(f"Error during fade effect: {e}")
                return False

    def cleanup(self):
        """
        Clean up the GPIO resources.
        """
        if not self.simulation_mode:
            try:
                self.gpio.cleanup(self.pin)
                logger.info(f"GPIO pin {self.pin} cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up GPIO: {e}")


def simple_led_control(led_state: bool, pin: int = 18, simulation_mode: bool = True) -> bool:
    """
    Simple function to control an LED without using the class.

    Args:
        led_state: True to turn on, False to turn off
        pin: GPIO pin number
        simulation_mode: If True, simulate hardware; if False, use real GPIO

    Returns:
        True if successful, False otherwise
    """
    if simulation_mode:
        state_str = "ON" if led_state else "OFF"
        logger.info(f"LED {state_str} (pin {pin}) - SIMULATION")
        return True
    else:
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)

            if led_state:
                GPIO.output(pin, GPIO.HIGH)
                logger.info(f"LED ON (pin {pin}) - REAL HARDWARE")
            else:
                GPIO.output(pin, GPIO.LOW)
                logger.info(f"LED OFF (pin {pin}) - REAL HARDWARE")

            return True
        except ImportError:
            logger.error("RPi.GPIO library not available")
            return False
        except Exception as e:
            logger.error(f"Error controlling LED: {e}")
            return False


def led_sequence_demo(pin: int = 18, simulation_mode: bool = True):
    """
    Demonstrate various LED control patterns.

    Args:
        pin: GPIO pin number
        simulation_mode: If True, simulate hardware; if False, use real GPIO
    """
    logger.info("Starting LED sequence demo...")

    led = LEDController(pin=pin, simulation_mode=simulation_mode)

    try:
        # Turn on
        led.turn_on()
        time.sleep(1)

        # Blink
        led.blink(duration=0.3, count=5)
        time.sleep(1)

        # Fade effect
        led.fade_in_out(step_duration=0.1, steps=8)
        time.sleep(1)

        # Turn off
        led.turn_off()

        logger.info("LED sequence demo completed")
    except Exception as e:
        logger.error(f"Error during LED demo: {e}")
    finally:
        led.cleanup()


if __name__ == "__main__":
    # Example usage
    print("Testing basic LED control functions...")

    # Test with simulation mode
    print("\n1. Testing with simulation mode:")
    led_sim = LEDController(simulation_mode=True)
    led_sim.turn_on()
    print(f"LED state after turn_on: {led_sim.get_state()}")
    led_sim.turn_off()
    print(f"LED state after turn_off: {led_sim.get_state()}")

    # Test simple function
    print("\n2. Testing simple LED control function:")
    simple_led_control(True, simulation_mode=True)
    simple_led_control(False, simulation_mode=True)

    # Test blink pattern
    print("\n3. Testing blink pattern:")
    led_sim.blink(duration=0.2, count=3)

    # Test fade effect
    print("\n4. Testing fade effect:")
    led_sim.fade_in_out(step_duration=0.05, steps=5)

    # Demo sequence
    print("\n5. Running LED sequence demo:")
    led_sequence_demo(simulation_mode=True)

    led_sim.cleanup()