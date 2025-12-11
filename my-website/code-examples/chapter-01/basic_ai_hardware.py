"""
Basic AI-Hardware Integration Example

This module integrates the sensor reading, AI decision model, and LED control
to create a complete AI-hardware interaction system. The AI makes decisions
based on temperature readings to control an LED.
"""

import time
import logging
from typing import Dict, Optional
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from sensor_integration.basic_sensor import read_temperature_sensor
from actuator_control.basic_led import LEDController
from ai_models.simple_decision import SimpleAIDecisionModel, create_temperature_based_model
from src.safety_framework import create_default_safety_framework, SafetyViolation


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BasicAIHardwareSystem:
    """
    A complete system that integrates AI decision making with hardware control.
    """

    def __init__(self, led_pin: int = 18, simulation_mode: bool = True):
        """
        Initialize the AI-Hardware system.

        Args:
            led_pin: GPIO pin for the LED
            simulation_mode: Whether to simulate hardware or use real components
        """
        self.led_controller = LEDController(pin=led_pin, simulation_mode=simulation_mode)
        self.ai_model = create_temperature_based_model()
        self.safety_framework = create_default_safety_framework()
        self.simulation_mode = simulation_mode
        self.running = False

        logger.info("AI-Hardware system initialized")
        logger.info(f"Simulation mode: {simulation_mode}")

    def run_single_cycle(self) -> bool:
        """
        Run one complete cycle of the AI-hardware loop:
        1. Sense: Read temperature
        2. Think: Process through AI model
        3. Act: Control LED based on decision

        Returns:
            True if cycle completed successfully, False otherwise
        """
        try:
            # Step 1: Sense - Read temperature sensor
            temperature = read_temperature_sensor(simulation_mode=self.simulation_mode)
            if temperature is None:
                logger.error("Failed to read temperature sensor")
                return False

            logger.info(f"Temperature reading: {temperature:.2f}°C")

            # Step 2: Think - Make AI decision
            sensor_data = {'temperature': temperature}

            # Check safety before making decision
            try:
                self.safety_framework.check_action_safety('read_temperature', sensor_data)
            except SafetyViolation as e:
                logger.error(f"Safety violation during sensing: {e}")
                self.safety_framework.activate_fail_safe()
                return False

            decision = self.ai_model.make_decision(sensor_data)
            logger.info(f"AI decision: {'ON' if decision else 'OFF'} (based on {temperature}°C)")

            # Step 3: Act - Control LED based on decision
            try:
                self.safety_framework.check_action_safety('control_led', {'state': decision})
            except SafetyViolation as e:
                logger.error(f"Safety violation during actuation: {e}")
                self.safety_framework.activate_fail_safe()
                return False

            success = self.led_controller.set_state(decision)
            if not success:
                logger.error("Failed to control LED")
                return False

            logger.info(f"LED set to: {'ON' if decision else 'OFF'}")
            return True

        except Exception as e:
            logger.error(f"Error in single cycle: {e}")
            return False

    def run_continuous(self, interval: float = 2.0, max_cycles: Optional[int] = None):
        """
        Run the AI-hardware loop continuously.

        Args:
            interval: Time between cycles in seconds
            max_cycles: Maximum number of cycles to run (None for infinite)
        """
        logger.info("Starting continuous AI-hardware loop")
        self.running = True

        cycle_count = 0
        while self.running:
            if max_cycles is not None and cycle_count >= max_cycles:
                break

            success = self.run_single_cycle()
            if not success:
                logger.error("Cycle failed, activating fail-safe")
                self.safety_framework.activate_fail_safe()
                break

            cycle_count += 1
            logger.info(f"Completed cycle {cycle_count}")

            # Check for timeout and safety status
            self.safety_framework.check_timeout(max_idle_time=60.0)

            # Check safety status
            safety_status = self.safety_framework.get_safety_status()
            if safety_status['fail_safe_active'] or safety_status['emergency_stop_active']:
                logger.warning("Safety system active, stopping loop")
                break

            time.sleep(interval)

        logger.info(f"Continuous loop stopped after {cycle_count} cycles")
        self.stop()

    def stop(self):
        """
        Stop the system and clean up resources.
        """
        logger.info("Stopping AI-Hardware system")
        self.running = False

        # Turn off LED and clean up
        self.led_controller.turn_off()
        self.led_controller.cleanup()

        # Deactivate safety systems
        self.safety_framework.deactivate_fail_safe()
        self.safety_framework.reset_emergency_stop()

    def get_system_status(self) -> Dict:
        """
        Get the current status of the system.

        Returns:
            Dictionary with system status information
        """
        return {
            'running': self.running,
            'led_state': self.led_controller.get_state(),
            'safety_status': self.safety_framework.get_safety_status(),
            'ai_performance': self.ai_model.get_performance_metrics(),
            'simulation_mode': self.simulation_mode
        }


def run_basic_example():
    """
    Run the basic AI-hardware integration example.
    """
    logger.info("Starting Basic AI-Hardware Integration Example")

    # Create system instance (using simulation mode)
    system = BasicAIHardwareSystem(simulation_mode=True)

    try:
        # Run a single cycle to demonstrate the system
        logger.info("Running single cycle...")
        success = system.run_single_cycle()
        if success:
            logger.info("Single cycle completed successfully")
        else:
            logger.error("Single cycle failed")

        # Get and display system status
        status = system.get_system_status()
        print("\nSystem Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Run for a few cycles to see the behavior
        logger.info("\nRunning continuous loop for 5 cycles...")
        system.run_continuous(interval=1.5, max_cycles=5)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error running example: {e}")
    finally:
        system.stop()
        logger.info("Example completed")


def run_hardware_demo():
    """
    Run a more comprehensive demo with hardware interaction.
    """
    logger.info("Starting Hardware Demo")

    # Create system with real hardware (will fall back to simulation if not available)
    system = BasicAIHardwareSystem(simulation_mode=False)

    try:
        # Display initial status
        status = system.get_system_status()
        print("Initial System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Run continuous loop for a longer period
        logger.info("Running extended demo (10 cycles)...")
        system.run_continuous(interval=2.0, max_cycles=10)

        # Display final status
        final_status = system.get_system_status()
        print("\nFinal System Status:")
        for key, value in final_status.items():
            print(f"  {key}: {value}")

    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Error in demo: {e}")
    finally:
        system.stop()
        logger.info("Demo completed")


if __name__ == "__main__":
    print("PHYSICAL-AI-BOOK: Basic AI-Hardware Integration")
    print("=" * 50)

    # Run the basic example
    run_basic_example()

    print("\n" + "=" * 50)
    print("Basic example completed. The system successfully integrated:")
    print("1. Sensor reading (temperature)")
    print("2. AI decision making (based on temperature threshold)")
    print("3. Hardware control (LED on/off)")
    print("4. Safety framework (fail-safe mechanisms)")
    print("\nAll components worked together in a complete AI-hardware loop.")