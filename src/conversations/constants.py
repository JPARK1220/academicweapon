from typing import Literal

STANDARD_CHARS_REGEX = r'^[A-Za-z0-9\s.,\-_&\'":;!?@#$%^*()\[\]{}+=\/\\]+$'
CONVERSATION_ROLES = ['user', 'assistant', 'system']
ConversationRoles = Literal['user', 'assistant', 'system']