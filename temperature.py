import client

messages = []

client.add_user_message(messages, 'Generate one joke in tamil.')

def chat(_messages, temperature=1.0):
    params = client.get_params(_messages)
    params['temperature'] = temperature
    message = client.get_anthropic_client().messages.create(
        **params
    )
    return message.content[0].text

def check_with_low():
    message = chat(messages, 0.1)
    print(message)

check_with_low()
print('____' * 50)
def check_with_high():
    message = chat(messages, 0.9)
    print(message)

check_with_high()
print('____' * 50)

def check_with_medium():
    message = chat(messages, 0.5)
    print(message)

check_with_medium()