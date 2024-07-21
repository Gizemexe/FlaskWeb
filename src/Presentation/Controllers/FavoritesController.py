from flask import Blueprint, jsonify, request
    
from src.Application.Features.Favorite.Commands.AddFavoriteCommand import AddFavoriteCommand
from src.Application.Features.Favorite.Commands.RemoveFavoriteCommand import RemoveFavoriteCommand
from src.Application.Features.Favorite.Queries.GetFavoritesQuery import GetFavoritesQuery
from src.Infrastructure.Services.FavoriteService import FavoriteService
from src.Infrastructure.Repositories.FavoriteRepository import FavoritesRepositoryImpl
from src.Application.Features.Favorite.Mapping.FavoriteMapper import FavoriteMapper
from src.Domain.Entities.Product import Products
from src.Application.Security.JWT import Token

favorites = Blueprint('favorites', __name__, url_prefix="/api/v1/favorites")

@favorites.route("/AddFavorite", methods=["POST"])
def add_favorite():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    try:
        favorite_service = FavoriteService(FavoritesRepositoryImpl())
        command = AddFavoriteCommand(user_id=user_id, product_id=product_id)
        new_favorite = favorite_service.add_favorite(command)
        return jsonify(FavoriteMapper.to_response(new_favorite)), 201
    except Exception as e:
        print('Error adding favorite:', e)
        return jsonify({'message': 'Failed to add favorite'}), 500

@favorites.route("/GetFavorites", methods=["GET"])
def get_favorites():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    try:
        favorite_service = FavoriteService(FavoritesRepositoryImpl())
        query = GetFavoritesQuery(user_id=user_id)
        favorites = favorite_service.get_favorites_by_user(query)

        favorite_products = []
        for favorite in favorites:
            product = Products.query.get(favorite.product_id)
            if product:
                favorite_products.append({
                    'id': product.Id,
                    'code': product.Code,
                    'name': product.Name,
                    'price': product.Price,
                    'description': product.Description,
                    'imagePath': product.Image or '',
                    'stock': product.Stock,
                })

        return jsonify({'favorite_products': favorite_products}), 200
    except Exception as e:
        print('Error getting favorites:', e)
        return jsonify({'message': 'Failed to get favorites'}), 500

@favorites.route("/RemoveFavorite", methods=["DELETE"])
def remove_favorite():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    try:
        favorite_service = FavoriteService(FavoritesRepositoryImpl())
        command = RemoveFavoriteCommand(user_id=user_id, product_id=product_id)
        favorite_service.remove_favorite(command)
        return jsonify({'message': 'Product removed from favorites'}), 200
    except Exception as e:
        print('Error removing favorite:', e)
        return jsonify({'message': 'Failed to remove favorite'}), 500
