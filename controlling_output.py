import client

prompt = """
Generate three different sample github cli commands. Each should be very short"
"""

messages = []

client.add_user_message(messages, prompt)
client.add_assistant_message(messages, 'Here all three commands in a single block without any comments:\n```bash')

answer = client.chat(messages, stop_sequences=['```'])

print(answer)