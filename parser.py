import os
import json

from datetime import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

def parse_event(user_text):
    today= datetime.now().strftime("%Y-%m-%d")
    prompt=f"""
    You are an assistant that converts the user's natural-language schedule description into strict JSON.
    Return only one JSON object with the following fields:
    -title (string)
    -date (YYYY-MM-DD)
    -start_time (HH:MM)
    -end_time (HH:MM or null)
    -Today's date is: {today}.
    All relative dates (e.g., "tomorrow," "this Friday," "the day after tomorrow afternoon") must be interpreted based on this date.
    Example input:
    "Meeting with the CEO from 10 AM to 11 AM tomorrow morning"
    Example output:
    {{
      "title": "Meeting with the CEO",
      "date": "2025-11-22",
      "start_time": "10:00",
      "end_time": "11:00",
      
    }}
    User input: "{user_text}"
    Only output valid JSON. Do not include any extra text. Do not include backquote outside of curly braces
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return json.loads(chat_completion.choices[0].message.content)