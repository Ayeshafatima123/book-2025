import { searchRelevantDocuments } from './embedding-service';
import OpenAI from 'openai';

// Initialize OpenAI client for response generation
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || 'your-openai-api-key', // Replace with your OpenAI API key
});

// Function to generate a response based on retrieved documents
export const generateResponse = async (query: string, contextDocuments: any[]) => {
  // Format the context from retrieved documents
  const context = contextDocuments
    .map((doc: any) => doc.payload?.content || '')
    .join('\n\n');

  // Create a prompt with the query and context
  const prompt = `
    You are an assistant for the Physical AI & Humanoid Robotics book.
    Use the following context to answer the user's question.
    If the context doesn't contain enough information, say so.

    Context:
    ${context}

    Question: ${query}

    Answer:
  `;

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo', // or gpt-4 if preferred
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant for the Physical AI & Humanoid Robotics book. Answer questions based on the provided context. Be concise but informative.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      max_tokens: 500,
      temperature: 0.7,
    });

    return response.choices[0].message.content || 'I couldn\'t generate a response for your query.';
  } catch (error) {
    console.error('Error generating response:', error);
    throw error;
  }
};

// Function to handle the complete RAG flow
export const handleRAGQuery = async (query: string) => {
  try {
    // Search for relevant documents
    const searchResults = await searchRelevantDocuments(query);

    // Generate response based on retrieved documents
    const response = await generateResponse(query, searchResults);

    return {
      response,
      sources: searchResults.map((result: any) => ({
        content: result.payload?.content?.substring(0, 200) + '...',
        metadata: result.payload,
        score: result.score,
      })),
    };
  } catch (error) {
    console.error('Error in RAG query:', error);
    throw error;
  }
};