from services.insights_service import ShopifyInsightsService

url = "https://memy.co.in"

try:
    result = ShopifyInsightsService.fetch_brand_insights(url)
    print(result)
except Exception as e:
    print("Service error:", e)
