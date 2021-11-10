from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_note

@app.route('/note/new/<int:category_id>')
def new_note(category_id):
    session['page'] = 'note_new'
    session['category_id'] = category_id
    return render_template('notes/note_new.html')

@app.route('/note/create', methods=['post'])
def create_note():
    category_id = session['category_id']

    
    del session['category_id']
    return redirect(f'/category/{category_id}')

@app.route('/note/<int:id>')
def show_note(id):
    return 'show note'

@app.route('/note/<int:id>/edit')
def edit_note(id):
    return 'edit note'

@app.route('/note/<int:id>/update', methods=['post'])
def update_note(id):
    return 'update note'

@app.route('/note/<int:id>/delete')
def delete_note(id):
    return 'delete note'