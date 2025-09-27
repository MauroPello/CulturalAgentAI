# # CULTURA Backend

FastAPI-based backend service providing intelligent document processing, cultural text alignment, and project planning capabilities.

## 🚀 Features

- **Document Processing**: Multi-format document upload and processing (PDF, DOCX, XLSX, XLS, TXT)
- **Intelligent Search**: Smart query routing with RAG, web search, and direct LLM responses
- **Vector Database**: ChromaDB integration for semantic document search
- **Gantt Planning**: Business description to structured project plan conversion
- **Cultural Text Processing**: AI-powered cultural adaptation of text content
- **Modern API**: FastAPI with automatic OpenAPI documentation

## 🏗️ Architecture

```
backend/
├── main.py              # FastAPI application entry point
├── config.py           # Configuration management
├── dependencies.py     # Dependency injection
├── requirements.txt    # Python dependencies
├── example.env         # Environment variables template
├── processing/         # Document processing pipeline
│   ├── loader.py      # Document text extraction
│   ├── chunker.py     # Text chunking logic
│   ├── embedder.py    # Text embedding generation
│   └── vector_store.py # ChromaDB integration
├── models/
│   └── schemas.py     # Pydantic models
├── services/          # Business logic services
│   ├── llm_services.py      # LLM client wrapper
│   ├── query_router.py      # Intelligent query routing
│   ├── rag_service.py       # RAG search implementation
│   └── web_search_service.py # Google search integration
├── routers/           # API route handlers
│   └── search.py     # Search-related endpoints
├── gantt/            # Gantt planning service
│   ├── models.py     # Gantt-specific models
│   └── planner.py    # Gantt plan generation
└── chroma_db/        # ChromaDB storage directory
```

## 🛠️ Setup

### Prerequisites

- Python 3.11+ (recommended)
- pip or poetry for dependency management

### Environment Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp example.env .env
   ```

   Edit `.env` with your actual API keys:
   ```env
   # Required API Keys
   PUBLIC_AI_KEY=your_public_ai_key_here
   GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id_here
   SWISS_AI_PLATFORM_API_KEY=your_swiss_ai_platform_api_key_here
   
   # Optional Configuration
   LLM_TEMPERATURE=0.1
   MAX_RAG_RESULTS=5
   ROUTER_CONFIDENCE_THRESHOLD=7.0
   ```

### Running the Server

**Development**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production**:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Document Processing

#### `POST /process-documents/`
Upload and process multiple documents for vector search.

**Request**:
```bash
curl -X POST "http://localhost:8000/process-documents/" \
  -F "files=@document1.pdf" \
  -F "files=@document2.docx"
```

**Response**:
```json
{
  "message": "Document processing finished.",
  "processed_files": [
    {
      "file_id": "uuid-string",
      "filename": "document1.pdf",
      "chunks_added": 25
    }
  ],
  "total_chunks_added": 25,
  "total_documents_in_store": 25
}
```

#### `POST /ask`
Intelligent query with smart routing (RAG, Web, Direct, or Hybrid).

**Request**:
```json
{
  "query": "What are the key market opportunities mentioned in the documents?",
  "force_strategy": "RAG"  // Optional: force specific strategy
}
```

**Response**:
```json
{
  "query": "What are the key market opportunities...",
  "strategy_used": "RAG",
  "confidence": 8.5,
  "answer": "Based on the uploaded documents, the key market opportunities include...",
  "sources": [
    {
      "source": "rag",
      "title": "Market Analysis Document",
      "content": "The European market shows strong growth...",
      "relevance_score": 0.89
    }
  ],
  "execution_time": 2.3,
  "tokens_used": 450
}
```

### Cultural Processing

#### `POST /cultural_align_text/`
Adapt text for specific cultures and languages.

**Request**:
```json
{
  "text": "We'll get back to you soon with our decision.",
  "target_culture": "Japanese Business Culture",
  "language": "English"
}
```

### Gantt Planning

#### `POST /convert`
Convert business description to structured Gantt chart.

**Request**:
```json
{
  "description": "Launch a mobile food delivery app in Switzerland targeting German-speaking regions...",
  "project_name": "SwissFood Mobile Launch"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PUBLIC_AI_KEY` | Yes | - | Public AI API key for LLM access |
| `GOOGLE_SEARCH_API_KEY` | Yes | - | Google Custom Search API key |
| `GOOGLE_SEARCH_ENGINE_ID` | Yes | - | Google Custom Search Engine ID |
| `SWISS_AI_PLATFORM_API_KEY` | Yes | - | Swiss AI Platform API key |
| `LLM_MODEL` | No | swiss-ai/apertus-8b-instruct | LLM model identifier |
| `LLM_TEMPERATURE` | No | 0.1 | LLM response temperature |
| `LLM_MAX_TOKENS` | No | 1000 | Maximum tokens per LLM response |
| `MAX_RAG_RESULTS` | No | 5 | Maximum RAG search results |
| `MAX_WEB_RESULTS` | No | 5 | Maximum web search results |
| `ROUTER_CONFIDENCE_THRESHOLD` | No | 7.0 | Query routing confidence threshold |
| `SERVER_HOST` | No | localhost | Server bind host |
| `SERVER_PORT` | No | 8000 | Server port |
| `DEBUG_MODE` | No | false | Enable debug logging |

### Supported File Types

| Type | MIME Type | Extensions |
|------|-----------|------------|
| PDF | application/pdf | .pdf |
| Word Document | application/vnd.openxmlformats-officedocument.wordprocessingml.document | .docx |
| Excel Spreadsheet | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | .xlsx |
| Legacy Excel | application/vnd.ms-excel | .xls |
| Text File | text/plain | .txt |

## 🔍 Intelligent Query Routing

The backend features sophisticated query analysis to automatically determine the best information retrieval strategy:

### Strategies

1. **RAG (Retrieval-Augmented Generation)**: Search uploaded documents
2. **WEB**: Google Custom Search for current information
3. **DIRECT**: LLM knowledge without external search
4. **HYBRID**: Combination of RAG and web search

### Routing Logic

- **Temporal indicators** (latest, current, today) → WEB search
- **Internal references** (our documents, uploaded files) → RAG search
- **General knowledge** questions → DIRECT response
- **Complex queries** requiring multiple sources → HYBRID approach

### Example Routing

```
"What are our Q3 sales figures?" → RAG (internal reference)
"Latest COVID-19 statistics in Switzerland" → WEB (temporal + location)
"What is the capital of France?" → DIRECT (general knowledge)
"Compare our revenue growth with industry trends" → HYBRID (internal + external)
```

## 🧪 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

### Code Quality

```bash
# Type checking
mypy .

# Code formatting
black .
isort .

# Linting
flake8 .
```

### Development Tools

- **Hot reload**: Automatic server restart on code changes
- **API docs**: Interactive documentation at `/docs`
- **Logging**: Structured logging with configurable levels
- **CORS**: Pre-configured for frontend development

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use environment-specific `.env` files
- Set `DEBUG_MODE=false` for production
- Configure proper logging levels
- Use reverse proxy (nginx) for static files
- Set up health checks for monitoring
- Consider using Redis for caching search results

## 📊 Monitoring

### Health Checks

The API includes built-in health check endpoints:
- `GET /` - Basic API status
- `GET /docs` - API documentation availability

### Logging

- Request/response logging with execution times
- Error tracking with stack traces
- Performance metrics for query routing
- Document processing statistics

## ❗ Troubleshooting

### Common Issues

1. **API Key Errors**: Verify all required keys are set in `.env`
2. **ChromaDB Issues**: Check directory permissions for `chroma_db/`
3. **Memory Usage**: Large documents may require increased memory limits
4. **Network Timeouts**: Increase timeout settings for slow networks

### Debug Mode

Enable debug mode for detailed logging:
```bash
DEBUG_MODE=true uvicorn main:app --reload
```

## 📞 Support

- Check API documentation at `/docs` for interactive testing
- Review logs for detailed error information  
- Ensure all dependencies are correctly installed
- Verify environment variables are properly set

---

**CulturalAgentAI Backend** - Intelligent document processing with cultural awareness.

FastAPI server providing dual functionality:
1. **Cultural Document Processing**: Upload, process, and query documents with AI
2. **SwissAI Gantt Planner**: Self-contained API module for project planning

## 🚀 Features

### Document Processing Pipeline
- Multi-format document support (PDF, DOCX, XLSX, XLS, TXT)
- Text extraction and intelligent chunking
- Vector embeddings for semantic search
- AI-powered document Q&A

### SwissAI Gantt Planner API
- Self-contained API module in `api/gantt/`
- Business plan to Gantt chart conversion
- Uses Swiss-AI Apertus-8B-Instruct model via Public AI
- Structured JSON output with tasks, milestones, timelines
- Automatic risk assessment and success metrics
- Can run independently on port 8001

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy the example environment file and configure your API keys:
```bash
cp .env.example .env
```

Edit `.env` file:
```env
PUBLIC_AI_KEY=your_ai_api_key_here
PUBLIC_AI_API_KEY=your_publicai_api_token_here
```

### 3. Start the Server
```bash
uvicorn main:app --reload
```

## 📊 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /docs` - Interactive API documentation

### Document Processing
- `POST /process-document/` - Upload and process documents
- `POST /query/` - Query processed documents with natural language
- `GET /uploaded-files` - List all uploaded files

### SwissAI Gantt Planner API
- `GET /gantt-api-info` - Information about the Gantt API service

**Note**: The SwissAI Gantt Planner runs as a separate self-contained API:

```bash
# Start the Gantt API (runs on port 8001)
python api/gantt/start_api.py
```

**Gantt API Endpoints** (at http://localhost:8001):
- `GET /` - API information
- `GET /health` - Health check
- `POST /convert` - Convert business description to Gantt plan
- `GET /docs` - Interactive API documentation

## 🧩 Module Structure

```
backend/
├── main.py                 # Main FastAPI application
├── processing/            # Document processing modules
│   ├── loader.py         # Document text extraction
│   ├── chunker.py        # Text chunking logic
│   ├── embedder.py       # Text embedding generation
│   └── vector_store.py   # Vector database operations
├── llm/                  # LLM integration utilities
├── api/                  # Self-contained API modules
│   └── gantt/            # SwissAI Gantt Planner API
│       ├── __init__.py   # Module initialization
│       ├── app.py        # FastAPI application for Gantt service
│       ├── config.py     # Configuration management
│       ├── models.py     # Pydantic data models
│       ├── planner.py    # Core planning logic with Public AI integration
│       └── start_api.py  # API server startup script
└── requirements.txt      # Python dependencies
```

## 🔧 Usage Examples

### Document Processing
```python
import requests

# Upload a document
with open('business_plan.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/process-document/', files=files)

# Query the document
query_data = {
    "query": "What are the main project milestones?",
    "n_results": 5
}
response = requests.post('http://localhost:8000/query/', json=query_data)
```

### SwissAI Gantt Planning
```python
import requests

# Convert business description to Gantt plan (separate API on port 8001)
gantt_request = {
    "description": """
    E-commerce platform development:
    - 3-month timeline
    - Team of 4 developers
    - Budget: $100,000
    - Features: user auth, product catalog, payment processing
    """,
    "project_name": "E-commerce Platform"
}
response = requests.post('http://localhost:8001/convert', json=gantt_request)
gantt_plan = response.json()
```

## 🐛 Troubleshooting

### SwissAI Gantt Planner Issues
1. **Module not loading**: Ensure `PUBLIC_AI_API_KEY` is set in `.env`
2. **API timeouts**: Complex projects may take 45+ seconds to process
3. **Missing dependencies**: Run `pip install -r requirements.txt`

### Document Processing Issues
1. **Unsupported file types**: Check supported formats in error messages
2. **Upload failures**: Ensure file isn't corrupted and meets size limits
3. **Query errors**: Verify documents are successfully processed first

## 📈 Performance Notes

- **SwissAI Processing Time**: 30-60 seconds for complex business plans
- **Document Processing**: Varies by file size and type
- **Memory Usage**: Scales with document size and embedding count

## 🔒 Security

- Environment variables for API key management
- CORS configured for frontend integration
- Input validation with Pydantic models
- Error handling prevents information leakage