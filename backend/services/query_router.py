import re
import asyncio
from typing import List, Tuple
from models.schemas import *
from services.llm_services import LLMService
from services.rag_service import RAGService
from services.web_search_service import WebSearchService

class QueryRouter:
    def __init__(
        self, 
        llm_service: LLMService,
        rag_service: RAGService,
        web_search_service: WebSearchService,
        confidence_threshold: float = 7.0
    ):
        self.llm_service = llm_service
        self.rag_service = rag_service
        self.web_search_service = web_search_service
        self.confidence_threshold = confidence_threshold
        
        # Keywords for quick pre-analysis
        self.temporal_keywords = [
            'latest', 'current', 'recent', 'today', 'now', 'breaking',
            'updated', 'new', 'fresh', 'live', 'real-time', 'yesterday',
            'this week', 'this month', 'this year', '2025', '2024'
        ]
        
        self.internal_keywords = [
            'our', 'my', 'document', 'file', 'report', 'project',
            'internal', 'company', 'team', 'organization', 'we',
            'uploaded', 'saved', 'stored'
        ]
    
    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Sophisticated query analysis using LLM"""
        
        # Quick keyword analysis for context
        temporal_found = [kw for kw in self.temporal_keywords if kw.lower() in query.lower()]
        internal_found = [kw for kw in self.internal_keywords if kw.lower() in query.lower()]
        
        # Get RAG similarity preview
        rag_similarity = await self.rag_service.quick_search(query) or 0.0
        
        system_prompt = """You are an expert at analyzing search queries to determine the best information retrieval strategy. You must respond in a specific format that can be parsed programmatically."""
        
        analysis_prompt = f"""
        Analyze this query to determine the best information retrieval strategy:
        
        Query: "{query}"
        
        Context Information:
        - Temporal keywords found: {temporal_found}
        - Internal reference keywords found: {internal_found}  
        - RAG similarity preview: {rag_similarity:.2f}
        
        Evaluation Framework:
        
        1. Information Type Analysis:
           - Is this asking for current/time-sensitive information?
           - Does it reference internal documents or company-specific data?
           - Is it a general knowledge question?
           - Does it require combining multiple information sources?
        
        2. Source Requirements:
           - TEMPORAL INDICATORS → Favor WEB search
           - INTERNAL REFERENCES → Favor RAG search  
           - GENERAL KNOWLEDGE → Use DIRECT response
           - COMPLEX/COMPARATIVE → Consider HYBRID approach
        
        3. Decision Tree:
           Step 1: Check for strong temporal signals (current, latest, today, breaking, etc.)
           → If YES and no internal references: WEB (confidence 8-9)
           
           Step 2: Check for internal document references (our, my, document, etc.)  
           → If YES and no temporal signals: RAG (confidence 8-9)
           
           Step 3: Check if it's answerable from general training knowledge
           → If YES and simple factual: DIRECT (confidence 7-8)
           
           Step 4: Check if it needs both current and internal information
           → If YES: HYBRID (confidence 6-7)
           
           Step 5: Default based on strongest signal
        
        4. Confidence Factors:
           - High (8-10): Clear single source needed, strong keyword signals
           - Medium (5-7): Multiple possible sources, moderate signals  
           - Low (1-4): Ambiguous query, weak signals
        
        Provide your analysis in this EXACT format:
        
        PRIMARY_STRATEGY: [RAG|WEB|DIRECT|HYBRID]
        CONFIDENCE: [1-10]
        BACKUP_STRATEGY: [RAG|WEB|DIRECT|HYBRID or NONE]
        REASONING: [2-3 sentences explaining the decision]
        KEY_FACTORS: [factor1, factor2, factor3]
        TEMPORAL_INDICATORS: [{temporal_found}]
        INTERNAL_REFERENCES: [{internal_found}]
        """
        
        try:
            response = await self.llm_service.generate(
                analysis_prompt,
                max_tokens=300,
                temperature=0.1,
                system_prompt=system_prompt
            )
            
            return self._parse_analysis(response.get('text', ''), temporal_found, internal_found)
        
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            # Fallback to rule-based analysis
            return self._fallback_analysis(query, temporal_found, internal_found, rag_similarity)
    
    def _parse_analysis(self, response_text: str, temporal_found: List[str], internal_found: List[str]) -> QueryAnalysis:
        """Parse LLM analysis response"""
        try:
            # Extract information using regex
            strategy_match = re.search(r'PRIMARY_STRATEGY:\s*(\w+)', response_text)
            confidence_match = re.search(r'CONFIDENCE:\s*(\d+)', response_text)
            backup_match = re.search(r'BACKUP_STRATEGY:\s*(\w+)', response_text)
            reasoning_match = re.search(r'REASONING:\s*([^\n]+(?:\n[^\n]+)*?)(?=KEY_FACTORS|$)', response_text)
            factors_match = re.search(r'KEY_FACTORS:\s*\[(.*?)\]', response_text)
            
            strategy = SearchStrategy(strategy_match.group(1)) if strategy_match else SearchStrategy.DIRECT
            confidence = float(confidence_match.group(1)) if confidence_match else 5.0
            backup = SearchStrategy(backup_match.group(1)) if backup_match and backup_match.group(1) != 'NONE' else None
            reasoning = reasoning_match.group(1).strip() if reasoning_match else "Analysis based on keyword patterns"
            
            key_factors = []
            if factors_match:
                factors_text = factors_match.group(1)
                key_factors = [f.strip().strip('"\'') for f in factors_text.split(',')]
            
            return QueryAnalysis(
                strategy=strategy,
                confidence=confidence,
                backup_strategy=backup,
                reasoning=reasoning,
                key_factors=key_factors,
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
        
        except Exception as e:
            print(f"Failed to parse analysis: {e}")
            # If parsing fails, return safe defaults
            return QueryAnalysis(
                strategy=SearchStrategy.HYBRID,
                confidence=5.0,
                reasoning="Failed to parse analysis, using safe default",
                key_factors=["parsing_error"],
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
    
    def _fallback_analysis(self, query: str, temporal_found: List[str], internal_found: List[str], rag_similarity: float) -> QueryAnalysis:
        """Rule-based fallback analysis"""
        
        temporal_score = len(temporal_found)
        internal_score = len(internal_found)
        
        if temporal_score > 0 and internal_score == 0:
            return QueryAnalysis(
                strategy=SearchStrategy.WEB,
                confidence=8.0,
                reasoning="Strong temporal indicators suggest web search needed",
                key_factors=["temporal_keywords", "no_internal_references"],
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
        elif internal_score > 0 and temporal_score == 0:
            return QueryAnalysis(
                strategy=SearchStrategy.RAG,
                confidence=8.0,
                reasoning="Internal references suggest RAG search needed",
                key_factors=["internal_references", "no_temporal_indicators"],
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
        elif temporal_score > 0 and internal_score > 0:
            return QueryAnalysis(
                strategy=SearchStrategy.HYBRID,
                confidence=7.0,
                reasoning="Both temporal and internal indicators present",
                key_factors=["temporal_keywords", "internal_references"],
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
        else:
            return QueryAnalysis(
                strategy=SearchStrategy.DIRECT,
                confidence=6.0,
                reasoning="No strong indicators, using direct response",
                key_factors=["no_clear_signals"],
                temporal_indicators=temporal_found,
                internal_references=internal_found
            )
    
    async def execute_search(self, query: str, analysis: QueryAnalysis) -> Tuple[List[SearchResult], SearchStrategy]:
        """Execute the search strategy"""
        
        strategy = analysis.strategy
        results = []
        
        try:
            if strategy == SearchStrategy.RAG:
                results = await self.rag_service.search(query)
                
            elif strategy == SearchStrategy.WEB:
                results = await self.web_search_service.search(query)
                
            elif strategy == SearchStrategy.HYBRID:
                # Execute both searches in parallel
                rag_task = self.rag_service.search(query)
                web_task = self.web_search_service.search(query)
                
                rag_results, web_results = await asyncio.gather(rag_task, web_task, return_exceptions=True)
                
                # Handle potential exceptions
                if not isinstance(rag_results, Exception):
                    results.extend(rag_results)
                if not isinstance(web_results, Exception):
                    results.extend(web_results)
                    
            elif strategy == SearchStrategy.DIRECT:
                # No external search needed
                results = []
            
            # If primary strategy failed or returned no results, try backup
            if not results and analysis.backup_strategy and analysis.confidence < self.confidence_threshold:
                backup_analysis = QueryAnalysis(
                    strategy=analysis.backup_strategy,
                    confidence=analysis.confidence - 1,
                    reasoning="Trying backup strategy",
                    key_factors=["backup_strategy"]
                )
                results, strategy = await self.execute_search(query, backup_analysis)
            
            return results, strategy
            
        except Exception as e:
            print(f"Search execution failed: {e}")
            # If all else fails, try the most likely alternative
            if strategy != SearchStrategy.DIRECT:
                return [], SearchStrategy.DIRECT
            raise e
    
    async def process_query(self, query: str) -> Tuple[str, List[SearchResult], QueryAnalysis, int]:
        """
        Processes a query from start to finish: analysis, execution, and response generation.
        """
        # 1. Analyze the query
        analysis = await self.analyze_query(query)
        
        # 2. Execute the search based on the analysis
        results, strategy = await self.execute_search(query, analysis)
        
        # 3. Generate the final response
        final_response, tokens_used = await self.generate_final_response(query, results, strategy, analysis)
        
        return final_response, results, analysis, tokens_used

    async def generate_final_response(
        self, 
        query: str, 
        results: List[SearchResult], 
        strategy: SearchStrategy,
        analysis: QueryAnalysis
    ) -> Tuple[str, int]:
        """Generate the final response using LLM"""
        
        context = ""
        if results:
            context = "Retrieved Information:\n"
            for i, result in enumerate(results, 1):
                context += f"{i}. [{result.source.upper()}] {result.title or 'Untitled'}\n"
                context += f"   {result.content[:300]}{'...' if len(result.content) > 300 else ''}\n"
                if result.url:
                    context += f"   Source: {result.url}\n"
                context += "\n"
        
        system_prompt = "You are a helpful AI assistant. Provide comprehensive, accurate answers based on the provided information and your knowledge."
        
        response_prompt = f"""
        Answer the user's query using the provided information and your knowledge.
        
        User Query: "{query}"
        
        Search Strategy Used: {strategy.value}
        Analysis Confidence: {analysis.confidence}/10
        
        {context}
        
        Instructions:
        - Provide a comprehensive, accurate answer
        - If using retrieved information, naturally reference the sources
        - If information is conflicting, mention this
        - If retrieved information is insufficient, supplement with your knowledge
        - Keep the response conversational and helpful
        - Don't mention the technical details of the search process
        
        Answer:
        """
        
        try:
            response = await self.llm_service.generate(
                response_prompt,
                max_tokens=1000,
                temperature=0.3,
                system_prompt=system_prompt
            )
            
            return response.get('text', 'I apologize, but I was unable to generate a proper response.'), response.get('tokens_used', 0)
        
        except Exception as e:
            print(f"Response generation failed: {e}")
            return f"I apologize, but I encountered an error while generating a response: {str(e)}", 0