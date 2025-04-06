import requests
from datetime import datetime
from urllib.parse import quote
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Setup OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Load groups and categories from the correct relative paths
GROUPS_FILE = "data/eventsData/groups.txt"
CATEGORIES_FILE = "data/eventsData/categories.txt"
OUTPUT_FILE = "data/eventsData/events_output.txt"

with open(GROUPS_FILE, "r") as f:
    groups_list = [line.strip() for line in f if line.strip()]

with open(CATEGORIES_FILE, "r") as f:
    categories_list = [line.strip() for line in f if line.strip()]

def get_event_filters_with_gpt(user_prompt, groups, categories):
    system_prompt = (
        "You are an assistant that extracts event filters for an event calendar API. "
        "Given a user query and lists of valid 'groups' and 'categories', extract:\n"
        "- the number of future days (default to 30 if not mentioned)\n"
        "- matching group names from the list\n"
        "- matching category names from the list\n\n"
        "Respond in JSON format as:\n"
        "{\n"
        '  "future_days": <int>,\n'
        '  "groups": [<list of strings>],\n'
        '  "categories": [<list of strings>]\n'
        "}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""User query: {user_prompt}

Available groups:
{groups}

Available categories:
{categories}
"""}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()

    return json.loads(content)

def fetch_filtered_events(groups=None, categories=None, future_days=1):
    base_url = "https://calendar.duke.edu/events/index.json"

    fixed_params = {
        "future_days": future_days,
        "local": "true",
        "feed_type": "simple"
    }

    query_parts = [f"{key}={value}" for key, value in fixed_params.items()]

    if groups and not ("all" in [g.lower() for g in groups]):
        query_parts += [f"gfu[]={quote(g)}" for g in groups]
    if categories and not ("all" in [c.lower() for c in categories]):
        query_parts += [f"cfu[]={quote(c)}" for c in categories]

    full_url = f"{base_url}?{'&'.join(query_parts)}"
    print(f"\n🔍 Constructed URL: {full_url}\n")

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()

        events = data.get("events", [])
        if not events:
            print("⚠️ No events found for the selected filters.\n")
            return

        print(f"📅 Found {len(events)} events. Saving to file...")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(f"🔗 Source URL:\n{full_url}\n\n")
            file.write(f"📅 Found {len(events)} upcoming events:\n\n")
            for event in events:
                title = event.get("summary", "No Title")
                description = event.get("description", "").strip()
                start_ts = event.get("start_timestamp", "")
                location = event.get("location", {}).get("address", "TBD")
                link = event.get("link", "")

                try:
                    start_dt = datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_start = start_dt.strftime("%b %d, %Y %I:%M %p")
                except:
                    formatted_start = start_ts

                file.write(f"🔹 {title}\n")
                file.write(f"   🕒 {formatted_start}\n")
                file.write(f"   📍 {location}\n")
                file.write(f"   🔗 {link}\n")
                file.write(f"   📝 {description[:150]}...\n\n" if description else "\n")

        print(f"✅ Saved to {OUTPUT_FILE}\n")

    except Exception as e:
        print(f"❌ Error fetching events: {e}")

if __name__ == "__main__":
    user_query = input("What kind of events are you looking for?\n> ")
    filters = get_event_filters_with_gpt(user_query, groups_list, categories_list)

    print("\n🧠 GPT-Extracted Filters:")
    print(json.dumps(filters, indent=2))

    groups = filters.get("groups", [])
    categories = filters.get("categories", [])
    future_days = filters.get("future_days", 30)

    fetch_filtered_events(
        groups=groups,
        categories=categories,
        future_days=future_days
    )