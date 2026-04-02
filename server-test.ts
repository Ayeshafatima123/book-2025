import express, { Request, Response } from 'express';
import cors from 'cors';
import { authenticateJWT } from './my-website/src/api/auth-middleware';

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  console.log('Health check received');
  res.status(200).json({ status: 'OK', message: 'RAG API server is running' });
});

// RAG query endpoint - requires authentication
app.post('/api/rag-query', authenticateJWT, async (req: Request, res: Response) => {
  try {
    const { query } = req.body;

    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        error: 'Query is required and must be a string'
      });
    }

    console.log(`Received RAG query: ${query.substring(0, 50)}...`);

    // For now, return a mock response
    // In the full implementation, this would call handleRAGQuery
    res.json({
      response: `This is a mock response for your query: "${query}". In the full implementation, this would connect to Qdrant and OpenAI to generate a contextual response.`,
      sources: [{ content: 'Mock source content...', metadata: { title: 'Mock Document', path: 'mock/path' }, score: 0.9 }],
      query: query,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error processing RAG query:', error);
    res.status(500).json({
      error: 'Internal server error while processing query',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Endpoint to trigger content indexing - requires authentication
app.post('/api/index-content', authenticateJWT, async (req: Request, res: Response) => {
  try {
    console.log('Starting content indexing process...');
    
    res.json({
      message: 'Content indexing would start now. In the full implementation, this would index documents into Qdrant.',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error during content indexing:', error);
    res.status(500).json({
      error: 'Internal server error during indexing',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'Physical AI RAG API Server',
    endpoints: {
      'POST /api/rag-query': 'Process a RAG query',
      'POST /api/index-content': 'Index book content into vector database',
      'GET /health': 'Health check'
    }
  });
});

const server = app.listen(PORT, () => {
  console.log(`RAG API server running on port ${PORT}`);
  console.log(`Ready to handle RAG queries...`);
});

// Add error handling for the server
server.on('error', (err) => {
  console.error('Server error:', err);
});

export default server;