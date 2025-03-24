# READ:
# undefined models mean there's no particularly good model for that subject,
# commented models mean they are runner-ups
# when in doubt, just use gemini-2.0-flash-001 aka default model
models = {
    "default": "google/gemini-2.0-flash-001",
    "math": "google/gemini-2.0-flash-001", # deepseek/deepseek-chat
    "english": "openai/gpt-4o", # openai/gpt-4.5-preview
    "science": "google/gemini-2.0-flash-001", # anthropic/claude-3.5-haiku, anthropic/claude-3.7-sonnet
    "social studies": "", 
    "foreign language": "anthropic/claude-3.5-sonnet", # google/gemini-2.0-flash-001
    "computer science": "anthropic/claude-3.5-sonnet",
}

# Define the prompt template without f-string
prompt_template = "You are an expert on {topic}. Answer the problem(s) in the following image(s)."

def get_model(topic):
    return models[topic] if models[topic] else models["default"]

# get_prompt("math")
def get_prompt(topic):
    return prompt_template.format(topic=topic)
