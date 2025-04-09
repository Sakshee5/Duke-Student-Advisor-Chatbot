from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_openai_client(api_key):
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def get_chat_completion(client, messages, tools=None, tool_choice="auto"):
    if not client:
        return None
        
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
    )
    
    return response.choices[0].message 