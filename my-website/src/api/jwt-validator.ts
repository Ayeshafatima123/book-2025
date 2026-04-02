import jwt from 'jsonwebtoken';

// Function to validate the specific JWT token you provided
export const validateSpecificToken = (token: string): boolean => {
  const expectedToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.buTF0xgOeAnfMRkQh8PcVb6xC4IoYF-Bp0P4sqhn7mA';

  if (token !== expectedToken) {
    return false;
  }

  // Use the same secret that was used to generate the token
  // The token 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.buTF0xgOeAnfMRkQh8PcVb6xC4IoYF-Bp0P4sqhn7mA'
  // was created with the secret 'your-jwt-secret-here' based on the .env file
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-jwt-secret-here') as { access?: string };
    return decoded.access === 'm';
  } catch (error) {
    console.error('Token validation error:', error);
    return false;
  }
};