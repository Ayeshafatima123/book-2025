---
title: "Chapter 5: Acting in the Physical World"
section: "5.1"
chapter: "5"
---

# 5.1 Types of Actuators

Actuators are the components that enable Physical AI systems to interact with and modify their physical environment. This section explores the various types of actuators used in Physical AI applications, their operating principles, and their specific applications.

## Electric Actuators

Electric actuators convert electrical energy into mechanical motion and are the most common type in Physical AI systems.

### DC Motors

DC motors are widely used for their simplicity and controllability.

#### Operating Principles
- **Construction**: Stator (field) and rotor (armature) with commutator
- **Principle**: Current-carrying conductors in magnetic field experience force
- **Speed Control**: Proportional to applied voltage
- **Torque Control**: Proportional to current

#### Characteristics
- **Speed-Torque Curve**: Inherently has negative slope
- **Efficiency**: Good efficiency across operating range
- **Control**: Simple voltage control for speed, current control for torque
- **Applications**: Wheeled robots, simple motion control

#### Variants
- **Brushed DC**: Mechanical commutation, simple control
- **Brushless DC**: Electronic commutation, higher efficiency
- **Gear Motors**: Integrated gearbox for higher torque, lower speed

```python
class DCMotor:
    def __init__(self, pwm_pin, dir_pin, max_speed=255):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.max_speed = max_speed
        self.current_speed = 0

    def set_speed(self, speed):
        """
        Set motor speed with direction control
        speed: -100 to 100 (negative = reverse)
        """
        if speed > 0:
            digitalWrite(self.dir_pin, HIGH)  # Forward
            pwm_value = int((speed / 100.0) * self.max_speed)
        elif speed < 0:
            digitalWrite(self.dir_pin, LOW)   # Reverse
            pwm_value = int((-speed / 100.0) * self.max_speed)
        else:
            pwm_value = 0  # Stop

        analogWrite(self.pwm_pin, pwm_value)
        self.current_speed = speed
```

### Stepper Motors

Stepper motors move in discrete steps and provide precise positioning without feedback.

#### Operating Principles
- **Construction**: Multiple stator phases, permanent magnet or variable reluctance rotor
- **Operation**: Sequential energization of phases moves rotor in steps
- **Step Angle**: Fixed angle per step (e.g., 1.8° = 200 steps/revolution)
- **Open-Loop Control**: Position maintained by step counting

#### Characteristics
- **Precision**: Accurate positioning without feedback
- **Holding Torque**: Maintains position when powered
- **Speed Limitations**: Torque decreases at higher speeds
- **Resonance**: Can experience resonance at certain speeds

#### Types
- **Permanent Magnet**: Lower torque, simpler control
- **Variable Reluctance**: Higher speed capability
- **Hybrid**: Best of both, most common type

### Servo Motors

Servo motors integrate motor, feedback, and control electronics for precise position control.

#### Operating Principles
- **Components**: Motor, encoder/feedback, control electronics
- **Control**: PWM signal specifies desired position
- **Feedback**: Continuous position monitoring and correction
- **Gearing**: Internal gearbox for higher torque, precision

#### Characteristics
- **Range**: Typically 0-180° rotation
- **Precision**: High positional accuracy
- **Speed**: Moderate speed with good control
- **Holding**: Maintains position under load

#### Types
- **Standard Servos**: Basic position control
- **Continuous Rotation**: Modified for continuous motion
- **Digital Servos**: Faster, more precise control
- **High-Torque Servos**: Higher power output

## Hydraulic and Pneumatic Actuators

These actuators use pressurized fluids to generate motion and are suitable for high-force applications.

### Hydraulic Actuators

Hydraulic actuators use pressurized liquid (typically oil) to generate force.

#### Operating Principles
- **Pascal's Law**: Pressure applied to fluid is transmitted equally
- **Cylinder Design**: Piston in cylinder with fluid on both sides
- **Force Generation**: Force = Pressure × Area
- **Control**: Valves control fluid flow and direction

#### Characteristics
- **High Force**: Capable of very high forces and torques
- **Precision**: Good force and position control
- **Power Density**: High power-to-weight ratio
- **Maintenance**: Requires fluid system maintenance

#### Applications
- **Heavy Machinery**: Construction equipment, industrial robots
- **Aerospace**: Flight control surfaces, landing gear
- **Manufacturing**: Presses, clamps, heavy assembly

### Pneumatic Actuators

Pneumatic actuators use compressed air to generate motion.

#### Operating Principles
- **Compressed Air**: Stores potential energy in compressed state
- **Cylinder Design**: Similar to hydraulic but with air
- **Force Generation**: Lower forces due to lower air pressure
- **Control**: Valves control air flow and direction

#### Characteristics
- **Clean Operation**: No fluid contamination risk
- **Fast Response**: Quick action due to air compressibility
- **Lower Forces**: Limited by air pressure constraints
- **Energy Efficiency**: Compressing air is energy intensive

#### Applications
- **Factory Automation**: Pick-and-place, assembly operations
- **Medical Equipment**: Surgical tools, patient positioning
- **Robotics**: Lightweight, fast-acting applications

## Linear Actuators

Linear actuators provide straight-line motion rather than rotational motion.

### Electric Linear Actuators

Electric linear actuators convert rotary motion to linear motion.

#### Screw-Based Actuators
- **Lead Screw**: Rotary motion converted to linear via screw threads
- **Ball Screw**: Lower friction, higher efficiency
- **Acme Screw**: Self-locking, moderate efficiency
- **Applications**: Positioning, lifting, pushing

#### Characteristics
- **Precision**: High positional accuracy
- **Speed**: Moderate speeds, depends on screw pitch
- **Force**: Good force capabilities
- **Self-Locking**: Some designs prevent back-driving

### Piezoelectric Actuators

Piezoelectric actuators use the piezoelectric effect for motion.

#### Operating Principles
- **Piezoelectric Effect**: Electric field causes dimensional change
- **Materials**: Ceramic materials like PZT
- **Motion**: Very small, precise displacements
- **Speed**: Very fast response times

#### Characteristics
- **Precision**: Nanometer-level positioning
- **Speed**: Microsecond response times
- **Force**: Limited force output
- **Stroke**: Very limited displacement

#### Applications
- **Precision Instruments**: Microscopes, optical equipment
- **Micro-Robotics**: Tiny manipulation tasks
- **Optics**: Mirror positioning, focusing

## Specialized Actuators

### Shape Memory Alloy (SMA) Actuators

SMA actuators change shape when heated.

#### Operating Principles
- **Material Property**: Crystal structure changes with temperature
- **Actuation**: Heat causes shape change, cooling returns to original
- **Force**: Significant force generation
- **Speed**: Slower heating/cooling cycle

#### Characteristics
- **Silent Operation**: No electromagnetic noise
- **High Force-to-Weight**: Good power density
- **Slow Response**: Limited by thermal time constants
- **Control**: Temperature-based control

### Electroactive Polymer (EAP) Actuators

EAP actuators change shape when electric field is applied.

#### Operating Principles
- **Electric Field**: Applied field causes polymer deformation
- **Materials**: Various polymer types with different properties
- **Motion**: Large strain capability
- **Applications**: Bio-inspired systems

#### Characteristics
- **Large Deformation**: Significant shape change possible
- **Low Voltage**: Some types operate at low voltages
- **Slow Response**: Generally slower than other actuators
- **Durability**: Long-term reliability concerns

## Actuator Selection Criteria

### Performance Requirements

#### Force/Torque Requirements
- **Static Load**: Force needed to hold position
- **Dynamic Load**: Force needed for acceleration
- **Safety Factor**: Design margin for unexpected loads
- **Efficiency**: Power consumption considerations

#### Speed Requirements
- **Maximum Speed**: Peak operational speed
- **Acceleration**: Required acceleration/deceleration
- **Response Time**: Time to reach commanded position
- **Bandwidth**: Frequency response requirements

#### Precision Requirements
- **Resolution**: Smallest incremental movement
- **Accuracy**: How close to commanded position
- **Repeatability**: Consistency of repeated movements
- **Linearity**: Deviation from ideal response

### Environmental Considerations

#### Operating Environment
- **Temperature**: Operating temperature range
- **Humidity**: Moisture protection requirements
- **Dust/Contamination**: Sealing requirements
- **Chemical Exposure**: Resistance to chemicals

#### Physical Constraints
- **Size**: Physical space limitations
- **Weight**: Weight considerations for mobile systems
- **Power**: Available power and efficiency needs
- **Heat**: Thermal management requirements

### Cost and Maintenance

#### Initial Cost
- **Component Cost**: Actuator and associated components
- **Integration Cost**: Mounting, wiring, control electronics
- **Development Cost**: Design and implementation time

#### Operating Cost
- **Power Consumption**: Energy usage over time
- **Maintenance**: Regular service requirements
- **Replacement**: Expected lifetime and replacement costs

Understanding the different types of actuators and their characteristics is essential for selecting the right actuation method for specific Physical AI applications and ensuring optimal system performance.