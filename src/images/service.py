import asyncio
from typing import Dict, List
import uuid
from src.database import get_bucket, get_redis
from src.images.constants import EXTENSION_TO_CONTENT_TYPE, UPLOAD_EXPIRATION, VIEW_EXPIRATION, LifecycleStatus
from src.images.models import CreatePresignedImageUrlRequest, GetTemporaryImageUrlRequest
from src.images.utils import create_file_key


class ImagesService:
    def __init__(self):
        pass

    async def create_presigned_image_url(self, user_id: str, create_presigned_image_url_request: CreatePresignedImageUrlRequest):
        file_uuid = str(uuid.uuid4())
        file_key = f"uploads/users/{user_id}/images/{file_uuid}/{create_presigned_image_url_request.file_name}.{create_presigned_image_url_request.file_extension.value}"
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

    async def get_temporary_image_url_with_key(self, file_key: str) -> str:
        urls = await self._get_presigned_urls([file_key])
        return { "temporary_url": urls[file_key] }

    async def get_batch_temporary_urls_with_keys(self, file_keys: List[str]) -> Dict[str, str]:
        return await self._get_presigned_urls(file_keys)

    async def _get_presigned_urls(self, file_keys: List[str]) -> Dict[str, str]:
        redis_client = get_redis()

        values = await redis_client.mget(*file_keys)

        cached_urls = {}
        missing_keys = []

        for key, value in zip(file_keys, values):
            if value:
                cached_urls[key] = value
            else:
                missing_keys.append(key)

        if missing_keys:
            async with get_bucket() as bucket:
                # Processes in chunks of 50 for efficiency and resource management
                chunk_size = 50
                all_generated = {}
                
                for i in range(0, len(missing_keys), chunk_size):
                    chunk = missing_keys[i:i+chunk_size]
                    tasks = [
                        bucket.meta.client.generate_presigned_url(
                            'get_object',
                            Params={'Bucket': bucket.name, 'Key': key},
                            ExpiresIn=VIEW_EXPIRATION
                        )
                        for key in chunk
                    ]
                    
                    generated = await asyncio.gather(*tasks)
                    
                    all_generated.update(dict(zip(chunk, generated)))
                
                pipe = redis_client.pipeline()
                for key, url in all_generated.items():
                    pipe.set(key, url, ex=VIEW_EXPIRATION)
                    cached_urls[key] = url
                    
                await pipe.execute()

        return cached_urls
    