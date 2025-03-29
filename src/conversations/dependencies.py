from src.conversations.service import ConversationsService


class ConversationsDependencies:
    @staticmethod
    def get_conversations_service():
        return ConversationsService()