import os
import requests
from typing import List, Dict, Optional

class PublicAIClient:
    def __init__(self, api_key: str = None, base_url: str = "https://api.publicai.co/v1"):
        if api_key is None:
            api_key = os.getenv("PUBLIC_AI_KEY")
        if api_key is None:
            raise ValueError("API key not provided and PUBLIC_AI_KEY environment variable not set")
        
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        
        # Debug: Check if API key looks valid
        if not api_key.startswith(('zpka_', 'sk-')):
            print(f"⚠️  Warning: API key format doesn't match expected patterns. Key starts with: {api_key[:10]}...")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "swiss-ai/apertus-8b-instruct",  # MANDATORY: Must use apertus
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: bool = False
    ) -> Dict:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages
        }
        
        # Add optional parameters if provided
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if stream:
            payload["stream"] = stream

        try:
            print(f"🔄 Making API request to: {url}")
            print(f"📦 Model: {model}")
            print(f"📝 Messages: {len(messages)} messages")
            print(f"🔑 API Key starts with: {self.api_key[:15]}...")
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=120)
            
            print(f"📊 Response status: {response.status_code}")
            
            if not response.ok:
                print(f"❌ Error response: {response.text}")
                try:
                    error_json = response.json()
                    print(f"📄 Error details: {error_json}")
                except:
                    pass
                
            response.raise_for_status()
            result = response.json()
            print(f"✅ API call successful")
            return result
            
        except requests.RequestException as e:
            print(f"❌ Error making API request: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"📄 Error response body: {e.response.text}")
            raise

    def simple_chat(self, user_message: str, model: str = "swiss-ai/apertus-8b-instruct") -> str:
        messages = [{"role": "user", "content": user_message}]
        try:
            response = self.chat_completion(messages, model)
            
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                print(f"⚠️  Unexpected response format: {response}")
                raise ValueError("Unexpected response format")
        except Exception as e:
            print(f"❌ Simple chat error: {e}")
            raise
        
def get_public_ai_client() -> PublicAIClient:
    return PublicAIClient()

class LLMService:
    def __init__(self, api_key: str, model: str = "swiss-ai/apertus-8b-instruct"):
        self.client = PublicAIClient(api_key=api_key)
        self.model = model
        self.total_tokens_used = 0
    
    async def generate(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.1,
        system_prompt: Optional[str] = None
    ) -> dict:
        """Generate response from LLM API"""
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Make the API call (synchronous, but we'll wrap it for async compatibility)
            response = self.client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract response text
            if "choices" in response and len(response["choices"]) > 0:
                text = response["choices"][0]["message"]["content"]
                
                # Track token usage if available
                tokens_used = response.get("usage", {}).get("total_tokens", 0)
                self.total_tokens_used += tokens_used
                
                return {
                    "text": text,
                    "tokens_used": tokens_used,
                    "full_response": response
                }
            else:
                raise ValueError("Unexpected response format from PublicAI API")
                
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    async def generate_with_messages(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.1
    ) -> dict:
        """Generate response using message format directly"""
        try:
            response = self.client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            if "choices" in response and len(response["choices"]) > 0:
                text = response["choices"][0]["message"]["content"]
                tokens_used = response.get("usage", {}).get("total_tokens", 0)
                self.total_tokens_used += tokens_used
                
                return {
                    "text": text,
                    "tokens_used": tokens_used,
                    "full_response": response
                }
            else:
                raise ValueError("Unexpected response format from PublicAI API")
                
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    def get_total_tokens_used(self) -> int:
        """Get total tokens used in this session"""
        return self.total_tokens_used
    
    def reset_token_counter(self):
        """Reset the token counter"""
        self.total_tokens_used = 0