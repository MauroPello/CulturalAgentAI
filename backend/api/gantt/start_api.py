#!/usr/bin/env python3
"""
Startup script for SwissAI Gantt Planner API
"""

import sys
import os
from pathlib import Path

# Add the backend path to sys.path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

def main():
    """Main startup function."""
    print("🚀 Starting SwissAI Gantt Planner API...")
    
    # Check for API key
    if not os.getenv("PUBLIC_AI_API_KEY"):
        print("❌ PUBLIC_AI_API_KEY environment variable is required")
        print("Set it with: export PUBLIC_AI_API_KEY='your_key_here'")
        return 1
    
    try:
        # Import and run the app
        import uvicorn
        from api.gantt.app import app
        
        print("📊 Model: swiss-ai/apertus-8b-instruct")
        print("🌐 Server starting at: http://localhost:8001")
        print("📖 API Documentation: http://localhost:8001/docs")
        print("❤️  Health Check: http://localhost:8001/health")
        print("\n" + "="*50 + "\n")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            reload=False,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install dependencies with: pip install -r api/gantt/requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Startup error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())