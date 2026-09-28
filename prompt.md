Convert the random-question CLI into a Streamlit app (app.py) using the
cli-to-streamlit skill.

Roster and questions are built up one at a time in the app: a text
input plus an "Add" button appends to the list, kept in
session_state, instead of reading from data.py. Show the current
list on screen. A Draw button picks one name and one question from
the accumulated lists, and there's a checkbox for "no repeats"
within the session.

On click, flash random name/question pairs on screen for about
3 seconds before revealing the actual pick.
