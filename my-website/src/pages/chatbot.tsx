import React from 'react';
import type { ReactNode } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Chatbot from '@site/src/components/Chatbot';

export default function ChatbotPage(): ReactNode {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`Physical AI Assistant - ${siteConfig.title}`}
      description="RAG Chatbot for Physical AI & Humanoid Robotics Book">
      <div style={{ padding: '2rem 0', minHeight: '80vh' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h1 style={{ fontSize: '2.5rem', color: '#3498db' }}>
              Physical AI Assistant
            </h1>
            <p style={{ fontSize: '1.2rem', color: '#7f8c8d', maxWidth: '600px', margin: '0.5rem auto' }}>
              Ask questions about the Physical AI & Humanoid Robotics book. Our RAG system will find relevant information from the book content.
            </p>
          </div>

          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <Chatbot />
          </div>

          <div style={{ textAlign: 'center', marginTop: '2rem', padding: '1rem', background: 'rgba(52, 152, 219, 0.1)', borderRadius: '10px' }}>
            <h3>How it works</h3>
            <p>
              This RAG (Retrieval-Augmented Generation) chatbot uses Qdrant vector database to find relevant
              sections from the Physical AI book based on your questions. It then generates contextual responses
              using the retrieved information.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}