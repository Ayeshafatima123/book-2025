import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <p className="hero__description">
          A comprehensive guide to bridging artificial intelligence with physical systems,
          covering everything from basic sensor integration to advanced robotics applications.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/introduction">
            Start Reading - 10min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI Book - Bridging Artificial Intelligence and Physical Systems">
      <HomepageHeader />
      <main>
        <section className={styles.bookDetails}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <div className={styles.bookCard}>
                  <h2>What You'll Learn</h2>
                  <ul>
                    <li>Sensor integration and data processing</li>
                    <li>Real-time AI decision making</li>
                    <li>Actuator control and feedback systems</li>
                    <li>Hardware-software integration</li>
                    <li>System architecture and design</li>
                    <li>Safety and reliability considerations</li>
                  </ul>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.bookCard}>
                  <h2>Target Audience</h2>
                  <p>Perfect for:</p>
                  <ul>
                    <li>AI/ML Engineers wanting to work with physical systems</li>
                    <li>Hardware Engineers exploring AI integration</li>
                    <li>Students in robotics and embedded systems</li>
                    <li>Researchers in AI and physical computing</li>
                    <li>Hobbyists and makers interested in smart devices</li>
                  </ul>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.bookCard}>
                  <h2>Hardware Covered</h2>
                  <ul>
                    <li>Raspberry Pi 4 and Zero</li>
                    <li>Arduino Uno and Nano</li>
                    <li>ESP32 and ESP8266</li>
                    <li>Sensors (temperature, light, motion, etc.)</li>
                    <li>Actuators (motors, servos, displays)</li>
                    <li>Communication modules (Wi-Fi, Bluetooth)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
