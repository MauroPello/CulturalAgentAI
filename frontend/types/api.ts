/**
 * TypeScript types for API communication
 * Mirrors the backend schema definitions
 */

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