from src.conversations.service import ConversationsService
from src.llm.dependencies import get_llm_service

async def get_conversations_service():
    llm_service = get_llm_service()
    return ConversationsService(llm_service)