import uuid
from src.database import get_bucket, get_redis
from src.images.constants import EXTENSION_TO_CONTENT_TYPE, UPLOAD_EXPIRATION, VIEW_EXPIRATION, LifecycleStatus
from src.images.models import CreatePresignedImageUrlRequest, CreateTemporaryImageUrlRequest


class ImagesService:
    def __init__(self):
        pass

    async def create_presigned_image_url(user_id: str, create_presigned_image_url_request: CreatePresignedImageUrlRequest):
        file_uuid = str(uuid.uuid4())
        file_key = f"uploads/users/{user_id}/images/{file_uuid}/{create_presigned_image_url_request.file_name}.{create_presigned_image_url_request.file_extension}"
        async with get_bucket() as bucket:
            presigned_url = await bucket.meta.client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket.name,
                    'Key': file_key,
                    'ContentType': EXTENSION_TO_CONTENT_TYPE[create_presigned_image_url_request.file_extension],
                    'Metadata': {
                        'status': LifecycleStatus.PENDING,
                    },
                },
                ExpiresIn=UPLOAD_EXPIRATION
            )
            return {"presigned_url": presigned_url}

    async def create_temporary_image_url(user_id: str, create_temporary_image_url_request: CreateTemporaryImageUrlRequest):
        redis_client = get_redis()
        redis_key = f"image:{user_id}:{create_temporary_image_url_request.file_uuid}"
        cached_url = await redis_client.get(redis_key)
        if cached_url:
            return { "temporary_url": cached_url }

        file_key = f"uploads/users/{user_id}/images/{create_temporary_image_url_request.uuid}/{create_temporary_image_url_request.file_name}.{create_temporary_image_url_request.file_extension}"
        async with get_bucket() as bucket:
            temp_url = await bucket.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket.name,
                'Key': file_key
            },
            ExpiresIn=VIEW_EXPIRATION
        )
        
        await redis_client.set(redis_key, temp_url, ex=VIEW_EXPIRATION)

        return { "temporary_url": temp_url }