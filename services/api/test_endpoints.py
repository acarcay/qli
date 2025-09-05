#!/usr/bin/env python3
"""
Test script for the Qlick API endpoints.
Run this after starting the API server to test all three endpoints.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(method, url, expected_status=200, description=""):
    """Test an endpoint and print results."""
    print(f"\n{'='*60}")
    print(f"Testing: {method} {url}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        else:
            response = requests.request(method, url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Expected: {expected_status}")
        
        if response.status_code == expected_status:
            print("✅ PASS")
        else:
            print("❌ FAIL")
        
        # Pretty print JSON response
        try:
            json_data = response.json()
            print(f"Response:\n{json.dumps(json_data, indent=2)}")
        except:
            print(f"Response (text): {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FAIL - Could not connect to server. Make sure the API is running on localhost:8000")
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")

def main():
    print("Qlick API Endpoint Tests")
    print("Make sure the API server is running: uvicorn app.main:app --reload")
    
    # Test 1: GET /menus/{restaurantSlug}
    test_endpoint(
        "GET", 
        f"{BASE_URL}/menus/qlick-demo",
        200,
        "Get menu by restaurant slug with categories and items"
    )
    
    # Test 2: GET /menus/{restaurantSlug} with pagination
    test_endpoint(
        "GET", 
        f"{BASE_URL}/menus/qlick-demo?page=1",
        200,
        "Get menu with pagination parameter"
    )
    
    # Test 3: GET /menus/{restaurantSlug} - non-existent restaurant
    test_endpoint(
        "GET", 
        f"{BASE_URL}/menus/non-existent-restaurant",
        404,
        "Get menu for non-existent restaurant (should return 404)"
    )
    
    # Test 4: GET /items/{id}
    test_endpoint(
        "GET", 
        f"{BASE_URL}/items/1",
        200,
        "Get item details with pairings"
    )
    
    # Test 5: GET /items/{id} - non-existent item
    test_endpoint(
        "GET", 
        f"{BASE_URL}/items/999",
        404,
        "Get non-existent item (should return 404)"
    )
    
    # Test 6: GET /search
    test_endpoint(
        "GET", 
        f"{BASE_URL}/search?q=chicken",
        200,
        "Search items by query"
    )
    
    # Test 7: GET /search with pagination
    test_endpoint(
        "GET", 
        f"{BASE_URL}/search?q=salmon&page=1&limit=5",
        200,
        "Search with pagination parameters"
    )
    
    # Test 8: GET /search - empty query
    test_endpoint(
        "GET", 
        f"{BASE_URL}/search?q=",
        400,
        "Search with empty query (should return 400)"
    )
    
    print(f"\n{'='*60}")
    print("Test Summary:")
    print("All tests completed. Check the results above.")
    print("Expected: 6 PASS, 2 FAIL (for error cases)")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
