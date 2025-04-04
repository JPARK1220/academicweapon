from src.conversations.service import ConversationsService
from src.llm.dependencies import get_llm_service
from src.conversations.schemas.conversation import Conversation

async def get_conversations_service():
    llm_service = get_llm_service()
    return ConversationsService(llm_service)

async def valid_conversation_id(conversation_id: str, user_id: str):
    conversation = await Conversation.find_one(
        (Conversation.id == conversation_id) & (Conversation.user_id == user_id)
    )
    if conversation is None:
        raise Exception("Conversation was not found!")
    return conversation