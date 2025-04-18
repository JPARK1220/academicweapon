from fastapi import APIRouter, Depends, Request

from src.auth.decorators import auth_guard
from src.auth.models import User
from src.conversations.dependencies import get_conversations_service
from src.conversations.model import CreateConversationRequest, CreateMessageRequest
from src.conversations.service import ConversationsService

router = APIRouter(prefix="/conversations", tags=["convo"])

@router.get("/{conversation_id}")
@auth_guard
async def get_conversation(
    request: Request,
    conversation_id: str,
    conversations_service: ConversationsService = Depends(get_conversations_service),
):
    user: User = request.state.user
    return {"conversation": await conversations_service.get_conversation(user.id, conversation_id)}

@router.post("/{conversation_id}")
@auth_guard
async def create_conversation(
    request: Request,
    conversation_id: str,
    create_message_request: CreateMessageRequest,
    conversations_service: ConversationsService = Depends(get_conversations_service),
):
    user: User = request.state.user
    return await conversations_service.create_message(user.id, conversation_id, create_message_request)

@router.post("/")
@auth_guard
async def create_conversation(
    request: Request,
    create_conversation_request: CreateConversationRequest,
    conversations_service: ConversationsService = Depends(get_conversations_service),
):
    user: User = request.state.user
    return await conversations_service.create_conversation(user.id, create_conversation_request)