from flask import Flask
app = Flask(__name__)
app.secret_key = 'Whos your daddy? Goons your daddy!'

DATABASE_SCHEMA = 'keep_track_db'

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)