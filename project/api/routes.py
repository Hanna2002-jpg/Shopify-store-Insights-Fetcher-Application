from fastapi import APIRouter, HTTPException
from models.schemas import ExtractRequest, BrandInsightsSchema
from services.insights_service import ShopifyInsightsService

router = APIRouter()

@router.post("/extract", response_model=BrandInsightsSchema)
def extract(payload: ExtractRequest):
    try:
        result = ShopifyInsightsService.fetch_brand_insights(payload.website_url)
        if "error" in result:
            # Return HTTP 400 with error message
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(status_code=500, detail=str(e))

