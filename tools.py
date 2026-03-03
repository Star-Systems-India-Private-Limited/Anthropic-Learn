import datetime
import client

from anthropic.types import ToolParam


def get_current_datetime(date_format='%Y-%m-%d %H:%M:%S'):
    if not date_format:
        raise ValueError('Date format not specified')
    return datetime.datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam(
    {
        "name": "get_current_datetime",
        "description": "Returns the current date and time formatted according to the specified format",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                    "default": "%Y-%m-%d %H:%M:%S"
                }
            },
            "required": []
        }
    }
)

messages = []
client.add_user_message(messages, 'What is the exact time, formatted as HH:MM:SS?')
response = client.create_method(messages, tools=[get_current_datetime_schema])


current_date_time = get_current_datetime(**response.content[0].input)

client.add_assistant_message(messages, response.content)
messages.append({
    "role": 'user',
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[0].id,
        "content": current_date_time,
        "is_error": False
    }]
})

message = client.create_method(messages, tools=[get_current_datetime_schema])
print(message.content[0].text)