import client
from client import add_user_message


def print_message():
    message = client.get_anthropic_client().messages.create(
        model=client.get_haiku(),
        max_tokens=1000,
        messages=[
            {
                "content": "Hello world!",
                "role": 'user'
            }
        ]
    )
    return message.content[0].text


# print(print_message())

def multi_turn_message():
    messages = []

    client.add_user_message(messages, 'Define quantum computing in one sentence')

    answer = client.chat(messages)

    client.add_assistant_message(messages, answer)

    add_user_message(messages, 'Write another sentence')

    final_message = client.chat(messages)
    messages.append(final_message)
    print(messages)

# multi_turn_message()

def math_prompt():
    messages = []
    system_prompt = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    """
    client.add_user_message(messages, 'How do I solve 5x + 2 = 3 for x?')
    answer = client.chat(messages)
    print(answer)
    final_message = client.chat(messages, system_prompt)
    print("---------")
    print(final_message)

# math_prompt()

def create_fun_with_stream():
    messages = []
    client.add_user_message(messages, 'Write a 1 sentence description of a fake database')
    stream = client.stream_basic(messages)
    for event in stream:
        print(event)

# create_fun_with_stream()

def test_stream():
    messages = []
    client.add_user_message(messages, 'Write a 1 sentence description of a fake database')
    with client.stream(messages) as stream:
        for event in stream.text_stream:
            print(event, end="")

# test_stream()