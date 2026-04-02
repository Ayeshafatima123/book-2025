import React from 'react';
import type { ReactNode } from 'react';
import Layout from '@theme/Layout';
import Slideshow from '@site/src/components/Slideshow';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Define the slides for the comprehensive slideshow covering multiple chapters
const introductionSlides = [
  {
    title: "Welcome to Physical AI",
    content: `
      <p>Welcome to the <strong>Physical AI Book</strong> - your comprehensive guide to understanding and implementing artificial intelligence systems that interact with the physical world.</p>
      <p>This book represents a new frontier in AI education, where digital algorithms meet tangible hardware, creating systems that can sense, think, and act in the real world.</p>
    `,
    color: "rgba(52, 152, 219, 0.1)"
  },
  {
    title: "What is Physical AI?",
    content: `
      <p>Physical AI is the discipline of creating artificial intelligence systems that can perceive, understand, and interact with the physical world.</p>
      <ul>
        <li><strong>Sense</strong> the physical environment through various sensors</li>
        <li><strong>Process</strong> information using AI algorithms</li>
        <li><strong>Act</strong> upon the physical world through actuators</li>
        <li><strong>Learn</strong> from physical interactions to improve performance</li>
      </ul>
    `,
    color: "rgba(46, 204, 113, 0.1)"
  },
  {
    title: "Why Physical AI Matters",
    content: `
      <p>The importance of Physical AI extends far beyond academic curiosity. It's driving innovation across multiple sectors:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div><strong>Healthcare</strong><br>Surgical robots, wearable devices</div>
        <div><strong>Manufacturing</strong><br>Quality control, predictive maintenance</div>
        <div><strong>Transportation</strong><br>Autonomous vehicles, smart traffic</div>
        <div><strong>Environment</strong><br>Monitoring, smart agriculture</div>
      </div>
    `,
    color: "rgba(241, 196, 15, 0.1)"
  },
  {
    title: "Core Components of Physical AI",
    content: `
      <p>Every Physical AI system contains these essential elements:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>1. Sensors</h4>
          <p>The robot's senses: cameras, ultrasonic sensors, gyroscopes, environmental sensors</p>
        </div>
        <div>
          <h4>2. Processing Unit</h4>
          <p>The robot's brain: microcontrollers, single-board computers, AI accelerators</p>
        </div>
        <div>
          <h4>3. Actuators</h4>
          <p>The robot's body: motors, servos, LEDs, speakers for physical actions</p>
        </div>
        <div>
          <h4>4. Software</h4>
          <p>The robot's mind: control algorithms, AI models, safety systems</p>
        </div>
      </div>
    `,
    color: "rgba(155, 89, 182, 0.1)"
  },
  {
    title: "Types of Robotic Systems",
    content: `
      <p>Physical AI systems come in various forms:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Mobile Robots</h4>
          <ul style="text-align: left;">
            <li>Wheeled robots (rovers, delivery bots)</li>
            <li>Legged robots (humanoids, quadrupeds)</li>
            <li>Flying robots (drones, quadcopters)</li>
          </ul>
        </div>
        <div>
          <h4>Stationary Robots</h4>
          <ul style="text-align: left;">
            <li>Robotic arms (assembly, pick-and-place)</li>
            <li>Cobots (collaborative robots)</li>
            <li>Industrial robots (welding, packaging)</li>
          </ul>
        </div>
        <div>
          <h4>Hybrid Systems</h4>
          <ul style="text-align: left;">
            <li>Mobile manipulators</li>
            <li>Modular robots</li>
            <li>Swarm robots</li>
          </ul>
        </div>
      </div>
    `,
    color: "rgba(231, 76, 60, 0.1)"
  },
  {
    title: "The Intelligence Loop",
    content: `
      <p>An intelligent robot follows the perception-action loop:</p>
      <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-block; padding: 1rem; background: rgba(255, 255, 255, 0.2); border-radius: 10px;">
          <p><strong>Sensors → Perception → Decision → Action → Learning</strong></p>
          <p style="margin-top: 1rem;">Feedback loop: Information flows back to improve future decisions</p>
        </div>
      </div>
      <p>This loop enables robots to perceive their environment, process information, make decisions, act in the physical world, and learn from experience.</p>
    `,
    color: "rgba(52, 73, 94, 0.1)"
  },
  {
    title: "Sensor Integration",
    content: `
      <p>Sensors are the foundation of Physical AI systems:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Proximity & Distance</h4>
          <p>Ultrasonic, infrared, LIDAR sensors for obstacle detection</p>
        </div>
        <div>
          <h4>Visual Sensors</h4>
          <p>Cameras, depth sensors for object recognition and navigation</p>
        </div>
        <div>
          <h4>Motion & Orientation</h4>
          <p>IMU, encoders for balance and position tracking</p>
        </div>
        <div>
          <h4>Environmental</h4>
          <p>Temperature, humidity, air quality sensors for environmental awareness</p>
        </div>
      </div>
    `,
    color: "rgba(241, 158, 194, 0.1)"
  },
  {
    title: "Data Processing & Filtering",
    content: `
      <p>Raw sensor data requires processing to be useful:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Digital Filtering</h4>
          <ul style="text-align: left;">
            <li>Moving average: Smooths random noise</li>
            <li>Kalman filter: Predicts true values</li>
            <li>Median filter: Removes outliers</li>
          </ul>
        </div>
        <div>
          <h4>Sensor Fusion</h4>
          <ul style="text-align: left;">
            <li>Complementary filters: Combine sensors optimally</li>
            <li>Extended Kalman filters: Handle non-linear relationships</li>
            <li>Particle filters: Track with uncertain data</li>
          </ul>
        </div>
        <div>
          <h4>Calibration</h4>
          <ul style="text-align: left;">
            <li>Offset correction: Account for sensor bias</li>
            <li>Scale factor adjustment: Convert to real units</li>
            <li>Temperature compensation: Adjust for environment</li>
          </ul>
        </div>
      </div>
    `,
    color: "rgba(230, 126, 34, 0.1)"
  },
  {
    title: "Key Algorithms in Physical AI",
    content: `
      <p>Physical AI systems rely on specialized algorithms:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Perception Algorithms</h4>
          <ul style="text-align: left;">
            <li>Computer vision (object detection, tracking)</li>
            <li>Sensor fusion (combining multiple data sources)</li>
            <li>SLAM (Simultaneous Localization and Mapping)</li>
          </ul>
        </div>
        <div>
          <h4>Decision Algorithms</h4>
          <ul style="text-align: left;">
            <li>Path planning (finding optimal routes)</li>
            <li>Reinforcement learning (learning through trial and error)</li>
            <li>State machines (behavioral patterns)</li>
          </ul>
        </div>
        <div>
          <h4>Control Algorithms</h4>
          <ul style="text-align: left;">
            <li>PID controllers (precise actuator control)</li>
            <li>Motion planning (smooth movement execution)</li>
            <li>Trajectory generation (desired movement paths)</li>
          </ul>
        </div>
      </div>
    `,
    color: "rgba(41, 128, 185, 0.1)"
  },
  {
    title: "Real-World Applications",
    content: `
      <p>Physical AI is transforming industries:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Industry 4.0</h4>
          <p>Smart factories with autonomous robots, quality control using computer vision</p>
        </div>
        <div>
          <h4>Healthcare Robotics</h4>
          <p>Surgical robots with AI-powered precision, rehabilitation robots</p>
        </div>
        <div>
          <h4>Autonomous Navigation</h4>
          <p>Self-driving cars, warehouse robots, delivery drones</p>
        </div>
        <div>
          <h4>Environmental Monitoring</h4>
          <p>Climate monitoring, agricultural automation, pollution detection</p>
        </div>
      </div>
    `,
    color: "rgba(39, 174, 96, 0.1)"
  },
  {
    title: "Challenges & Solutions",
    content: `
      <p>Physical AI systems face several challenges:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Challenge: Sensor Noise</h4>
          <p><strong>Solution:</strong> Use filtering algorithms and sensor fusion to clean data</p>
        </div>
        <div>
          <h4>Challenge: Real-time Processing</h4>
          <p><strong>Solution:</strong> Optimize algorithms and use appropriate hardware</p>
        </div>
        <div>
          <h4>Challenge: Safety & Reliability</h4>
          <p><strong>Solution:</strong> Implement multiple safety checks and fallback behaviors</p>
        </div>
        <div>
          <h4>Challenge: Environmental Adaptation</h4>
          <p><strong>Solution:</strong> Use adaptive algorithms and machine learning</p>
        </div>
      </div>
    `,
    color: "rgba(192, 57, 43, 0.1)"
  },
  {
    title: "Learning Philosophy",
    content: `
      <p>This book is built on several core principles:</p>
      <ol>
        <li><strong>Hands-On Learning</strong> - Theory with practical projects</li>
        <li><strong>Safety-First Approach</strong> - Comprehensive safety measures</li>
        <li><strong>Accessibility</strong> - For varying backgrounds</li>
        <li><strong>Reproducible Science</strong> - Using accessible hardware</li>
        <li><strong>Cross-Disciplinary Integration</strong> - Multiple domains</li>
      </ol>
    `,
    color: "rgba(142, 68, 173, 0.1)"
  },
  {
    title: "What You'll Learn",
    content: `
      <p>By working through this book, you will develop expertise in:</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div>
          <h4>Core Concepts</h4>
          <ul style="text-align: left;">
            <li>Sensor Integration</li>
            <li>Actuator Control</li>
            <li>Real-Time Processing</li>
          </ul>
        </div>
        <div>
          <h4>Technical Skills</h4>
          <ul style="text-align: left;">
            <li>Hardware-Software Integration</li>
            <li>AI Model Deployment</li>
            <li>System Architecture</li>
          </ul>
        </div>
        <div>
          <h4>Practical Applications</h4>
          <ul style="text-align: left;">
            <li>Robotics</li>
            <li>IoT Systems</li>
            <li>Automation</li>
          </ul>
        </div>
      </div>
    `,
    color: "rgba(211, 84, 0, 0.1)"
  },
  {
    title: "Get Started",
    content: `
      <p>To begin your journey with Physical AI:</p>
      <ol>
        <li>Gather the basic hardware components</li>
        <li>Set up your development environment</li>
        <li>Start with basic sensor readings</li>
        <li>Document your experiments</li>
        <li>Join the community</li>
      </ol>
      <p>Every project you complete brings you closer to becoming a practitioner of Physical AI!</p>
    `,
    color: "rgba(44, 62, 80, 0.1)"
  }
];

export default function IntroductionSlideshow(): ReactNode {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`Introduction - ${siteConfig.title}`}
      description="Interactive slideshow introduction to Physical AI & Humanoid Robotics">
      <div style={{ padding: '2rem 0', minHeight: '80vh', display: 'flex', alignItems: 'center' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h1 style={{ fontSize: '2.5rem', color: '#2c3e50' }}>
              Introduction to Physical AI & Humanoid Robotics
            </h1>
            <p style={{ fontSize: '1.2rem', color: '#7f8c8d' }}>
              Interactive slideshow to explore the world of Physical AI
            </p>
          </div>

          <Slideshow slides={introductionSlides} autoPlay={true} interval={8000} />

          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <a
              href="/docs/introduction"
              className="button button--primary button--lg"
              style={{ margin: '0.5rem' }}
            >
              Read Full Introduction
            </a>
            <a
              href="/docs/chapter1"
              className="button button--secondary button--lg"
              style={{ margin: '0.5rem' }}
            >
              Start Reading Chapters
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
}