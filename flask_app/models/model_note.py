from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base
from flask_app import DATABASE_SCHEMA
import re

class Note(model_base.base_model):
    table = 'notes'
    def __init__(self, data):
        super().__init__(data)
        self.name = data['name']
        self.content = data['content']
    
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 1:
            is_valid = False
            flash('Name is required', 'err_note_name')

        if len(data['content']) < 1:
            is_valid = False
            flash('Content is required', 'err_note_content')
        
        return is_valid