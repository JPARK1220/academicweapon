from fastapi import APIRouter
from fastapi_utils.cbv import cbv

router = APIRouter(prefix="/auth", tags=["authentication"])

@cbv(router)
class ConversationsRouter:

  @router.get("/{conversationId}")
  def get_conversation(self, conversationId: str):
    return {"conversationId": conversationId}