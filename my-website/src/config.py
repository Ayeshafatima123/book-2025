"""
Configuration Management for Different Hardware Platforms

This module handles configuration settings for different hardware platforms
(Arduino, Raspberry Pi, etc.) and provides a centralized way to manage
platform-specific settings.
"""

import os
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class HardwareConfig:
    """Configuration for a specific hardware platform."""
    platform_name: str
    connection_params: Dict[str, Any]
    sensor_configs: Dict[str, Dict[str, Any]]
    actuator_configs: Dict[str, Dict[str, Any]]
    safety_limits: Dict[str, Dict[str, Any]]
    default_timeout: float = 30.0
    simulation_mode: bool = True


class ConfigManager:
    """
    Configuration manager that handles settings for different hardware platforms.
    """

    def __init__(self, config_file: Optional[str] = None):
        self.configs: Dict[str, HardwareConfig] = {}
        self.active_config: Optional[HardwareConfig] = None
        self.default_platform = "mock"

        if config_file:
            self.load_config_from_file(config_file)
        else:
            # Create default configurations
            self._create_default_configs()

    def _create_default_configs(self):
        """Create default configurations for common hardware platforms."""

        # Raspberry Pi configuration
        raspberry_pi_config = HardwareConfig(
            platform_name="raspberry_pi",
            connection_params={
                "gpio_mode": "BCM",
                "default_pins": {
                    "led": 18,
                    "button": 23,
                    "temperature_sensor": 4,
                    "servo": 12
                }
            },
            sensor_configs={
                "dht22": {
                    "type": "temperature_humidity",
                    "pin": 4,
                    "read_interval": 2.0
                },
                "ldr": {
                    "type": "light",
                    "pin": "GPIO.ADC",
                    "read_interval": 1.0
                }
            },
            actuator_configs={
                "led": {
                    "type": "digital_output",
                    "pin": 18,
                    "pwm": False
                },
                "servo": {
                    "type": "servo",
                    "pin": 12,
                    "min_pulse": 0.5,
                    "max_pulse": 2.5
                },
                "relay": {
                    "type": "digital_output",
                    "pin": 24,
                    "pwm": False
                }
            },
            safety_limits={
                "temperature": {"min": -10, "max": 80},
                "voltage": {"min": 0, "max": 5.5},
                "current": {"min": 0, "max": 1.0}
            },
            default_timeout=30.0,
            simulation_mode=False
        )

        self.configs["raspberry_pi"] = raspberry_pi_config

        # Arduino configuration
        arduino_config = HardwareConfig(
            platform_name="arduino",
            connection_params={
                "port": "/dev/ttyUSB0",
                "baudrate": 9600,
                "timeout": 1
            },
            sensor_configs={
                "analog_sensor": {
                    "type": "analog",
                    "pin": "A0",
                    "read_interval": 0.5
                },
                "digital_sensor": {
                    "type": "digital",
                    "pin": 2,
                    "read_interval": 1.0
                }
            },
            actuator_configs={
                "digital_output": {
                    "type": "digital",
                    "pin": 13,
                    "active_high": True
                },
                "pwm_output": {
                    "type": "pwm",
                    "pin": 9,
                    "frequency": 490
                },
                "servo": {
                    "type": "servo",
                    "pin": 10,
                    "min_pulse": 544,
                    "max_pulse": 2400
                }
            },
            safety_limits={
                "voltage": {"min": 0, "max": 12},
                "current": {"min": 0, "max": 2.0},
                "pwm_duty_cycle": {"min": 0, "max": 100}
            },
            default_timeout=30.0,
            simulation_mode=False
        )

        self.configs["arduino"] = arduino_config

        # Mock/Simulation configuration
        mock_config = HardwareConfig(
            platform_name="mock",
            connection_params={},
            sensor_configs={
                "mock_temperature": {
                    "type": "temperature",
                    "simulated_range": [15, 35],
                    "read_interval": 1.0
                },
                "mock_light": {
                    "type": "light",
                    "simulated_range": [0, 100],
                    "read_interval": 1.0
                }
            },
            actuator_configs={
                "mock_led": {
                    "type": "digital_output",
                    "state": False
                },
                "mock_motor": {
                    "type": "motor",
                    "speed_range": [0, 100]
                }
            },
            safety_limits={
                "temperature": {"min": -10, "max": 80},
                "voltage": {"min": 0, "max": 12},
                "current": {"min": 0, "max": 5}
            },
            default_timeout=30.0,
            simulation_mode=True
        )

        self.configs["mock"] = mock_config

    def load_config_from_file(self, config_file: str):
        """Load configuration from a JSON or YAML file."""
        if config_file.endswith('.json'):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        elif config_file.endswith(('.yml', '.yaml')):
            if yaml is None:
                raise ImportError("PyYAML is required to load YAML configuration files. Install it with 'pip install PyYAML'")
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
        else:
            raise ValueError("Config file must be JSON or YAML")

        # Convert the loaded data to HardwareConfig objects
        for platform_name, config_dict in config_data.items():
            config = HardwareConfig(
                platform_name=platform_name,
                connection_params=config_dict.get('connection_params', {}),
                sensor_configs=config_dict.get('sensor_configs', {}),
                actuator_configs=config_dict.get('actuator_configs', {}),
                safety_limits=config_dict.get('safety_limits', {}),
                default_timeout=config_dict.get('default_timeout', 30.0),
                simulation_mode=config_dict.get('simulation_mode', True)
            )
            self.configs[platform_name] = config

    def save_config_to_file(self, config_file: str, platform_name: Optional[str] = None):
        """Save configuration to a JSON or YAML file."""
        if platform_name:
            config_dict = asdict(self.configs[platform_name])
            configs_to_save = {platform_name: config_dict}
        else:
            configs_to_save = {}
            for name, config in self.configs.items():
                configs_to_save[name] = asdict(config)

        if config_file.endswith('.json'):
            with open(config_file, 'w') as f:
                json.dump(configs_to_save, f, indent=2)
        elif config_file.endswith(('.yml', '.yaml')):
            if yaml is None:
                raise ImportError("PyYAML is required to save YAML configuration files. Install it with 'pip install PyYAML'")
            with open(config_file, 'w') as f:
                yaml.dump(configs_to_save, f, default_flow_style=False)
        else:
            raise ValueError("Config file must be JSON or YAML")

    def get_config(self, platform_name: str) -> Optional[HardwareConfig]:
        """Get configuration for a specific platform."""
        return self.configs.get(platform_name)

    def set_active_config(self, platform_name: str) -> bool:
        """Set the active configuration to the specified platform."""
        if platform_name in self.configs:
            self.active_config = self.configs[platform_name]
            return True
        return False

    def get_active_config(self) -> Optional[HardwareConfig]:
        """Get the currently active configuration."""
        return self.active_config

    def get_platform_names(self) -> list:
        """Get list of available platform names."""
        return list(self.configs.keys())

    def update_sensor_config(self, platform_name: str, sensor_id: str, config: Dict[str, Any]):
        """Update configuration for a specific sensor on a platform."""
        if platform_name in self.configs:
            self.configs[platform_name].sensor_configs[sensor_id] = config

    def update_actuator_config(self, platform_name: str, actuator_id: str, config: Dict[str, Any]):
        """Update configuration for a specific actuator on a platform."""
        if platform_name in self.configs:
            self.configs[platform_name].actuator_configs[actuator_id] = config

    def get_sensor_config(self, platform_name: str, sensor_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific sensor on a platform."""
        if platform_name in self.configs:
            return self.configs[platform_name].sensor_configs.get(sensor_id)
        return None

    def get_actuator_config(self, platform_name: str, actuator_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific actuator on a platform."""
        if platform_name in self.configs:
            return self.configs[platform_name].actuator_configs.get(actuator_id)
        return None


# Global configuration manager instance
_config_manager = None


def get_config_manager(config_file: Optional[str] = None) -> ConfigManager:
    """
    Get the global configuration manager instance.

    Args:
        config_file: Optional path to a config file to load

    Returns:
        ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager


def get_active_config() -> Optional[HardwareConfig]:
    """Get the currently active hardware configuration."""
    config_manager = get_config_manager()
    return config_manager.get_active_config()


def set_active_platform(platform_name: str) -> bool:
    """
    Set the active hardware platform.

    Args:
        platform_name: Name of the platform to activate

    Returns:
        True if successful, False otherwise
    """
    config_manager = get_config_manager()
    return config_manager.set_active_config(platform_name)


def get_platform_config(platform_name: str) -> Optional[HardwareConfig]:
    """
    Get configuration for a specific platform.

    Args:
        platform_name: Name of the platform

    Returns:
        HardwareConfig if found, None otherwise
    """
    config_manager = get_config_manager()
    return config_manager.get_config(platform_name)