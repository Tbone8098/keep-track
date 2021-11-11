from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_family
from flask_app.config.helper_func import generate_family_code


@app.route('/family/clear')
def clear_family():
    del session['family_id']
    return redirect('/register')

@app.route('/family/join', methods=['post'])
def join_family():
    family = model_family.Family.get_one(code=request.form['code'])
    if not family:
        flash('No family found by that Code', 'err_family_code')
        return redirect('/register')
    session['family_id'] = family.id
    return redirect('/register')

@app.route('/family/create', methods=['post'])
def create_family():
    code = generate_family_code()
    
    id = model_family.Family.create(name=request.form['name'], code=code)
    session['family_id'] = id 
    return redirect('/register')

@app.route('/family/<int:id>')
def show_family(id):
    return 'show family'

@app.route('/family/<int:id>/edit')
def edit_family(id):
    return 'edit family'

@app.route('/family/<int:id>/update', methods=['post'])
def update_family(id):
    return 'update family'

@app.route('/family/<int:id>/delete')
def delete_family(id):
    return 'delete family'