"""
Testing Framework for Code and Hardware Tests

This module sets up the testing framework using pytest for code validation
and provides utilities for hardware testing procedures.
"""

import pytest
import unittest
from typing import Any, Dict, List, Callable
import time
import threading
from .hardware_interface import HardwareInterface, MockInterface
from .safety_framework import SafetyFramework, create_default_safety_framework
from .config import ConfigManager, HardwareConfig


class HardwareTestResult:
    """Represents the result of a hardware test."""

    def __init__(self, test_name: str, passed: bool, duration: float,
                 error_message: str = "", details: Dict[str, Any] = None):
        self.test_name = test_name
        self.passed = passed
        self.duration = duration
        self.error_message = error_message
        self.details = details or {}
        self.timestamp = time.time()


class HardwareTestSuite:
    """A suite of hardware tests."""

    def __init__(self, name: str, hardware_interface: HardwareInterface):
        self.name = name
        self.hardware_interface = hardware_interface
        self.tests = []
        self.results = []

    def add_test(self, test_func: Callable, test_name: str = None):
        """Add a test function to the suite."""
        name = test_name or test_func.__name__
        self.tests.append((name, test_func))

    def run_all_tests(self) -> List[HardwareTestResult]:
        """Run all tests in the suite and return results."""
        self.results = []

        for test_name, test_func in self.tests:
            start_time = time.time()
            try:
                # Run the test with the hardware interface
                test_func(self.hardware_interface)
                duration = time.time() - start_time
                result = HardwareTestResult(test_name, True, duration)
            except Exception as e:
                duration = time.time() - start_time
                result = HardwareTestResult(test_name, False, duration, str(e))

            self.results.append(result)

        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of test results."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        return {
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'success_rate': passed / total if total > 0 else 0,
            'total_duration': sum(r.duration for r in self.results)
        }


def create_basic_hardware_tests(hardware_interface: HardwareInterface) -> HardwareTestSuite:
    """Create a basic suite of hardware tests."""

    suite = HardwareTestSuite("Basic Hardware Tests", hardware_interface)

    def test_connection(hw_interface):
        """Test that we can connect to the hardware."""
        assert hw_interface.connect() == True
        assert hw_interface.connected == True
        hw_interface.disconnect()

    def test_sensor_reading(hw_interface):
        """Test that we can read from a sensor."""
        hw_interface.connect()
        value = hw_interface.read_sensor("temperature_sensor")
        assert value is not None
        hw_interface.disconnect()

    def test_actuator_control(hw_interface):
        """Test that we can control an actuator."""
        hw_interface.connect()
        result = hw_interface.write_actuator("led", True)
        assert result == True
        hw_interface.disconnect()

    def test_multiple_sensors(hw_interface):
        """Test reading from multiple sensors."""
        hw_interface.connect()
        temp = hw_interface.read_sensor("temperature_sensor")
        light = hw_interface.read_sensor("light_sensor")
        assert temp is not None
        assert light is not None
        hw_interface.disconnect()

    suite.add_test(test_connection)
    suite.add_test(test_sensor_reading)
    suite.add_test(test_actuator_control)
    suite.add_test(test_multiple_sensors)

    return suite


def pytest_configure(config):
    """Configure pytest for hardware testing."""
    config.addinivalue_line(
        "markers", "hardware: mark test as a hardware test"
    )
    config.addinivalue_line(
        "markers", "simulation: mark test as a simulation test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )


class TestSafetyFramework(unittest.TestCase):
    """Unit tests for the safety framework."""

    def setUp(self):
        self.safety_framework = create_default_safety_framework()

    def test_safety_framework_initialization(self):
        """Test that safety framework initializes correctly."""
        self.assertFalse(self.safety_framework.fail_safe_active)
        self.assertFalse(self.safety_framework.emergency_stop_active)
        self.assertGreater(len(self.safety_framework.safety_rules), 0)

    def test_temperature_safety_check(self):
        """Test temperature safety rule."""
        # This should pass
        result = self.safety_framework.check_action_safety('set_temperature', {'value': 25})
        self.assertTrue(result)

        # This should fail
        with self.assertRaises(Exception):
            self.safety_framework.check_action_safety('set_temperature', {'value': 100})

    def test_emergency_stop(self):
        """Test emergency stop functionality."""
        self.safety_framework.emergency_stop()
        self.assertTrue(self.safety_framework.emergency_stop_active)

        with self.assertRaises(Exception):
            self.safety_framework.check_action_safety('set_temperature', {'value': 25})

        self.safety_framework.reset_emergency_stop()
        self.assertFalse(self.safety_framework.emergency_stop_active)

    def test_fail_safe_mode(self):
        """Test fail-safe mode."""
        self.safety_framework.activate_fail_safe()
        self.assertTrue(self.safety_framework.fail_safe_active)

        # Read operations should still work
        # Note: We can't test actual read_sensor here as it's not part of safety framework directly
        # but we can test that non-read operations are blocked when implemented in the system

        self.safety_framework.deactivate_fail_safe()
        self.assertFalse(self.safety_framework.fail_safe_active)


class TestConfigManager(unittest.TestCase):
    """Unit tests for the configuration manager."""

    def setUp(self):
        self.config_manager = ConfigManager()

    def test_config_manager_initialization(self):
        """Test that config manager initializes with default configs."""
        self.assertIsNotNone(self.config_manager.get_config("mock"))
        self.assertIsNotNone(self.config_manager.get_config("raspberry_pi"))
        self.assertIsNotNone(self.config_manager.get_config("arduino"))

    def test_active_config_setting(self):
        """Test setting and getting active config."""
        result = self.config_manager.set_active_config("mock")
        self.assertTrue(result)

        active_config = self.config_manager.get_active_config()
        self.assertIsNotNone(active_config)
        self.assertEqual(active_config.platform_name, "mock")

    def test_platform_names(self):
        """Test getting platform names."""
        platforms = self.config_manager.get_platform_names()
        self.assertIn("mock", platforms)
        self.assertIn("raspberry_pi", platforms)
        self.assertIn("arduino", platforms)


def run_unit_tests():
    """Run all unit tests."""
    # Discover and run all unit tests in the current package
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__, fromlist=['TestSafetyFramework', 'TestConfigManager']))
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


def run_hardware_tests(simulation_mode: bool = True):
    """Run hardware tests, either in simulation or with real hardware."""
    if simulation_mode:
        # Use mock interface for testing
        hw_interface = MockInterface()
    else:
        # In a real implementation, you would use the actual hardware interface
        # For now, we'll use the mock to avoid requiring actual hardware
        hw_interface = MockInterface()

    suite = create_basic_hardware_tests(hw_interface)
    results = suite.run_all_tests()

    # Print results
    summary = suite.get_summary()
    print(f"\nHardware Test Results for '{suite.name}':")
    print(f"Total tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success rate: {summary['success_rate']:.2%}")
    print(f"Total duration: {summary['total_duration']:.2f}s")

    for result in results:
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"  {status} {result.test_name} ({result.duration:.2f}s)")
        if not result.passed:
            print(f"    Error: {result.error_message}")

    return results


def run_all_tests(hardware_tests: bool = True, unit_tests: bool = True, simulation_mode: bool = True):
    """Run all types of tests."""
    print("Running PHYSICAL-AI-BOOK test suite...")

    results = {}

    if unit_tests:
        print("\n" + "="*50)
        print("RUNNING UNIT TESTS")
        print("="*50)
        unit_results = run_unit_tests()
        results['unit_tests'] = unit_results

    if hardware_tests:
        print("\n" + "="*50)
        print("RUNNING HARDWARE TESTS")
        print("="*50)
        hw_results = run_hardware_tests(simulation_mode)
        results['hardware_tests'] = hw_results

    return results


if __name__ == "__main__":
    # If run as a script, execute all tests
    run_all_tests()