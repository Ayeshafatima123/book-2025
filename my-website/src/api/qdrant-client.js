const { QdrantClient } = require('@qdrant/js-client-rest');

// Initialize Qdrant client with cloud configuration
const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL || 'https://your-cluster-name.europe-west3-0.gcp.cloud.qdrant.io:6333', // Replace with your Qdrant Cloud URL
  apiKey: process.env.QDRANT_API_KEY || 'your-api-key-here', // Replace with your Qdrant API key
});

// Collection name for the book content
const COLLECTION_NAME = 'physical_ai_book';

// Define the vector configuration
const VECTOR_CONFIG = {
  size: 1536, // OpenAI embedding dimension
  distance: 'Cosine',

};

// Initialize the collection if it doesn't exist
const initializeCollection = async () => {
  try {
    // Check if collection exists
    await qdrantClient.getCollection(COLLECTION_NAME);
    console.log(`Collection ${COLLECTION_NAME} already exists`);
  } catch (error) {
    // Collection doesn't exist, create it
    console.log(`Creating collection ${COLLECTION_NAME}`);
    await qdrantClient.createCollection(COLLECTION_NAME, {
      vectors: VECTOR_CONFIG,
    });
    console.log(`Collection ${COLLECTION_NAME} created successfully`);
  }
};

// Function to upsert documents to Qdrant
const upsertDocuments = async (documents) => {
  // First, generate embeddings for each document
  const points = [];
  for (const doc of documents) {
    const embedding = await require('./embedding-service.js').generateEmbeddings(doc.content);
    
    points.push({
      id: doc.id,
      vector: embedding, // Now we have the actual embedding
      payload: {
        content: doc.content,
        ...doc.metadata,
      },
    });
  }

  await qdrantClient.upsert(COLLECTION_NAME, {
    wait: true,
    points,
  });
};

// Function to search documents in Qdrant
const searchDocuments = async (queryVector, limit = 5) => {
  const results = await qdrantClient.search(COLLECTION_NAME, {
    vector: queryVector,
    limit,
    with_payload: true,
  });

  return results;
};

module.exports = {
  initializeCollection,
  upsertDocuments,
  searchDocuments,
  qdrantClient
};