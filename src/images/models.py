from pydantic import BaseModel, Field

from src.images.constants import ImageFileExtension

class CreatePresignedImageUrlRequest(BaseModel):
    file_name: str = Field(default="user-uploaded-content", description="Image file name.")
    file_extension: ImageFileExtension = Field(..., description="Image files may only be of a supported image file extension.")

class GetTemporaryImageUrlRequest(CreatePresignedImageUrlRequest):
    file_uuid: str = Field(description="File uuid is needed.")