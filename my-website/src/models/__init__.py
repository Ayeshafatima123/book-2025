"""
Base models for the PHYSICAL-AI-BOOK project.

This module defines the core data models based on the data model specification:
- Chapter
- CodeExample
- HardwareComponent
- SafetyGuideline
- Project
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class DifficultyLevel(Enum):
    """Enumeration for difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class HardwareType(Enum):
    """Enumeration for hardware component types."""
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    CONTROLLER = "controller"
    OTHER = "other"


class RiskLevel(Enum):
    """Enumeration for risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Chapter:
    """Represents a book chapter."""
    id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    hardware_required: List[str]
    estimated_time: int  # in minutes
    objectives: List[str]
    prerequisites: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.difficulty, str):
            self.difficulty = DifficultyLevel(self.difficulty)
        if not isinstance(self.hardware_required, list):
            self.hardware_required = []
        if not isinstance(self.objectives, list):
            self.objectives = []
        if not isinstance(self.prerequisites, list):
            self.prerequisites = []


@dataclass
class CodeExample:
    """Represents a code example within a chapter."""
    id: str
    chapter_id: str
    title: str
    description: str
    language: str
    code: str
    hardware_setup: str
    expected_output: str
    safety_considerations: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class HardwareComponent:
    """Represents a hardware component."""
    id: str
    name: str
    type: HardwareType
    description: str
    compatibility: List[str]  # e.g., ["Arduino", "Raspberry Pi"]
    cost_range: str  # e.g., "$5-10"
    difficulty: DifficultyLevel
    common_uses: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = HardwareType(self.type)
        if isinstance(self.difficulty, str):
            self.difficulty = DifficultyLevel(self.difficulty)
        if not isinstance(self.compatibility, list):
            self.compatibility = []
        if not isinstance(self.common_uses, list):
            self.common_uses = []


@dataclass
class SafetyGuideline:
    """Represents a safety guideline."""
    id: str
    component_id: Optional[str]  # Foreign key to HardwareComponent, optional
    chapter_id: Optional[str]    # Foreign key to Chapter, optional
    title: str
    description: str
    risk_level: RiskLevel
    required_equipment: List[str]
    emergency_procedures: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.risk_level, str):
            self.risk_level = RiskLevel(self.risk_level)
        if not isinstance(self.required_equipment, list):
            self.required_equipment = []


@dataclass
class Project:
    """Represents a project within a chapter."""
    id: str
    chapter_id: str
    title: str
    description: str
    materials_needed: List[str]
    steps: List[str]
    expected_outcome: str
    troubleshooting_tips: List[str]
    validation_tests: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not isinstance(self.materials_needed, list):
            self.materials_needed = []
        if not isinstance(self.steps, list):
            self.steps = []
        if not isinstance(self.troubleshooting_tips, list):
            self.troubleshooting_tips = []
        if not isinstance(self.validation_tests, list):
            self.validation_tests = []


# Helper functions for creating model instances

def create_chapter(**kwargs) -> Chapter:
    """Create a Chapter instance with validation."""
    return Chapter(**kwargs)


def create_code_example(**kwargs) -> CodeExample:
    """Create a CodeExample instance with validation."""
    return CodeExample(**kwargs)


def create_hardware_component(**kwargs) -> HardwareComponent:
    """Create a HardwareComponent instance with validation."""
    return HardwareComponent(**kwargs)


def create_safety_guideline(**kwargs) -> SafetyGuideline:
    """Create a SafetyGuideline instance with validation."""
    return SafetyGuideline(**kwargs)


def create_project(**kwargs) -> Project:
    """Create a Project instance with validation."""
    return Project(**kwargs)


# Sample data creation functions

def create_sample_chapter_01() -> Chapter:
    """Create a sample Chapter 1 instance."""
    return create_chapter(
        id="ch-01-intro-ai-hardware",
        title="Introduction to AI-Hardware Interaction",
        description="Learn the basics of how AI systems can interact with physical hardware.",
        difficulty=DifficultyLevel.BEGINNER,
        hardware_required=["LED", "Temperature Sensor", "Raspberry Pi"],
        estimated_time=120,
        objectives=[
            "Understand basic AI-hardware interaction concepts",
            "Set up a simple sensor-actuator system",
            "Implement basic safety measures"
        ],
        prerequisites=[
            "Basic Python knowledge",
            "Familiarity with electronics concepts"
        ]
    )


def create_sample_code_example_01() -> CodeExample:
    """Create a sample CodeExample for Chapter 1."""
    sample_code = '''
import time
import random

def read_temperature():
    # Simulate temperature reading
    return round(random.uniform(20.0, 30.0), 2)

def control_led(temperature):
    if temperature > 25:
        print("LED ON - High temperature detected")
        return True
    else:
        print("LED OFF - Temperature normal")
        return False

# Main loop
while True:
    temp = read_temperature()
    led_state = control_led(temp)
    print(f"Temperature: {temp}°C, LED: {led_state}")
    time.sleep(2)
'''

    return create_code_example(
        id="ce-01-basic-ai-control",
        chapter_id="ch-01-intro-ai-hardware",
        title="Basic AI Decision Making with LED Control",
        description="A simple example of AI making decisions based on sensor input to control an LED.",
        language="Python",
        code=sample_code,
        hardware_setup="Connect LED to GPIO pin 18, Temperature sensor to GPIO pin 4",
        expected_output="LED turns on when simulated temperature exceeds 25°C",
        safety_considerations="Ensure proper current limiting resistors are used with the LED to prevent damage."
    )


def create_sample_hardware_component() -> HardwareComponent:
    """Create a sample HardwareComponent."""
    return create_hardware_component(
        id="hc-01-dht22-sensor",
        name="DHT22 Temperature/Humidity Sensor",
        type=HardwareType.SENSOR,
        description="Digital temperature and humidity sensor with calibrated digital signal output.",
        compatibility=["Raspberry Pi", "Arduino"],
        cost_range="$3-5",
        difficulty=DifficultyLevel.BEGINNER,
        common_uses=[
            "Temperature monitoring",
            "Humidity sensing",
            "Environmental control systems"
        ]
    )


def create_sample_safety_guideline() -> SafetyGuideline:
    """Create a sample SafetyGuideline."""
    return create_safety_guideline(
        id="sg-01-temperature-sensor",
        component_id="hc-01-dht22-sensor",
        chapter_id="ch-01-intro-ai-hardware",
        title="Temperature Sensor Safety",
        description="Proper handling and installation of temperature sensors to prevent electrical hazards.",
        risk_level=RiskLevel.LOW,
        required_equipment=["Multimeter", "Safety glasses"],
        emergency_procedures="If sensor becomes hot or emits smoke, disconnect power immediately and allow to cool before inspection."
    )


def create_sample_project() -> Project:
    """Create a sample Project for Chapter 1."""
    return create_project(
        id="proj-01-led-temp-control",
        chapter_id="ch-01-intro-ai-hardware",
        title="Smart LED Temperature Control",
        description="Build a system that automatically controls an LED based on temperature readings.",
        materials_needed=[
            "Raspberry Pi",
            "DHT22 Temperature Sensor",
            "LED",
            "220Ω Resistor",
            "Breadboard",
            "Jumper wires"
        ],
        steps=[
            "Connect the DHT22 sensor to the Raspberry Pi",
            "Connect the LED with a current limiting resistor",
            "Install required Python libraries",
            "Run the AI control code"
        ],
        expected_outcome="LED automatically turns on/off based on temperature readings",
        troubleshooting_tips=[
            "Check all connections if sensor readings are 0 or incorrect",
            "Verify GPIO pin assignments in code match physical connections",
            "Ensure sensor is not in direct sunlight which may affect readings"
        ],
        validation_tests=[
            "Verify temperature readings change when sensor is heated/cooled",
            "Confirm LED responds appropriately to temperature changes",
            "Test safety measures work correctly"
        ]
    )