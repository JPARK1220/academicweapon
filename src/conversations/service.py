from src.conversations.model import CreateConversationRequest
from src.conversations.schemas.conversation import Conversation
from src.conversations.schemas.settings import Settings
from src.conversations.schemas.message import Message

class ConversationsService:
    def __init__(self):
        pass
    
    async def create_conversation(self, user_id: str, create_conversation_request: CreateConversationRequest):
        settings = Settings(
            model = create_conversation_request.settings.model,
        )

        message = Message(
            role=create_conversation_request.message.role,
            content=create_conversation_request.message.content,
            image_urls=create_conversation_request.message.image_urls,
        )

        conversation = Conversation(
            user_id=user_id,
            title=create_conversation_request.title,
            settings=settings,
            messages=[message]
        )

        conversation.save()

        return conversation

    async def get_conversation(self, conversation_id: str):
        pass