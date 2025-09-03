#!/usr/bin/env python3
"""
Test script cho CCCD OCR System
"""

import os
import sys
import requests
import json
import base64
from datetime import datetime

dir = os.getcwd()

def test_ocr_model():
    """Test OCR model directly"""
    print("🧪 Testing OCR Model...")
    
    try:
        sys.path.append(os.path.join(dir, "Doctor_app"))
        from cccd_ocr_model import test_extraction
        
        result = test_extraction()
        if result and result.get('success'):
            print("✅ OCR Model test passed!")
            return True
        else:
            print("❌ OCR Model test failed!")
            return False
            
    except Exception as e:
        print(f"❌ OCR Model test error: {e}")
        return False

def test_ocr_server():
    """Test OCR server endpoints"""
    print("\n🌐 Testing OCR Server...")
    
    base_url = "http://127.0.0.1:5001"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except:
        print("❌ OCR Server not running")
        return False
    
    # Test extraction with sample image
    try:
        response = requests.get(f"{base_url}/test-extract", timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Test extraction working")
                return True
            else:
                print(f"❌ Test extraction failed: {result.get('message')}")
                return False
        else:
            print(f"❌ Test extraction endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test extraction error: {e}")
        return False

def test_streamlit_integration():
    """Test Streamlit integration"""
    print("\n📱 Testing Streamlit Integration...")
    
    try:
        sys.path.append(os.path.join(dir, "Doctor_app"))
        from cccd_client import CCCDOCRClient
        
        client = CCCDOCRClient()
        if client.check_server_health():
            print("✅ Streamlit client can connect to server")
            return True
        else:
            print("❌ Streamlit client cannot connect to server")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit integration error: {e}")
        return False

def run_full_test():
    """Run complete system test"""
    print("🚀 CCCD OCR System Full Test")
    print("=" * 50)
    
    results = []
    
    # Test 1: OCR Model
    results.append(test_ocr_model())
    
    # Test 2: OCR Server
    results.append(test_ocr_server())
    
    # Test 3: Streamlit Integration
    results.append(test_streamlit_integration())
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    
    tests = [
        "OCR Model",
        "OCR Server", 
        "Streamlit Integration"
    ]
    
    for i, (test_name, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test_name}: {status}")
    
    total_passed = sum(results)
    print(f"\nOverall: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("🎉 All tests passed! System ready for use.")
    else:
        print("⚠️  Some tests failed. Check the logs above.")
        
        # Troubleshooting tips
        print("\n🔧 Troubleshooting:")
        if not results[0]:
            print("- Check if cccd_ocr_model.py exists and dependencies are installed")
        if not results[1]:
            print("- Make sure OCR server is running: python cccd_ocr_server.py")
        if not results[2]:
            print("- Check if cccd_client.py exists and requests library is installed")

if __name__ == "__main__":
    run_full_test()
