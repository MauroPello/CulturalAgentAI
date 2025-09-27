/**
 * Centralized API service for the CulturalAgentAI frontend
 * Handles all backend communication with proper error handling and type safety
 */

// API Types matching backend schemas
export enum SearchStrategy {
  RAG = "RAG",
  WEB = "WEB", 
  DIRECT = "DIRECT",
  HYBRID = "HYBRID"
}

export interface QueryAnalysis {
  strategy: SearchStrategy
  confidence: number
  backup_strategy?: SearchStrategy
  reasoning: string
  key_factors: string[]
  temporal_indicators: string[]
  internal_references: string[]
}

export interface SearchResult {
  source: string  // "rag", "web", "direct"
  title?: string
  content: string
  url?: string
  relevance_score?: number
}

export interface IntelligentSearchRequest {
  query: string
  user_id?: string
  session_id?: string
  force_strategy?: SearchStrategy
}

export interface IntelligentSearchResponse {
  query: string
  strategy_used: SearchStrategy
  confidence: number
  answer: string
  sources: SearchResult[]
  analysis: QueryAnalysis
  execution_time: number
  tokens_used: number
}

interface ProcessDocumentsResponse {
  message: string
  processed_files: Array<{
    file_id: string
    filename: string
    chunks_added: number
  }>
  errors: Array<{
    filename: string
    error: string
  }>
  total_chunks_added: number
  total_documents_in_store: number
}

interface UploadedFile {
  filename: string
  file_size: number
  upload_time: number
  file_path: string
  file_type: string
}

interface UploadedFilesResponse {
  message: string
  files: UploadedFile[]
  total_files: number
}

interface CulturalAlignRequest {
  text: string
  target_culture: string
  language: string
}

interface CulturalAlignResponse {
  text: string
  target_culture: string
  language: string
  better_version: string
}

interface GanttRequest {
  description: string
  project_name?: string
}

interface GanttResponse {
  success: boolean
  gantt_plan?: any
  error?: string
  processing_time_seconds: number
  timestamp: string
}

class ApiService {
  private baseURL: string

  constructor() {
    // Use a simple approach that works in all contexts
    if (typeof window !== 'undefined') {
      // Client-side: use environment variable or default
      this.baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    } else {
      // Server-side: try to get from runtime config or use default
      try {
        const config = useRuntimeConfig()
        this.baseURL = (config.public?.apiBase as string) || 'http://localhost:8000'
      } catch {
        this.baseURL = 'http://localhost:8000'
      }
    }
  }

  private async makeRequest<T>(
    endpoint: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
      body?: string | FormData
      headers?: Record<string, string>
    } = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    try {
      // For FormData, don't set Content-Type header
      const headers = options.body instanceof FormData 
        ? options.headers || {}
        : {
            'Content-Type': 'application/json',
            ...options.headers,
          }

      const response = await $fetch(url, {
        method: options.method || 'GET',
        body: options.body,
        headers,
      }) as T
      
      return response
    } catch (error: any) {
      console.error(`API Error [${endpoint}]:`, error)
      
      // Handle different types of errors
      if (error.data) {
        // Server responded with error status
        throw new Error(error.data.detail || error.statusText || 'Server error')
      } else {
        // Network or other error
        throw new Error(error.message || 'Network error: Unable to connect to server')
      }
    }
  }

  // Health check
  async healthCheck(): Promise<{ message: string }> {
    return this.makeRequest('/')
  }

  // Intelligent search/ask endpoint
  async ask(request: IntelligentSearchRequest): Promise<IntelligentSearchResponse> {
    return this.makeRequest<IntelligentSearchResponse>('/ask', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Document processing
  async processDocuments(files: File[]): Promise<ProcessDocumentsResponse> {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    return this.makeRequest<ProcessDocumentsResponse>('/process-documents/', {
      method: 'POST',
      body: formData,
    })
  }

  // Get uploaded files
  async getUploadedFiles(): Promise<UploadedFilesResponse> {
    return this.makeRequest<UploadedFilesResponse>('/uploaded-files')
  }

  // Delete document
  async deleteDocument(filename: string): Promise<{ message: string, filename: string }> {
    return this.makeRequest<{ message: string, filename: string }>(`/delete-document/${encodeURIComponent(filename)}`, {
      method: 'DELETE',
    })
  }

  // Clear library
  async clearLibrary(): Promise<{ message: string, total_deleted: number }> {
    return this.makeRequest<{ message: string, total_deleted: number }>('/clear-library', {
      method: 'DELETE',
    })
  }

  // Cultural alignment
  async culturalAlignText(request: CulturalAlignRequest): Promise<CulturalAlignResponse> {
    return this.makeRequest<CulturalAlignResponse>('/cultural_align_text/', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Gantt chart conversion
  async convertToGantt(request: GanttRequest): Promise<GanttResponse> {
    return this.makeRequest<GanttResponse>('/convert', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }
}

// Global API service instance (singleton)
let apiServiceInstance: ApiService | null = null

// Composable to use the API service
export const useApi = () => {
  // Create singleton instance
  if (!apiServiceInstance) {
    apiServiceInstance = new ApiService()
  }

  return {
    api: apiServiceInstance,
    
    // Convenience method for making API calls with reactive state
    useAsyncApi: <T>(apiCall: () => Promise<T>) => {
      const data = ref<T | null>(null)
      const error = ref<string | null>(null)
      const pending = ref(false)

      const execute = async () => {
        pending.value = true
        error.value = null
        
        try {
          data.value = await apiCall()
        } catch (err) {
          error.value = err instanceof Error ? err.message : 'Unknown error'
          console.error('API Error:', err)
        } finally {
          pending.value = false
        }
      }

      return {
        data: readonly(data),
        error: readonly(error), 
        pending: readonly(pending),
        execute
      }
    }
  }
}

// Simplified utility functions for common operations
export const useApiCall = () => {
  const { api } = useApi()

  return {
    // Simple ask function
    async ask(query: string): Promise<IntelligentSearchResponse> {
      return api.ask({ query })
    },

    // Upload documents
    async uploadDocuments(files: File[]): Promise<ProcessDocumentsResponse> {
      return api.processDocuments(files)
    },

    // Get files
    async getFiles(): Promise<UploadedFilesResponse> {
      return api.getUploadedFiles()
    },

    // Delete document
    async deleteDocument(filename: string): Promise<{ message: string, filename: string }> {
      return api.deleteDocument(filename)
    },

    // Clear library
    async clearLibrary(): Promise<{ message: string, total_deleted: number }> {
      return api.clearLibrary()
    },

    // Generate Gantt chart
    async generateGantt(description: string, projectName?: string): Promise<GanttResponse> {
      return api.convertToGantt({ description, project_name: projectName })
    },

    // Cultural alignment
    async alignText(text: string, culture: string, language: string): Promise<CulturalAlignResponse> {
      return api.culturalAlignText({ text, target_culture: culture, language })
    }
  }
}