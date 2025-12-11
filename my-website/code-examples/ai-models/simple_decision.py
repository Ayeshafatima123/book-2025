"""
Simple AI Decision Model

This module implements a basic AI decision-making model that processes
sensor data to control physical actuators. The model demonstrates fundamental
AI concepts applied to physical systems.
"""

import time
import logging
from typing import Dict, List, Tuple, Union, Optional
from enum import Enum
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Enumeration for different types of decisions."""
    BINARY = "binary"  # On/Off decisions
    MULTIPLE_CHOICE = "multiple_choice"  # Multiple discrete options
    CONTINUOUS = "continuous"  # Continuous range of values


class SimpleAIDecisionModel:
    """
    A simple AI decision model that processes sensor inputs to make control decisions.
    """

    def __init__(self, decision_type: DecisionType = DecisionType.BINARY):
        """
        Initialize the AI decision model.

        Args:
            decision_type: Type of decisions the model will make
        """
        self.decision_type = decision_type
        self.decision_history = []
        self.thresholds = {}
        self.weights = {}
        self.learning_enabled = False
        self.performance_metrics = {
            'decisions_made': 0,
            'accuracy': 0.0,
            'average_response_time': 0.0
        }

    def set_threshold(self, sensor_type: str, threshold_value: float, comparison: str = "greater"):
        """
        Set a threshold for decision making.

        Args:
            sensor_type: Type of sensor (e.g., 'temperature', 'light')
            threshold_value: Value to compare against
            comparison: Comparison type ('greater', 'less', 'equal')
        """
        self.thresholds[sensor_type] = {
            'value': threshold_value,
            'comparison': comparison
        }

    def set_weight(self, sensor_type: str, weight: float):
        """
        Set the weight/importance of a sensor in decision making.

        Args:
            sensor_type: Type of sensor
            weight: Weight value (0.0 to 1.0)
        """
        self.weights[sensor_type] = max(0.0, min(1.0, weight))  # Clamp between 0 and 1

    def make_decision(self, sensor_data: Dict[str, float]) -> Union[bool, int, float, str]:
        """
        Make a decision based on sensor data.

        Args:
            sensor_data: Dictionary of sensor readings

        Returns:
            Decision result (type depends on decision_type)
        """
        start_time = time.time()

        if self.decision_type == DecisionType.BINARY:
            decision = self._make_binary_decision(sensor_data)
        elif self.decision_type == DecisionType.MULTIPLE_CHOICE:
            decision = self._make_multiple_choice_decision(sensor_data)
        elif self.decision_type == DecisionType.CONTINUOUS:
            decision = self._make_continuous_decision(sensor_data)
        else:
            raise ValueError(f"Unknown decision type: {self.decision_type}")

        # Record decision in history
        decision_record = {
            'timestamp': time.time(),
            'input': sensor_data.copy(),
            'output': decision,
            'response_time': time.time() - start_time
        }
        self.decision_history.append(decision_record)

        # Update performance metrics
        self.performance_metrics['decisions_made'] += 1
        avg_time = self.performance_metrics['average_response_time']
        new_avg = (avg_time * (self.performance_metrics['decisions_made'] - 1) + decision_record['response_time']) / self.performance_metrics['decisions_made']
        self.performance_metrics['average_response_time'] = new_avg

        logger.info(f"Decision made: {decision} based on {sensor_data}")
        return decision

    def _make_binary_decision(self, sensor_data: Dict[str, float]) -> bool:
        """
        Make a binary (True/False) decision based on sensor data.

        Args:
            sensor_data: Dictionary of sensor readings

        Returns:
            Binary decision result
        """
        # Calculate weighted score based on sensor readings and thresholds
        score = 0.0
        total_weight = 0.0

        for sensor_type, reading in sensor_data.items():
            if sensor_type in self.thresholds:
                threshold_info = self.thresholds[sensor_type]
                weight = self.weights.get(sensor_type, 1.0)

                # Compare sensor reading to threshold
                if threshold_info['comparison'] == 'greater':
                    comparison_result = reading > threshold_info['value']
                elif threshold_info['comparison'] == 'less':
                    comparison_result = reading < threshold_info['value']
                elif threshold_info['comparison'] == 'equal':
                    comparison_result = abs(reading - threshold_info['value']) < 0.1  # Small tolerance
                else:
                    comparison_result = False

                # Add weighted result to score
                score += weight * (1.0 if comparison_result else 0.0)
                total_weight += weight

        # If no thresholds were applicable, use a default decision based on average
        if total_weight == 0:
            avg_reading = sum(sensor_data.values()) / len(sensor_data) if sensor_data else 0
            return avg_reading > 25  # Default threshold

        # Normalize score by total weight
        normalized_score = score / total_weight if total_weight > 0 else 0.5

        # Return True if normalized score is greater than 0.5
        return normalized_score > 0.5

    def _make_multiple_choice_decision(self, sensor_data: Dict[str, float]) -> int:
        """
        Make a multiple choice decision based on sensor data.

        Args:
            sensor_data: Dictionary of sensor readings

        Returns:
            Integer representing the choice (0, 1, 2, etc.)
        """
        # For this simple model, we'll categorize based on temperature ranges
        temp = sensor_data.get('temperature', 20.0)

        if temp < 18:
            return 0  # Cold
        elif temp < 25:
            return 1  # Normal
        elif temp < 30:
            return 2  # Warm
        else:
            return 3  # Hot

    def _make_continuous_decision(self, sensor_data: Dict[str, float]) -> float:
        """
        Make a continuous decision based on sensor data.

        Args:
            sensor_data: Dictionary of sensor readings

        Returns:
            Float value representing the decision
        """
        # Calculate a continuous value based on weighted sensor inputs
        result = 0.0
        total_weight = 0.0

        for sensor_type, reading in sensor_data.items():
            weight = self.weights.get(sensor_type, 1.0)
            result += weight * reading
            total_weight += weight

        if total_weight > 0:
            result = result / total_weight
        else:
            result = sum(sensor_data.values()) / len(sensor_data) if sensor_data else 0.0

        # Normalize to a reasonable range (0-100 for demonstration)
        result = max(0.0, min(100.0, result))
        return result

    def learn_from_feedback(self, decision_id: int, correct: bool):
        """
        Learn from feedback on a previous decision (simple reinforcement learning).

        Args:
            decision_id: Index of the decision in history
            correct: Whether the decision was correct
        """
        if not self.learning_enabled:
            return

        if decision_id < 0 or decision_id >= len(self.decision_history):
            logger.warning(f"Invalid decision ID: {decision_id}")
            return

        # In a more complex model, we would adjust weights/thresholds based on feedback
        # For this simple model, we'll just log the feedback
        decision_record = self.decision_history[decision_id]
        logger.info(f"Feedback received for decision at {decision_record['timestamp']}: {'Correct' if correct else 'Incorrect'}")

        # Update accuracy metric
        if self.performance_metrics['decisions_made'] > 0:
            current_accuracy = self.performance_metrics['accuracy']
            total_decisions = self.performance_metrics['decisions_made']
            new_accuracy = ((current_accuracy * (total_decisions - 1)) + (1.0 if correct else 0.0)) / total_decisions
            self.performance_metrics['accuracy'] = new_accuracy

    def get_performance_metrics(self) -> Dict[str, Union[int, float]]:
        """
        Get performance metrics for the decision model.

        Returns:
            Dictionary of performance metrics
        """
        return self.performance_metrics.copy()

    def reset_performance_metrics(self):
        """
        Reset all performance metrics to initial values.
        """
        self.performance_metrics = {
            'decisions_made': 0,
            'accuracy': 0.0,
            'average_response_time': 0.0
        }

    def get_decision_history(self) -> List[Dict]:
        """
        Get the history of all decisions made.

        Returns:
            List of decision records
        """
        return self.decision_history.copy()


def create_temperature_based_model() -> SimpleAIDecisionModel:
    """
    Create a pre-configured model for temperature-based decisions.

    Returns:
        Configured SimpleAIDecisionModel instance
    """
    model = SimpleAIDecisionModel(DecisionType.BINARY)

    # Set threshold for temperature: turn on cooling if temp > 25°C
    model.set_threshold('temperature', 25.0, 'greater')

    # Set weight for temperature sensor
    model.set_weight('temperature', 1.0)

    return model


def create_multi_sensor_model() -> SimpleAIDecisionModel:
    """
    Create a pre-configured model for multi-sensor decisions.

    Returns:
        Configured SimpleAIDecisionModel instance
    """
    model = SimpleAIDecisionModel(DecisionType.BINARY)

    # Set thresholds for multiple sensors
    model.set_threshold('temperature', 25.0, 'greater')
    model.set_threshold('light', 50.0, 'less')  # If light is low

    # Set weights for different sensors
    model.set_weight('temperature', 0.7)  # Temperature is more important
    model.set_weight('light', 0.3)        # Light is less important

    return model


def simulate_ai_decision_process(duration: float = 10.0, interval: float = 2.0):
    """
    Simulate an AI decision-making process over time.

    Args:
        duration: Total duration of simulation in seconds
        interval: Interval between decisions in seconds
    """
    logger.info("Starting AI decision-making simulation...")

    # Create a temperature-based model
    model = create_temperature_based_model()

    start_time = time.time()
    decision_count = 0

    while time.time() - start_time < duration:
        # Simulate sensor data (temperature that varies randomly)
        temperature = 22.0 + random.uniform(-5.0, 8.0)  # Base temp + random variation
        sensor_data = {'temperature': temperature}

        # Make a decision based on sensor data
        decision = model.make_decision(sensor_data)

        # Log the decision and its rationale
        action = "Activate cooling" if decision else "No action needed"
        logger.info(f"Temperature: {temperature:.2f}°C -> Decision: {decision} ({action})")

        decision_count += 1
        time.sleep(interval)

    # Print performance summary
    metrics = model.get_performance_metrics()
    logger.info(f"Simulation completed. Made {metrics['decisions_made']} decisions.")
    logger.info(f"Average response time: {metrics['average_response_time']:.4f}s")


def run_ai_model_demo():
    """
    Run a demonstration of the AI decision model.
    """
    logger.info("Running AI Decision Model Demo")

    # Create models
    temp_model = create_temperature_based_model()
    multi_model = create_multi_sensor_model()

    # Test with temperature data
    print("\n1. Testing temperature-based model:")
    temp_data = {'temperature': 28.5}
    decision = temp_model.make_decision(temp_data)
    print(f"Temperature {temp_data['temperature']}°C -> Decision: {decision}")

    temp_data = {'temperature': 20.0}
    decision = temp_model.make_decision(temp_data)
    print(f"Temperature {temp_data['temperature']}°C -> Decision: {decision}")

    # Test with multi-sensor data
    print("\n2. Testing multi-sensor model:")
    multi_data = {'temperature': 26.0, 'light': 30.0}
    decision = multi_model.make_decision(multi_data)
    print(f"Temp: {multi_data['temperature']}°C, Light: {multi_data['light']}% -> Decision: {decision}")

    multi_data = {'temperature': 22.0, 'light': 70.0}
    decision = multi_model.make_decision(multi_data)
    print(f"Temp: {multi_data['temperature']}°C, Light: {multi_data['light']}% -> Decision: {decision}")

    # Show performance metrics
    print("\n3. Performance metrics:")
    metrics = temp_model.get_performance_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    # Show decision history
    print("\n4. Decision history:")
    history = temp_model.get_decision_history()
    for i, record in enumerate(history):
        print(f"  Decision {i+1}: Input={record['input']}, Output={record['output']}")


if __name__ == "__main__":
    # Run the demo
    run_ai_model_demo()

    print("\n" + "="*50)
    print("Starting simulation...")
    simulate_ai_decision_process(duration=5.0, interval=1.0)