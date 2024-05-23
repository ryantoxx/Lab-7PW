from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.recipes import Recipe
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
    jwt = JWTManager(app)
    
    import routes
    app.run(port=6060, debug=True)


