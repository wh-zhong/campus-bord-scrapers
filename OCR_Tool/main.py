import os
from dotenv import load_dotenv
import requests
import base64

load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")

url = "https://genai.rcac.purdue.edu/api/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

with open("./test_images/flyer2.jpeg", "rb") as image_file:
    image = base64.b64encode(image_file.read()).decode("utf-8")

body = {
    "model": "gemma4:26b-a4b",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}"
                    }
                },
                {
                    "type": "text",
                    "text": "Given this flyer, give me the event details. You should include the title of the event, its location (which should include the building), its start and end time (I want these in UNIX time and if the end time doesn't exist, assume the event is one hour long), a short description if possible, and the main organization involved in the event (there should only be one organization). Return all this information in the form of a JSON file.",
                }
            ],
        },
    ],
    "stream": False,
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "event_details",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "orgs": {"type": "string"},
                    "loc": {"type": "string"},
                    "startTime": {"type": "number"},
                    "endTime": {"type": "number"},
                    "desc": {"type": "string"},
                },
                "required": ["title", "loc", "startTime", "endTime"],
            },
        },
    },
}

response = requests.post(url, headers=headers, json=body, timeout=120)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])