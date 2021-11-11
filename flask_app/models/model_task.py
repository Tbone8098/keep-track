from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base
from flask_app import DATABASE_SCHEMA
import re

class Task(model_base.base_model):
    table = 'tasks'
    def __init__(self, data):
        super().__init__(data)
        self.name = data['name']
        self.description = data['description']
        self.is_completed = data['is_completed']
        self.category_id = data['category_id']
        self.user_id = data['user_id']
        self.is_main = data['is_main']

    @property
    def sub_tasks(self):
        query = f'SELECT * FROM tasks i1 JOIN inner_tasks ON inner_tasks.task_id = i1.id JOIN tasks i2 ON inner_tasks.inner_task_id = i2.id WHERE i1.id =  {self.id};'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            sub_tasks = []
            for task in results:
                data = {
                    'id': task['i2.id'],
                    'name': task['i2.name'],
                    'description': task['i2.description'],
                    'is_completed': task['i2.is_completed'],
                    'category_id': task['i2.category_id'],
                    'user_id': task['i2.user_id'],
                    'is_main': task['i2.is_main'],
                    'created_at': task['i2.created_at'],
                    'updated_at': task['i2.updated_at'],
                }
                sub_tasks.append(Task(data))
            return sub_tasks
        return results

    @classmethod
    def create_join(cls, data):
        query = 'INSERT INTO inner_tasks (task_id, inner_task_id) VALUES (%(task_id)s, %(inner_task_id)s)'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

    @classmethod
    def delete_one(cls, **data):
        task = Task.get_one(id=data['id'])
        sub_tasks = task.sub_tasks

        for sub_task in sub_tasks:
            sub_task.delete_one(id=sub_task.id)
        
        query = f'DELETE FROM tasks WHERE id = {task.id}'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query)

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 1:
            flash('name is required', 'err_task_name')
            is_valid=False

        # if len(data['description']) < 1:
        #     flash('description is required', 'err_task_description')
        #     is_valid=False

        return is_valid