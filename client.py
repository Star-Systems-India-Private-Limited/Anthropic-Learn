from dotenv import load_dotenv

load_dotenv()

from anthropic import Anthropic


def get_haiku():
    return "claude-haiku-4-5-20251001"


def get_anthropic_client():
    client = Anthropic()
    return client


def add_user_message(messages, text):
    user_message = {'role': 'user', 'content': text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {'role': 'assistant', 'content': text}
    messages.append(assistant_message)


def get_params(messages):
    params = {
        "model": get_haiku(),
        "max_tokens": 1000,
        "messages": messages,
    }
    return params


def chat(messages, system=None):
    params = get_params(messages)
    if system:
        params["system"] = system
    message = get_anthropic_client().messages.create(**params)
    return message.content[0].text


def stream_basic(messages):
    params = get_params(messages)
    params['stream'] = True
    return get_anthropic_client().messages.create(**params)


def stream(messages):
    params = get_params(messages)
    return get_anthropic_client().messages.stream(**params)
