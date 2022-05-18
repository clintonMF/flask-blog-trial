from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db_name = 'blogdatabase.sqlite'
db = SQLAlchemy()

def create_app():
    """this function is used for creating and initializing the app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "just a secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    
    
    from .views import views
    from .auth import auth
    from .models import User,Post,Comment,Like
    
    
    
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    
    db.init_app(app) #for creating the database
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" #this takes users who aren't looged in to the login page
    login_manager.init_app(app)
    
    create_database(app)
    
    @login_manager.user_loader
    def load_user(id):
        """this function is used to store user session data"""
        return User.query.get(int(id))
    
    return app



def create_database(app):
    """To create the database"""
    if not path.exists('website' + db_name):
        db.create_all(app=app)
        print("database created")