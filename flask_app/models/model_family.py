from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_user
from flask_app import DATABASE_SCHEMA
import re

class Family(model_base.base_model):
    table = 'families'
    def __init__(self, data):
        super().__init__(data)
        self.name = data['name']
        self.code = data['code']

    @property
    def members(self):
        query = f'SELECT * FROM families JOIN users ON families.id = users.family_id WHERE families.id = {self.id};'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            members = []
            for member in results:
                data = {
                    'id': member['users.id'],
                    'first_name': member['first_name'],
                    'last_name': member['last_name'],
                    'email': member['email'],
                    'hash_pw': member['hash_pw'],
                    'is_varified': member['is_varified'],
                    'family_id': self.id,
                    'created_at': member['users.created_at'],
                    'updated_at': member['users.updated_at'],
                }
                members.append(model_user.User(data))
            return members
        return results