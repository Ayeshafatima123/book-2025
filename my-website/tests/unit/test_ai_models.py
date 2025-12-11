"""
Unit tests for AI model components.
"""

import unittest
import sys
import os

# Add the code-examples directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../code-examples/ai-models'))

from simple_decision import SimpleAIDecisionModel, DecisionType, create_temperature_based_model, create_multi_sensor_model


class TestAIDecisionModel(unittest.TestCase):
    """Unit tests for AI decision model."""

    def test_model_initialization_binary(self):
        """Test model initialization with binary decision type."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        self.assertEqual(model.decision_type, DecisionType.BINARY)
        self.assertEqual(len(model.decision_history), 0)

    def test_model_initialization_multiple_choice(self):
        """Test model initialization with multiple choice decision type."""
        model = SimpleAIDecisionModel(DecisionType.MULTIPLE_CHOICE)
        self.assertEqual(model.decision_type, DecisionType.MULTIPLE_CHOICE)

    def test_set_threshold(self):
        """Test setting a threshold for decision making."""
        model = SimpleAIDecisionModel()
        model.set_threshold('temperature', 25.0, 'greater')

        self.assertIn('temperature', model.thresholds)
        self.assertEqual(model.thresholds['temperature']['value'], 25.0)
        self.assertEqual(model.thresholds['temperature']['comparison'], 'greater')

    def test_set_weight(self):
        """Test setting a weight for a sensor."""
        model = SimpleAIDecisionModel()
        model.set_weight('temperature', 0.8)

        self.assertIn('temperature', model.weights)
        self.assertEqual(model.weights['temperature'], 0.8)

    def test_set_weight_clamping(self):
        """Test that weights are clamped between 0 and 1."""
        model = SimpleAIDecisionModel()
        model.set_weight('temperature', 1.5)  # Should be clamped to 1.0
        self.assertEqual(model.weights['temperature'], 1.0)

        model.set_weight('humidity', -0.5)  # Should be clamped to 0.0
        self.assertEqual(model.weights['humidity'], 0.0)

    def test_binary_decision_true_condition(self):
        """Test binary decision when condition is true."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        model.set_threshold('temperature', 20.0, 'greater')
        model.set_weight('temperature', 1.0)

        sensor_data = {'temperature': 25.0}
        decision = model.make_decision(sensor_data)
        self.assertTrue(decision)  # 25 > 20, so decision should be True

    def test_binary_decision_false_condition(self):
        """Test binary decision when condition is false."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        model.set_threshold('temperature', 30.0, 'greater')
        model.set_weight('temperature', 1.0)

        sensor_data = {'temperature': 25.0}
        decision = model.make_decision(sensor_data)
        self.assertFalse(decision)  # 25 is not > 30, so decision should be False

    def test_binary_decision_less_comparison(self):
        """Test binary decision with 'less' comparison."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        model.set_threshold('temperature', 30.0, 'less')
        model.set_weight('temperature', 1.0)

        sensor_data = {'temperature': 25.0}
        decision = model.make_decision(sensor_data)
        self.assertTrue(decision)  # 25 < 30, so decision should be True

    def test_multiple_choice_decision(self):
        """Test multiple choice decision making."""
        model = SimpleAIDecisionModel(DecisionType.MULTIPLE_CHOICE)

        # Test different temperature ranges
        sensor_data = {'temperature': 15.0}  # Should be cold (0)
        decision = model.make_decision(sensor_data)
        self.assertEqual(decision, 0)

        sensor_data = {'temperature': 22.0}  # Should be normal (1)
        decision = model.make_decision(sensor_data)
        self.assertEqual(decision, 1)

        sensor_data = {'temperature': 28.0}  # Should be warm (2)
        decision = model.make_decision(sensor_data)
        self.assertEqual(decision, 2)

        sensor_data = {'temperature': 35.0}  # Should be hot (3)
        decision = model.make_decision(sensor_data)
        self.assertEqual(decision, 3)

    def test_continuous_decision(self):
        """Test continuous decision making."""
        model = SimpleAIDecisionModel(DecisionType.CONTINUOUS)
        model.set_weight('temperature', 1.0)

        sensor_data = {'temperature': 25.0}
        decision = model.make_decision(sensor_data)
        # Should be the temperature value, normalized to 0-100 range
        self.assertIsInstance(decision, float)
        self.assertGreaterEqual(decision, 0.0)
        self.assertLessEqual(decision, 100.0)

    def test_decision_history_tracking(self):
        """Test that decisions are tracked in history."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        model.set_threshold('temperature', 25.0, 'greater')

        sensor_data = {'temperature': 30.0}
        model.make_decision(sensor_data)

        self.assertEqual(len(model.decision_history), 1)
        record = model.decision_history[0]
        self.assertIn('timestamp', record)
        self.assertIn('input', record)
        self.assertIn('output', record)
        self.assertIn('response_time', record)
        self.assertEqual(record['input'], sensor_data)
        self.assertEqual(record['output'], True)

    def test_performance_metrics_tracking(self):
        """Test that performance metrics are updated."""
        model = SimpleAIDecisionModel(DecisionType.BINARY)
        model.set_threshold('temperature', 25.0, 'greater')

        initial_metrics = model.get_performance_metrics()
        self.assertEqual(initial_metrics['decisions_made'], 0)

        sensor_data = {'temperature': 30.0}
        model.make_decision(sensor_data)

        updated_metrics = model.get_performance_metrics()
        self.assertEqual(updated_metrics['decisions_made'], 1)
        self.assertGreaterEqual(updated_metrics['average_response_time'], 0)

    def test_create_temperature_based_model(self):
        """Test creating a pre-configured temperature-based model."""
        model = create_temperature_based_model()

        self.assertEqual(model.decision_type, DecisionType.BINARY)
        self.assertIn('temperature', model.thresholds)
        self.assertEqual(model.thresholds['temperature']['value'], 25.0)
        self.assertEqual(model.thresholds['temperature']['comparison'], 'greater')
        self.assertIn('temperature', model.weights)
        self.assertEqual(model.weights['temperature'], 1.0)

    def test_create_multi_sensor_model(self):
        """Test creating a pre-configured multi-sensor model."""
        model = create_multi_sensor_model()

        self.assertEqual(model.decision_type, DecisionType.BINARY)
        self.assertIn('temperature', model.thresholds)
        self.assertIn('light', model.thresholds)
        self.assertIn('temperature', model.weights)
        self.assertIn('light', model.weights)
        # Check that temperature has higher weight than light
        self.assertGreater(model.weights['temperature'], model.weights['light'])


if __name__ == '__main__':
    unittest.main()