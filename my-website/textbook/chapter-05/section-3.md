---
title: "Chapter 5: Acting in the Physical World"
section: "5.3"
chapter: "5"
---

# 5.3 Feedback Control Loops

Feedback control loops are essential for precise and stable operation of Physical AI systems. They continuously monitor system performance and adjust control actions to achieve desired behavior despite disturbances and uncertainties. This section explores the principles, design, and implementation of feedback control systems.

## Fundamentals of Feedback Control

### Control System Components

A feedback control system consists of several key components working together:

#### Plant
- **Definition**: The physical system being controlled (motor, robot, mechanism)
- **Characteristics**: Dynamic behavior, inputs, outputs, disturbances
- **Modeling**: Mathematical representation of system behavior
- **Complexity**: Can range from simple to highly complex systems

#### Sensor
- **Function**: Measure system output or relevant variables
- **Types**: Position, velocity, force, temperature, pressure sensors
- **Characteristics**: Accuracy, resolution, bandwidth, noise
- **Selection**: Match to control requirements and environment

#### Controller
- **Function**: Process sensor data and generate control signals
- **Types**: PID, state-space, adaptive, robust controllers
- **Implementation**: Analog or digital, hardware or software
- **Tuning**: Adjust parameters for desired performance

#### Actuator
- **Function**: Apply control signal to the plant
- **Types**: Motors, valves, heaters, pumps
- **Characteristics**: Bandwidth, saturation, deadband, efficiency
- **Integration**: Interface between controller and plant

### Control System Objectives

#### Stability
- **Definition**: System returns to equilibrium after disturbances
- **Importance**: Fundamental requirement for all control systems
- **Analysis**: Various methods for stability assessment
- **Design**: Primary concern in controller design

#### Accuracy
- **Definition**: System output matches desired reference
- **Steady-state error**: Error after system reaches equilibrium
- **Tracking**: Ability to follow time-varying references
- **Disturbance rejection**: Minimize effect of external disturbances

#### Transient Response
- **Rise time**: Time to reach target value
- **Overshoot**: Exceeding target value during response
- **Settling time**: Time to stay within tolerance band
- **Oscillations**: Undesired oscillatory behavior

## Classical Control Theory

### Transfer Functions

Transfer functions describe the input-output relationship in the frequency domain.

#### Definition
- **Mathematical form**: Ratio of Laplace transforms of output to input
- **Assumptions**: Linear, time-invariant systems
- **Representation**: Polynomial ratio (numerator/denominator)
- **Poles and zeros**: Roots of denominator and numerator polynomials

#### Common Transfer Functions
- **First-order**: G(s) = K/(τs + 1) - Simple lag behavior
- **Second-order**: G(s) = ωn²/(s² + 2ζωns + ωn²) - Oscillatory behavior
- **Integrator**: G(s) = K/s - Accumulating behavior
- **Delay**: G(s) = e^(-Ls) - Time delay (approximated)

#### System Response Analysis
- **Step response**: Response to unit step input
- **Frequency response**: Response to sinusoidal inputs
- **Stability margins**: Gain and phase margins
- **Bode plots**: Graphical frequency response representation

### PID Controllers

PID (Proportional-Integral-Derivative) controllers are the most widely used controllers.

#### Mathematical Form
- **Equation**: u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt
- **Proportional**: Immediate response to current error
- **Integral**: Eliminates steady-state error
- **Derivative**: Anticipates future error based on rate of change

#### Controller Tuning
- **Ziegler-Nichols**: Empirical tuning rules
- **Cohen-Coon**: Based on process reaction curve
- **Frequency response**: Based on system frequency characteristics
- **Auto-tuning**: Automatic parameter adjustment

```python
class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, output_limits=(None, None)):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Min and max output values

        self.reset()

    def reset(self):
        """Reset the PID controller"""
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._last_error = 0
        self._last_time = None

    def update(self, setpoint, measurement, current_time=None):
        """
        Update the PID controller and calculate output
        """
        if current_time is None:
            current_time = time.time()

        if self._last_time is None:
            self._last_time = current_time
            return 0.0

        dt = current_time - self._last_time
        if dt <= 0:
            return self._output

        error = setpoint - measurement

        # Proportional term
        self._proportional = self.kp * error

        # Integral term with anti-windup
        self._integral += self.ki * error * dt
        if self.output_limits[0] is not None:
            self._integral = max(self.output_limits[0],
                                min(self._integral, self.output_limits[1]))

        # Derivative term
        if dt > 0:
            self._derivative = self.kd * (error - self._last_error) / dt
        else:
            self._derivative = 0

        # Calculate output
        output = self._proportional + self._integral + self._derivative

        # Apply output limits
        if self.output_limits[0] is not None:
            output = max(self.output_limits[0], min(output, self.output_limits[1]))

        # Update for next iteration
        self._last_error = error
        self._last_time = current_time
        self._output = output

        return output
```

### Controller Tuning Methods

#### Ziegler-Nichols Method
- **Process**: Find ultimate gain and period through oscillation
- **Steps**: Increase gain until sustained oscillation occurs
- **Formulas**: Calculate PID parameters from ultimate values
- **Limitations**: May result in aggressive response

#### Cohen-Coon Method
- **Process**: Based on first-order plus dead time model
- **Parameters**: Process gain, time constant, dead time
- **Advantages**: Better for processes with significant dead time
- **Tuning**: More conservative than Ziegler-Nichols

## Digital Control Systems

### Discretization

Digital control systems operate on discrete-time signals rather than continuous-time.

#### Sampling Process
- **Sample and hold**: Convert continuous signal to discrete
- **Sampling rate**: Must satisfy Nyquist criterion
- **Aliasing**: Prevent with anti-aliasing filters
- **Quantization**: Finite precision effects

#### Discrete-Time Controllers
- **Z-transform**: Discrete equivalent of Laplace transform
- **Difference equations**: Discrete-time system representation
- **Implementation**: Digital signal processing
- **Advantages**: Flexibility, programmability

### Digital PID Implementation

#### Position Form
- **Equation**: Direct implementation of PID equation
- **Characteristics**: Calculates absolute control output
- **Advantages**: Simple to understand and implement
- **Disadvantages**: Accumulated errors, integral windup

#### Velocity Form
- **Equation**: Calculates change in control output
- **Characteristics**: Incremental control action
- **Advantages**: Natural integral windup protection
- **Disadvantages**: Requires memory of previous output

```python
class DigitalPID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt  # Sample time

        # State variables
        self.integral = 0
        self.prev_error = 0
        self.prev_output = 0

    def compute(self, setpoint, measurement):
        """Compute control output using discrete PID"""
        error = setpoint - measurement

        # Proportional term
        p_term = self.kp * error

        # Integral term (trapezoidal integration)
        self.integral += (error + self.prev_error) * self.dt / 2
        i_term = self.ki * self.integral

        # Derivative term (backward difference)
        if self.dt > 0:
            derivative = (error - self.prev_error) / self.dt
        else:
            derivative = 0
        d_term = self.kd * derivative

        # Total output
        output = p_term + i_term + d_term

        # Update state
        self.prev_error = error

        return output

    def reset(self):
        """Reset the controller state"""
        self.integral = 0
        self.prev_error = 0
        self.prev_output = 0
```

### Implementation Considerations

#### Sample Rate Selection
- **Rule of thumb**: 10-20 times the system bandwidth
- **Constraints**: Computational resources, sensor limitations
- **Effects**: Too slow causes instability, too fast adds noise
- **Tuning**: May require adjustment based on performance

#### Quantization Effects
- **ADC resolution**: Limits measurement precision
- **DAC resolution**: Limits control precision
- **Arithmetic precision**: Affects calculation accuracy
- **Mitigation**: Use appropriate data types and scaling

## Advanced Control Techniques

### State-Space Control

State-space representation provides a comprehensive framework for control design.

#### System Representation
- **State equation**: dx/dt = Ax + Bu
- **Output equation**: y = Cx + Du
- **Advantages**: Handles multi-input, multi-output systems
- **Flexibility**: Multiple analysis and design techniques

#### State Feedback
- **Control law**: u = -Kx + r (state feedback + reference)
- **Pole placement**: Place closed-loop poles for desired response
- **Controllability**: System must be controllable
- **Observability**: System must be observable

### Observer Design

Observers estimate system states when not all states are measurable.

#### Luenberger Observer
- **Structure**: Model-based state estimation
- **Equation**: dx̂/dt = Ax̂ + Bu + L(y - ŷ)
- **Gain selection**: Observer poles faster than system poles
- **Applications**: State feedback when not all states measured

#### Kalman Filter
- **Application**: Optimal state estimation with noise
- **Characteristics**: Handles process and measurement noise
- **Advantages**: Statistically optimal estimates
- **Implementation**: Recursive algorithm suitable for real-time

### Robust Control

Robust control designs maintain performance despite uncertainties.

#### H-infinity Control
- **Objective**: Minimize worst-case performance
- **Uncertainty**: Handles structured and unstructured uncertainty
- **Design**: Optimization-based approach
- **Applications**: Systems with significant modeling uncertainty

#### Sliding Mode Control
- **Concept**: Force system to follow sliding surface
- **Characteristics**: Robust to matched uncertainties
- **Advantages**: Insensitive to certain disturbances
- **Disadvantages**: Chattering in real implementation

## Control System Design Process

### System Modeling

Accurate modeling is essential for effective control system design.

#### Mathematical Modeling
- **Physics-based**: Derive from fundamental physical laws
- **Parameters**: Identify and measure system parameters
- **Validation**: Compare model predictions with measurements
- **Simplification**: Balance accuracy with complexity

#### System Identification
- **Approach**: Determine model from input-output data
- **Excitation**: Apply known inputs to identify system
- **Methods**: Least squares, prediction error, subspace methods
- **Validation**: Test model with independent data

### Controller Design

#### Classical Design
- **Frequency domain**: Bode, Nyquist, Nichols plots
- **Root locus**: Pole placement method
- **Specifications**: Stability margins, bandwidth, disturbance rejection
- **Implementation**: Analog or digital implementation

#### Modern Design
- **State-space**: MIMO systems, optimal control
- **Optimal control**: LQR, LQG, H-infinity
- **Nonlinear control**: Feedback linearization, Lyapunov methods
- **Adaptive control**: Time-varying or unknown parameters

### Performance Analysis

#### Time-Domain Analysis
- **Step response**: Rise time, settling time, overshoot
- **Ramp response**: Tracking ability
- **Disturbance response**: Rejection capability
- **Robustness**: Sensitivity to parameter changes

#### Frequency-Domain Analysis
- **Gain margin**: Amount of gain increase before instability
- **Phase margin**: Amount of phase lag before instability
- **Bandwidth**: Frequency range of good tracking
- **Sensitivity**: Effect of disturbances and noise

## Practical Implementation Issues

### Actuator Limitations

Real actuators have physical limitations that affect control performance.

#### Saturation
- **Effect**: Actuator reaches maximum/minimum output
- **Consequences**: Integrator windup, performance degradation
- **Solutions**: Anti-windup compensation, gain scheduling
- **Design**: Consider saturation in design process

#### Deadband
- **Cause**: Region where small inputs produce no output
- **Effect**: Limit cycle oscillations, poor tracking
- **Compensation**: Nonlinear compensation, modified control laws
- **Minimization**: Mechanical design improvements

#### Backlash
- **Cause**: Mechanical play in transmission systems
- **Effect**: Non-symmetric response, limit cycles
- **Compensation**: Backlash models, pre-compensation
- **Design**: Minimize mechanically when possible

### Sensor Issues

Sensor characteristics affect control system performance.

#### Noise
- **Sources**: Electronic, quantization, environmental
- **Effects**: Reduced accuracy, control signal noise
- **Filtering**: Low-pass filtering, Kalman filtering
- **Trade-offs**: Noise reduction vs. phase lag

#### Delay
- **Sources**: Processing, communication, sensor dynamics
- **Effects**: Reduced stability margins, performance
- **Compensation**: Smith predictor, delay compensation
- **Minimization**: Fast sensors, efficient processing

### Implementation Non-idealities

Real-world implementation introduces various non-idealities.

#### Computational Delay
- **Sources**: Processing time, scheduling, communication
- **Effects**: Phase lag, reduced stability margins
- **Mitigation**: Fast processors, efficient algorithms
- **Design**: Account for delays in design

#### Sampling Effects
- **Aliasing**: High-frequency signals appearing as low-frequency
- **Resolution**: Quantization effects
- **Jitter**: Timing variations in sampling
- **Mitigation**: Proper anti-aliasing, stable clocks

Feedback control loops form the foundation of precise and reliable Physical AI systems, enabling them to achieve desired behavior despite disturbances and uncertainties through continuous monitoring and adjustment.