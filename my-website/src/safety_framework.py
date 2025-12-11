"""
Safety Framework with Fail-Safes

This module implements safety measures for physical AI systems to prevent
harmful actions and provide fail-safe mechanisms when controlling hardware.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
import time
import logging


class RiskLevel(Enum):
    """Enumeration of risk levels for safety checks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class SafetyViolation(Exception):
    """Exception raised when a safety check fails."""
    pass


class SafetyFramework:
    """
    Safety framework that provides fail-safes and risk assessment for physical AI systems.
    """

    def __init__(self):
        self.fail_safe_active = False
        self.emergency_stop_active = False
        self.safety_rules = []
        self.logger = logging.getLogger(__name__)
        self.hardware_limits = {}
        self.last_action_time = time.time()

    def add_safety_rule(self, rule_name: str, check_function, risk_level: RiskLevel, description: str = ""):
        """
        Add a safety rule to the framework.

        Args:
            rule_name: Name of the rule
            check_function: Function that takes action parameters and returns True if safe
            risk_level: Risk level of violating this rule
            description: Description of the rule
        """
        self.safety_rules.append({
            'name': rule_name,
            'check': check_function,
            'risk_level': risk_level,
            'description': description
        })

    def check_action_safety(self, action_type: str, action_params: Dict[str, Any]) -> bool:
        """
        Check if an action is safe to perform based on all safety rules.

        Args:
            action_type: Type of action (e.g., 'set_temperature', 'move_actuator')
            action_params: Parameters for the action

        Returns:
            True if action is safe, raises SafetyViolation if not safe
        """
        if self.emergency_stop_active:
            raise SafetyViolation("Emergency stop is active. No actions allowed.")

        if self.fail_safe_active:
            # In fail-safe mode, only allow safe actions
            if action_type not in ['read_sensor', 'get_status']:
                raise SafetyViolation("Fail-safe mode active. Only safe read operations allowed.")

        # Check all safety rules
        for rule in self.safety_rules:
            try:
                if not rule['check'](action_type, action_params):
                    raise SafetyViolation(
                        f"Safety rule '{rule['name']}' violated. Risk level: {rule['risk_level'].name}. "
                        f"Description: {rule['description']}"
                    )
            except Exception as e:
                raise SafetyViolation(f"Safety check failed: {str(e)}")

        # Update last action time
        self.last_action_time = time.time()

        return True

    def activate_fail_safe(self):
        """Activate fail-safe mode - restricts all non-essential hardware operations."""
        self.fail_safe_active = True
        self.logger.warning("Fail-safe mode activated")
        print("⚠️  FAIL-SAFE MODE ACTIVATED: All non-essential hardware operations restricted")

    def deactivate_fail_safe(self):
        """Deactivate fail-safe mode."""
        self.fail_safe_active = False
        self.logger.info("Fail-safe mode deactivated")
        print("✅ Fail-safe mode deactivated")

    def emergency_stop(self):
        """Activate emergency stop - stops all hardware operations immediately."""
        self.emergency_stop_active = True
        self.logger.critical("Emergency stop activated")
        print("🚨 EMERGENCY STOP: All hardware operations halted immediately")

    def reset_emergency_stop(self):
        """Reset emergency stop."""
        self.emergency_stop_active = False
        self.logger.info("Emergency stop reset")
        print("✅ Emergency stop reset")

    def set_hardware_limit(self, component: str, parameter: str, min_val: float, max_val: float):
        """
        Set safety limits for hardware components.

        Args:
            component: Name of the hardware component
            parameter: Parameter to limit (e.g., 'temperature', 'voltage', 'speed')
            min_val: Minimum allowed value
            max_val: Maximum allowed value
        """
        if component not in self.hardware_limits:
            self.hardware_limits[component] = {}
        self.hardware_limits[component][parameter] = {'min': min_val, 'max': max_val}

    def validate_hardware_value(self, component: str, parameter: str, value: float) -> bool:
        """
        Validate that a hardware value is within safety limits.

        Args:
            component: Name of the hardware component
            parameter: Parameter to validate
            value: Value to validate

        Returns:
            True if value is within limits, raises SafetyViolation if not
        """
        if component in self.hardware_limits:
            if parameter in self.hardware_limits[component]:
                limits = self.hardware_limits[component][parameter]
                if value < limits['min'] or value > limits['max']:
                    raise SafetyViolation(
                        f"Value {value} for {component}.{parameter} is outside safety limits "
                        f"({limits['min']} - {limits['max']})"
                    )
        return True

    def check_timeout(self, max_idle_time: float = 30.0) -> bool:
        """
        Check if the system has been idle for too long and activate fail-safe if needed.

        Args:
            max_idle_time: Maximum allowed idle time in seconds

        Returns:
            True if within timeout, activates fail-safe if timeout exceeded
        """
        current_time = time.time()
        idle_time = current_time - self.last_action_time

        if idle_time > max_idle_time:
            self.logger.warning(f"System idle for {idle_time:.1f}s, activating fail-safe")
            self.activate_fail_safe()
            return False

        return True

    def get_safety_status(self) -> Dict[str, Any]:
        """
        Get current safety status of the system.

        Returns:
            Dictionary with safety status information
        """
        return {
            'fail_safe_active': self.fail_safe_active,
            'emergency_stop_active': self.emergency_stop_active,
            'total_safety_rules': len(self.safety_rules),
            'hardware_limits_set': len(self.hardware_limits),
            'last_action_time': self.last_action_time,
            'idle_time': time.time() - self.last_action_time
        }


def create_default_safety_framework() -> SafetyFramework:
    """
    Create a safety framework with default safety rules appropriate for physical AI systems.

    Returns:
        Configured SafetyFramework instance
    """
    sf = SafetyFramework()

    # Rule 1: Temperature limits
    def temp_check(action_type, action_params):
        if action_type == 'set_temperature' and 'value' in action_params:
            temp = action_params['value']
            return -10 <= temp <= 80  # Safe temperature range
        return True

    sf.add_safety_rule(
        'temperature_limit',
        temp_check,
        RiskLevel.HIGH,
        'Temperature must be between -10°C and 80°C'
    )

    # Rule 2: Voltage limits
    def voltage_check(action_type, action_params):
        if action_type == 'set_voltage' and 'value' in action_params:
            voltage = action_params['value']
            return 0 <= voltage <= 12  # Safe voltage range for common components
        return True

    sf.add_safety_rule(
        'voltage_limit',
        voltage_check,
        RiskLevel.HIGH,
        'Voltage must be between 0V and 12V'
    )

    # Rule 3: Motor speed limits
    def speed_check(action_type, action_params):
        if action_type == 'set_motor_speed' and 'value' in action_params:
            speed = abs(action_params['value'])
            return speed <= 100  # Max 100% speed
        return True

    sf.add_safety_rule(
        'speed_limit',
        speed_check,
        RiskLevel.MEDIUM,
        'Motor speed must not exceed 100%'
    )

    # Set default hardware limits
    sf.set_hardware_limit('heater', 'temperature', 0, 70)
    sf.set_hardware_limit('motor', 'speed', -100, 100)
    sf.set_hardware_limit('power_supply', 'voltage', 0, 12)
    sf.set_hardware_limit('power_supply', 'current', 0, 5)

    return sf