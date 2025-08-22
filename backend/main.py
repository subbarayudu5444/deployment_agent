from fastapi import FastAPI
import os
from routers import deployment, lightning
from config import APP_CONFIG

# Create FastAPI app
app = FastAPI(
    title=APP_CONFIG["title"],
    description=APP_CONFIG["description"],
    version=APP_CONFIG["version"]
)

@app.get("/",tags=["deployment"])
async def root():
    return {"message": "Hello, Welcome to Coastal Seven Deployment Agent"}

# Include routers
app.include_router(deployment.router)
#app.include_router(lightning.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)