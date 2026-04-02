---
title: "Chapter 5: Acting in the Physical World"
section: "5.2"
chapter: "5"
---

# 5.2 Motor Control Systems

Motor control systems are fundamental to Physical AI applications, enabling precise control of rotational motion for navigation, manipulation, and other physical interactions. This section covers the principles, components, and techniques for controlling various types of motors in Physical AI systems.

## Fundamentals of Motor Control

### Control Objectives

Motor control systems aim to achieve specific performance objectives:

#### Position Control
- **Objective**: Move motor to specific angular position
- **Applications**: Robotic joints, camera positioning, antenna pointing
- **Requirements**: High precision, good stability
- **Techniques**: PID control, trajectory planning

#### Velocity Control
- **Objective**: Maintain specific rotational speed
- **Applications**: Conveyor systems, mobile robot wheels, fans
- **Requirements**: Good speed regulation, disturbance rejection
- **Techniques**: Speed feedback, current control

#### Torque Control
- **Objective**: Apply specific amount of rotational force
- **Applications**: Robotic manipulation, force control, clutches
- **Requirements**: Accurate force control, safety limits
- **Techniques**: Current control, force feedback

#### Multi-Variable Control
- **Objective**: Simultaneously control multiple variables
- **Applications**: Advanced robotic systems, coordinated motion
- **Requirements**: Complex control algorithms, coordination
- **Techniques**: MIMO control, advanced control theory

### Control System Architecture

#### Open-Loop Control
- **Concept**: Control signal applied without feedback
- **Advantages**: Simple, low cost, fast response
- **Disadvantages**: No error correction, affected by disturbances
- **Applications**: Simple on/off control, speed control without precision

#### Closed-Loop Control
- **Concept**: Feedback used to adjust control signal
- **Advantages**: Error correction, disturbance rejection
- **Disadvantages**: More complex, potential stability issues
- **Applications**: Precise position/velocity control

```python
class MotorController:
    def __init__(self, motor, encoder, kp=1.0, ki=0.1, kd=0.01):
        self.motor = motor
        self.encoder = encoder
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.prev_error = 0
        self.integral = 0
        self.setpoint = 0

    def update(self, dt):
        """Update controller with current time step"""
        current_position = self.encoder.read_position()
        error = self.setpoint - current_position

        # PID calculations
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0

        output = (self.kp * error +
                 self.ki * self.integral +
                 self.kd * derivative)

        # Apply control output to motor
        self.motor.set_voltage(output)
        self.prev_error = error

        return output
```

## DC Motor Control

### Basic DC Motor Control

DC motors are controlled by adjusting the voltage applied to the armature.

#### Voltage Control
- **Principle**: Motor speed is proportional to applied voltage
- **Implementation**: PWM (Pulse Width Modulation) for voltage control
- **Advantages**: Simple, efficient
- **Limitations**: No current limiting, speed varies with load

#### Current Control
- **Principle**: Torque is proportional to current
- **Implementation**: Current sensing and feedback
- **Advantages**: Direct torque control, protection
- **Applications**: Force control, stall protection

### H-Bridge Circuits

H-bridge circuits enable bidirectional motor control.

#### Circuit Configuration
- **Components**: Four switches (transistors) arranged in H configuration
- **Operation**: Different switch combinations control direction and braking
- **Modes**: Forward, reverse, brake, coast
- **Protection**: Flyback diodes protect against inductive kickback

#### Control Modes
- **Lock Anti-Phase**: PWM applied to both sides, smooth operation
- **Sign-Magnitude**: Direction and PWM separate, good for position control
- **Synchronous Rectification**: Active braking and efficiency

```python
class HBridgeController:
    def __init__(self, in1_pin, in2_pin, pwm_pin):
        self.in1_pin = in1_pin  # Direction pin 1
        self.in2_pin = in2_pin  # Direction pin 2
        self.pwm_pin = pwm_pin  # PWM speed control
        self.current_speed = 0

    def set_speed(self, speed):
        """
        Control motor speed and direction
        speed: -100 to 100 (negative = reverse)
        """
        if speed > 0:
            # Forward direction
            digitalWrite(self.in1_pin, HIGH)
            digitalWrite(self.in2_pin, LOW)
            pwm_value = int((speed / 100.0) * 255)
        elif speed < 0:
            # Reverse direction
            digitalWrite(self.in1_pin, LOW)
            digitalWrite(self.in2_pin, HIGH)
            pwm_value = int((-speed / 100.0) * 255)
        else:
            # Stop (brake)
            digitalWrite(self.in1_pin, HIGH)
            digitalWrite(self.in2_pin, HIGH)
            pwm_value = 0

        analogWrite(self.pwm_pin, pwm_value)
        self.current_speed = speed

    def brake(self):
        """Apply dynamic braking"""
        digitalWrite(self.in1_pin, HIGH)
        digitalWrite(self.in2_pin, HIGH)
        analogWrite(self.pwm_pin, 0)

    def coast(self):
        """Allow motor to coast freely"""
        digitalWrite(self.in1_pin, LOW)
        digitalWrite(self.in2_pin, LOW)
        analogWrite(self.pwm_pin, 0)
```

### Speed and Position Control

#### Speed Control
- **Feedback**: Tachometer or encoder for speed measurement
- **Controller**: PID or other feedback controller
- **Applications**: Mobile robots, conveyor systems
- **Challenges**: Load variations, friction effects

#### Position Control
- **Feedback**: Encoder or potentiometer for position
- **Controller**: Cascade of position and velocity controllers
- **Applications**: Robotic joints, camera positioning
- **Challenges**: Mechanical backlash, friction

## Stepper Motor Control

### Stepper Motor Fundamentals

Stepper motors move in discrete angular steps and provide precise positioning.

#### Step Modes
- **Full Step**: One phase or two phases energized
- **Half Step**: Alternates between one and two phases
- **Microstepping**: Fractional steps using current control
- **Advantages**: Higher resolution, smoother motion in microstepping

#### Drive Methods
- **Wave Drive**: One phase at a time, lower torque
- **Full Step Drive**: Two phases, higher torque
- **Half Step Drive**: Alternates between one/two phases
- **Microstepping**: Smooth current control for fine motion

### Stepper Motor Controllers

#### Basic Control
- **Step Pulses**: Digital pulses advance motor one step
- **Direction Signal**: Digital signal sets rotation direction
- **Enable Signal**: Turns motor on/off for power saving
- **Resolution**: Determined by motor and driver

#### Advanced Features
- **Current Control**: Chopper drive for constant current
- **Decay Modes**: Fast/slow decay for different performance
- **Microstepping**: Fractional step resolution
- **Stall Detection**: Detect when motor stalls

```python
class StepperController:
    def __init__(self, step_pin, dir_pin, enable_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.position = 0
        self.microsteps = 1  # Steps per full step

    def step(self, direction=1, steps=1):
        """Generate step pulses to move motor"""
        digitalWrite(self.dir_pin, HIGH if direction > 0 else LOW)

        for _ in range(steps * self.microsteps):
            digitalWrite(self.step_pin, HIGH)
            delayMicroseconds(5)  # Pulse width
            digitalWrite(self.step_pin, LOW)
            delayMicroseconds(5)  # Inter-step delay

        self.position += direction * steps

    def move_to(self, target_position, speed=1000):
        """Move to absolute position"""
        steps_needed = target_position - self.position
        direction = 1 if steps_needed > 0 else -1
        steps = abs(steps_needed)

        # Calculate delay based on speed
        delay_us = max(100, 1000000 // speed)  # Minimum 100us

        for _ in range(steps * self.microsteps):
            digitalWrite(self.step_pin, HIGH)
            delayMicroseconds(5)
            digitalWrite(self.step_pin, LOW)
            delayMicroseconds(delay_us)

        self.position = target_position

    def set_microstepping(self, divisor):
        """Set microstepping resolution"""
        self.microsteps = divisor
```

## Servo Motor Control

### Servo Control Principles

Servo motors use closed-loop control for precise position control.

#### PWM Control Signal
- **Frequency**: Typically 50 Hz (20 ms period)
- **Pulse Width**: 1-2 ms range for 180° rotation
- **Neutral**: 1.5 ms pulse for center position
- **Range**: 1 ms to 2 ms for full rotation

#### Internal Control
- **Feedback**: Potentiometer for position feedback
- **Controller**: Internal electronics for position control
- **Motor**: DC motor with gear reduction
- **Protection**: Stall detection, thermal protection

### Advanced Servo Control

#### Continuous Rotation Servos
- **Modification**: Feedback removed or modified
- **Control**: Speed and direction via pulse width
- **Applications**: Mobile robot wheels, continuous motion
- **Limitations**: No position feedback

#### Digital Servos
- **Advantages**: Faster, more precise control
- **Features**: Higher resolution, better holding torque
- **Communication**: Digital rather than analog control
- **Applications**: High-performance robotics

```python
class ServoController:
    def __init__(self, pwm_pin, min_pulse=500, max_pulse=2500, angle_range=180):
        self.pwm_pin = pwm_pin
        self.min_pulse = min_pulse  # microseconds
        self.max_pulse = max_pulse  # microseconds
        self.angle_range = angle_range
        self.current_angle = 90  # Default to center

    def set_angle(self, angle):
        """Set servo to specific angle"""
        # Clamp angle to valid range
        angle = max(0, min(self.angle_range, angle))

        # Convert angle to pulse width
        pulse_width = self.min_pulse + (angle / self.angle_range) * (self.max_pulse - self.min_pulse)

        # Generate PWM pulse
        self._generate_pwm_pulse(pulse_width)
        self.current_angle = angle

    def _generate_pwm_pulse(self, pulse_width):
        """Generate PWM pulse for servo control"""
        digitalWrite(self.pwm_pin, HIGH)
        delayMicroseconds(pulse_width)
        digitalWrite(self.pwm_pin, LOW)

        # Wait for remainder of 20ms period
        remaining_time = 20000 - pulse_width
        if remaining_time > 0:
            delayMicroseconds(remaining_time)

    def sweep(self, start_angle, end_angle, step=1, delay_ms=20):
        """Sweep servo between angles"""
        direction = 1 if end_angle > start_angle else -1
        for angle in range(int(start_angle), int(end_angle) + direction, direction * step):
            self.set_angle(angle)
            delay(delay_ms)
```

## Brushless DC Motor Control

### BLDC Fundamentals

Brushless DC motors eliminate mechanical commutation with electronic control.

#### Construction
- **Stator**: Electromagnetic windings (usually 3-phase)
- **Rotor**: Permanent magnets
- **Sensors**: Hall effect sensors or encoder for position
- **Controller**: Electronic commutation circuitry

#### Advantages
- **Efficiency**: Higher efficiency than brushed motors
- **Reliability**: No brushes to wear out
- **Speed**: Higher speed capability
- **Control**: Better speed/torque characteristics

### Electronic Commutation

#### Trapezoidal Control
- **Method**: 6-step commutation sequence
- **Advantages**: Simple, robust
- **Characteristics**: Trapezoidal back-EMF
- **Applications**: Cost-sensitive applications

#### Sinusoidal Control
- **Method**: Sinusoidal phase currents
- **Advantages**: Smooth operation, low noise
- **Characteristics**: Sinusoidal back-EMF
- **Applications**: Precision applications

#### Field-Oriented Control (FOC)
- **Method**: Vector control of magnetic fields
- **Advantages**: Optimal torque production
- **Complexity**: More complex control algorithm
- **Applications**: High-performance applications

## Control System Design

### PID Control in Motor Systems

PID (Proportional-Integral-Derivative) control is widely used in motor control.

#### Proportional Control
- **Action**: Proportional to current error
- **Effect**: Reduces steady-state error
- **Limitations**: May cause oscillation
- **Tuning**: Higher Kp = faster response

#### Integral Control
- **Action**: Proportional to accumulated error
- **Effect**: Eliminates steady-state error
- **Limitations**: Can cause instability
- **Anti-Windup**: Prevents integrator saturation

#### Derivative Control
- **Action**: Proportional to error rate of change
- **Effect**: Anticipates future error
- **Limitations**: Sensitive to noise
- **Filtering**: Often filtered in implementation

### Cascade Control

Cascade control uses multiple control loops for better performance.

#### Position-Velocity Loop
- **Outer Loop**: Position control
- **Inner Loop**: Velocity control
- **Advantages**: Better disturbance rejection
- **Implementation**: Two PID controllers

#### Velocity-Current Loop
- **Outer Loop**: Velocity control
- **Inner Loop**: Current (torque) control
- **Advantages**: Direct torque control
- **Applications**: Force control applications

### Advanced Control Techniques

#### Model Predictive Control (MPC)
- **Concept**: Optimize control over future time horizon
- **Advantages**: Handles constraints naturally
- **Applications**: High-performance systems
- **Complexity**: Computationally intensive

#### Adaptive Control
- **Concept**: Adjust parameters based on changing conditions
- **Advantages**: Maintains performance with changing loads
- **Applications**: Varying operating conditions
- **Challenges**: Stability and convergence

Motor control systems are critical for the precise and reliable operation of Physical AI systems. Understanding the different control techniques and their applications enables the design of effective motor control solutions for various physical AI applications.