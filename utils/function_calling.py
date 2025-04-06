from utils.openai_client import get_openai_client, get_chat_completion
from utils.all_tools import TOOLS, get_tool_function
import json

def get_response(messages, api_key):
    client = get_openai_client(api_key)
    if not client:
        return None
        
    response_message = get_chat_completion(client, messages, tools=TOOLS)
    
    # Check if the model wants to call a function
    if response_message.tool_calls:
        # Get the function call
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Get the function implementation
        function_to_call = get_tool_function(function_name)
        
        # Call the function
        function_response = function_to_call(**function_args)
        
        # Add the function response to the messages
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": function_name,
                    "arguments": tool_call.function.arguments
                }
            }]
        })
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(function_response)
        })
        
        # Get a final response from the model
        return get_chat_completion(client, messages, tools=TOOLS)
    
    return response_message
