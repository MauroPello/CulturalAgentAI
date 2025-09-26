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
    duration_days: int = Field(..., description="Task duration in days")
    dependencies: List[str] = Field(default=[], description="List of dependent task IDs")
    priority: str = Field(..., description="Task priority: high, medium, low")
    status: str = Field(..., description="Task status")
    progress_percentage: int = Field(..., ge=0, le=100, description="Task progress percentage")
    assigned_to: List[str] = Field(default=[], description="List of assigned team members")
    resources: List[str] = Field(default=[], description="List of required resources")
    tags: List[str] = Field(default=[], description="List of task tags")
    estimated_effort_hours: int = Field(..., ge=0, description="Estimated effort in hours")


class Milestone(BaseModel):
    """Milestone model for Gantt planning."""
    id: str = Field(..., description="Unique milestone identifier")
    name: str = Field(..., description="Milestone name")
    description: str = Field(..., description="Milestone description")
    due_date: str = Field(..., description="Milestone due date (YYYY-MM-DD)")
    success_criteria: List[str] = Field(default=[], description="List of success criteria")


class GanttPlan(BaseModel):
    """Complete Gantt plan model."""
    confidence: float = Field(..., ge=0.0, le=1.0, description="Plan confidence score")
    project_name: str = Field(..., description="Project name")
    project_description: str = Field(..., description="Project description")
    project_owner: str = Field(..., description="Project owner")
    project_start_date: str = Field(..., description="Project start date (YYYY-MM-DD)")
    project_end_date: str = Field(..., description="Project end date (YYYY-MM-DD)")
    total_duration_weeks: int = Field(..., ge=1, description="Total project duration in weeks")
    tasks: List[Task] = Field(..., description="List of project tasks")
    milestones: List[Milestone] = Field(..., description="List of project milestones")
    phases: List[str] = Field(..., description="List of project phases")
    budget_estimate: float = Field(..., ge=0, description="Estimated project budget")
    risk_factors: List[str] = Field(default=[], description="List of identified risk factors")
    success_metrics: List[str] = Field(default=[], description="List of success metrics")
    metadata: Dict[str, Any] = Field(default={}, description="Additional project metadata")


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


class APIGanttResponse(BaseModel):
    """API response model."""
    success: bool = Field(..., description="Request success status")
    gantt_plan: Optional[Dict[str, Any]] = Field(None, description="Generated Gantt plan data")
    error: Optional[str] = Field(None, description="Error message if request failed")
    processing_time_seconds: Optional[float] = Field(None, description="Request processing time")
    api_version: str = Field(default="1.0.0", description="API version")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Response timestamp")