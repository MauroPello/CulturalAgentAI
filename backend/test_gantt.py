#!/usr/bin/env python3
"""
Simple test script to verify SwissAI Gantt Planner functionality
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

def test_gantt_converter():
    """Test the Gantt converter with a simple business description"""
    
    print("🧪 Testing SwissAI Gantt Planner...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if API key is set
    api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    if not api_key:
        return "❌ FAILED: SWISS_AI_PLATFORM_API_KEY environment variable not set"
    
    print(f"✅ API key is set (first 10 chars: {api_key[:10]}...)")
    
    try:
        # Import the planner
        from api.gantt.planner import SwissAIGanttPlanner
        print("✅ Successfully imported SwissAIGanttPlanner")
        
        # Initialize planner
        planner = SwissAIGanttPlanner()
        print("✅ Successfully initialized planner")
        
        # Test with simple description
        test_description = "Build a simple e-commerce website in 6 weeks with a team of 3 developers. Include user authentication, product catalog, shopping cart, and payment processing."
        project_name = "E-commerce Website Project"
        
        print(f"🚀 Testing with description: '{test_description}'")
        print("📡 Calling API...")
        
        result = planner.generate_gantt_plan(test_description, project_name)
        
        print("✅ API call successful!")
        print(f"Result type: {type(result)}")
        
        # Debug: Print the actual result structure
        print("📋 Full result structure:")
        print(json.dumps(result, indent=2, default=str))
        
        # Check if result has expected structure
        if not isinstance(result, dict):
            return "❌ FAILED: Result is not a dictionary"
            
        # Handle different possible response structures
        gantt_plan = None
        if "gantt_plan" in result:
            gantt_plan = result["gantt_plan"]
        elif "GanttResponse" in result:
            gantt_response = result["GanttResponse"]
            if isinstance(gantt_response, dict) and "gantt_plan" in gantt_response:
                gantt_plan = gantt_response["gantt_plan"]
            else:
                gantt_plan = gantt_response
        else:
            return f"❌ FAILED: No gantt_plan or GanttResponse found. Available keys: {list(result.keys())}"
            
        if gantt_plan is None:
            return "❌ FAILED: Could not extract gantt_plan from response"
            
        print(f"✅ Found gantt plan in result")
        
        # Check required fields
        required_fields = ["project_name", "tasks", "milestones", "project_start_date"]
        missing_fields = [field for field in required_fields if field not in gantt_plan]
        
        if missing_fields:
            return f"❌ FAILED: Missing required fields: {missing_fields}. Available fields: {list(gantt_plan.keys())}"
        
        print(f"✅ All required fields present: {required_fields}")
        
        # Check tasks
        tasks = gantt_plan["tasks"]
        if not isinstance(tasks, list) or len(tasks) == 0:
            return f"❌ FAILED: No tasks generated. Tasks: {tasks}"
        
        print(f"✅ Generated {len(tasks)} tasks")
        
        # Print some details
        print(f"📋 Project: {gantt_plan['project_name']}")
        print(f"📅 Start Date: {gantt_plan['project_start_date']}")
        print(f"🎯 Milestones: {len(gantt_plan.get('milestones', []))}")
        
        # Print first few tasks
        print("📝 First 3 tasks:")
        for i, task in enumerate(tasks[:3]):
            task_name = task.get('name', task.get('task_name', 'Unknown'))
            start_date = task.get('start_date', 'Unknown')
            duration = task.get('duration_days', 'Unknown')
            print(f"  {i+1}. {task_name} (Start: {start_date}, Duration: {duration} days)")
        
        return "✅ SUCCESS: Gantt converter works properly!"
        
    except ImportError as e:
        return f"❌ FAILED: Import error - {str(e)}"
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

if __name__ == "__main__":
    result = test_gantt_converter()
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print(result)
    print("="*50)