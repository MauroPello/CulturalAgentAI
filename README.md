# CulturalAgentAI

A comprehensive AI-powered platform combining cultural document processing with intelligent project planning capabilities, built on Vue/Nuxt.js frontend and FastAPI backend.

## 🌟 Features

### Cultural Document Processing
- **Multi-format Document Support**: Process PDF, DOCX, XLSX, XLS, and TXT files
- **Text Extraction & Chunking**: Intelligent text processing and segmentation
- **Vector Search**: Semantic search across uploaded documents using ChromaDB embeddings
- **AI-Powered Q&A**: Query documents with natural language and get contextual answers

### SwissAI Gantt Planner
- **Business Plan Conversion**: Transform business descriptions into structured Gantt charts
- **AI-Powered Planning**: Uses Swiss-AI Apertus-8B-Instruct model for intelligent project planning
- **Integrated API**: Built-in service with comprehensive endpoints
- **Structured Output**: Generate JSON-formatted project plans with tasks, milestones, and timelines
- **Risk Assessment**: Automatic identification of project risks and success metrics

### Browser Extension
- **Text Selection**: Select text from any web page and send to Cultural Agent
- **Cultural Alignment**: Process text for cultural adaptation
- **Manifest V3**: Modern Chrome extension with service worker architecture

## 🏗️ Architecture

```
CulturalAgentAI/
├── frontend/          # Nuxt.js 3 web application
│   ├── components/    # Vue 3 components
│   ├── pages/         # Application pages
│   ├── composables/   # Vue composables
│   └── types/         # TypeScript definitions
├── backend/           # FastAPI server
│   ├── processing/    # Document processing pipeline
│   ├── llm/          # LLM integration utilities
│   ├── gantt/        # Gantt planner service
│   ├── models/       # Pydantic models
│   ├── routers/      # API route handlers
│   └── services/     # Business logic services
├── web_extension/     # Chrome extension (Manifest V3)
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended)
- Node.js 18+ and npm
- API keys for:
  - Public AI (for Swiss-AI models)
  - Google Search API
  - Swiss AI Platform

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   ```bash
   cp example.env .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   PUBLIC_AI_KEY=your_public_ai_key_here
   GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id_here
   SWISS_AI_PLATFORM_API_KEY=your_swiss_ai_platform_api_key_here
   ```

5. **Start the server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   The web application will be available at: http://localhost:3000

### Browser Extension Setup

1. **Open Chrome Extensions** (chrome://extensions/)
2. **Enable Developer mode**
3. **Click "Load unpacked"**
4. **Select the `web_extension` folder**

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Key Endpoints

#### Document Processing
- `POST /process-documents/` - Upload and process multiple documents
- `POST /ask` - Intelligent query routing with search capabilities
- `GET /uploaded-files` - List uploaded files

#### Gantt Planning
- `POST /convert` - Convert business description to Gantt chart
- **Note**: Gantt planning is integrated into the main API

#### Cultural Text Processing
- `POST /cultural_align_text/` - Adapt text for different cultures and languages

## 💡 Usage Examples

### Document Processing
```python
import requests

# Upload documents
files = [
    ('files', ('business_plan.pdf', open('business_plan.pdf', 'rb'), 'application/pdf')),
    ('files', ('market_analysis.docx', open('market_analysis.docx', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'))
]
response = requests.post('http://localhost:8000/process-documents/', files=files)

# Intelligent query
query = {"query": "What are the main market opportunities mentioned in the documents?"}
response = requests.post('http://localhost:8000/ask', json=query)
print(response.json())
```

### Gantt Planning
```python
import requests

gantt_request = {
    "description": "Launch a mobile app for food delivery in Switzerland targeting German-speaking regions. Team of 8 developers, 3 designers, budget $500k, 6-month timeline.",
    "project_name": "SwissFood Mobile App Launch"
}
response = requests.post('http://localhost:8000/convert', json=gantt_request)
print(response.json())
```

### Cultural Text Alignment
```python
import requests

cultural_request = {
    "text": "Thanks for your business proposal. We'll review it and get back to you soon.",
    "target_culture": "Japanese Business Culture",
    "language": "English"
}
response = requests.post('http://localhost:8000/cultural_align_text/', json=cultural_request)
print(response.json())
```

## 🛠️ Development

### Project Structure
- **Backend**: FastAPI with async support, Pydantic models, modular services
- **Frontend**: Nuxt.js 3 with Vue 3, TypeScript, Tailwind CSS, Nuxt UI
- **Extension**: Manifest V3 Chrome extension with service worker
- **Database**: ChromaDB for vector storage, local file storage for uploads

### Key Technologies
- **Backend**: FastAPI, Pydantic, ChromaDB, Sentence Transformers, PyPDF, python-docx
- **Frontend**: Nuxt.js 3, Vue 3, TypeScript, Tailwind CSS, Nuxt UI, Axios
- **AI Models**: Swiss-AI Apertus-8B-Instruct, Sentence Transformers embeddings
- **Extension**: Chrome Extensions API, Manifest V3

### Development Commands

#### Backend
```bash
cd backend
# Run with auto-reload
uvicorn main:app --reload

# Run tests (if available)
pytest

# Type checking
mypy .
```

#### Frontend
```bash
cd frontend
# Development server
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint:fix
```

## 📋 Environment Variables

### Required Variables
- `PUBLIC_AI_KEY`: API key for Public AI service
- `GOOGLE_SEARCH_API_KEY`: Google Custom Search API key
- `GOOGLE_SEARCH_ENGINE_ID`: Google Custom Search Engine ID
- `SWISS_AI_PLATFORM_API_KEY`: Swiss AI Platform API key

### Optional Variables
- `LLM_MODEL`: LLM model to use (default: swiss-ai/apertus-8b-instruct)
- `LLM_TEMPERATURE`: Temperature for LLM responses (default: 0.1)
- `LLM_MAX_TOKENS`: Maximum tokens for LLM responses (default: 1000)
- `SERVER_HOST`: Server host (default: localhost)
- `SERVER_PORT`: Server port (default: 8000)
- `DEBUG_MODE`: Enable debug mode (default: false)

## 🚀 Deployment

### Backend Deployment
1. Set up production environment variables
2. Install production dependencies: `pip install -r requirements.txt`
3. Run with production ASGI server: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy the `.output` folder to your hosting provider
3. Configure environment variables for production API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Swiss-AI** for the Apertus-8B-Instruct model
- **Public AI** for providing API access to Swiss-AI models
- **FastAPI** community for the excellent web framework
- **Nuxt.js** team for the amazing full-stack framework

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the backend and frontend documentation

---

**CulturalAgentAI** - Bridging cultural document understanding with intelligent project planning.