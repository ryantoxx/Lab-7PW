from flask import request, jsonify
from models.database import db
from models.recipes import Recipe
from __main__ import app
from app import authenticate
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

def admin_required(fn):
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return jsonify({"error": "Admin access required"}), 401
        return fn(*args, **kwargs)
    return wrapper

# TOKEN CREATION
@app.route('/api/token', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username and password:
        if authenticate(username, password):
            access_token = create_access_token(identity=username)
            return jsonify({'Bearer': access_token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return jsonify({'error': 'Username and password required'}), 400

# GET REQUEST
@app.route('/api/recipes', methods=['GET'])
@jwt_required()
def get_recipes():
    try:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=3, type=int)  

        search_query = request.args.get('q', '')
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{search_query}%')).paginate(page=page, per_page=limit, error_out=False)
        data = [recipe.to_dict() for recipe in recipes]
        pagination_data = {
        'total_pages': recipes.pages,
        'total_items': recipes.total,
        'current_page': recipes.page,
        'per_page': recipes.per_page,
        'next_page': recipes.next_num,
        'prev_page': recipes.prev_num,
        'recipes': data
    }
        return jsonify(pagination_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
   
@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe_by_id(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe is not None:
        return jsonify({
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "servings": recipe.servings,
            "instructions": recipe.instructions
        }), 200
    else:
        return jsonify({"error": "Recipe not found"}), 404

# POST REQUEST
@app.route('/api/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    try:
        data = request.get_json()
        new_recipe = Recipe(**data)
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"message": "Recipe created successfully"}), 201
    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400

# PUT
@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    try:
        data = request.get_json()
        recipe = Recipe.query.get(recipe_id)
            
        if recipe is not None:
            
            for key, value in data.items():
                setattr(recipe, key, value)
                
            db.session.commit()
                
            return jsonify({"message": "Recipe updated successfully"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_recipe(recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        if recipe is not None:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted successfully"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



