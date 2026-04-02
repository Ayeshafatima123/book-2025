import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { validateSpecificToken } from './jwt-validator';

// JWT authentication middleware
export const authenticateJWT = (req: Request, res: Response, next: NextFunction) => {
  // Allow health checks without authentication
  if (req.path === '/health' && req.method === 'GET') {
    return next();
  }

  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({
      error: 'Access token required'
    });
  }

  // Validate the specific token provided by the user
  if (!validateSpecificToken(token)) {
    return res.status(403).json({
      error: 'Invalid or unauthorized token'
    });
  }

  // Token is valid, continue with request
  next();
};