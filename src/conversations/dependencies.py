from src.conversations.service import ConversationsService
from src.images.dependencies import get_images_service
from src.llm.dependencies import get_llm_service

async def get_conversations_service():
    llm_service = get_llm_service()
    images_service = get_images_service()
    return ConversationsService(llm_service, images_service)