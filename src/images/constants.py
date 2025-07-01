from enum import Enum

# Accepted formats for image uploads
class ImageFileExtension(str, Enum):
    jpg = "jpg"
    jpeg = "jpeg"
    png = "png"
    webp = "webp"

EXTENSION_TO_CONTENT_TYPE = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp"
}

UPLOAD_EXPIRATION = 180 # 3 minutes
VIEW_EXPIRATION = 259200 # 3 days

class LifecycleStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    COMPLETED = "completed"