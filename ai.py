from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

client = OpenAI(

api_key=os.getenv(
"GROK_API_KEY"
),

base_url=
"https://api.x.ai/v1"

)

def ask_ai(question):

    try:

        response = client.chat.completions.create(

        model="grok-3-mini",

        messages=[

        {
        "role":"user",

        "content":question

        }

        ]

        )

        return response.choices[
        0
        ].message.content

    except Exception as e:

        print(e)

        return "AI Error Boss"