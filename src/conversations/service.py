from beanie import PydanticObjectId
from src.conversations.model import CreateConversationRequest, CreateMessageRequest
from src.conversations.schemas import settings
from src.conversations.schemas.conversation import Conversation
from src.conversations.schemas.settings import Settings
from src.conversations.schemas.message import Message
from src.conversations.utils import format_openai_message
from src.llm.service import LlmService
from src.llm.utils import get_expert_prompt, get_follow_up_questions_prompt

class ConversationsService:
    def __init__(self, llm_service: LlmService):
        self.llm_service = llm_service
    
    async def create_conversation(self, user_id: str, create_conversation_request: CreateConversationRequest):
        settings = Settings(
            # model = create_conversation_request.settings.model,
            topic = create_conversation_request.settings.topic,
        )

        message = Message(
            role=create_conversation_request.message.role,
            content=create_conversation_request.message.content,
            image_urls=create_conversation_request.message.image_urls,
        )

        try:
            formatted_message = format_openai_message(message)
            response = await self.llm_service.get_llm_response(settings.topic, [formatted_message])
            # response = formatted_message
            
            assistant_message = Message(
                role="assistant",
                content=response,
                image_urls=[]
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
        message = Message(
            role="user",
            content=create_message_request.content,
            image_urls=create_message_request.image_urls,
        )
        conversation.messages.append(message)
        convo = [format_openai_message(msg) for msg in conversation.messages]
        response = await self.llm_service.get_llm_response(conversation.settings.topic, convo)
        conversation.messages.append(Message(
            role="assistant",
            content=response,
            image_urls=[]
        ))

        await conversation.save()
        
        return {
            "response": response, #llm response, i also need the user's image input
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
    





    async def get_follow_up_questions(self, conversation: Conversation):
        # conversation

        # add follow up question prompt
        message = Message(
            role="system",
            content=get_follow_up_questions_prompt(conversation.settings.topic),
            image_urls=[],
        )
        conversation.messages.append(message)

        # valid array
        convo = [format_openai_message(msg) for msg in conversation.messages]

        # ask model for follow up questions
        follow_up_questions = await self.llm_service.get_llm_response(conversation.settings.topic, convo)

        # return follow up questions
        return follow_up_questions

    async def create_expert_conversation(self, user_id: str, create_conversation_request: CreateConversationRequest):
        create_conversation_request.message.role = "system"
        create_conversation_request.message.content = get_expert_prompt(create_conversation_request.settings.topic)
        conversation = await self.create_conversation(user_id, create_conversation_request)
        follow_up_questions = await self.get_follow_up_questions(conversation)

        return {
            "conversation": conversation,
            "follow_up_questions": follow_up_questions,
        }
    
        


