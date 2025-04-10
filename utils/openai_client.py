from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def get_openai_client(api_key):
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def get_chat_completion(client, messages, tools=None, tool_choice="auto"):
    if not client:
        return None

    # Build request kwargs conditionally
    kwargs = {
        "model": "gpt-4o-mini",
        "messages": messages,
    }

    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice

    try:
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message
    except Exception as e:
        print(f"❌ OpenAI API call failed: {e}")
        return None

def get_embeddings_model(api_key=None):
    """
    Creates and returns an OpenAIEmbeddings object using the provided API key
    """
    if not api_key:
        return None

    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )
