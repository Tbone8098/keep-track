from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

@app.route('/login')
def login():
    session['page'] = 'login'
    return render_template('landing_page/login.html')

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')

@app.route('/register')
def register():
    session['page'] = 'register'

    return render_template('landing_page/register.html')

@app.route('/user/settings')
def user_settings():
    session['page'] = 'user_settings'
    user = model_user.User.get_one(id=session['uuid'])
    context = {
        'user': user,
    }
    return render_template('settings/index.html', **context)

@app.route('/user/create', methods=['post'])
def create_user():
    if not model_user.User.validate(request.form):
        return redirect('/register')
    
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'family_id': session['family_id'],
        'hash_pw': hash_pw
    }

    del data['pw']
    del data['confirm_pw']

    id = model_user.User.create(**data)
    session['uuid'] = id
    del session['family_id']

    return redirect('/')

@app.route('/user/<int:id>')
def show_user(id):
    return 'show user'

@app.route('/user/<int:id>/edit')
def edit_user(id):
    return 'edit user'

@app.route('/user/<int:id>/update', methods=['post'])
def update_user(id):
    return 'update user'

@app.route('/user/<int:id>/delete')
def delete_user(id):
    return 'delete user'