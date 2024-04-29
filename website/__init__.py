from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME='database.db'

def create_app():
    app=Flask(__name__)
    
#################  for importing all the blue prints  #########################################
    from .views import views
    from .auth import auth
    app.config['SECRET_KEY']='sdfsdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Corrected key name
   

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

#################  database  ##########################################
    db.init_app(app) 
    from .models import User,Note
    create_database(app)
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))       


    return app

def create_database(app):
    with app.app_context():
        if not path.exists('website/'+DB_NAME):
            db.create_all()