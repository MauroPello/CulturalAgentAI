# CulturalAgentAI

An AI-powered platform for small and medium-sized businesses to expand into foreign markets with confidence. Built with Swiss-AI Apertus LLM for cultural intelligence and transparent, self-hostable AI consultation services.

## 🌟 Key Features

- **AI Market Expansion Consulting** - Interactive chat for expansion strategies
- **Gantt Chart Generation** - Convert discussions into actionable project plans  
- **Cultural Intelligence** - Powered by Apertus LLM trained on global languages/cultures
- **Document Intelligence** - Upload company docs for contextual recommendations
- **Privacy First** - Self-hostable with complete data sovereignty

## 🐳 Docker Setup

### Prerequisites
- Docker & Docker Compose

### Quick Start

1. **Configure environment**:
   ```bash
   cp backend/example.env backend/.env
   ```
   Edit `backend/.env` with your API keys:
   ```env
   SWISS_AI_PLATFORM_API_KEY=your_swiss_ai_platform_api_key_here
   GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id_here
   PUBLIC_AI_KEY=your_public_ai_key_here
   ```

2. **Build and run**:
   ```bash
   docker-compose up --build
   ```

3. **Access the platform**:
   - **Business Platform**: http://localhost:3000
   - **AI API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

4. **Stop the platform**:
   ```bash
   docker-compose down
   ```