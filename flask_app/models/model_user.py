from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_family, model_category
from flask_app import DATABASE_SCHEMA

class User(model_base.base_model):
    table = 'users'
    def __init__(self, data):
        super().__init__(data)
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.hash_pw = data['hash_pw']
        self.is_varified = data['is_varified']
        self.family_id = data['family_id']
    
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def categories(self):
        query = f'SELECT * FROM categories WHERE user_id = {self.id} AND is_main = 1'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            all_categories = []
            for category in results:
                all_categories.append(model_category.Category(category))
        return results


    @property
    def family(self):
        return model_family.Family.get_one(id=self.family_id)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('First name is required', 'err_user_reg_first_name')
            is_valid = False
        if len(data['last_name']) < 1:
            flash('Last name is required', 'err_user_reg_last_name')
            is_valid = False
        if len(data['email']) < 1:
            flash('Email is required', 'err_user_reg_email')
            is_valid = False

        if len(data['pw']) < 1:
            flash('Password is required', 'err_user_reg_pw')
            is_valid = False
        if len(data['confirm_pw']) < 1:
            flash('Confirm Password is required', 'err_user_reg_confirm_pw')
            is_valid = False
        if data['confirm_pw'] != data['pw']:
            flash('Passwords do not match', 'err_user_reg_confirm_pw')
            is_valid = False
        return is_valid

