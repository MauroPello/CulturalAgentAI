import type { Task } from "./plan"

export interface Message {
  content: string
  role: "user" | "assistant" | "system"
}

export interface ChatCompletionResponse {
  choices: Array<{
    message: {
      role: string
      content: string
    }
    finish_reason: string
  }>
  usage: {
    total_tokens: number
  }
  model: string
}

export interface Chat {
  id: number
  title: string
  messages: Message[]
}

export interface GanttPlanResponse {
  success: boolean
  gantt_plan?: {
    project_name: string
    project_description: string
    tasks: Array<Task>
  }
  error?: string
  processing_time_seconds: number
  timestamp: string
}
