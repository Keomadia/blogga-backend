from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)  

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flask_blogga_db_user:2HqlPA71gjDk0SstSwEbl25rQe64eSmx@dpg-d0aacdbuibrs73blmu80-a.oregon-postgres.render.com/flask_blogga_db"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

    

db = SQLAlchemy(app)
migrate = Migrate(app, db)

