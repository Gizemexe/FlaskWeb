from flask import Blueprint,jsonify,request

from src.Infrastructure.Services.CartService import cart_service
from src.Application.Security.JWT import Token


carts = Blueprint('carts', __name__, url_prefix="/api/v1/carts")

# get all products
@carts.route("/GetAll", methods=["GET"])  #CartController
async def get_cart():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    response = await cart_service.get_all_cart_items(user_id)

    if response["success"]:
        return jsonify(response["cartItems"]), 200
    else:
        return jsonify({'message': response["message"]}), 404


@carts.route('/add', methods=['POST'])
async def add():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    request_data = request.get_json()
    response = await cart_service.add_item_to_cart(user_id, request_data)
    return jsonify(response)

@carts.route('/update', methods=['PUT'])
async def update():
    request_data = request.get_json()
    cart_id = request_data.get("id")  # cartID
    if not cart_id:
        return jsonify({'message': 'Cart ID is required'}), 400

    response = await cart_service.update_cart_item(cart_id, request_data)
    return jsonify(response)


@carts.route('/remove', methods=['DELETE'])
async def remove():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    cart_id = request.args.get('cartId')
    if cart_id is None:
        return jsonify({'message': 'Cart ID is required'}), 400

    response = await cart_service.remove_cart(cart_id, user_id)

    return jsonify(response)



