from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_task, model_category

@app.route('/task/new/<int:category_id>')
@app.route('/task/new/<int:category_id>/<int:task_id>')
def new_task(category_id, task_id=0):
    session['page'] = 'task_new'
    session['category_id'] = category_id
    print(f"set category_id into session {session['category_id']}")
    if task_id > 0:
        print("set task_id in session")
        session['task_id'] = task_id
    return render_template('tasks/task_new.html')

@app.route('/task/create', methods=['post'])
def create_task():
    if not model_task.Task.validate(request.form):
        return redirect('/task/new')

    category = model_category.Category.get_one(id=session['category_id'])
    if not category.user_id == session['uuid']:
        return redirect(f'/task/new/{session["category_id"]}')
    
    if 'task_id' in session:
        task = model_task.Task.get_one(id=session['task_id'])
        if task.user_id != session['uuid']:
            return redirect(f'/task/new/{session["category_id"]}')

    data = {
        **request.form,
        'category_id': session['category_id'],
        'user_id': session['uuid'],
    }
    if 'task_id' in session:
        data['is_main'] = 0
    else:
        data['is_main'] = 1

    id = model_task.Task.create(**data)

    if 'task_id' in session:
        data = {
            'task_id': session['task_id'],
            'inner_task_id': id,
        }

        model_task.Task.create_join(data)
    
        task_id = session['task_id']
        del session['task_id']
        del session['category_id']
        return redirect(f"/task/{task_id}")
        
    del session['category_id']
    return redirect(f"/category/{category.id}")

@app.route('/task/<int:id>')
def show_task(id):
    context = {
        'task': model_task.Task.get_one(id=id)
    }
    return render_template('tasks/task_show.html', **context)

@app.route('/task/<int:id>/edit')
def edit_task(id):
    return 'edit task'

@app.route('/task/<int:id>/update', methods=['post'])
def update_task(id):
    return 'update task'

@app.route('/task/<int:task_id>/complete')
def complete_task(task_id):
    task = model_task.Task.get_one(id=task_id)

    if task.is_completed:
        completed = False
    else:
        completed = True
    print(completed)

    task.update_one(id=task_id ,is_completed=completed)
    return redirect(f"/category/{task.category_id}")

@app.route('/task/<int:id>/delete')
def delete_task(id):
    task = model_task.Task.get_one(id=id)
    model_task.Task.delete_one(id=id)
    return redirect(f'/category/{task.category_id}')