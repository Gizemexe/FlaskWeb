from flask import Blueprint,jsonify
from src.Domain.Entities.Category import Categories
from src.Domain.Schemas.CategorySchema import schema

categories = Blueprint('categories', __name__, url_prefix="/api/v1/categories")

# get all Categories
@categories.route("/GetAll", methods=["GET"])  #CategoriesController
def get_categories():
    categories = Categories.query.all()
    result_set = schema.dump(categories)
    return jsonify(result_set), 200
