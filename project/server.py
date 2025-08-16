from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Brand Insights API")

class ExtractRequest(BaseModel):
    website_url: str

@app.get("/")
def read_root():
    return {"message": "Brand Insights API is running", "docs": "/docs"}

@app.get("/api/health")  
def health():
    return {"status": "healthy", "message": "Extract API is running"}

@app.post("/api/extract")
def extract_data(request: ExtractRequest):
    logger.info("=== Extract endpoint called ===")
    logger.info(f"Received URL: {request.website_url}")
    
    try:
        # Simple test response first
        logger.info("Processing request...")
        
        result = {
            "success": True,
            "website_url": request.website_url,
            "brand_name": "Test Brand",
            "description": "This is a test response",
            "products": [],
            "social_media": {},
            "contact_info": {},
            "message": "Test extraction successful"
        }
        
        logger.info("Returning successful result")
        return result
        
    except Exception as e:
        logger.error(f"Error in extract endpoint: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)