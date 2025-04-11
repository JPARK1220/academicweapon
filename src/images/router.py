
from fastapi import APIRouter, Depends, Request
from src.auth.decorators import auth_guard
from src.images.dependencies import get_images_service
from src.images.models import CreatePresignedImageUrlRequest, CreateTemporaryImageUrlRequest
from src.images.service import ImagesService

router = APIRouter(prefix="/images", tags=["convo"])
@router.post("/presigned", response_model=dict)
@auth_guard
async def get_presigned_url(
    request: Request,
    create_presigned_image_url_request: CreatePresignedImageUrlRequest,
    images_service: ImagesService = Depends(get_images_service)
):
    return await images_service.create_presigned_image_url(request.state.user.id, create_presigned_image_url_request)

@router.get("/temporary-url/{image_uuid}", response_model=dict)
@auth_guard
async def get_temporary_image_url(
    request: Request,
    file_uuid: str,
    file_name: str,
    file_extension: str,
    images_service: ImagesService = Depends(get_images_service)
):
    return await images_service.create_temporary_image_url(request.state.user.id, CreateTemporaryImageUrlRequest(file_name, file_extension, file_uuid))
    

