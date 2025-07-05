from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('note')

        if note_content:
            new_note = Note(content=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully!", category='success')
        else:
            flash("Note content is required.", category='error')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted successfully!", category='success')
            return jsonify({})
        else:
            flash("You do not have permission to delete this note.", category='error')