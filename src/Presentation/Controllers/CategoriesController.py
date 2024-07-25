from flask import Blueprint,jsonify
from src.Application.Features.Category.Mapping.CategoryMapper import CategoryMapper
from src.Infrastructure.Services.CategoryService import CategoryService
from src.Application.Features.Category.Queries.GetCategoriesQuery import GetCategoriesQuery
from src.Infrastructure.Repositories.CategoryRepository import CategoriesRepositoryImpl
import re

categories = Blueprint('categories', __name__, url_prefix="/api/v1/categories")

def convert_to_direct_link(share_link):
    match = re.search(r'/d/([^/]+)/', share_link)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?id={file_id}'
    return share_link  # Eğer link uygun değilse orijinal linki döndür

# Ürünlerin resim bağlantılarını dönüştürme fonksiyonu
def convert_category_image_links(category_dto):
    if 'image' in category_dto and category_dto['image']:
        category_dto['image'] = convert_to_direct_link(category_dto['image'])
    return category_dto

# get all Categories
@categories.route("/GetAll", methods=["GET"])  #CategoriesController
def get_categories():
    try:
        categories_repository = CategoriesRepositoryImpl()
        query = GetCategoriesQuery(categories_repository)
        category_service = CategoryService(categories_repository)
        result_set = category_service.get_all_categories(query)
        result_set = [CategoryMapper.to_response(category) for category in result_set]
        result_set = convert_category_image_links(result_set)
        return jsonify(result_set), 200
    except Exception as e:
        print('Error getting products:', e)
        return jsonify({'message': 'Failed to get products'}), 500



