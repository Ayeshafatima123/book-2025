# Physical AI & Humanoid Robotics Book

Welcome to the Physical AI & Humanoid Robotics book repository. This comprehensive guide covers everything from basic sensor integration to advanced robotics applications.

## Features

- Interactive Docusaurus-based website
- Comprehensive book content covering Physical AI concepts
- Hands-on examples and projects
- RAG (Retrieval-Augmented Generation) Chatbot - Ask questions about the book content
- Colorful and engaging UI with slideshow presentations

## RAG Chatbot

This repository includes an AI-powered chatbot that can answer questions about the book content using Retrieval-Augmented Generation (RAG). The chatbot uses:

- **Qdrant Cloud** for vector storage and similarity search
- **OpenAI API** for response generation
- **Book content** as the knowledge base

To learn how to set up and run the RAG chatbot, see [../RAG_SETUP.md](../RAG_SETUP.md).

## Overview

This book provides practical examples of AI controlling physical processes, sensors, actuators, and robotic systems. Each chapter includes hands-on projects that readers can build themselves using accessible hardware like Arduino and Raspberry Pi.

## Structure

- `content/` - Book chapters and content
- `code-examples/` - Python and hardware code examples
- `hardware-guides/` - Hardware setup instructions
- `tests/` - Code validation and hardware tests
- `docs/` - Additional documentation

## Getting Started

1. Install dependencies: `npm install`
2. Start the development server: `npm start`
3. For the RAG chatbot: `npm run dev` (starts both website and API server)

## Prerequisites

- Node.js v18+ (for the website and RAG API)
- Python 3.9+ (for code examples)
- Hardware: Raspberry Pi or Arduino with connected sensors/actuators
- Qdrant Cloud account and OpenAI API key (for RAG chatbot)

## Safety First

⚠️ Always follow safety guidelines when working with physical AI systems. See `docs/safety-guidelines/` for detailed safety information.

## Running with RAG Chatbot

To run both the website and the RAG API server:

```bash
npm run dev
```

This will start both the Docusaurus website and the RAG API server simultaneously.

## Deployment

This site is automatically deployed to GitHub Pages using GitHub Actions. Any changes pushed to the `main` branch will trigger a new build and deployment.

To deploy manually, run:
```bash
npm run build
npm run deploy
```

The site is published at: https://hackathon-book-2025.github.io
