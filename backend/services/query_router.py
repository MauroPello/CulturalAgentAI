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
        
        # Keywords for quick pre-analysis - more specific patterns
        self.temporal_keywords = [
            'latest', 'current', 'recent', 'today', 'now', 'breaking',
            'updated', 'new', 'fresh', 'live', 'real-time', 'yesterday',
            'this week', 'this month', 'this year', '2025', '2024',
            'just happened', 'happening now', 'trending', 'news'
        ]
        
        self.internal_keywords = [
            'our company', 'my document', 'our document', 'our file', 'our report', 
            'my file', 'my report', 'company document', 'internal document',
            'uploaded file', 'saved document', 'stored file', 'project file',
            'company data', 'internal data', 'our database', 'our system'
        ]
        
        # Strong temporal patterns (regex)
        self.temporal_patterns = [
            r'\b(what\'?s|what is) (new|latest|happening|current)',
            r'\b(today\'?s|this (week|month|year)\'?s)',
            r'\b(current|latest|recent) (news|updates|developments)',
            r'\b(breaking|live|real-time)',
            r'\b(just (happened|released|announced))',
        ]
        
        # Strong internal patterns (regex)  
        self.internal_patterns = [
            r'\b(our|my) (document|file|report|data|system)',
            r'\b(company|internal|organization) (document|file|data)',
            r'\b(uploaded|saved|stored) (document|file)',
            r'\b(find|show|search) (my|our) ',
            r'\b(in (our|my|the) (database|system|files))',
        ]
    
    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Enhanced query analysis with improved rule-based logic and LLM backup"""
        
        # First, try robust rule-based analysis
        rule_based_analysis = await self._rule_based_analysis(query)
        
        # If confidence is high enough, use rule-based result
        if rule_based_analysis.confidence >= 7.5:  # Increased threshold
            return rule_based_analysis
        
        # Otherwise, try LLM analysis as enhancement
        try:
            llm_analysis = await self._llm_analysis(query, rule_based_analysis)
            
            # Validate LLM analysis makes sense
            if self._validate_analysis(llm_analysis, rule_based_analysis):
                return llm_analysis
            else:
                # LLM analysis doesn't make sense, use rule-based
                return rule_based_analysis
                
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return rule_based_analysis

    async def _rule_based_analysis(self, query: str) -> QueryAnalysis:
        """Improved rule-based query analysis"""
        query_lower = query.lower()
        
        # Calculate scores using both keywords and patterns
        temporal_score = self._calculate_temporal_score(query_lower)
        internal_score = self._calculate_internal_score(query_lower)
        
        # Get context from RAG
        rag_similarity = await self.rag_service.quick_search(query) or 0.0
        
        # Enhanced decision logic
        if temporal_score >= 1 and internal_score >= 1:
            # Mixed signals -> HYBRID (prioritize this check first)
            return QueryAnalysis(
                strategy=SearchStrategy.HYBRID,
                confidence=7.0 + min(temporal_score + internal_score, 3.0) * 0.5,
                reasoning=f"Mixed indicators: temporal ({temporal_score}) + internal ({internal_score})",
                key_factors=["mixed_signals", "hybrid_needed"],
                temporal_indicators=self._get_temporal_matches(query_lower),
                internal_references=self._get_internal_matches(query_lower)
            )
        elif temporal_score >= 2 and internal_score <= 0:
            # Strong temporal signals, no internal signals -> WEB
            return QueryAnalysis(
                strategy=SearchStrategy.WEB,
                confidence=8.0 + min(temporal_score * 0.5, 2.0),
                reasoning=f"Strong temporal indicators detected (score: {temporal_score})",
                key_factors=["high_temporal_score", "no_internal_signals"],
                temporal_indicators=self._get_temporal_matches(query_lower),
                internal_references=self._get_internal_matches(query_lower)
            )
        elif internal_score >= 2 and temporal_score <= 0:
            # Strong internal signals, no temporal signals -> RAG
            confidence = 8.0 + min(internal_score * 0.5, 2.0)
            if rag_similarity > 0.3:  # Boost confidence if RAG has relevant content
                confidence += 1.0
                
            return QueryAnalysis(
                strategy=SearchStrategy.RAG,
                confidence=confidence,
                reasoning=f"Strong internal document indicators detected (score: {internal_score})",
                key_factors=["high_internal_score", "no_temporal_signals"],
                temporal_indicators=self._get_temporal_matches(query_lower),
                internal_references=self._get_internal_matches(query_lower)
            )
        elif self._is_factual_question(query_lower):
            # Simple factual questions -> DIRECT
            return QueryAnalysis(
                strategy=SearchStrategy.DIRECT,
                confidence=8.0,
                reasoning="Simple factual question that can be answered directly",
                key_factors=["factual_question", "no_external_data_needed"],
                temporal_indicators=self._get_temporal_matches(query_lower),
                internal_references=self._get_internal_matches(query_lower)
            )
        else:
            # Ambiguous -> Try RAG first if there's similarity, otherwise DIRECT
            if rag_similarity > 0.2:
                return QueryAnalysis(
                    strategy=SearchStrategy.RAG,
                    confidence=6.0,
                    backup_strategy=SearchStrategy.DIRECT,
                    reasoning="Ambiguous query but RAG has some relevant content",
                    key_factors=["ambiguous", "rag_similarity"],
                    temporal_indicators=self._get_temporal_matches(query_lower),
                    internal_references=self._get_internal_matches(query_lower)
                )
            else:
                return QueryAnalysis(
                    strategy=SearchStrategy.DIRECT,
                    confidence=6.0,
                    backup_strategy=SearchStrategy.WEB,
                    reasoning="Ambiguous query with no clear indicators",
                    key_factors=["ambiguous", "default_choice"],
                    temporal_indicators=self._get_temporal_matches(query_lower),
                    internal_references=self._get_internal_matches(query_lower)
                )

    def _calculate_temporal_score(self, query_lower: str) -> float:
        """Calculate temporal relevance score"""
        score = 0.0
        
        # Check keywords
        for keyword in self.temporal_keywords:
            if keyword.lower() in query_lower:
                score += 1.0
        
        # Check patterns (stronger signal)
        for pattern in self.temporal_patterns:
            if re.search(pattern, query_lower):
                score += 2.0
        
        return score
    
    def _calculate_internal_score(self, query_lower: str) -> float:
        """Calculate internal document relevance score"""
        score = 0.0
        
        # Check keywords  
        for keyword in self.internal_keywords:
            if keyword.lower() in query_lower:
                score += 1.0
        
        # Check patterns (stronger signal)
        for pattern in self.internal_patterns:
            if re.search(pattern, query_lower):
                score += 2.0
        
        return score
    
    def _get_temporal_matches(self, query_lower: str) -> List[str]:
        """Get temporal keywords/patterns that matched"""
        matches = []
        for keyword in self.temporal_keywords:
            if keyword.lower() in query_lower:
                matches.append(keyword)
        return matches
    
    def _get_internal_matches(self, query_lower: str) -> List[str]:
        """Get internal keywords/patterns that matched"""
        matches = []
        for keyword in self.internal_keywords:
            if keyword.lower() in query_lower:
                matches.append(keyword)
        return matches
    
    def _is_factual_question(self, query_lower: str) -> bool:
        """Detect simple factual questions"""
        factual_patterns = [
            r'\bwhat is\b',
            r'\bwho is\b', 
            r'\bwhen was\b',
            r'\bwhere is\b',
            r'\bhow to\b',
            r'\bdefine\b',
            r'\bexplain\b',
            r'\bcapital of\b',
            r'\bpopulation of\b',
            r'\bhistory of\b'
        ]
        
        return any(re.search(pattern, query_lower) for pattern in factual_patterns)
    
    async def _llm_analysis(self, query: str, rule_based: QueryAnalysis) -> QueryAnalysis:
        """LLM-enhanced analysis with better prompt and validation"""
        
        system_prompt = """You are an expert query analyzer. Respond in the EXACT format requested."""
        
        analysis_prompt = f"""
        Analyze this query for the best search strategy. Base your analysis on the patterns you see.
        
        Query: "{query}"
        
        Rule-based analysis suggests: {rule_based.strategy} (confidence: {rule_based.confidence:.1f})
        Reasoning: {rule_based.reasoning}
        
        Choose the BEST strategy:
        - RAG: For questions about internal documents, company data, uploaded files
        - WEB: For current events, latest news, real-time information  
        - DIRECT: For general knowledge, definitions, simple facts
        - HYBRID: When both internal and current information needed
        
        Respond in this EXACT format:
        STRATEGY: [RAG|WEB|DIRECT|HYBRID]
        CONFIDENCE: [1-10]
        REASONING: [One clear sentence why this strategy is best]
        """
        
        response = await self.llm_service.generate(
            analysis_prompt,
            max_tokens=200,
            temperature=0.1,
            system_prompt=system_prompt
        )
        
        return self._parse_llm_response(response.get('text', ''), rule_based)
    
    def _parse_llm_response(self, response_text: str, rule_based: QueryAnalysis) -> QueryAnalysis:
        """Parse LLM response with better error handling"""
        try:
            strategy_match = re.search(r'STRATEGY:\s*(\w+)', response_text)
            confidence_match = re.search(r'CONFIDENCE:\s*(\d+)', response_text)
            reasoning_match = re.search(r'REASONING:\s*([^\n]+)', response_text)
            
            if not all([strategy_match, confidence_match]):
                return rule_based
            
            strategy_str = strategy_match.group(1)
            if strategy_str not in ['RAG', 'WEB', 'DIRECT', 'HYBRID']:
                return rule_based
            
            strategy = SearchStrategy(strategy_str)
            confidence = float(confidence_match.group(1))
            reasoning = reasoning_match.group(1).strip() if reasoning_match else "LLM analysis"
            
            return QueryAnalysis(
                strategy=strategy,
                confidence=min(confidence, 10.0),
                reasoning=reasoning,
                key_factors=["llm_analysis"] + rule_based.key_factors,
                temporal_indicators=rule_based.temporal_indicators,
                internal_references=rule_based.internal_references
            )
        
        except Exception as e:
            print(f"Failed to parse LLM response: {e}")
            return rule_based
    
    def _validate_analysis(self, llm_analysis: QueryAnalysis, rule_based: QueryAnalysis) -> bool:
        """Validate that LLM analysis makes sense compared to rule-based"""
        
        # If rule-based confidence is very high and strategies differ significantly, be suspicious
        if rule_based.confidence >= 8.5 and llm_analysis.strategy != rule_based.strategy:
            # Check if the difference makes sense
            if rule_based.strategy == SearchStrategy.WEB and llm_analysis.strategy == SearchStrategy.DIRECT:
                # Suspicious: rule-based found strong temporal signals but LLM suggests DIRECT
                return False
            elif rule_based.strategy == SearchStrategy.RAG and llm_analysis.strategy == SearchStrategy.DIRECT:
                # Suspicious: rule-based found strong internal signals but LLM suggests DIRECT  
                return False
        
        # LLM confidence should be reasonable
        if llm_analysis.confidence > 10.0 or llm_analysis.confidence < 1.0:
            return False
        
        return True
    
    async def _fallback_analysis(self, query: str, temporal_found: List[str], internal_found: List[str], rag_similarity: float) -> QueryAnalysis:
        """Legacy fallback - now just calls the new rule-based analysis"""
        return await self._rule_based_analysis(query)
    
    async def execute_search(self, query: str, analysis: QueryAnalysis) -> Tuple[List[SearchResult], SearchStrategy]:
        """Execute the search strategy"""
        
        strategy = analysis.strategy
        results = []
        
        try:
            if strategy == SearchStrategy.RAG:
                print("Executing RAG search...")
                results = await self.rag_service.search(query)
                
            elif strategy == SearchStrategy.WEB:
                print("Executing Web search...")
                results = await self.web_search_service.search(query)
                
            elif strategy == SearchStrategy.HYBRID:
                # Execute both searches in parallel
                print("Executing Hybrid search (RAG + Web)...")
                rag_task = self.rag_service.search(query)
                web_task = self.web_search_service.search(query)
                
                rag_results, web_results = await asyncio.gather(rag_task, web_task, return_exceptions=True)
                
                # Handle potential exceptions
                if not isinstance(rag_results, Exception):
                    results.extend(rag_results)
                if not isinstance(web_results, Exception):
                    results.extend(web_results)
                    
            elif strategy == SearchStrategy.DIRECT:
                print("No search needed, using Direct response.")
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