# CulturalAgentAI Backend

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