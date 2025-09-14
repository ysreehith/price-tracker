#!/usr/bin/env python3
"""
Simple test script to verify the backend is working correctly
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Price Tracker API...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✓ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test 2: Get products (should be empty initially)
    try:
        response = requests.get(f"{API_BASE_URL}/products/")
        print(f"✓ Get products: {response.status_code} - {len(response.json())} products")
    except Exception as e:
        print(f"✗ Get products failed: {e}")
        return False
    
    # Test 3: Add a test product (Amazon example)
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"  # Example Amazon product
    try:
        response = requests.post(
            f"{API_BASE_URL}/products/",
            json={"url": test_url}
        )
        if response.status_code == 200:
            product = response.json()
            print(f"✓ Add product: {product['name'][:50]}... - ${product['current_price']}")
            product_id = product['id']
        else:
            print(f"✗ Add product failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Add product failed: {e}")
        return False
    
    # Test 4: Get product with history
    try:
        response = requests.get(f"{API_BASE_URL}/products/{product_id}")
        if response.status_code == 200:
            product_data = response.json()
            print(f"✓ Get product history: {len(product_data['price_history'])} price entries")
        else:
            print(f"✗ Get product history failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Get product history failed: {e}")
    
    # Test 5: Update product price
    try:
        response = requests.post(f"{API_BASE_URL}/products/{product_id}/update")
        if response.status_code == 200:
            updated_product = response.json()
            print(f"✓ Update price: ${updated_product['current_price']}")
        else:
            print(f"✗ Update price failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Update price failed: {e}")
    
    # Test 6: Delete test product
    try:
        response = requests.delete(f"{API_BASE_URL}/products/{product_id}")
        if response.status_code == 200:
            print(f"✓ Delete product: {response.json()['message']}")
        else:
            print(f"✗ Delete product failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Delete product failed: {e}")
    
    print("\n🎉 API tests completed!")
    return True

if __name__ == "__main__":
    print("Make sure the backend is running on http://localhost:8000")
    print("You can start it with: cd backend && python main.py")
    print("-" * 50)
    
    test_api()

