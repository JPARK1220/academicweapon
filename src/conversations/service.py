import select
from typing import Dict, Union

from fastapi import HTTPException
from src.conversations.entities.conversation_message import ConversationMessage
from src.conversations.model import CreateConversationRequest, CreateMessageRequest
from src.conversations.entities.conversation import Conversation
from src.conversations.entities.message import Message
from src.images.service import ImagesService
from src.llm.service import LlmService

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.llm.utils import Role, Model, get_model

class ConversationsService:
    def __init__(self, llm_service: LlmService, images_service: ImagesService):
        self.llm_service = llm_service
        # self.images_service = images_service
    
    async def create_conversation(self, session: AsyncSession, user_id: str, create_conversation_request: CreateConversationRequest):

        conversation = Conversation(
            user_id = user_id,
            title=create_conversation_request.title,
            settings=create_conversation_request.settings.model_dump()
        )

        session.add(conversation)
        await session.flush()

        # Set model from settings
        create_conversation_request.message.model = create_conversation_request.settings.model

        result = await self.create_message(
            session=session,
            user_id=user_id, 
            conversation_id=str(conversation.id),
            create_message_request=create_conversation_request.message
        )
        
        return result
        
    async def create_message(self, session: AsyncSession, user_id: str, conversation_id: str, create_message_request: CreateMessageRequest):
        conversation = await self.get_conversation(session, user_id, conversation_id)
        
        user_message = Message(role=Role.USER, content=create_message_request.content)
        
        try:
            openai_conversation = []
            for cm in conversation.conversation_messages:
                openai_conversation.append(await self._format_openai_message(user_id, cm.message))
            openai_conversation.append(await self._format_openai_message(user_id, user_message))

            response = await self.llm_service.generate_llm_response(get_model(create_message_request.model), openai_conversation) # TODO CHANGE THIS LOGIC, GET MODEL SETTING LOGIC >>>
            
            assistant_message = Message(role=Role.ASSISTANT, content=response)
            base_order_index = len(conversation.conversation_messages)
            await self._add_message_to_conversation(session, conversation, user_message, base_order_index)
            await self._add_message_to_conversation(session, conversation, assistant_message, base_order_index + 1)
            
            await session.commit()
            
        except Exception:
            await session.rollback()
            raise
        
        return {"user_message": user_message, "assistant_message": assistant_message}
    
    async def _add_message_to_conversation(self, session: AsyncSession, conversation: Conversation, message: Message, index: int):
        session.add(message)
        await session.flush()
        
        conv_message = ConversationMessage(
            conversation_id=conversation.id,
            message_id=message.id,
            order_index=index
        )
        session.add(conv_message)

    async def get_conversation(self, session: AsyncSession, user_id: str, conversation_id: str) -> Conversation:
        result = await session.execute(
            select(Conversation)
            .options(selectinload(Conversation.conversation_messages).selectinload(ConversationMessage.message))
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )

        conversation = result.scalar_one_or_none()

        if conversation is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return conversation
    

    async def _create_conversation_query(self, session: AsyncSession):
        pass

    async def _format_openai_message(self, user_id: str, message: Message) -> Dict[str, Union[str, list]]:
        message_obj = {}
        message_obj["role"] = message.role
          
        if (True): # Attachment checl
            message_obj["content"] = message.content
        
        else:
            message_obj["content"] = []
            message_obj["content"].append({
                "type": "text",
                "text": message.content,
            })
            temp_urls_dict = await self.images_service.get_batch_temporary_urls_with_keys(user_id, message.image_keys)
            for image_key in message.image_keys:
                message_obj["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": temp_urls_dict[image_key],
                        "detail": "auto",
                    }
                })
        
        return message_obj