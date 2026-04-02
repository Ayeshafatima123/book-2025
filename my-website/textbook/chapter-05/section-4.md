---
title: "Chapter 5: Acting in the Physical World"
section: "5.4"
chapter: "5"
---

# 5.4 Motion Planning

Motion planning is the process of determining a sequence of movements that allows a Physical AI system to achieve its goals while avoiding obstacles and satisfying various constraints. This section covers the fundamental concepts, algorithms, and techniques used in motion planning for physical systems.

## Fundamentals of Motion Planning

### Problem Definition

Motion planning addresses the challenge of finding a valid path from a start configuration to a goal configuration.

#### Configuration Space (C-space)
- **Definition**: Space of all possible configurations of the system
- **Dimensions**: Number of degrees of freedom of the system
- **Obstacles**: Regions in C-space that correspond to collisions
- **Free space**: Valid configurations without collisions

#### Types of Motion Planning Problems
- **Point-to-point**: Move from start to goal configuration
- **Path following**: Follow a specified geometric path
- **Trajectory planning**: Plan both path and timing information
- **Optimization**: Find optimal path according to criteria

### Planning vs. Control Distinction

#### Motion Planning
- **Focus**: Finding geometric path in configuration space
- **Time**: Often ignores dynamic constraints initially
- **Output**: Sequence of configurations or waypoints
- **Approach**: Discrete, combinatorial methods

#### Motion Control
- **Focus**: Executing planned motions with dynamic constraints
- **Time**: Considers timing and dynamic feasibility
- **Output**: Control signals to actuators
- **Approach**: Continuous, feedback control methods

## Configuration Space Representation

### 2D Configuration Spaces

For simple systems, configuration space can be visualized directly.

#### Point Robot in 2D
- **Configuration**: (x, y) position coordinates
- **C-space**: Same as workspace with expanded obstacles
- **Obstacle expansion**: Robot size accounted for in C-space
- **Path planning**: Find collision-free path in 2D space

#### Rigid Body in 2D
- **Configuration**: (x, y, θ) position and orientation
- **C-space**: 3D space with 2D translation and 1D rotation
- **Complexity**: Significantly more complex than point robot
- **Approximation**: Often use bounding boxes or circles

### 3D Configuration Spaces

Three-dimensional motion planning is more complex but more realistic.

#### Point Robot in 3D
- **Configuration**: (x, y, z) position coordinates
- **C-space**: 3D workspace with expanded obstacles
- **Applications**: Drone navigation, 3D printing
- **Complexity**: Moderate computational requirements

#### Rigid Body in 3D
- **Configuration**: (x, y, z, roll, pitch, yaw) pose
- **C-space**: 6D space (3 translation, 3 rotation)
- **Complexity**: Very high computational requirements
- **Approximation**: Often simplified to 3-4D problems

### High-Dimensional Configuration Spaces

Robot manipulators and complex systems have high-dimensional C-spaces.

#### Robot Manipulators
- **Configuration**: Joint angles (n-dimensional for n-DOF robot)
- **C-space**: n-dimensional joint space
- **Obstacles**: Self-collisions, environment collisions
- **Visualization**: Difficult to visualize, requires projection

#### Multi-Robot Systems
- **Configuration**: Concatenated configurations of all robots
- **C-space**: Sum of individual C-space dimensions
- **Complexity**: Exponential growth with number of robots
- **Approaches**: Decentralized, priority-based methods

## Motion Planning Algorithms

### Sampling-Based Methods

Sampling-based methods randomly sample the configuration space to find paths.

#### Probabilistic Roadmap (PRM)
- **Approach**: Pre-sample C-space, build roadmap
- **Process**: Sample → Connect → Query
- **Advantages**: Good for high-dimensional spaces
- **Disadvantages**: Preprocessing time, incomplete

```python
import numpy as np
from scipy.spatial import KDTree

class ProbabilisticRoadmap:
    def __init__(self, start, goal, obstacles, max_samples=1000):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.max_samples = max_samples
        self.samples = []
        self.graph = {}

    def is_collision_free(self, config):
        """Check if configuration is collision-free"""
        # Check against obstacles
        for obstacle in self.obstacles:
            if self.in_obstacle(config, obstacle):
                return False
        return True

    def sample_free_space(self):
        """Generate random collision-free samples"""
        samples = []
        for _ in range(self.max_samples):
            # Generate random configuration
            config = self.generate_random_config()
            if self.is_collision_free(config):
                samples.append(config)
        return samples

    def connect_neighbors(self, samples, max_dist=1.0):
        """Connect nearby samples to form roadmap"""
        tree = KDTree(samples)
        graph = {i: [] for i in range(len(samples))}

        for i, config in enumerate(samples):
            # Find nearby configurations
            neighbors = tree.query_ball_point(config, max_dist)
            for j in neighbors:
                if i != j and self.is_collision_free_path(samples[i], samples[j]):
                    graph[i].append(j)
                    graph[j].append(i)

        return graph, samples

    def plan_path(self):
        """Plan path from start to goal using roadmap"""
        # Add start and goal to samples
        samples = [self.start] + self.samples + [self.goal]

        # Build graph
        graph, samples = self.connect_neighbors(samples)

        # Use graph search (e.g., A*) to find path
        path = self.graph_search(graph, 0, len(samples)-1)
        return path
```

#### Rapidly-exploring Random Trees (RRT)
- **Approach**: Grow tree from start configuration
- **Process**: Random sampling → Nearest neighbor → Extend
- **Advantages**: Good for narrow passages, any-time algorithm
- **Disadvantages**: Biased toward large free space regions

#### RRT*
- **Improvement**: Asymptotically optimal version of RRT
- **Approach**: Rewire tree to find better paths
- **Advantages**: Finds optimal solutions given enough time
- **Applications**: Optimal motion planning problems

### Grid-Based Methods

Grid-based methods discretize the configuration space into a grid.

#### A* Algorithm
- **Approach**: Best-first search with heuristic
- **Heuristic**: Estimated cost to goal
- **Optimality**: Finds optimal path if heuristic is admissible
- **Applications**: 2D navigation, simple path planning

#### Dijkstra's Algorithm
- **Approach**: Expand from start with increasing cost
- **Optimality**: Finds optimal path without heuristic
- **Disadvantages**: Slower than A*, no heuristic guidance
- **Applications**: When heuristic is difficult to define

#### D* Algorithm
- **Approach**: Dynamic path planning with changing environment
- **Advantages**: Replans efficiently when environment changes
- **Applications**: Mobile robot navigation with new obstacles
- **Complexity**: More complex than A*

### Potential Field Methods

Potential field methods use artificial forces for navigation.

#### Attractive Field
- **Function**: Pulls robot toward goal
- **Shape**: Typically quadratic near goal
- **Properties**: Vanishes at goal location
- **Design**: Avoid local minima near goal

#### Repulsive Field
- **Function**: Pushes robot away from obstacles
- **Shape**: Strong near obstacles, decreases with distance
- **Properties**: Infinite at obstacle boundary
- **Design**: Balance with attractive field

#### Limitations
- **Local minima**: Robot can get trapped
- **Oscillations**: Unstable in certain configurations
- **Tuning**: Difficult to tune parameters
- **Applications**: Real-time reactive navigation

## Trajectory Planning

### Path vs. Trajectory

#### Path Planning
- **Output**: Geometric path in configuration space
- **Time**: No timing information
- **Focus**: Spatial feasibility
- **Methods**: Path planning algorithms

#### Trajectory Planning
- **Output**: Path with timing information
- **Time**: Explicit time parameterization
- **Focus**: Dynamic feasibility
- **Methods**: Spline interpolation, optimization

### Polynomial Trajectory Generation

Polynomial trajectories provide smooth motion profiles.

#### Cubic Polynomials
- **Degrees of freedom**: 4 (position and velocity at start/end)
- **Continuity**: C¹ continuity (position and velocity)
- **Applications**: Simple point-to-point motion
- **Limitations**: Limited acceleration constraints

#### Quintic Polynomials
- **Degrees of freedom**: 6 (position, velocity, acceleration at start/end)
- **Continuity**: C² continuity (smooth acceleration)
- **Applications**: Smooth motion with acceleration constraints
- **Advantages**: Better dynamic properties

```python
import numpy as np

class PolynomialTrajectory:
    def __init__(self, start_pos, start_vel, start_acc,
                 end_pos, end_vel, end_acc, duration):
        self.start_pos = start_pos
        self.start_vel = start_vel
        self.start_acc = start_acc
        self.end_pos = end_pos
        self.end_vel = end_vel
        self.end_acc = end_acc
        self.duration = duration

        # Solve for polynomial coefficients (quintic)
        # q(t) = a₀ + a₁t + a₂t² + a₃t³ + a₄t⁴ + a₅t⁵
        A = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0],
            [1, self.duration, self.duration**2, self.duration**3,
             self.duration**4, self.duration**5],
            [0, 1, 2*self.duration, 3*self.duration**2,
             4*self.duration**3, 5*self.duration**4],
            [0, 0, 2, 6*self.duration, 12*self.duration**2,
             20*self.duration**3]
        ])

        b = np.array([start_pos, start_vel, start_acc,
                      end_pos, end_vel, end_acc])

        self.coeffs = np.linalg.solve(A, b)

    def position(self, t):
        """Calculate position at time t"""
        t = max(0, min(t, self.duration))  # Clamp to valid range
        return sum(c * t**i for i, c in enumerate(self.coeffs))

    def velocity(self, t):
        """Calculate velocity at time t"""
        t = max(0, min(t, self.duration))
        return sum(i * c * t**(i-1) for i, c in enumerate(self.coeffs) if i > 0)

    def acceleration(self, t):
        """Calculate acceleration at time t"""
        t = max(0, min(t, self.duration))
        return sum(i * (i-1) * c * t**(i-2)
                  for i, c in enumerate(self.coeffs) if i > 1)
```

### Spline-Based Trajectories

Spline trajectories provide piecewise smooth paths.

#### Cubic Splines
- **Construction**: Piecewise cubic polynomials
- **Continuity**: C² continuity at waypoints
- **Applications**: Smooth path following
- **Advantages**: Flexible, smooth curves

#### B-splines
- **Construction**: Basis spline functions
- **Properties**: Local control, convex hull property
- **Applications**: CAD, smooth trajectory generation
- **Advantages**: Stable numerical properties

#### Bezier Curves
- **Construction**: Bernstein polynomial basis
- **Control**: Control points define curve shape
- **Applications**: Path shaping, animation
- **Properties**: Endpoint interpolation

### Time-Optimal Trajectory Planning

Time-optimal trajectories minimize execution time while respecting constraints.

#### Velocity and Acceleration Constraints
- **Limits**: Maximum velocity and acceleration
- **Profile**: Trapezoidal or S-curve velocity profiles
- **Optimization**: Minimize time subject to constraints
- **Applications**: Fast robot motion

#### Path Parameterization
- **Method**: Parameterize path by arc length
- **Optimization**: Optimize timing along geometric path
- **Advantages**: Separate geometry from timing
- **Applications**: Path following with constraints

## Real-Time Motion Planning

### Reactive Planning

Reactive planning adjusts motion based on sensor feedback.

#### Vector Field Histogram
- **Approach**: Local navigation using sensor histogram
- **Advantages**: Fast, reactive to obstacles
- **Applications**: Mobile robot navigation
- **Limitations**: Local method, no global optimality

#### Dynamic Window Approach
- **Approach**: Evaluate feasible velocity commands
- **Window**: Feasible velocities in current time window
- **Selection**: Choose best velocity based on criteria
- **Applications**: Mobile robot navigation

### Hierarchical Planning

Hierarchical approaches combine global and local planning.

#### Global Planner
- **Function**: Generate high-level path
- **Resolution**: Coarse resolution, large scale
- **Methods**: Grid search, sampling-based
- **Update**: Infrequent updates

#### Local Planner
- **Function**: Execute path with obstacle avoidance
- **Resolution**: Fine resolution, local scale
- **Methods**: Reactive, optimization-based
- **Update**: Frequent updates based on sensors

#### Coordination
- **Interface**: Global path as reference for local planner
- **Recovery**: Local planner handles unexpected obstacles
- **Optimization**: Balance global optimality with local safety
- **Applications**: Mobile robot navigation

## Multi-Robot Motion Planning

### Coordination Challenges

Multi-robot systems face additional coordination challenges.

#### Communication Constraints
- **Bandwidth**: Limited communication capacity
- **Latency**: Delay in information exchange
- **Reliability**: Communication failures
- **Topology**: Changing communication networks

#### Computational Complexity
- **Exponential growth**: With number of robots
- **Centralized**: Single point of failure
- **Decentralized**: Coordination challenges
- **Distributed**: Balance between local and global

### Coordination Strategies

#### Centralized Planning
- **Approach**: Single planner for all robots
- **Advantages**: Global optimality, coordination
- **Disadvantages**: Computational complexity, single point of failure
- **Applications**: Small robot teams

#### Decentralized Planning
- **Approach**: Each robot plans independently
- **Advantages**: Scalability, robustness
- **Disadvantages**: Coordination challenges, suboptimal solutions
- **Applications**: Large robot teams

#### Priority-Based Methods
- **Approach**: Plan for robots in sequence
- **Priorities**: Based on urgency, proximity, etc.
- **Advantages**: Simpler than centralized
- **Disadvantages**: Priority assignment challenges

Motion planning is essential for enabling Physical AI systems to navigate and operate effectively in complex environments while avoiding obstacles and achieving their objectives.