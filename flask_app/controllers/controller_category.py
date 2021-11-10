from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_category

@app.route('/category/new')
@app.route('/category/new/<int:category_id>')
def new_category(category_id=0):
    session['page'] = 'category_new'
    context = {
        'category_id': category_id
    }
    return render_template('category/category_new.html', **context)

@app.route('/category/create', methods=['post'])
def create_category():
    if not model_category.Category.validate(request.form):
        if 'category_id' in request.form:
            return redirect(f'/category/new/{request.form["category_id"]}')
        else:
            return redirect('/category/new')

    if 'category_id' in request.form:
        data = {
            **request.form,
            'user_id': session['uuid'],
            'is_main': 0
        }

        del data['category_id']

        id = model_category.Category.create(**data)
        model_category.Category.create_join({
            'category_id': int(request.form['category_id']),
            'inner_category_id': id
        })
    else:
        data = {
            **request.form,
            'user_id': session['uuid'],
            'is_main': 1
        }
        model_category.Category.create(**data)
    return redirect('/')

@app.route('/category/<int:id>')
def show_category(id):
    session['page'] = 'category_show'
    context = {
        'category': model_category.Category.get_one(id=id)
    }
    return render_template('category/category_show.html', **context)

@app.route('/category/<int:id>/edit')
def edit_category(id):
    return 'edit category'

@app.route('/category/<int:id>/update', methods=['post'])
def update_category(id):
    return 'update category'

@app.route('/category/<int:id>/delete')
def delete_category(id):
    model_category.Category.delete_one(id=id)
    return redirect('/')