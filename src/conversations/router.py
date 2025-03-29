from fastapi import APIRouter, Depends, Request

from src.auth.decorators import auth_guard
from src.auth.models import User
from src.conversations.dependencies import ConversationsDependencies
from src.conversations.model import CreateConversationRequest
from src.conversations.service import ConversationsService

router = APIRouter(prefix="/conversations", tags=["convo"])

@router.get("/{conversationId}", include_in_schema=False)
@auth_guard
async def get_conversation(
    conversationId: str,
    conversations_service: ConversationsService = Depends(ConversationsDependencies.get_conversations_service),
):
    return {"conversationId": conversationId}

@router.post("/")
@auth_guard
async def create_conversation(
    request: Request,
    create_conversation_request: CreateConversationRequest,
    conversations_service: ConversationsService = Depends(ConversationsDependencies.get_conversations_service),
):
    user: User = request.state.user
    return await conversations_service.create_conversation(user.id, create_conversation_request)