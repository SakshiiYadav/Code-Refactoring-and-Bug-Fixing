from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Dictionary to store notes for each session
user_notes = {}

@app.route('/', methods=["GET", "POST"])
def index():
    # Generate a session ID if it doesn't exist
    if 'id' not in session:
        session['id'] = os.urandom(16).hex()  # Generate a random 32-character hexadecimal string

    # Get or initialize notes for the current session
    session_notes = user_notes.get(session['id'], [])
    
    if request.method == "POST":
        if "note" in request.form:
            note = request.form["note"]
            if note.strip():  
                session_notes.append(note.strip())
        elif "delete_note" in request.form:
            note_to_delete = request.form["delete_note"]
            if note_to_delete in session_notes:
                session_notes.remove(note_to_delete)
        # Update the notes for the current session
        user_notes[session['id']] = session_notes
    
    return render_template("home.html", notes=session_notes)

if __name__ == '__main__':
    app.run(debug=True)
