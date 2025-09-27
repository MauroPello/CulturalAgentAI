#!/usr/bin/env python3
"""
Test script to validate PublicAI API connection and troubleshoot issues
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if API key is properly configured"""
    api_key = os.getenv("PUBLIC_AI_KEY")
    
    if not api_key:
        print("❌ PUBLIC_AI_KEY not found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:15]}...")
    
    if not api_key.startswith(('zpka_', 'sk-')):
        print(f"⚠️  Warning: API key format might be incorrect")
    
    return api_key

def test_api_models():
    """Test what models are available"""
    api_key = test_api_key()
    if not api_key:
        return
    
    print("\n🔍 Testing available models...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try to get models list
        response = requests.get("https://api.publicai.co/v1/models", headers=headers, timeout=10)
        print(f"Models endpoint status: {response.status_code}")
        
        if response.ok:
            models = response.json()
            print("Available models:")
            for model in models.get('data', []):
                print(f"  - {model.get('id', 'Unknown')}")
        else:
            print(f"Models endpoint error: {response.text}")
    
    except Exception as e:
        print(f"Error getting models: {e}")

def test_simple_chat():
    """Test a simple chat completion"""
    api_key = test_api_key()
    if not api_key:
        return
    
    print("\n💬 Testing chat completion...")
    
    # Try different model names - APERTUS IS MANDATORY
    models_to_try = [
        "swiss-ai/apertus-8b-instruct",  # MANDATORY PRIMARY MODEL
        "apertus-8b-instruct",
        "swiss-ai/apertus"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in models_to_try:
        print(f"\n🧪 Trying model: {model}")
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hello, can you help me test this API?"}
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                "https://api.publicai.co/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            print(f"Status: {response.status_code}")
            
            if response.ok:
                result = response.json()
                print(f"✅ Success with {model}!")
                if 'choices' in result and len(result['choices']) > 0:
                    print(f"Response: {result['choices'][0]['message']['content']}")
                else:
                    print(f"Unexpected format: {result}")
                break  # Success, stop trying other models
            else:
                error_text = response.text
                try:
                    error_json = response.json()
                    print(f"❌ Error: {error_json}")
                except:
                    print(f"❌ Error: {error_text}")
        
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    else:
        print("❌ All models failed")

def test_alternative_endpoints():
    """Test alternative endpoint formats"""
    api_key = test_api_key()
    if not api_key:
        return
    
    print("\n🔀 Testing alternative endpoints...")
    
    # Try different base URLs
    base_urls = [
        "https://api.publicai.co/v1",
        "https://publicai.co/api/v1",
        "https://api.publicai.co"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for base_url in base_urls:
        print(f"\n🌐 Trying base URL: {base_url}")
        try:
            response = requests.get(f"{base_url}/models", headers=headers, timeout=5)
            print(f"Status: {response.status_code}")
            if response.ok:
                print(f"✅ Working base URL: {base_url}")
                break
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    print("🚀 PublicAI API Connection Test")
    print("=" * 40)
    
    test_api_key()
    test_api_models()
    test_simple_chat()
    test_alternative_endpoints()
    
    print("\n" + "=" * 40)
    print("Test complete! Check the results above.")