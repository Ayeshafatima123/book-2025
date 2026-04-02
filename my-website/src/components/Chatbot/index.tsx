import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './Chatbot.module.css';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

interface Source {
  content: string;
  metadata: {
    title?: string;
    relativePath?: string;
    bookSection?: string;
    bookType?: string;
    chunkLabel?: string;
    fileName?: string;
  };
  score: number;
}

interface RAGResponse {
  response: string;
  sources: Source[];
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hello! I\'m your Physical AI & Humanoid Robotics assistant. Ask me anything about the book content, and I\'ll find relevant information for you.',
      role: 'assistant',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Try to call the real RAG API, fallback to simulated response
      let response;
      try {
        response = await callRagApi(inputValue);
      } catch (apiError) {
        console.warn('RAG API not available, using simulated response:', apiError);
        // Fallback to simulated response
        response = await simulateRAGResponse(inputValue);
      }

      // Handle both types of responses (with or without sources)
      if (typeof response === 'object' && 'response' in response) {
        // Full RAG response with sources
        const ragResponse = response as RAGResponse;

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: ragResponse.response,
          role: 'assistant',
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
        setSources(ragResponse.sources);
      } else {
        // Simulated response string
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response as string,
          role: 'assistant',
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
        setSources([]);
      }
    } catch (error) {
      console.error('Error getting response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error instanceof Error ? error.message : 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setSources([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Make a real RAG API call via the backend server
  const callRagApi = async (query: string): Promise<RAGResponse | string> => {
    try {
      const response = await fetch('http://localhost:3002/api/rag-query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        response: data.response,
        sources: data.sources,
      };
    } catch (error) {
      console.error('Error calling RAG API:', error);
      throw error;
    }
  };

  // Simulate RAG response for static site or when API is unavailable
  const simulateRAGResponse = async (query: string): Promise<RAGResponse> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Return a contextual response based on common questions about Physical AI
    const lowerQuery = query.toLowerCase();

    let responseText = '';
    if (lowerQuery.includes('what') && lowerQuery.includes('physical ai')) {
      responseText = 'Physical AI refers to artificial intelligence systems designed to operate in and interact with the physical world. It combines robotics, sensors, actuators, and AI algorithms to create systems that can perceive, think, and act in real environments.';
    } else if (lowerQuery.includes('robot') || lowerQuery.includes('robotics')) {
      responseText = 'Robotics is a key component of Physical AI. It involves the design, construction, and operation of robots that can interact with the physical world. Robots use sensors to perceive their environment and actuators to perform physical actions.';
    } else if (lowerQuery.includes('sensor') || lowerQuery.includes('sensors')) {
      responseText = 'Sensors are crucial for Physical AI systems. They allow robots and AI systems to perceive their environment by detecting light, sound, temperature, pressure, motion, and other physical properties. Common sensors include cameras, ultrasonic sensors, IMUs, and environmental sensors.';
    } else if (lowerQuery.includes('actuator') || lowerQuery.includes('actuators')) {
      responseText = 'Actuators are components that enable Physical AI systems to interact with the physical world. They convert control signals into physical movement or action. Common actuators include motors, servos, and various types of linear actuators.';
    } else if (lowerQuery.includes('chapter') || lowerQuery.includes('content')) {
      responseText = 'The Physical AI book covers topics from basic sensor integration to advanced robotics applications. It includes hands-on projects and examples using accessible hardware like Arduino and Raspberry Pi.';
    } else {
      responseText = `Based on the Physical AI & Humanoid Robotics book, ${query} relates to the intersection of artificial intelligence and physical systems. The book covers how AI algorithms can be applied to control physical devices, process sensor data, and enable robots to interact with the real world.`;
    }

    // Simulate sources for the mock response
    const mockSources: Source[] = [
      {
        content: 'Physical AI refers to artificial intelligence systems designed to operate in and interact with the physical world...',
        metadata: {
          title: 'Introduction to Physical AI',
          relativePath: 'docs/chapter1.md',
          bookSection: 'chapter1',
          bookType: 'documentation',
          fileName: 'chapter1.md'
        },
        score: 0.9
      },
      {
        content: 'Robotics is a key component of Physical AI. It involves the design, construction, and operation of robots...',
        metadata: {
          title: 'Fundamentals of Robotics & AI',
          relativePath: 'textbook/chapter-01/introduction.md',
          bookSection: 'chapter-01',
          bookType: 'textbook',
          fileName: 'introduction.md'
        },
        score: 0.85
      }
    ];

    return {
      response: responseText,
      sources: mockSources
    };
  };

  // Function to format source metadata for display
  const formatSourceTitle = (metadata: Source['metadata']) => {
    if (metadata.title) return metadata.title;
    if (metadata.chunkLabel) return metadata.chunkLabel;
    if (metadata.fileName) return metadata.fileName;
    return 'Unknown Source';
  };

  // Function to get a descriptive label for the book section
  const getSectionLabel = (metadata: Source['metadata']) => {
    if (metadata.bookType === 'textbook' && metadata.bookSection) {
      return `From Textbook: ${metadata.bookSection}`;
    } else if (metadata.bookType === 'documentation' && metadata.bookSection) {
      return `From Documentation: ${metadata.bookSection}`;
    } else if (metadata.bookSection) {
      return metadata.bookSection;
    }
    return 'From Book Content';
  };

  return (
    <div className={clsx(styles.chatbot, 'chatbot-container')}>
      <div className={styles.chatHeader}>
        <h3>Physical AI Assistant</h3>
        <p>Ask questions about the book content</p>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              styles.message,
              message.role === 'user' ? styles.userMessage : styles.assistantMessage
            )}
          >
            <div className={styles.messageContent}>
              {message.content}
            </div>
            <div className={styles.messageTimestamp}>
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={clsx(styles.message, styles.assistantMessage)}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        {sources.length > 0 && (
          <div className={styles.sourcesContainer}>
            <h4>References from the Book:</h4>
            <div className={styles.sourcesList}>
              {sources.slice(0, 3).map((source, index) => ( // Limit to top 3 sources
                <div key={index} className={styles.sourceItem}>
                  <div className={styles.sourceHeader}>
                    <span className={styles.sourceTitle}>{formatSourceTitle(source.metadata)}</span>
                    <span className={styles.sourceSection}>{getSectionLabel(source.metadata)}</span>
                  </div>
                  <div className={styles.sourcePreview}>
                    {source.content.substring(0, 150)}...
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about Physical AI..."
          className={styles.chatInput}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={styles.chatSubmitButton}
          disabled={isLoading || !inputValue.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;