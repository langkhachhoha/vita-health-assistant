#!/usr/bin/env python3
"""
Test script cho Doctor Chatbot Server
"""

import requests
import json
import time

SERVER_URL = "http://localhost:8502"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is healthy")
            print(f"   Model: {data.get('model')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_patient_info():
    """Test patient info endpoint"""
    print("\n📋 Testing patient info...")
    try:
        response = requests.get(f"{SERVER_URL}/patient-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print("✅ Patient data loaded successfully")
                segments = data.get('data', {})
                print(f"   Segments available: {list(segments.keys())}")
            else:
                print(f"⚠️  No patient data: {data.get('message')}")
            return True
        else:
            print(f"❌ Patient info failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Patient info failed: {e}")
        return False

def test_chat_simple():
    """Test simple chat without streaming"""
    print("\n💬 Testing simple chat...")
    try:
        messages = [
            {"role": "user", "content": "Xin chào, bạn có thể giúp tôi về sức khỏe không?"}
        ]
        
        response = requests.post(
            f"{SERVER_URL}/chat",
            json={"messages": messages, "stream": False},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', '')
            print("✅ Simple chat successful")
            print(f"   Response: {content[:100]}...")
            return True
        else:
            print(f"❌ Simple chat failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Simple chat failed: {e}")
        return False

def test_chat_streaming():
    """Test streaming chat"""
    print("\n🌊 Testing streaming chat...")
    try:
        messages = [
            {"role": "user", "content": "Chỉ số BMI của tôi có bình thường không?"}
        ]
        
        response = requests.post(
            f"{SERVER_URL}/chat",
            json={"messages": messages, "stream": True},
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Streaming chat started")
            full_response = ""
            chunk_count = 0
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        if 'content' in data:
                            if data['content'] == '[DONE]':
                                break
                            full_response += data['content']
                            chunk_count += 1
                            if chunk_count <= 3:  # Show first few chunks
                                print(f"   Chunk {chunk_count}: {data['content']}")
            
            print(f"✅ Streaming completed with {chunk_count} chunks")
            print(f"   Full response: {full_response[:100]}...")
            return True
        else:
            print(f"❌ Streaming chat failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Streaming chat failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Dr. HealthBot Server Test Suite")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python Doctor_chatbot_server.py")
        return
    
    # Test 2: Patient info
    test_patient_info()
    
    # Test 3: Simple chat
    test_chat_simple()
    
    # Test 4: Streaming chat
    test_chat_streaming()
    
    print("\n🎉 All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
