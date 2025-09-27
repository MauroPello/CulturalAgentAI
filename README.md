<div align="center">
  <img src="assets/cultura_logo_no_bg.png" alt="Cultura Logo" width="300">
</div>

# Cultura - Cultural AI Agent

An AI-powered platform for small and medium-sized businesses to expand into foreign markets with confidence. Built with the Swiss Apertus LLM for **multicultural** intelligence, **multilingual** understanding, and **transparent**, **self-hostable** AI consultation services.

## 🌟 Key Features

- **AI market expansion consulting**: Interactive chat for expansion strategies
- **Gantt chart generation**: Convert discussions into actionable project plans  
- **Cultural intelligence**: Powered by Apertus LLM trained on global languages and cultures
- **Document intelligence**: Upload company docs for contextual recommendations
- **Cultural alignment web extension**: Align any text/email/message on the browser to target language and culture 
- **Privacy-first** - Self-hostable with complete data sovereignty

## 🧩 Components of Cultura

Our solutions is composed of 2+1 **amazing** parts:

- **Website for expansion strategies**: Add your company's documents, chat with our agent (which has RAG and web search), define your goals and have the agent generate a contextually-relevant plan
- **Web extension for cultural alignment**: When emailing a colleague in a different country, use our extension to align your text to the colleague's language and culture, avoiding misunderstandings
- **Fine-tuned Apertus for tool use**: We contribute to the development of Apertus by fine-tuning the 8B model for function calling. We made this version available on [Hugging Face](https://huggingface.co/mattiaferrarini/Apertus-8B-Instruct-2509-tool-use) with the [training code](https://huggingface.co/mattiaferrarini/Apertus-8B-Instruct-2509-tool-use/blob/main/apertus_function_calling.ipynb) as well

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

**Note**: While we fine-tuned the Apertus model for function calling, this fine-tuned version is not used in the app. The decision was made due to token limitations and associated costs. In an ideal scenario, we would integrate the fine-tuned model directly into the app, as it would eliminate the need for a prompting approach to guide the model on whether to perform RAG, web search, or other tasks. This would result in a more efficient and streamlined process.