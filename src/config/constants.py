import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model_name": "gpt-4-1106-preview"
    # "model_name": "gpt-3.5-turbo"
}