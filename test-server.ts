import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  console.log('Health check received');
  res.status(200).json({ status: 'OK', message: 'Test server is running' });
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  console.log('Root endpoint received');
  res.json({
    message: 'Test server running'
  });
});

const server = app.listen(PORT, () => {
  console.log(`Test server running on port ${PORT}`);
});

// Add error handling
server.on('error', (err) => {
  console.error('Server error:', err);
});

export default server;