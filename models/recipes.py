from models.database import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    
    def __init__(self, title, ingredients, servings, instructions):
        self.title = title
        self.ingredients = ingredients
        self.servings = servings
        self.instructions = instructions
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'servings': self.servings,
            'instructions': self.instructions
        }
