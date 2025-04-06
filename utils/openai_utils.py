from dotenv import load_dotenv
from openai import OpenAI


def get_response(messages, api_key):
    if api_key:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        return response.choices[0].message
    
    else:
        return None
