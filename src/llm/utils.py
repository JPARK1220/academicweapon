# READ:
# undefined models mean there's no particularly good model for that subject,
# commented models mean they are runner-ups
# when in doubt, just use gemini-2.0-flash-001 aka default model

from enum import Enum

class Topic(str, Enum):
    DEFAULT = "default"
    MATH = "math"
    ENGLISH = "english"
    SCIENCE = "science" 
    SOCIAL_STUDIES = "social studies"
    FOREIGN_LANGUAGE = "foreign language"
    COMPUTER_SCIENCE = "computer science"

models = {
    Topic.DEFAULT: "google/gemini-2.0-flash-001",
    Topic.MATH: "google/gemini-2.0-flash-001",
    Topic.ENGLISH: "openai/gpt-4o",
    Topic.SCIENCE: "google/gemini-2.0-flash-001",
    Topic.SOCIAL_STUDIES: "google/gemini-2.0-flash-001",
    Topic.FOREIGN_LANGUAGE: "anthropic/claude-3.5-sonnet",
    Topic.COMPUTER_SCIENCE: "anthropic/claude-3.5-sonnet", # @jpark HOLY WERE RICH ENOUGH TO SUPPORT THIS?
}

# Define the prompt template without f-string
prompt_template = (
    "You are an expert on {topic}. Answer the problem(s) in the following image(s)."
)


def get_model(topic):
    return models[topic] if models[topic] else models["default"]


# get_prompt("math")
def get_prompt(topic):
    return prompt_template.format(topic=topic)
