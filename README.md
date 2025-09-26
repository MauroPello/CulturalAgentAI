# CulturalAgentAI

A comprehensive AI-powered platform combining cultural document processing with intelligent project planning capabilities.

## 🌟 Features

### Cultural Document Processing
- **Multi-format Document Support**: Process PDF, DOCX, XLSX, XLS, and TXT files
- **Text Extraction & Chunking**: Intelligent text processing and segmentation
- **Vector Search**: Semantic search across uploaded documents using embeddings
- **AI-Powered Q&A**: Query documents with natural language and get contextual answers

### SwissAI Gantt Planner
- **Business Plan Conversion**: Transform business descriptions into structured Gantt charts
- **AI-Powered Planning**: Uses Swiss-AI Apertus-8B-Instruct model for intelligent project planning
- **Self-Contained API**: Independent service with its own documentation and endpoints
- **Structured Output**: Generate JSON-formatted project plans with tasks, milestones, and timelines
- **Risk Assessment**: Automatic identification of project risks and success metrics

## 🏗️ Architecture

```
CulturalAgentAI/
├── frontend/          # React-based web interface
├── backend/           # FastAPI server with dual functionality
│   ├── processing/    # Document processing pipeline
│   ├── llm/          # LLM integration utilities
│   ├── api/          # Self-contained API modules
│   │   └── gantt/    # SwissAI Gantt Planner API
│   └── main.py       # Main FastAPI application
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Public AI API key (for SwissAI Gantt Planner)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the backend directory:
   ```bash
   cp backend/.env.example backend/.env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   PUBLIC_AI_KEY=your_ai_api_key_here
   PUBLIC_AI_API_KEY=your_publicai_api_token_here
   ```

4. **Start the server**:
   ```bash
   uvicorn main:app --reload
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
   npm start
   ```

   The web interface will be available at: http://localhost:3000

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Key Endpoints

#### Document Processing
- `POST /process-document/` - Upload and process documents
- `POST /query/` - Query processed documents
- `GET /uploaded-files` - List uploaded files

#### SwissAI Gantt Planner
- `GET /gantt-api-info` - Information about the Gantt API service

**Note**: The SwissAI Gantt Planner runs as a separate API service. To use it:

```bash
# Start the Gantt API (separate from main backend)
cd backend
python api/gantt/start_api.py
# Available at http://localhost:8001/docs
```

## 💡 Usage Examples

### Document Processing
```python
import requests

# Upload a document
files = {'file': open('business_plan.pdf', 'rb')}
response = requests.post('http://localhost:8000/process-document/', files=files)

# Query the document
query = {"query": "What are the main objectives?", "n_results": 5}
response = requests.post('http://localhost:8000/query/', json=query)
```

### SwissAI Gantt Planning
```python
import requests

# The Gantt API runs on a separate port (8001)
gantt_request = {
    "description": "Launch a mobile app in 3 months with team of 5 developers",
    "project_name": "Mobile App Launch"
}
response = requests.post('http://localhost:8001/convert', json=gantt_request)
```

**To start the Gantt API:**
```bash
cd backend
export PUBLIC_AI_API_KEY="your_key"
python api/gantt/start_api.py
```

## 🛠️ Development

### Project Structure
- **Backend**: FastAPI-based server with modular API architecture
- **Frontend**: React application with modern UI/UX
- **API Modules**: Self-contained services (document processing, Gantt planning)
- **Modular Design**: Each API module can run independently or as part of the main service

### Key Technologies
- **Backend**: FastAPI, Pydantic, Requests, ChromaDB
- **Frontend**: React, TypeScript, Material-UI
- **AI Models**: Swiss-AI Apertus-8B-Instruct, Various embedding models

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

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the backend and frontend README files for detailed setup instructions

---

**CulturalAgentAI** - Bridging cultural document understanding with intelligent project planning.