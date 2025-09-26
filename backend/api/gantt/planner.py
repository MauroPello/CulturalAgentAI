"""
SwissAI Gantt Planner Core Functionality

This module handles the interaction with the Swiss-AI Apertus model
to generate structured Gantt project plans from business descriptions.
"""

import json
import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class SwissAIGanttPlanner:
    """SwissAI Gantt Planner using Apertus-8B-Instruct model via Public AI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the planner with Public AI API settings."""
        if api_key is None:
            api_key = os.getenv("PUBLIC_AI_API_KEY")
        
        if not api_key:
            raise ValueError("PUBLIC_AI_API_KEY environment variable is required or provide api_key parameter")
        
        self.api_key = api_key
        self.api_url = "https://api.publicai.co/v1/chat/completions"
        self.model = "swiss-ai/apertus-8b-instruct"
    
    def generate_gantt_plan(self, description: str, project_name: Optional[str] = None) -> dict:
        """Generate a Gantt plan from a business description."""
        
        # Create a detailed prompt with schema information
        schema_description = """
Expected JSON Schema Structure:

GanttResponse:
- success: boolean
- gantt_plan: GanttPlan object
- metadata: dict

GanttPlan:
- confidence: float (0.0-1.0)
- project_name: string
- project_description: string
- project_owner: string
- project_start_date: string (YYYY-MM-DD format)
- project_end_date: string (YYYY-MM-DD format)
- total_duration_weeks: integer
- tasks: array of Task objects
- milestones: array of Milestone objects
- phases: array of strings
- budget_estimate: float
- risk_factors: array of strings
- success_metrics: array of strings
- metadata: dict

Task:
- id: string
- name: string (not task_name)
- description: string
- start_date: string (YYYY-MM-DD format)
- end_date: string (YYYY-MM-DD format)
- duration_days: integer
- dependencies: array of strings (task IDs)
- priority: string ("high", "medium", "low")
- status: string
- progress_percentage: integer (0-100)
- assigned_to: array of strings
- resources: array of strings
- tags: array of strings
- estimated_effort_hours: integer

Milestone:
- id: string
- name: string (not milestone_name)
- description: string
- due_date: string (YYYY-MM-DD format)
- success_criteria: array of strings

IMPORTANT: Use exact field names as specified above. Use 'name' not 'task_name' or 'milestone_name'.
"""

        messages = [
            {"role": "system", "content": f"""You are an AI project planner. Given a business plan description, generate a structured Gantt project plan as JSON strictly matching the schema below.

{schema_description}

Return ONLY valid JSON matching this exact schema with all required fields. Use the field names exactly as specified."""},
            {"role": "user", "content": f"Create a detailed Gantt project plan for this business description: {description}\n\n{f'Project name should be: {project_name}' if project_name else ''}\n\nGenerate a complete JSON response following the exact schema structure provided in the system message. Ensure all required fields are included with appropriate values."}
        ]

        print(f"Making API call to {self.model}...")
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "CulturalAgentAI-Gantt/1.0"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.0,
                "max_tokens": 4000
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            resp_data = response.json()
            print("API call successful!")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except Exception as e:
            raise Exception(f"API call failed: {e}")

        # Parse response
        try:
            json_text = resp_data["choices"][0]["message"]["content"]
            
            # Clean up the response - remove markdown code blocks if present
            if json_text.startswith('```json'):
                json_text = json_text[7:]  # Remove ```json
            if json_text.startswith('```'):
                json_text = json_text[3:]   # Remove ```
            if json_text.endswith('```'):
                json_text = json_text[:-3]  # Remove trailing ```
            json_text = json_text.strip()
            
            data = json.loads(json_text)
            return data
            
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing failed: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {e}")
        except Exception as e:
            raise Exception(f"Response processing failed: {e}")


def create_planner(api_key: Optional[str] = None) -> SwissAIGanttPlanner:
    """Factory function to create a SwissAI Gantt Planner instance."""
    return SwissAIGanttPlanner(api_key=api_key)