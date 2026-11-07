import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY", None)
if api_key is None:
    raise RuntimeError("api key not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", # overwrite the default (openAI) to open router
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

# https://developers.openai.com/api/reference/resources/chat
# https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
response = client.chat.completions.create(
    model="openrouter/free", # rotating free tier models, 50 requests per day or specify manualy ID from https://openrouter.ai/models?max_price=0 (must end with free)
    messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ],
)
if response.usage is None:
    raise RuntimeError("API request failed")
# https://developers.openai.com/api/docs/guides/token-counting
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Response tokens: {response.usage.completion_tokens}")
print(response.choices[0].message.content)
