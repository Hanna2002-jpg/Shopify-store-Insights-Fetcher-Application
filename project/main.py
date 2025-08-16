# main.py (in your project root directory)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Brand Insights API",
    description="API for extracting brand insights from websites",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include router
try:
    from api.routes import router
    app.include_router(router, prefix="/api", tags=["extraction"])
    print("✅ Router included successfully")
except ImportError as e:
    print(f"❌ Error importing router: {e}")
    print("Make sure you have api/__init__.py and api/routes.py files")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Brand Insights API is running", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)