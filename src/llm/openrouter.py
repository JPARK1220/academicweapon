from openai import OpenAI
import os

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  model="openai/gpt-4o-mini",
  messages=[
    {"role": "user", "content": "Hello, my name is Jun and this is a test message. Write me back a poem about struggling cs majors."},
  ],
)

print(completion.choices[0].message.content)