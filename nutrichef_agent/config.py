# nutrichef_agent/config.py
import os
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

LLM_MODEL_NAME = "gemini-2.5-flash-lite" # Or "gemini-1.5-flash" if you want to try it
APP_NAME = "NUTRICHEF_AGENT"

# retry_config needs to be defined if used in Agent init
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)