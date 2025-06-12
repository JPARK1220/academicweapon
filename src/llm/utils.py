# READ:
# undefined models mean there's no particularly good model for that subject,
# commented models mean they are runner-ups
# when in doubt, just use gemini-2.0-flash-001 aka default model

# TODO Move this to be stored in the database for dynamic updating

from enum import Enum

class Model(str, Enum):
    GEMINI_FLASH = "GEMINI_FLASH"
    GEMINI_PRO = "GEMINI_PRO" 
    GPT_4O = "GPT_4O"
    SONNET = "SONNET"
    DEFAULT = "DEFAULT"
    
# class Model(Enum):
#     GEMINI_FLASH = "google/gemini-2.5-flash-preview-05-20"
#     GEMINI_PRO = "google/gemini-2.5-pro-preview"
#     GPT_4O = "openai/chatgpt-4o-latest"
#     SONNET = "anthropic/claude-sonnet-4"
#     DEFAULT = "google/gemini-2.5-flash-preview-05-20"

class Topic(str, Enum):
    DEFAULT = Model.DEFAULT
    MATH = Model.GEMINI_FLASH
    ENGLISH = Model.GPT_4O
    SCIENCE = Model.GEMINI_PRO
    SOCIAL_STUDIES = Model.GEMINI_PRO
    FOREIGN_LANGUAGE = Model.GEMINI_PRO
    COMPUTER_SCIENCE = Model.SONNET

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Define the prompt template without f-string
prompt_template = (
    "You are an expert on {topic}. Answer the problem(s) in the following image(s)."
)

MODEL_MAPPING = {
    "GEMINI_FLASH": "google/gemini-2.5-flash-preview-05-20",
    "GEMINI_PRO": "google/gemini-2.5-pro-preview",
    "GPT_4O": "openai/chatgpt-4o-latest",
    "SONNET": "anthropic/claude-sonnet-4",
    "DEFAULT": "google/gemini-2.5-flash-preview-05-20",
}

def get_model(topic):
    return MODEL_MAPPING[topic] if MODEL_MAPPING[topic] else MODEL_MAPPING["default"]


# # get_prompt("math")
# def get_prompt(topic):
#     return prompt_template.format(topic=topic)
