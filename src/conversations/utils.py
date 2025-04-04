from typing import Dict, Union
from src.conversations.schemas.message import Message

def format_openai_message(message: Message) -> Dict[str, Union[str, list]]:
    message_obj = {}
    message_obj["role"] = message.role
    
    if (len(message.image_urls) == 0):
        message_obj["content"] = message.content
    
    else:
        message_obj["content"] = []
        message_obj["content"].append({
            "type": "text",
            "text": message.content,
        })
        for image_url in message.image_urls:
            message_obj["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "auto",
                }
            })
    
    return message_obj