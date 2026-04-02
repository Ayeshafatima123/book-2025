const express = require('express');
const cors = require('cors');
const { authenticateJWT } = require('./my-website/src/api/auth-middleware');

// Import rag-api and document-indexer with better error handling
let handleRAGQuery;
let indexBookContent;

try {
  const ragModule = require('./my-website/src/api/rag-api');
  handleRAGQuery = ragModule.handleRAGQuery;
  const indexerModule = require('./my-website/src/api/document-indexer');
  indexBookContent = indexerModule.indexBookContent;
} catch (error) {
  console.warn('Warning: Could not load RAG modules. Using mock implementation.');
  console.warn('Error details:', error);
  
  // Provide mock implementations
  handleRAGQuery = async (query) => {
    return {
      response: `This is a mock response for your query: "${query}". To enable the full RAG functionality, please ensure all required API keys are configured in the .env file.`,
      sources: [{ content: 'Mock source content...', metadata: { title: 'Mock Document', path: 'mock/path' }, score: 0.9 }],
    };
  };
  
  indexBookContent = async () => {
    console.log('Mock indexing function called');
    return Promise.resolve();
  };
}

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK', message: 'RAG API server is running' });
});

// RAG query endpoint - requires authentication
app.post('/api/rag-query', authenticateJWT, async (req, res) => {
  try {
    const { query } = req.body;

    if (!query || typeof query !== 'string') {
      return res.status(400).json({
        error: 'Query is required and must be a string'
      });
    }

    console.log(`Received RAG query: ${query.substring(0, 50)}...`);

    // Process the RAG query
    const result = await handleRAGQuery(query);

    res.json({
      response: result.response,
      sources: result.sources,
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
app.post('/api/index-content', authenticateJWT, async (req, res) => {
  try {
    console.log('Starting content indexing process...');
    await indexBookContent();

    res.json({
      message: 'Content indexing completed successfully',
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
app.get('/', (req, res) => {
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

module.exports = server;