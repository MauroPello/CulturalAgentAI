# CulturalAgentAI API Module

Self-contained API services for the CulturalAgentAI platform.

## 🏗️ Structure

```
api/
├── __init__.py
└── gantt/              # SwissAI Gantt Planner API
    ├── __init__.py     # Module initialization
    ├── app.py          # FastAPI application
    ├── planner.py      # Core planner logic
    ├── models.py       # Pydantic data models
    ├── config.py       # Configuration settings
    ├── requirements.txt # Module dependencies
    ├── .env.example    # Environment template
    ├── start_api.py    # Startup script
    └── README.md       # Module documentation
```

## 🚀 Available APIs

### SwissAI Gantt Planner (`/api/gantt/`)

Convert business plan descriptions into structured Gantt chart JSON using Swiss-AI Apertus model.

**Features:**
- AI-powered project planning
- Structured JSON output with tasks, milestones, budgets
- REST API with automatic documentation
- Self-contained and modular

**Quick Start:**
```bash
cd CulturalAgentAI/backend
export PUBLIC_AI_API_KEY="your_key_here"
python api/gantt/start_api.py
```

## 📖 Documentation

Each API module contains its own comprehensive documentation:
- Module README with setup instructions
- API endpoint documentation
- Usage examples and integration guides

## 🧪 Testing

Test scripts are provided for each module:

```bash
# Test core functionality
python test_gantt_core.py

# Test full integration
python test_api_integration.py
```

## 🔧 Integration

The API modules are designed to be:
- **Self-contained**: Each module has its own dependencies and configuration
- **Modular**: Can be imported and used independently
- **Scalable**: Can run as standalone services or integrated into larger applications

### Direct Usage

```python
from api.gantt import create_planner

planner = create_planner(api_key="your_key")
result = planner.generate_gantt_plan("Build a website in 2 months")
```

### As Microservices

Each API module can run as an independent microservice with its own port and configuration.

## 🌐 Development

To add new API modules:

1. Create a new directory under `api/`
2. Follow the structure pattern of existing modules
3. Include comprehensive documentation and tests
4. Update this overview README

## 📝 License

Part of the CulturalAgentAI project. See main project license.

---

**CulturalAgentAI API Module** - Modular AI-powered services 🚀