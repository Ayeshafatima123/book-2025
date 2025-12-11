# Quickstart Guide for PHYSICAL-AI-BOOK

## Prerequisites

Before starting with the PHYSICAL-AI-BOOK examples, you'll need:

### Software Requirements
- Python 3.9 or higher
- pip package manager
- Git for version control
- Text editor or IDE (VS Code recommended)

### Hardware Requirements (Basic Setup)
- 1x Raspberry Pi 4 (or newer) with power supply
- 1x MicroSD card (32GB recommended)
- Jumper wires (male-to-female and male-to-male)
- Breadboard
- Resistors (220Ω, 1kΩ, 10kΩ)
- LEDs (various colors)
- Push buttons
- Temperature/humidity sensor (DHT22 recommended)

## Setup Steps

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-repo/physical-ai-book.git
cd physical-ai-book

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Hardware Setup
1. Insert the MicroSD card into your Raspberry Pi
2. Connect power supply and boot the Raspberry Pi
3. Connect to the Raspberry Pi via SSH or use a monitor directly
4. Connect the breadboard and components as shown in the wiring diagrams

### 3. First Example: LED Control with AI Decision
```python
# Navigate to the first example
cd code-examples/ai-models

# Run the LED control example
python led_ai_control.py
```

This example demonstrates a simple AI model that decides when to turn an LED on or off based on sensor input.

## Running Examples

Each chapter has its own directory with examples:

```bash
# To run examples from Chapter 1
cd code-examples/chapter-01/
python example_01.py

# To run hardware tests
cd tests/hardware/
python test_led.py
python test_sensor.py
```

## Safety Guidelines

⚠️ **IMPORTANT**: Always follow safety guidelines when working with physical AI systems:

1. Disconnect power before making hardware changes
2. Verify all connections before applying power
3. Never exceed component voltage/current ratings
4. Have a fire extinguisher nearby when working with power circuits
5. Use appropriate personal protective equipment when required

## Troubleshooting

### Common Issues

**Issue**: Code runs but hardware doesn't respond
- Check GPIO pin connections
- Verify correct pin numbers in code
- Ensure proper power supply to components

**Issue**: Sensor readings are inaccurate
- Check wiring connections
- Verify sensor power supply
- Calibrate sensor if required

**Issue**: AI model produces unexpected results
- Verify training data quality
- Check model parameters
- Ensure proper input preprocessing

## Next Steps

1. Complete the setup and run the first example
2. Read Chapter 1 to understand the theoretical background
3. Try modifying the example code to see different behaviors
4. Move to Chapter 2 for more advanced physical AI concepts