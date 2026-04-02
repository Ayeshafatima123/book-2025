# Physical AI Book RAG Chatbot Setup

This guide explains how to set up and run the RAG (Retrieval-Augmented Generation) chatbot for the Physical AI & Humanoid Robotics book.

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Qdrant Cloud account
- OpenAI API key

## Configuration

1. **Set up environment variables**

Create a `.env` file in the root directory with the following:

```env
QDRANT_URL=https://your-cluster-name.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=your-openai-api-key
```

2. **Install dependencies**

```bash
cd my-website
npm install
```

## Running the Application

### Development Mode

To run both the Docusaurus website and the RAG API server simultaneously:

```bash
cd my-website
npm run dev
```

This will start:
- Docusaurus website on http://localhost:3000
- RAG API server on http://localhost:3002

### Production Mode

1. Build the server:
```bash
cd my-website
npm run server:build
```

2. Build the website:
```bash
npm run build
```

3. Run the production server:
```bash
npm run server:prod
```

## API Endpoints

The RAG API server provides the following endpoints:

- `GET /` - API information and available endpoints
- `GET /health` - Health check
- `POST /api/rag-query` - Process a RAG query
- `POST /api/index-content` - Index book content into Qdrant

## How It Works

1. **Document Indexing**: The system reads all markdown files from the book content (docs, textbook, blog, content directories) and indexes them into Qdrant vector database.

2. **Query Processing**: When a user asks a question, the system:
   - Generates embeddings for the query using OpenAI
   - Searches for relevant documents in Qdrant
   - Uses the retrieved documents as context for the LLM
   - Generates a contextual response

3. **Response Generation**: The system uses GPT to generate responses based on the retrieved context.

## Environment Variables

- `QDRANT_URL`: Your Qdrant Cloud URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `OPENAI_API_KEY`: Your OpenAI API key

## Troubleshooting

1. **Qdrant Connection Issues**: Ensure your Qdrant URL and API key are correct
2. **OpenAI API Issues**: Verify your OpenAI API key is valid and has sufficient credits
3. **Content Not Found**: Run the indexing endpoint to ensure all book content is in the vector database
4. **Chatbot Not Showing**: Make sure the API server is running on port 3002 when using the full RAG functionality

## Security Note

Never commit your API keys to version control. Always use environment variables and ensure your `.env` file is in `.gitignore`.

## Architecture

- Frontend: Docusaurus-based website with React chatbot component
- Backend: Express.js API server
- Vector Database: Qdrant Cloud
- LLM: OpenAI GPT models

## Using the Chatbot

The chatbot is accessible in multiple locations:
- Main navigation menu: "AI Assistant" link
- Left sidebar: "🤖 AI Assistant" link
- Footer navigation: "AI Assistant" link
- Direct URL: `/chatbot`

The chatbot is implemented with a fallback mechanism for static builds, so even if the backend API is not running, users will see a functional chatbot with simulated responses based on the book content.