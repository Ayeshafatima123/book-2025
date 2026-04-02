#!/bin/bash

# Build and serve script for Docusaurus with RAG server

echo "Starting build and serve process for Docusaurus with RAG server..."

# Function to clean up background processes on exit
cleanup() {
    echo "Shutting down services..."
    jobs -p | xargs -r kill
    exit 0
}

# Set up trap to handle Ctrl+C
trap cleanup INT TERM

# Start the RAG API server in the background
echo "Starting RAG API server..."
cd /mnt/c/Users/ahmed/OneDrive/Documents/GitHub/hackathon--book-2025
npm run server &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 3

# Check if server started successfully
if kill -0 $SERVER_PID 2>/dev/null; then
    echo "RAG API server is running (PID: $SERVER_PID)"
else
    echo "Failed to start RAG API server"
    exit 1
fi

# Build the Docusaurus site
echo "Building Docusaurus site..."
cd /mnt/c/Users/ahmed/OneDrive/Documents/GitHub/hackathon--book-2025/my-website
npm run build

if [ $? -eq 0 ]; then
    echo "Docusaurus build completed successfully"
else
    echo "Docusaurus build failed"
    kill $SERVER_PID
    exit 1
fi

# Start Docusaurus server in the background
echo "Starting Docusaurus server..."
npm run serve &
DOCUSITE_PID=$!

# Wait for both processes
wait $SERVER_PID $DOCUSITE_PID