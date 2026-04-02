import { QdrantClient } from '@qdrant/js-client-rest';

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
  distance: 'Cosine' as const,

};

// Initialize the collection if it doesn't exist
export const initializeCollection = async () => {
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
export const upsertDocuments = async (documents: Array<{
  id: string;
  content: string;
  metadata: Record<string, any>;
}>) => {
  const points = documents.map((doc) => ({
    id: doc.id,
    vector: [] as number[], // This will be populated with embeddings
    payload: {
      content: doc.content,
      ...doc.metadata,
    },
  }));

  // Note: In a real implementation, you'd call an embedding API here
  // For now, we'll need to pass pre-computed embeddings

  await qdrantClient.upsert(COLLECTION_NAME, {
    wait: true,
    points,
  });
};

// Function to search documents in Qdrant
export const searchDocuments = async (queryVector: number[], limit: number = 5) => {
  const results = await qdrantClient.search(COLLECTION_NAME, {
    vector: queryVector,
    limit,
    with_payload: true,
  });

  return results;
};

export default qdrantClient;