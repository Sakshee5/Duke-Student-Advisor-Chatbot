import json
from utils.openai_client import get_chat_completion, get_openai_client
from tools.memDatabaseTool import search as mem_search
from tools.prattDatabaseTool import search as pratt_search
from tools.curriculumTool import get_courses, get_course_details
from tools.eventsTool import get_events
from tools.aipiDatabaseTool import get_AIPI_details
from tools.tools_schema import TOOLS_SCHEMA

def get_tool_function(tool_name: str):
    """Get the actual function implementation for a tool name"""
    tool_functions = {
        "mem_search": mem_search,
        "pratt_search": pratt_search,
        "get_courses": get_courses,
        "get_course_details": get_course_details,
        "get_events": get_events,
        "get_AIPI_details": get_AIPI_details
    }
    return tool_functions.get(tool_name) 

def get_response(messages, api_key, first_call=True):
    client = get_openai_client(api_key)
    if not client:
        yield "Error: Could not initialize OpenAI client"
        return None
    
    if first_call:
        yield "Analyzing your question..."
    else:
        yield "Analyzing whether another tool call is needed..."
    response_message = get_chat_completion(client, messages, tools=TOOLS_SCHEMA)
    
    # Check if the model wants to call a function
    if response_message.tool_calls:
        # Get the function call
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        yield f"Executing Tool: {function_name}..."
        
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
        
        yield "Tool Call Completed. Processing the results..."
        
        for status in get_response(messages, api_key, first_call=False):
            yield status

        return
    
    yield "Generating final response..."
    yield response_message
