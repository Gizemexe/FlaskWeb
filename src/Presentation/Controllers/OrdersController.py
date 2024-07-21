from flask import Blueprint,jsonify,request
from src.Infrastructure.Services.OrderService import order_service
from src.Application.Security.JWT import Token
from src.Infrastructure.Database.database import db
from src.Domain.Entities.Order import Orders

orders = Blueprint('orders', __name__, url_prefix="/api/v1/orders")


# create order
@orders.route("/create", methods=["POST"])  #OrderController
def create_order():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.json

    orderNumber = data.get("orderNumber")
    total = data.get("total")
    address = data.get("address")
    status = data.get("status")

    new_order = Orders(
        UserId=user_id,
        OrderNumber=orderNumber,
        Total=total,
        Address=address,
        Status=status
    )

    print("New order:", new_order)

    new_order.save()

    # Siparişin JSON formatına dönüştürülmesi
    order_dict = {
        'orderNumber': new_order.OrderNumber,
        'total': new_order.Total,
        'address': new_order.Address,
        'status': new_order.Status
    }

    return jsonify({"message": "Order registered successfully", }, order_dict), 200

@orders.route("/GetAll", methods=["GET"])
async def get_all_orders():
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    response = await order_service.get_all_order_items(user_id)

    if response["success"]:
        return jsonify({"orderItems": response["orderItems"]}), 200

    else:
        return jsonify({'message': response["message"]}), 404


@orders.route("/GetOrderById", methods=["GET"])
def get_order_by_id():
    pass

@orders.route("/getOrderIdByOrderNumber", methods=["GET"])
def get_orderId_by_OrderNumber():
    order_number = request.args.get('orderNumber')
    order = Orders.query.filter_by(OrderNumber=order_number).first()
    if order:
        order_id = order.Id
        return jsonify({"orderId": order_id}), 200
    else:
        return jsonify({"error": "Order not found"}), 404


@orders.route("/updateStatus", methods=["POST"])
def update_status():
    data = request.get_json()

    if not data or 'orderId' not in data or 'status' not in data:
        return jsonify({"error": "Missing orderId or status in request body"}), 400

    order_id = data['orderId']
    status = data['status']
    order = Orders.query.filter_by(Id=order_id).first()

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    # Güncellenecek durumun kontrolü
    if status not in ['Onay Bekleniyor', 'Hazırlanıyor', 'Gönderildi', 'Tamamlandı']:
        return jsonify({"error": "Invalid status"}), 400

    # Siparişin durumunu güncelle
    order.Status = status
    db.session.commit()

    return jsonify({"status": "Order status updated successfully"}), 200
  
