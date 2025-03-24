from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from llm import get_llm_response

app = FastAPI(
    title="Academic Weapon API",
    description="API for processing images with specialized LLM models",
    version="1.0.0",
    openapi_url="/openapi.json",
)

class ImageRequest(BaseModel):
    topic: str
    image_urls: list[str]
    
class ImageResponse(BaseModel):
    result: str

@app.post("/process-image", response_model=ImageResponse)
async def process_image(request: ImageRequest):
    """
    Process multiple images using the specialized LLM model.
    
    Parameters:
    - topic: The topic/subject area for specialization (e.g., "math")
    - image_urls: List of URLs of the images to process
    
    Returns:
    - result: The LLM's response to the images
    """
    try:
        result = get_llm_response(request.topic, request.image_urls)
        return ImageResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 