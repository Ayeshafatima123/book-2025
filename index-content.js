// Simplified content indexing script
const fs = require('fs');
const path = require('path');
const { processAndIndexDocument } = require('./my-website/src/api/document-indexer'); // This will use the CommonJS version

// Read markdown files function
function readMarkdownFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);

  files.forEach((file) => {
    const filePath = path.join(dirPath, file);
    if (fs.statSync(filePath).isDirectory()) {
      arrayOfFiles = readMarkdownFiles(filePath, arrayOfFiles);
    } else if (file.endsWith('.md') || file.endsWith('.mdx')) {
      arrayOfFiles.push(filePath);
    }
  });

  return arrayOfFiles;
}

// Extract markdown content function
function extractMarkdownContent(filePath) {
  const fileContent = fs.readFileSync(filePath, 'utf8');

  // Extract frontmatter if present
  let content = fileContent;
  let title = '';
  let metadata = { filePath };

  // Simple frontmatter extraction (YAML between ---)
  const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)/);
  if (frontmatterMatch) {
    const frontmatter = frontmatterMatch[1];
    content = frontmatterMatch[2];

    // Parse simple key-value pairs from frontmatter
    const lines = frontmatter.split('\n');
    lines.forEach(line => {
      const [key, ...valueParts] = line.split(': ');
      if (key && valueParts.length > 0) {
        const value = valueParts.join(': ').trim();
        metadata[key.trim()] = value.startsWith('"') && value.endsWith('"')
          ? value.slice(1, -1)
          : value;
      }
    });
  }

  // Extract title from first heading if not in frontmatter
  if (!metadata.title) {
    const titleMatch = content.match(/^#\s+(.+)$/m);
    if (titleMatch) {
      title = titleMatch[1];
      metadata.title = title;
    }
  }

  // Add file path as metadata
  metadata.relativePath = path.relative(path.join(process.cwd(), 'my-website'), filePath);
  metadata.fileName = path.basename(filePath);
  
  // Try to extract the book chapter information from the file path
  const pathParts = filePath.split('/');
  const textbookDirIndex = pathParts.indexOf('textbook');
  const docsDirIndex = pathParts.indexOf('docs');
  
  if (textbookDirIndex !== -1 && pathParts[textbookDirIndex + 1]) {
    metadata.bookSection = pathParts[textbookDirIndex + 1];  // e.g., 'chapter-01'
    metadata.bookType = 'textbook';
  } else if (docsDirIndex !== -1 && pathParts[docsDirIndex + 1]) {
    metadata.bookSection = pathParts[docsDirIndex + 1];  // e.g., 'tutorial-basics'
    metadata.bookType = 'documentation';
  } else {
    metadata.bookType = 'other';
  }

  return { content, metadata };
}

// Enhanced function to split content into semantic chunks
function chunkContentSemantically(content) {
  // Split content into sections based on headings
  const sectionRegex = /^(#{1,6}\s+.*)$/gm;
  const sections = [];
  let lastIndex = 0;
  let match;

  while ((match = sectionRegex.exec(content)) !== null) {
    if (match.index > lastIndex) {
      // Capture content between previous section and current section
      sections.push(content.substring(lastIndex, match.index));
    }
    // Capture the section header plus content until the next section
    const sectionStart = match.index;
    const nextSectionMatch = content.substring(sectionStart + match[0].length).match(sectionRegex);
    const sectionEnd = nextSectionMatch ? 
      sectionStart + match[0].length + nextSectionMatch.index : 
      content.length;
    
    sections.push(content.substring(sectionStart, sectionEnd));
    lastIndex = sectionEnd;
  }

  if (lastIndex < content.length) {
    sections.push(content.substring(lastIndex));
  }

  // Further split large sections
  const chunks = [];
  for (const section of sections) {
    if (section.trim().length === 0) continue;
    
    if (section.length > 2000) {
      // Break down large sections into smaller chunks
      const subChunks = chunkBySentences(section, 1000);
      chunks.push(...subChunks);
    } else {
      chunks.push(section);
    }
  }

  return chunks.filter(chunk => chunk.trim().length > 0);
}

// Helper function to chunk by sentences
function chunkBySentences(text, maxChunkSize = 1000) {
  const sentences = text.split(/(?<=[.!?])\s+/);
  const chunks = [];
  let currentChunk = '';

  for (const sentence of sentences) {
    if (currentChunk.length + sentence.length <= maxChunkSize) {
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
}

// Main indexing function
async function indexBookContent() {
  console.log('Starting to index book content...');

  // Define directories to index
  const directories = [
    './my-website/docs',
    './my-website/textbook',
    './my-website/blog',
    './my-website/content'
  ];

  for (const dir of directories) {
    if (fs.existsSync(dir)) {
      console.log(`Indexing files from ${dir}...`);
      const markdownFiles = readMarkdownFiles(dir);

      for (const filePath of markdownFiles) {
        try {
          console.log(`Processing file: ${filePath}`);
          const { content, metadata } = extractMarkdownContent(filePath);

          // Create semantic chunks of content
          const chunks = chunkContentSemantically(content);
          
          console.log(`Split ${filePath} into ${chunks.length} chunks for indexing`);

          for (let i = 0; i < chunks.length; i++) {
            // Create a unique ID for each chunk
            const chunkId = `doc_${filePath.replace(/[\/\\]/g, '_').replace(/[^a-zA-Z0-9_]/g, '_')}_chunk_${i}`;
            
            // Enhance metadata for each chunk
            const chunkMetadata = {
              ...metadata,
              chunkIndex: i,
              totalChunks: chunks.length,
              chunkLabel: `${metadata.title || metadata.fileName} - Chunk ${i+1}/${chunks.length}`
            };

            // Process and index the document chunk
            await processAndIndexDocument(chunkId, chunks[i], chunkMetadata);

            console.log(`Indexed chunk: ${chunkId}`);
          }
        } catch (error) {
          console.error(`Error processing file ${filePath}:`, error);
        }
      }
    } else {
      console.log(`Directory does not exist: ${dir}`);
    }
  }

  console.log('Completed indexing book content.');
}

// Run indexing if this file is executed directly
if (require.main === module) {
  indexBookContent().catch(console.error);
}