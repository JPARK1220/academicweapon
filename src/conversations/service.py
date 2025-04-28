from typing import Dict, Union
from beanie import PydanticObjectId
from src.conversations.model import CreateConversationRequest, CreateImageAttachmentRequest, CreateMessageRequest
from src.conversations.schemas.conversation import Conversation
from src.conversations.schemas.settings import Settings
from src.conversations.schemas.message import Message
from src.conversations.utils import attach_images, format_openai_message
from src.images.service import ImagesService
from src.llm.service import LlmService
from src.llm.utils import get_prompt

class ConversationsService:
    def __init__(self, llm_service: LlmService, images_service: ImagesService):
        self.llm_service = llm_service
        self.images_service = images_service

    async def create_problem_conversation(self, user_id: str, create_conversation_request: CreateConversationRequest):
        create_conversation_request.message.role = "system"
        create_conversation_request.message.content = get_prompt(create_conversation_request.settings.topic)
        return await self.create_conversation(user_id, create_conversation_request)
    
    async def create_conversation(self, user_id: str, create_conversation_request: CreateConversationRequest):
        settings = Settings(
            # model = create_conversation_request.settings.model,
            topic = create_conversation_request.settings.topic,
        )

        image_keys = attach_images(user_id, create_conversation_request.message.image_attachments)

        message = Message(
            role=create_conversation_request.message.role,
            content=create_conversation_request.message.content,
            image_keys=image_keys,
        )

        try:
            formatted_message = await self.format_openai_message(message)
            response = await self.llm_service.get_llm_response(settings.topic, [formatted_message])
            # response = formatted_message
            
            assistant_message = Message(
                role="assistant",
                content=response,
                image_keys=[]
            )
            conversation = Conversation(
                user_id=user_id,
                title=create_conversation_request.title,
                settings=settings,
                messages=[message, assistant_message]
            )
            try:
                await conversation.save()
            except Exception as db_error:
                # Database save failed
                raise Exception(f"Failed to save conversation: {str(db_error)}")
            return {
                "response": response,
                "conversation": conversation,
            }
        except Exception as llm_error:
            raise Exception(f"Failed to get response from LLM: {str(llm_error)}")

    async def create_message(self, user_id: str, conversation_id: str, create_message_request: CreateMessageRequest):
        conversation: Conversation = await self.get_conversation(user_id, conversation_id)
        image_keys = attach_images(user_id, create_message_request.image_attachments)
        message = Message(
            role="user",
            content=create_message_request.content,
            image_keys=image_keys,
        )
        conversation.messages.append(message)
        convo = [await self.format_openai_message(msg) for msg in conversation.messages]
        response = await self.llm_service.get_llm_response(conversation.settings.topic, convo)
        conversation.messages.append(Message(
            role="assistant",
            content=response,
            image_keys=[]
        ))

        await conversation.save()
        
        return {
            "response": response,
            "conversation": conversation,
        }

    async def get_conversation(self, user_id: str, conversation_id: str) -> Conversation:
        # check if user owns conversation 
        conversation = await Conversation.find_one({
            "_id": PydanticObjectId(conversation_id),
            "user_id": user_id
        })
        if conversation == None:
            raise Exception("Conversation was not found!")

        return conversation
    
    async def format_openai_message(self, user_id: str, message: Message) -> Dict[str, Union[str, list]]:
        message_obj = {}
        message_obj["role"] = message.role
        
        if (len(message.image_keys) == 0):
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