from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.config import database_uri


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from app import views