// API Configuration
export const API_CONFIG = {
  baseUrl: process.env.RAG_API_BASE_URL || 'http://localhost:3002',
  auth: {
    // Placeholder for JWT token - in production, this would come from secure storage
    // after a proper authentication flow
    token: process.env.REACT_APP_RAG_JWT_TOKEN || null,
  }
};

export default API_CONFIG;