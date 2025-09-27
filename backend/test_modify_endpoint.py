#!/usr/bin/env python3
"""
Test script for the new modify_gantt endpoint
"""

import json
import requests

# Sample Gantt plan to modify
sample_gantt_plan = {
    "success": True,
    "gantt_plan": {
        "confidence": 0.9,
        "project_name": "Sample Project",
        "project_description": "A sample project for testing",
        "project_owner": "Project Manager",
        "project_start_date": "2025-01-01",
        "project_end_date": "2025-03-31",
        "total_duration_weeks": 12,
        "tasks": [
            {
                "id": "task-1",
                "name": "Task 1",
                "description": "First task description",
                "start_date": "2025-01-01",
                "end_date": "2025-01-15",
                "duration_days": 14,
                "dependencies": [],
                "priority": "high",
                "status": "not_started",
                "progress_percentage": 0,
                "assigned_to": ["Developer 1"],
                "resources": ["Computer", "IDE"],
                "tags": ["development"],
                "estimated_effort_hours": 80
            },
            {
                "id": "task-2",
                "name": "Task 2",
                "description": "Second task description",
                "start_date": "2025-01-16",
                "end_date": "2025-02-15",
                "duration_days": 30,
                "dependencies": ["task-1"],
                "priority": "medium",
                "status": "not_started",
                "progress_percentage": 0,
                "assigned_to": ["Developer 2"],
                "resources": ["Computer", "Database"],
                "tags": ["database", "backend"],
                "estimated_effort_hours": 120
            }
        ],
        "milestones": [
            {
                "id": "milestone-1",
                "name": "First Milestone",
                "description": "Completion of first phase",
                "due_date": "2025-02-15",
                "success_criteria": ["Task 1 completed", "Task 2 completed"]
            }
        ],
        "phases": ["Planning", "Development", "Testing"],
        "budget_estimate": 50000.0,
        "risk_factors": ["Technical complexity", "Timeline constraints"],
        "success_metrics": ["On-time delivery", "Budget adherence"],
        "metadata": {}
    },
    "metadata": {}
}

def test_modify_endpoint():
    """Test the modify_gantt endpoint"""
    url = "http://localhost:8000/modify_gantt"
    
    # Test data
    payload = {
        "gantt_plan": sample_gantt_plan["gantt_plan"],
        "prompt": "Add a new task called 'Testing Phase' that should start after Task 2 and take 2 weeks to complete. Also add a milestone for the completion of testing."
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing modify_gantt endpoint...")
        print(f"URL: {url}")
        print(f"Payload keys: {payload.keys()}")
        print(f"Prompt: {payload['prompt']}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            # Navigate to the correct nested structure
            gantt_plan = result.get('gantt_plan', {}).get('gantt_plan', {})
            tasks = gantt_plan.get('tasks', [])
            milestones = gantt_plan.get('milestones', [])
            print(f"Modified plan received with {len(tasks)} tasks")
            print(f"Modified plan received with {len(milestones)} milestones")
            
            # Show the new additions
            print("\n📋 Tasks in modified plan:")
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. {task.get('name', 'Unknown')} (ID: {task.get('id', 'Unknown')})")
            
            print("\n🎯 Milestones in modified plan:")
            for i, milestone in enumerate(milestones, 1):
                print(f"  {i}. {milestone.get('name', 'Unknown')} (ID: {milestone.get('id', 'Unknown')})")
            
            print(f"\n⏱️  Processing time: {result.get('processing_time_seconds', 0):.2f} seconds")
            
            # Pretty print the response for inspection
            with open("/home/mattia/Documents/GitHub/CulturalAgentAI/backend/test_response.json", "w") as f:
                json.dump(result, f, indent=2)
            print("Full response saved to test_response.json")
            
        else:
            print("❌ Error!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_modify_endpoint()