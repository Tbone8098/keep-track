from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    session['page'] = 'landing_page'
    return render_template('landing_page/index.html')


@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    session['page'] = 'dashboard'
    
    context = {
        'user': model_user.User.get_one(id=session['uuid'])
    }
    return render_template('dashboard/index.html', **context)

# @app.after_request
# def test(resp):
#     # print(request.remote_addr)
#     return resp

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'