import streamlit as st
from google import genai

MODEL = "gemini-3.8-flash"

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
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    response = client.models.generate_content(model=MODEL, contents=PROMPT)
    return response.text.strip()
