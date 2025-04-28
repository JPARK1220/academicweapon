from typing import List
from src.conversations.model import CreateImageAttachmentRequest
from src.conversations.schemas.message import Message
from src.images.utils import create_file_key

def attach_images(self, user_id: str, image_attachment_list: List[CreateImageAttachmentRequest]):
    keys = []
    for create_image_attachment_request in image_attachment_list:
        file_key = create_file_key(user_id, create_image_attachment_request.file_uuid, create_image_attachment_request.file_name, create_image_attachment_request.file_extension)
        # Check validity (exists in postgres)
        # Turn it to non-pending ('attached' etc)
        # Error out if either are faulty
        keys.append(file_key)
    
    return keys