import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-3.8-flash"

# Retry automatically when Gemini is busy (503) or rate-limited (429).
RETRY = types.HttpRetryOptions(attempts=4, http_status_codes=[429, 503])

PROMPT = """
Generate ONE funny, everyday life question to a randomly selected individual at a break-ice event.
Requirements:
- concise
- do not provide the answer; output only the question
"""


def generate_question():
    """Ask Gemini for one icebreaker question and return its text.

    The client is created here (not at import time) so a missing or bad
    key raises when the button is clicked, where app.py can catch it.
    """
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(retry_options=RETRY),
    )
    response = client.models.generate_content(model=MODEL, contents=PROMPT)
    return response.text.strip()
