"""
SwissAI Gantt Planner Core Functionality

This module handles the interaction with the Swiss AI Platform Apertus-70B model
to generate structured Gantt project plans from business descriptions.
"""

import json
import os
import openai
from typing import Optional
from dotenv import load_dotenv
from gantt.models import GanttPlan
from pydantic import TypeAdapter, ValidationError

load_dotenv()

class SwissAIGanttPlanner:
    """SwissAI Gantt Planner using Apertus-70B model via Swiss AI Platform."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the planner with Swiss AI Platform API settings."""
        if api_key is None:
            api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")

        if not api_key:
            raise ValueError("SWISS_AI_PLATFORM_API_KEY environment variable is required or provide api_key parameter")

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
        )
        self.model = "swiss-ai/Apertus-70B"
        self.gantt_plan_adapter = TypeAdapter(GanttPlan)

    def _parse_and_validate_gantt_plan(self, json_text: str) -> GanttPlan:
        """Parse and validate the JSON output against the GanttPlan model."""
        try:
            # Clean up the response
            if json_text.startswith('```json'):
                json_text = json_text[7:]
            if json_text.startswith('```'):
                json_text = json_text[3:]
            if json_text.endswith('```'):
                json_text = json_text[:-3]
            json_text = json_text.strip()

            # Validate and parse the JSON using the TypeAdapter
            validated_plan = self.gantt_plan_adapter.validate_json(json_text)
            return validated_plan

        except ValidationError as e:
            raise e  # Re-raise validation errors to be handled by the caller
        except json.JSONDecodeError as e:
            raise ValidationError.from_exception_data(
                title="JSONDecodeError",
                line_errors=[{"error": str(e), "loc": ("body",)}]
            )

    def generate_gantt_plan(self, description: str, project_name: Optional[str] = None, max_retries: int = 3) -> dict:
        """Generate a Gantt plan from a business description with validation and retries."""

        schema_description = self.gantt_plan_adapter.json_schema()

        messages = [
            {"role": "system", "content": f"""You are an AI project planner. Given a business plan description, generate a structured Gantt project plan as JSON strictly matching the schema below.

{json.dumps(schema_description, indent=2)}

Return ONLY valid JSON matching this exact schema with all required fields. Use the field names exactly as specified."""},
            {"role": "user", "content": f"Create a detailed Gantt project plan for this business description: {description}\n\n{f'Project name should be: {project_name}' if project_name else ''}\n\nGenerate a complete JSON response following the exact schema structure provided in the system message. Ensure all required fields are included with appropriate values."}
        ]

        for attempt in range(max_retries):
            print(f"Making API call to {self.model} (Attempt {attempt + 1}/{max_retries})...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )

                json_text = response.choices[0].message.content

                # Validate the response
                validated_plan = self._parse_and_validate_gantt_plan(json_text)
                print("API call and validation successful!")
                return validated_plan.model_dump()

            except ValidationError as e:
                print(f"Validation failed on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    # Add the error to the chat history to guide the next attempt
                    error_feedback = f"The previous JSON was invalid. Please correct it. Errors:\n{e}"
                    messages.append({"role": "assistant", "content": json_text})
                    messages.append({"role": "user", "content": error_feedback})
                    print("Retrying with corrective feedback...")
                else:
                    raise Exception(f"Failed to generate a valid Gantt plan after {max_retries} attempts. Last error: {e}")

            except Exception as e:
                raise Exception(f"API call or processing failed: {e}")

        raise Exception("Failed to generate a valid Gantt plan.")

    def modify_gantt_plan(self, existing_plan: dict, prompt: str, max_retries: int = 3) -> dict:
        """Modify an existing Gantt plan based on a prompt with validation and retries."""

        schema_description = self.gantt_plan_adapter.json_schema()

        messages = [
            {"role": "system", "content": f"""You are an AI project planner. Given an existing Gantt project plan and modification instructions, generate an updated Gantt project plan as JSON strictly matching the schema below.

{json.dumps(schema_description, indent=2)}

Return ONLY valid JSON matching this exact schema with all required fields. Use the field names exactly as specified. Make sure to preserve the existing structure and data while applying the requested modifications."""},
            {"role": "user", "content": f"""Here is the existing Gantt project plan:
{json.dumps(existing_plan, indent=2)}

Please modify this plan according to these instructions: {prompt}

Generate the complete updated JSON response following the exact schema structure provided in the system message. Ensure all required fields are included and the modifications are properly applied while maintaining data consistency."""}
        ]

        for attempt in range(max_retries):
            print(f"Making API call to {self.model} for plan modification (Attempt {attempt + 1}/{max_retries})...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )

                json_text = response.choices[0].message.content

                # Validate the response
                validated_plan = self._parse_and_validate_gantt_plan(json_text)
                print("API call and validation successful!")
                return validated_plan.model_dump()

            except ValidationError as e:
                print(f"Validation failed on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    # Add error feedback for the next attempt
                    error_feedback = f"The previous JSON was invalid. Please correct it. Errors:\n{e}"
                    messages.append({"role": "assistant", "content": json_text})
                    messages.append({"role": "user", "content": error_feedback})
                    print("Retrying with corrective feedback...")
                else:
                    raise Exception(f"Failed to generate a valid modified Gantt plan after {max_retries} attempts. Last error: {e}")

            except Exception as e:
                raise Exception(f"API call or processing failed: {e}")

        raise Exception("Failed to generate a valid modified Gantt plan.")


def create_planner(api_key: Optional[str] = None) -> SwissAIGanttPlanner:
    """Factory function to create a SwissAI Gantt Planner instance."""
    return SwissAIGanttPlanner(api_key=api_key)