# SwissAI Gantt Planner API

A self-contained FastAPI service for converting business plan descriptions into structured Gantt chart JSON using the Swiss-AI Apertus model via Public AI.

## 🚀 Features

- **AI-Powered Planning**: Uses Swiss-AI Apertus-8B-Instruct model for intelligent project planning
- **Structured Output**: Generates comprehensive JSON-formatted project plans
- **REST API**: FastAPI-based service with automatic documentation
- **Flexible Input**: Accepts business descriptions of any complexity
- **Comprehensive Plans**: Includes tasks, milestones, timelines, budgets, and risk assessments

## 📁 Structure

```
api/gantt/
├── __init__.py         # Package initialization
├── app.py             # FastAPI application
├── planner.py         # Core planner logic
├── models.py          # Pydantic data models
├── config.py          # Configuration settings
├── requirements.txt   # Dependencies
├── .env.example      # Environment template
└── README.md         # This file
```

## 🛠️ Installation

### 1. Environment Setup

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` with your Public AI API key:
```env
PUBLIC_AI_API_KEY=your_publicai_api_key_here
```

### 2. Install Dependencies

```bash
# From the gantt directory
pip install -r requirements.txt

# Or from the project root
pip install -r api/gantt/requirements.txt
```

### 3. Run the API

```bash
# Option 1: Run directly
python -m api.gantt.app

# Option 2: Use uvicorn
uvicorn api.gantt.app:app --host 0.0.0.0 --port 8001 --reload

# Option 3: From the gantt directory
cd api/gantt
python app.py
```

The API will be available at: http://localhost:8001

## 📖 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

## 🔌 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check with configuration status
- `POST /convert` - Convert business description to Gantt plan
- `GET /ping` - Simple monitoring endpoint

### Convert Endpoint

**POST /convert**

Request body:
```json
{
  "description": "Launch a mobile app in 3 months with team of 5 developers",
  "project_name": "Mobile App Launch"  // optional
}
```

Response:
```json
{
  "success": true,
  "gantt_plan": {
    "project_name": "Mobile App Launch",
    "total_duration_weeks": 12,
    "budget_estimate": 150000.0,
    "tasks": [...],
    "milestones": [...],
    // ... complete plan structure
  },
  "processing_time_seconds": 2.34,
  "timestamp": "2025-09-26T10:30:00"
}
```

## 🎯 Usage Examples

### Python Client

```python
import requests

# Convert business description
response = requests.post("http://localhost:8001/convert", json={
    "description": "Build an e-commerce platform in 6 months with $200k budget",
    "project_name": "E-commerce Platform"
})

gantt_plan = response.json()["gantt_plan"]
print(f"Project: {gantt_plan['project_name']}")
print(f"Duration: {gantt_plan['total_duration_weeks']} weeks")
print(f"Tasks: {len(gantt_plan['tasks'])}")
```

### cURL

```bash
curl -X POST "http://localhost:8001/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Launch a SaaS product in 4 months with 3 developers",
    "project_name": "SaaS Launch"
  }'
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8001/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: 'Create a mobile game in 8 weeks',
    project_name: 'Mobile Game Development'
  })
});

const result = await response.json();
console.log(`Generated ${result.gantt_plan.tasks.length} tasks`);
```

## 📊 Output Schema

The API generates comprehensive project plans with:

- **Project Metadata**: Name, description, owner, dates, duration
- **Tasks**: Detailed tasks with dependencies, assignments, estimates
- **Milestones**: Key project milestones with success criteria
- **Budget**: Estimated project budget
- **Risk Factors**: Identified project risks
- **Success Metrics**: KPIs and success measurements
- **Phases**: Project phases organization

## ⚙️ Configuration

Environment variables (in `.env`):

```env
# Required
PUBLIC_AI_API_KEY=your_api_key

# Optional
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=false
LOG_LEVEL=info
MAX_TOKENS=4000
TEMPERATURE=0.0
REQUEST_TIMEOUT=60
```

## 🔧 Integration

### As a Microservice

The API is designed to be a self-contained microservice:

```python
from api.gantt.planner import create_planner

# Direct usage without FastAPI
planner = create_planner(api_key="your_key")
result = planner.generate_gantt_plan("Build a website in 2 months")
```

### With Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY api/gantt/ ./
RUN pip install -r requirements.txt

EXPOSE 8001
CMD ["python", "app.py"]
```

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8001/health
```

### Simple Test

```bash
curl -X POST http://localhost:8001/convert \
  -H "Content-Type: application/json" \
  -d '{"description": "Test project"}'
```

## ⚠️ Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `PUBLIC_AI_API_KEY` is set in `.env`
2. **Import Errors**: Install dependencies: `pip install -r requirements.txt`
3. **Port Conflicts**: Change `API_PORT` in `.env` or command line
4. **Request Timeouts**: Increase `REQUEST_TIMEOUT` for complex projects

### Debug Mode

Enable debug mode for detailed error messages:

```env
DEBUG=true
LOG_LEVEL=debug
```

## 📈 Performance

- **Typical Response Time**: 2-5 seconds for standard projects
- **Complex Projects**: 5-15 seconds for detailed business plans
- **Rate Limits**: Depends on Public AI API limits
- **Concurrent Requests**: FastAPI handles multiple concurrent requests

## 🤝 Integration with CulturalAgentAI

This module integrates seamlessly with the main CulturalAgentAI backend:

```python
# From main backend
from api.gantt import create_planner

def generate_project_plan(description: str):
    planner = create_planner()
    return planner.generate_gantt_plan(description)
```

## 📝 License

Part of the CulturalAgentAI project. See main project license.

---

**SwissAI Gantt Planner API** - Intelligent project planning powered by Swiss-AI 🚀