# Initializes the package.
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# This is how flask is initialized; __name__ represents the name of the file that was run:
app = Flask(__name__)
# Storing database inside website folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///global_health_tracker.db'
# config variable encrypts and secures the cookies and session data related to the website:
app.config['SECRET_KEY'] = 'GHT APP'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from global_health_tracker import views
