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

    # Prepare messages with system prompt if provided
    all_messages = []
    
    # Add system message if provided
    system_prompt = "You are a helpful assistant for Duke University, you answer questions about the university and partocular programs based on the user's request. Give out long and elaborate answers whenever possible. You have a few tools provided to you for usage, you them based on each question."
    all_messages.append({"role": "system", "content": system_prompt})
    
    # Add the rest of the messages
    all_messages.extend(messages)

    # Build request kwargs conditionally
    kwargs = {
        "model": "gpt-4o-mini",
        "messages": all_messages,
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
