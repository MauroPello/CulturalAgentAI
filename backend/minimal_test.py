#!/usr/bin/env python3
"""
Minimal test for PublicAI API with apertus model
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Get API key
api_key = os.getenv("PUBLIC_AI_KEY")
print(f"🔑 API Key: {api_key[:20]}..." if api_key else "❌ No API key found")

if not api_key:
    print("Please set PUBLIC_AI_KEY in your .env file")
    exit(1)

# Test minimal request with apertus model
url = "https://api.publicai.co/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Minimal payload with MANDATORY apertus model
payload = {
    "model": "swiss-ai/apertus-8b-instruct",
    "messages": [
        {"role": "user", "content": "Hello, this is a test. Please respond briefly."}
    ],
    "max_tokens": 50
}

print("📤 Sending request...")
print(f"URL: {url}")
print(f"Model: {payload['model']}")
print(f"Headers: {list(headers.keys())}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    
    if response.ok:
        result = response.json()
        print("✅ SUCCESS!")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(f"🤖 AI Response: {content}")
        
    else:
        print("❌ FAILED!")
        print(f"Error: {response.text}")
        
        try:
            error_json = response.json()
            print(f"Error JSON: {json.dumps(error_json, indent=2)}")
        except:
            pass
            
except Exception as e:
    print(f"💥 Exception: {e}")
    import traceback
    traceback.print_exc()