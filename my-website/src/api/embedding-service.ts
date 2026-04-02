
import OpenAI from 'openai';
import { initializeCollection, upsertDocuments } from './qdrant-client';

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || 'your-openai-api-key', // Replace with your OpenAI API key
});

// Function to generate embeddings for text
export const generateEmbeddings = async (text: string): Promise<number[]> => {
  try {
    const response = await openai.embeddings.create({
      model: 'text-embedding-ada-002',
      input: text,
    });

    return response.data[0].embedding;
  } catch (error) {
    console.error('Error generating embeddings:', error);
    throw error;
  }
};

// Function to chunk large documents into smaller pieces
export const chunkText = (text: string, chunkSize: number = 1000): string[] => {
  const sentences = text.split(/(?<=[.!?])\s+/);
  const chunks: string[] = [];
  let currentChunk = '';

  for (const sentence of sentences) {
    if (currentChunk.length + sentence.length <= chunkSize) {
      currentChunk += sentence + ' ';
    } else {
      if (currentChunk.trim().length > 0) {
        chunks.push(currentChunk.trim());
      }
      currentChunk = sentence + ' ';
    }
  }

  if (currentChunk.trim().length > 0) {
    chunks.push(currentChunk.trim());
  }

  return chunks;
};

// Function to process and index a document
export const processAndIndexDocument = async (
  id: string,
  content: string,
  metadata: Record<string, any>
) => {
  // Initialize the collection
  await initializeCollection();

  // Chunk the content
  const chunks = chunkText(content);

  // Process each chunk
  const documentsToUpsert = [];
  for (let i = 0; i < chunks.length; i++) {
    const chunkId = `${id}-chunk-${i}`;
    const embedding = await generateEmbeddings(chunks[i]);

    documentsToUpsert.push({
      id: chunkId,
      content: chunks[i],
      metadata: {
        ...metadata,
        chunk_index: i,
        total_chunks: chunks.length,
      },
    });
  }

  // Upsert all chunks to Qdrant
  await upsertDocuments(documentsToUpsert);
};

// Function to search for relevant documents
export const searchRelevantDocuments = async (query: string, limit: number = 5) => {
  // Generate embedding for the query
  const queryEmbedding = await generateEmbeddings(query);

  // Search in Qdrant
  const searchResults = await import('./qdrant-client.js').then(
    async ({ searchDocuments }) => await searchDocuments(queryEmbedding, limit)
  );

  return searchResults;
};