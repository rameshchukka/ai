pip install -r requirements.txt

Module Descriptions
config.py

Manages all configuration settings
Loads and validates environment variables
Provides default values
Centralized configuration access

pdf_processor.py

Extracts text from PDF files using Docling
Chunks documents into manageable pieces
Filters chunks by minimum length
Provides extraction statistics

embeddings.py

Generates embeddings using Gemini API
Handles rate limiting with retry logic
Supports both document and query embeddings
Exponential backoff for API errors

vector_store.py

Manages Neo4j database operations
Stores chunks with embeddings
Performs vector similarity search
Handles database schema setup
Provides CRUD operations for documents

response_generator.py

Generates responses using Gemini LLM
Creates context-aware prompts
Handles rate limiting
Formats responses with citations

rag_orchestrator.py

Coordinates all RAG components
Manages end-to-end pipelines
Provides high-level API
Handles component initialization

app.py

Gradio web interface
Multi-tab layout
File upload handling
Real-time query processing
Database management UI

🎨 Using the Gradio UI
Upload Documents Tab

Click "Upload PDF File"
Select your PDF document
Click "🚀 Process PDF"
Wait for processing (shows progress)
View statistics and database status

Query Knowledge Base Tab

Enter your question
Adjust number of chunks (1-10)
Click "🔍 Search"
View AI-generated answer
Check source citations

Manage Database Tab

View current database status
See all indexed documents
Delete specific documents by name
Refresh status

System Info Tab

View configuration settings
Check model information
See API rate limits
Review features