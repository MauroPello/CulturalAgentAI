import requests
import json
import os
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
            "User-Agent": "CulturalAgentAI/1.0"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "swiss-ai/apertus-8b-instruct",
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
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            raise
    
    def simple_chat(self, user_message: str, model: str = "swiss-ai/apertus-8b-instruct") -> str:
        messages = [{"role": "user", "content": user_message}]
        response = self.chat_completion(messages, model)
        
        # Extract the content from the response
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise ValueError("Unexpected response format")


def get_public_ai_client() -> PublicAIClient:
    return PublicAIClient()


# Example usage
if __name__ == "__main__":
    # Initialize the client (will automatically read from PUBLIC_AI_KEY environment variable)
    client = PublicAIClient()
    
    try:
        # Example 1: Simple chat
        response_text = client.simple_chat("Hello! Can you help me understand open-source AI?")
        print("Response:", response_text)
        
        # Example 2: More complex chat with conversation history
        messages = [
            {"role": "user", "content": "Hello! Can you help me understand open-source AI?"},
            {"role": "assistant", "content": "Hello! I'd be happy to help you understand open-source AI..."},
            {"role": "user", "content": "What are some popular open-source AI models?"}
        ]
        
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        print("\nFull response:")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
