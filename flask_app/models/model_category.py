from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_task
from flask_app import DATABASE_SCHEMA
import re

class Category(model_base.base_model):
    table = 'categories'
    def __init__(self, data):
        super().__init__(data)
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.is_public = data['is_public']

    @property
    def parent(self):
        query = f'SELECT * FROM inner_categories JOIN categories ON categories.id = inner_categories.category_id WHERE inner_categories.inner_category_id = {self.id};'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            data = {
                'id': results[0]['id'],
                'name': results[0]['name'],
                'description': results[0]['description'],
                'user_id': results[0]['user_id'],
                'is_public': results[0]['is_public'],
                'created_at': results[0]['created_at'],
                'updated_at': results[0]['updated_at'],
            }
            return Category(data)
        return results

    @property
    def inner_categories(self):
        query = f'SELECT * FROM categories l1 JOIN inner_categories ON inner_categories.category_id = l1.id JOIN categories l2 ON inner_categories.inner_category_id = l2.id WHERE l1.id = {self.id};'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        print(results)
        if results:
            categories = []
            for category in results:
                data = {
                    'id': category['l2.id'],
                    'name': category['l2.name'],
                    'description': category['l2.description'],
                    'user_id': category['l2.user_id'],
                    'is_public': category['l2.is_public'],
                    'created_at': category['l2.created_at'],
                    'updated_at': category['l2.updated_at'],
                }
                categories.append(Category(data))
            return categories
        return results
        
    @property
    def tasks(self):
        query = f'SELECT * FROM categories JOIN tasks ON tasks.category_id = categories.id WHERE categories.id = {self.id}'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            tasks = []
            for item in results:
                data = {
                    'id': item['tasks.id'],
                    'name': item['tasks.name'],
                    'description': item['tasks.description'],
                    'is_completed': item['is_completed'],
                    'user_id': item['user_id'],
                    'is_main': item['tasks.is_main'],
                    'category_id': self.id,
                    'created_at': item['tasks.created_at'],
                    'updated_at': item['tasks.updated_at'],
                }
                tasks.append(model_task.Task(data))
            return tasks
        return results

    @classmethod
    def create_join(cls, data):
        query = 'INSERT INTO inner_categories (category_id, inner_category_id) VALUES (%(category_id)s, %(inner_category_id)s)'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 1:
            flash('Name is required', 'err_category_name')
            is_valid = False
        
        # if len(data['description']) < 1:
        #     flash('description is required', 'err_category_description')
        #     is_valid = False
        
        return is_valid