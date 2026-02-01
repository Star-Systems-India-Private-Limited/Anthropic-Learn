import json
import os

import client
from client import add_assistant_message


def generate_dataset():
    prompt = """
    Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
      {
        "task": "Description of task",
        "format": "json" or "python" or "regex
      },
      ...additional
    ]
    ```
    
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code
    
    Please generate 3 objects.
    """
    return prompt


def test_eval():
    messages = []
    client.add_user_message(messages, generate_dataset())
    add_assistant_message(messages, '```json')
    text = client.chat(messages, stop_sequences=['```'])
    with open(os.path.join(client.get_media_dir(), 'dataset.json'), 'w') as f:
        json.dump(json.loads(text), f, indent=2)


test_eval()
