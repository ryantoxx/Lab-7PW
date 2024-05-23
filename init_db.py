from app import create_app, db
from models.recipes import Recipe

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()

if __name__ == "__main__":
    init_database()
