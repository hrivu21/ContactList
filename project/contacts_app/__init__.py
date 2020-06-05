from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "5da5ea90223c3d8d5843"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site1.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from contacts_app import routes
