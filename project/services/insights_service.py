#!/usr/bin/env python3

# Quick test of the service
import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.getcwd())

def test_service():
    try:
        print("Testing service...")
        from services.insights_service import ShopifyInsightsService
        
        print("✅ Service imported successfully")
        
        # Test with a simple website
        result = ShopifyInsightsService.fetch_brand_insights("https://example.com")
        
        print(f"Result type: {type(result)}")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if "error" in result:
            print(f"❌ Service returned error: {result['error']}")
        else:
            print("✅ Service returned success")
            print(f"Brand name: {result.get('brand_name')}")
            print(f"Description: {result.get('description')}")
            
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=== TESTING SHOPIFY INSIGHTS SERVICE ===")
    result = test_service()
    
    if result:
        print("\n✅ Service test completed!")
    else:
        print("\n❌ Service test failed!")
        print("\nMake sure you have:")
        print("1. beautifulsoup4 installed: pip install beautifulsoup4")
        print("2. requests installed: pip install requests") 
        print("3. services/__init__.py exists")
        print("4. services/insights_service.py exists")