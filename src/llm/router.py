from .dependencies import LlmDependencies
from .models import ImageResponse, ImageRequest
from fastapi import APIRouter, Depends

class LlmRouter:
  router = APIRouter()

  @router.post("/process", response_model=ImageResponse)
  async def process(request: ImageRequest, llm_service = Depends(LlmDependencies.get_llm_service)):
    return await llm_service.process(request)

llm_router = LlmRouter().router