import os

from dotenv import load_dotenv

load_dotenv()

from anthropic import Anthropic
from anthropic.types import Message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

os.makedirs(MEDIA_DIR, exist_ok=True)


def get_haiku():
    return "claude-haiku-4-5"


def get_anthropic_client():
    client = Anthropic()
    return client


def add_user_message(messages, message):
    user_message = {'role': 'user', 'content': message.content if isinstance(message, Message) else message}
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {'role': 'assistant', 'content': message.content if isinstance(messages, Message) else message}
    messages.append(assistant_message)


def get_params(messages):
    params = {
        "model": get_haiku(),
        "max_tokens": 1000,
        "messages": messages,
    }
    return params


def create_method(messages, system=None, temperature=1.0, stop_sequences=None, tools=None):
    if stop_sequences is None:
        stop_sequences = []
    params = get_params(messages)
    params['temperature'] = temperature
    params['stop_sequences'] = stop_sequences
    if system:
        params["system"] = system
    if tools:
        params["tools"] = tools
    message = get_anthropic_client().messages.create(**params)
    return message


def chat(messages, system=None, temperature=1.0, stop_sequences=None, tools=None):
    message = create_method(messages, system, temperature, stop_sequences, tools)
    return message.content[0].text


def stream_basic(messages):
    params = get_params(messages)
    params['stream'] = True
    return get_anthropic_client().messages.create(**params)


def stream(messages):
    params = get_params(messages)
    return get_anthropic_client().messages.stream(**params)


def get_media_dir():
    return MEDIA_DIR


def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
