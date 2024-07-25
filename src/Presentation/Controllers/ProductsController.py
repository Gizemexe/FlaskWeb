from flask import Blueprint,jsonify,request

from src.Application.Features.Product.Queries.SearchProductsQuery import SearchProductsQuery
from src.Application.Features.Product.Queries.GetProductsByCategoryIdQuery import GetProductsByCategoryIdQuery
from src.Application.Features.Product.Mapping.ProductMapper import ProductMapper
from src.Infrastructure.Services.ProductService import ProductService
from src.Application.Features.Product.Queries.GetProductsQuery import GetProductsQuery
from src.Infrastructure.Repositories.ProductRepository import ProductsRepositoryImpl
import re

products = Blueprint('products', __name__, url_prefix="/api/v1/products")

def convert_to_direct_link(share_link):
    match = re.search(r'/d/([^/]+)/', share_link)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?id={file_id}'
    return share_link  # Eğer link uygun değilse orijinal linki döndür

# Ürünlerin resim bağlantılarını dönüştürme fonksiyonu
def convert_product_image_links(product_dto):
    if 'image' in product_dto and product_dto['image']:
        product_dto['image'] = convert_to_direct_link(product_dto['image'])
    return product_dto

# get all products
@products.route("/Products", methods=["GET"])  #ProductController
def get_products():
    try:
        products_repository = ProductsRepositoryImpl()
        query = GetProductsQuery(products_repository)
        product_service = ProductService(products_repository)
        result_set = product_service.get_all_products(query)
        result_set = [ProductMapper.to_response(product) for product in result_set]
        result_set = convert_product_image_links(result_set)
        return jsonify(result_set), 200
    except Exception as e:
        print('Error getting products:', e)
        return jsonify({'message': 'Failed to get products'}), 500

#get specific products
@products.route("/GetAllByCategoryId", methods=["GET"])
def get_product():
    category_id = request.args.get('categoryId')
    if category_id is None:
        return jsonify({"message": "Category ID is missing"}), 400

    try:
        get_products_by_category_query = GetProductsByCategoryIdQuery(category_id)
        product_service = ProductService(ProductsRepositoryImpl())
        result_set = product_service.get_products_by_category(get_products_by_category_query)
        result_set = [ProductMapper.to_response(ProductMapper.to_dto(product)) for product in result_set]
        result_set = convert_product_image_links(result_set)
        return jsonify(result_set), 200
    except Exception as e:
        print('Error getting products by category:', e)
        return jsonify({'message': 'Failed to get products by category'}), 500

@products.route('/SearchProducts', methods=['GET'])
def search_products():
    query = request.args.get('search')

    if not query:
        return jsonify([])
    try:
        search_query = SearchProductsQuery(query=query)
        product_service = ProductService(ProductsRepositoryImpl())
        result_set = product_service.search_products(search_query)
        result_set = [ProductMapper.to_response(product) for product in result_set]
        return jsonify(result_set), 200
    except Exception as e:
        print('Error searching products:', e)
        return jsonify({'message': 'Failed to search products'}), 500
