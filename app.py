import random
import time

import streamlit as st

from rand_question_v4.selector import draw, pick
from use_gemini import generate_question

FLASH_SECONDS = 3.0
FLASH_DELAY_SECONDS = 0.1

defaults = {
    "rng": random.Random(),
    "roster": [],
    "question_list": [],
    "used_names": set(),
    "used_questions": set(),
    "current_pick": None,
    "history": [],
    "animate": False,
    "message": None,  # (level, text) shown once on the next render
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def format_pick(chosen_name, chosen_question):
    return f"{chosen_name}, please answer: {chosen_question}"


st.title("Random Question Draw")

# --- Event handlers: mutate state only ---------------------------------------

with st.form("add_name_form", clear_on_submit=True):
    new_name = st.text_input("Name")
    if st.form_submit_button("Add name") and new_name.strip():
        st.session_state.roster.append(new_name.strip())

with st.form("add_question_form", clear_on_submit=True):
    new_question = st.text_input("Question")
    if st.form_submit_button("Add question") and new_question.strip():
        st.session_state.question_list.append(new_question.strip())

if st.button("Generate AI Question"):
    try:
        with st.spinner("Asking Gemini..."):
            ai_question = generate_question()
    except Exception:
        st.session_state.message = (
            "error",
            "Couldn't get an AI question. Check that GEMINI_API_KEY is set in "
            ".streamlit/secrets.toml and try again.",
        )
    else:
        st.session_state.question_list.append(ai_question)
        st.session_state.message = ("success", f"AI question added: {ai_question}")

no_repeats = st.checkbox("No repeats within this session")

col_draw, col_reset = st.columns(2)

with col_draw:
    if st.button("Draw"):
        if not st.session_state.roster or not st.session_state.question_list:
            st.session_state.message = (
                "error",
                "Add at least one name and one question before drawing.",
            )
        else:
            used_names = st.session_state.used_names if no_repeats else ()
            used_questions = st.session_state.used_questions if no_repeats else ()
            try:
                chosen = draw(
                    st.session_state.roster,
                    st.session_state.question_list,
                    st.session_state.rng,
                    used_names,
                    used_questions,
                )
            except ValueError:
                st.session_state.message = (
                    "warning",
                    "Every name or question has already been drawn. "
                    "Add more, or press Reset.",
                )
            else:
                st.session_state.used_names.add(chosen[0])
                st.session_state.used_questions.add(chosen[1])
                st.session_state.current_pick = chosen
                st.session_state.history.append(chosen)
                st.session_state.animate = True

with col_reset:
    if st.button("Reset"):
        for key in ("roster", "question_list", "used_names", "used_questions", "history"):
            st.session_state[key] = type(defaults[key])()
        st.session_state.current_pick = None
        st.session_state.animate = False

# --- Rendering: always reads from session_state ------------------------------

if st.session_state.message:
    level, text = st.session_state.message
    getattr(st, level)(text)
    st.session_state.message = None

st.subheader("Roster")
st.write(st.session_state.roster or "No names added yet.")

st.subheader("Questions")
st.write(st.session_state.question_list or "No questions added yet.")

st.subheader("Result")
placeholder = st.empty()

if st.session_state.animate:
    deadline = time.monotonic() + FLASH_SECONDS
    while time.monotonic() < deadline:
        flash = (
            pick(st.session_state.roster, st.session_state.rng),
            pick(st.session_state.question_list, st.session_state.rng),
        )
        placeholder.write(format_pick(*flash))
        time.sleep(FLASH_DELAY_SECONDS)
    st.session_state.animate = False

if st.session_state.current_pick:
    placeholder.write(format_pick(*st.session_state.current_pick))
else:
    placeholder.write("No draw yet.")

if st.session_state.history:
    st.subheader("History")
    for past_name, past_question in reversed(st.session_state.history):
        st.write(f"- {format_pick(past_name, past_question)}")
