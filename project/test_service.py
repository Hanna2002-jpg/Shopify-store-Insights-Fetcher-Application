#!/usr/bin/env python3

print("Testing Python setup...")
print("Python is working!")

# Test imports
try:
    import sys
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
except Exception as e:
    print(f"Error with sys: {e}")

try:
    import fastapi
    print("✅ FastAPI is installed")
except ImportError:
    print("❌ FastAPI is NOT installed")

try:
    import uvicorn
    print("✅ Uvicorn is installed")
except ImportError:
    print("❌ Uvicorn is NOT installed")

# If both are installed, try to run a simple server
try:
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI()
    
    @app.get("/")
    def root():
        return {"message": "Python and FastAPI are working!"}
    
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
except Exception as e:
    print(f"Error starting server: {e}")
    print("Please install fastapi and uvicorn first")
    print("Run: python -m pip install fastapi uvicorn")