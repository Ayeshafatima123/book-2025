"""
Hardware Interface Abstraction Layer

This module provides an abstraction layer for interacting with different hardware platforms
(Arduino, Raspberry Pi, etc.) to control physical components like sensors and actuators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class HardwareInterface(ABC):
    """
    Abstract base class for hardware interfaces.
    Provides a common interface for different hardware platforms.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the hardware platform."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the hardware platform."""
        pass

    @abstractmethod
    def read_sensor(self, sensor_id: str) -> Any:
        """Read value from a sensor."""
        pass

    @abstractmethod
    def write_actuator(self, actuator_id: str, value: Any) -> bool:
        """Write value to an actuator."""
        pass


class RaspberryPiInterface(HardwareInterface):
    """
    Hardware interface implementation for Raspberry Pi.
    """

    def __init__(self):
        self.connected = False
        self.gpio_initialized = False

    def connect(self) -> bool:
        """Connect to Raspberry Pi GPIO."""
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            self.gpio_initialized = True
            self.connected = True
            return True
        except ImportError:
            print("RPi.GPIO library not available. Running in simulation mode.")
            self.connected = True  # Allow simulation mode
            return True
        except Exception as e:
            print(f"Failed to connect to Raspberry Pi: {e}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from Raspberry Pi GPIO."""
        try:
            import RPi.GPIO as GPIO
            if self.gpio_initialized:
                GPIO.cleanup()
        except ImportError:
            pass
        except Exception as e:
            print(f"Error during GPIO cleanup: {e}")

        self.connected = False
        return True

    def read_sensor(self, sensor_id: str) -> Any:
        """Read value from a sensor on Raspberry Pi."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        # In simulation mode, return mock values
        # In real mode, this would interface with actual GPIO pins
        if sensor_id == "temperature_sensor":
            import random
            return round(random.uniform(20.0, 30.0), 2)  # Simulate temperature reading
        elif sensor_id == "light_sensor":
            import random
            return random.randint(0, 100)  # Simulate light level (0-100)
        else:
            raise ValueError(f"Unknown sensor: {sensor_id}")

    def write_actuator(self, actuator_id: str, value: Any) -> bool:
        """Write value to an actuator on Raspberry Pi."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        # In simulation mode, just print the action
        # In real mode, this would control actual GPIO pins
        print(f"Setting {actuator_id} to {value}")
        return True


class ArduinoInterface(HardwareInterface):
    """
    Hardware interface implementation for Arduino.
    Uses serial communication to interact with Arduino.
    """

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.connected = False

    def connect(self) -> bool:
        """Connect to Arduino via serial."""
        try:
            import serial
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            self.connected = True
            return True
        except ImportError:
            print("pyserial library not available.")
            return False
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            return False

    def disconnect(self) -> bool:
        """Disconnect from Arduino."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self.connected = False
        return True

    def read_sensor(self, sensor_id: str) -> Any:
        """Read value from a sensor on Arduino."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        # Send command to Arduino to read sensor
        command = f"READ_{sensor_id}\n"
        self.serial_conn.write(command.encode())
        response = self.serial_conn.readline().decode().strip()

        try:
            return float(response)
        except ValueError:
            return response

    def write_actuator(self, actuator_id: str, value: Any) -> bool:
        """Write value to an actuator on Arduino."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        # Send command to Arduino to set actuator
        command = f"SET_{actuator_id}_{value}\n"
        self.serial_conn.write(command.encode())
        return True


class MockInterface(HardwareInterface):
    """
    Mock hardware interface for testing and simulation.
    """

    def __init__(self):
        self.connected = False
        self.hardware_state = {}

    def connect(self) -> bool:
        """Connect to mock hardware."""
        self.connected = True
        return True

    def disconnect(self) -> bool:
        """Disconnect from mock hardware."""
        self.connected = False
        return True

    def read_sensor(self, sensor_id: str) -> Any:
        """Read value from a mock sensor."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        # Simulate different sensor readings
        import random
        if sensor_id == "temperature_sensor":
            return round(random.uniform(20.0, 30.0), 2)
        elif sensor_id == "light_sensor":
            return random.randint(0, 100)
        elif sensor_id == "motion_sensor":
            return random.choice([True, False])
        else:
            return random.random()

    def write_actuator(self, actuator_id: str, value: Any) -> bool:
        """Write value to a mock actuator."""
        if not self.connected:
            raise RuntimeError("Hardware not connected")

        self.hardware_state[actuator_id] = value
        return True


def get_hardware_interface(platform: str = "mock") -> HardwareInterface:
    """
    Factory function to get the appropriate hardware interface.

    Args:
        platform: One of "raspberry_pi", "arduino", or "mock"

    Returns:
        An instance of the appropriate HardwareInterface subclass
    """
    if platform == "raspberry_pi":
        return RaspberryPiInterface()
    elif platform == "arduino":
        return ArduinoInterface()
    else:
        return MockInterface()