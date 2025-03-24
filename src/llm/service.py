from fastapi import HTTPException
from llm.llm import get_llm_response
from models import ImageRequest, ImageResponse

# Todo: get_llm_response should be a service

class LlmService:
    def __init__(self):
      pass

    async def process(request: ImageRequest):
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