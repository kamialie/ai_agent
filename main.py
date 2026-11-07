import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

def parse_arguments():
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    return args

def prepare_messages(user_prompt, verbose):
    messages = []

    if verbose:
        print(f"User prompt: {user_prompt}")
    # openai message consists of role and content keys
    messages.append({
        "role": "user",
        "content": user_prompt
    })

    return messages

def get_client(api_key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", # overwrite the default (openAI) to open router
        api_key=api_key,
    )

    return client

def generate_content(client, messages, verbose):
    # https://developers.openai.com/api/reference/resources/chat
    # https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
    response = client.chat.completions.create(
        model="openrouter/free", # rotating free tier models, 50 requests per day or specify manualy ID from https://openrouter.ai/models?max_price=0 (must end with free)
        messages=messages
    )
    if response.usage is None:
        raise RuntimeError("API request failed")

    if verbose:
        # https://developers.openai.com/api/docs/guides/token-counting
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY", None)
    if api_key is None:
        raise RuntimeError("api key not found")

    args = parse_arguments()
    messages = prepare_messages(args.user_prompt, args.verbose)
    client = get_client(api_key)
    generate_content(client, messages, args.verbose)

if __name__ == '__main__':
    main()
