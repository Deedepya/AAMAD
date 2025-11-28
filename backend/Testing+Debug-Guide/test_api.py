#!/usr/bin/env python3
"""
Simple API Test Script
Tests the backend API endpoints
"""

import requests
import uuid
import sys
from io import BytesIO

BASE_URL = "http://localhost:8000"
ENDPOINTS = {
    "health": f"{BASE_URL}/documents/health",
    "upload": f"{BASE_URL}/documents/upload"
}

def print_test_header(test_name):
    """Print formatted test header"""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)

def test_health_check():
    """Test 1: Health Check Endpoint"""
    print_test_header("Health Check")
    try:
        response = requests.get(ENDPOINTS["health"], timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        if response.status_code == 200:
            print("✓ PASS: Health check successful")
            return True
        else:
            print("✗ FAIL: Unexpected status code")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ FAIL: Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        return False

def test_upload_success():
    """Test 2: Successful Document Upload"""
    print_test_header("Document Upload - Success Case")
    try:
        # Create a test file in memory
        test_content = b"This is a test document for API testing"
        test_file = BytesIO(test_content)
        test_file.name = "test_document.txt"
        
        files = {"file": ("test_document.txt", test_file, "text/plain")}
        data = {
            "document_type": "I9",
            "user_id": str(uuid.uuid4())
        }
        
        response = requests.post(ENDPOINTS["upload"], files=files, data=data, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ PASS: Document upload successful")
            return True
        else:
            print("✗ FAIL: Upload failed")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ FAIL: Cannot connect to server")
        return False
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        return False

def test_upload_missing_file():
    """Test 3: Upload with Missing File (Error Case)"""
    print_test_header("Document Upload - Missing File (Error Case)")
    try:
        data = {
            "document_type": "I9",
            "user_id": str(uuid.uuid4())
        }
        
        response = requests.post(ENDPOINTS["upload"], data=data, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        
        if response.status_code == 400 or response.status_code == 422:
            print("✓ PASS: Correctly rejected missing file")
            return True
        else:
            print("✗ FAIL: Should have returned 400 or 422")
            return False
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        return False

def test_upload_invalid_document_type():
    """Test 4: Upload with Invalid Document Type"""
    print_test_header("Document Upload - Invalid Document Type")
    try:
        test_content = b"Test document"
        test_file = BytesIO(test_content)
        test_file.name = "test.txt"
        
        files = {"file": ("test.txt", test_file, "text/plain")}
        data = {
            "document_type": "INVALID_TYPE",
            "user_id": str(uuid.uuid4())
        }
        
        response = requests.post(ENDPOINTS["upload"], files=files, data=data, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        
        if response.status_code == 400 or response.status_code == 422:
            print("✓ PASS: Correctly rejected invalid document type")
            return True
        else:
            print("✗ FAIL: Should have returned 400 or 422")
            return False
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        return False

def test_different_document_types():
    """Test 5: Upload with Different Valid Document Types"""
    print_test_header("Document Upload - Different Document Types")
    valid_types = ["I9", "W4", "ID", "PASSPORT", "DRIVERSLICENSE", "SOCIALSECURITYCARD"]
    results = []
    
    for doc_type in valid_types:
        try:
            test_content = b"Test document"
            test_file = BytesIO(test_content)
            test_file.name = f"test_{doc_type}.txt"
            
            files = {"file": (test_file.name, test_file, "text/plain")}
            data = {
                "document_type": doc_type,
                "user_id": str(uuid.uuid4())
            }
            
            response = requests.post(ENDPOINTS["upload"], files=files, data=data, timeout=10)
            if response.status_code == 200:
                print(f"✓ {doc_type}: Success")
                results.append(True)
            else:
                print(f"✗ {doc_type}: Failed ({response.status_code})")
                results.append(False)
        except Exception as e:
            print(f"✗ {doc_type}: Error - {str(e)}")
            results.append(False)
    
    success_count = sum(results)
    print(f"\n✓ PASS: {success_count}/{len(valid_types)} document types accepted")
    return success_count == len(valid_types)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("BACKEND API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Make sure the server is running: python main.py")
    
    tests = [
        ("Health Check", test_health_check),
        ("Upload Success", test_upload_success),
        ("Upload Missing File", test_upload_missing_file),
        ("Upload Invalid Type", test_upload_invalid_document_type),
        ("Different Document Types", test_different_document_types),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n\nTests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

