# from .dependencies import LlmDependencies
# from .models import LlmResponse, LlmRequest
# from fastapi import APIRouter, Depends


# class LlmRouter:
#     router = APIRouter()

#     @router.post("/process", response_model=LlmResponse)
#     async def process(
#         request: LlmRequest, llm_service=Depends(LlmDependencies.get_llm_service)
#     ):
#         return await llm_service.process(request)

# llm_router = LlmRouter().router
