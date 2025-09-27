"""
Pydantic models for SwissAI Gantt Planner API
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    """Task model for Gantt planning."""
    id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    start_date: str = Field(..., description="Task start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Task end date (YYYY-MM-DD)")
    dependencies: List[str] = Field(default=[], description="List of dependent task IDs")
    status: str = Field(..., description="Task status")
    progress: int = Field(..., ge=0, le=100, description="Task progress percentage")
    assignee: str = Field(default="", description="Assigned team member")


class GanttPlan(BaseModel):
    """Complete Gantt plan model."""
    id: str = Field(..., description="Unique project identifier")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Plan confidence score")
    project_name: str = Field(..., description="Project name")
    project_description: str = Field(..., description="Project description")
    tasks: List[Task] = Field(..., description="List of project tasks")


class GanttResponse(BaseModel):
    """Complete API response model."""
    success: bool = Field(..., description="Response success status")
    gantt_plan: Optional[GanttPlan] = Field(None, description="Generated Gantt plan")
    metadata: Dict[str, Any] = Field(default={}, description="Response metadata")


# API Request/Response Models
class GanttRequest(BaseModel):
    """API request model for Gantt plan generation."""
    description: str = Field(..., min_length=10, description="Business plan description")
    project_name: Optional[str] = Field(None, description="Optional project name")


class ModifyGanttRequest(BaseModel):
    """API request model for modifying an existing Gantt plan."""
    gantt_plan: Dict[str, Any] = Field(..., description="Existing Gantt plan data to modify")
    prompt: str = Field(..., min_length=5, description="Modification instructions or prompt")


class APIGanttResponse(BaseModel):
    """API response model."""
    success: bool = Field(..., description="Request success status")
    gantt_plan: Optional[Dict[str, Any]] = Field(None, description="Generated Gantt plan data")
    error: Optional[str] = Field(None, description="Error message if request failed")
    processing_time_seconds: Optional[float] = Field(None, description="Request processing time")
    api_version: str = Field(default="1.0.0", description="API version")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Response timestamp")