from flask import jsonify, request, Blueprint
from src.Infrastructure.Database.database import db
from src.Domain.Entities.OrderDetail import OrderDetails
from src.Application.Security.JWT import Token

orderDetails = Blueprint('orderDetails', __name__, url_prefix="/api/v1/orderDetails")

# create orderDetail
@orderDetails.route("/create", methods=["POST"])  #OrderDetailsController
def create_order_details():
    try:
        data = request.json
        order_id = data.get('orderId')
        order_details = data.get("orderDetails")

        for order_detail in order_details:
            product_id = order_detail.get('productId')
            quantity = order_detail.get('quantity')
            unit_price = order_detail.get('unitPrice')

            # Check if required fields are present
            if order_id is None or product_id is None or quantity is None or unit_price is None:
               return jsonify({"message": "Missing required fields"}), 400

            # Sipariş detayı oluştur
            order_detaill = OrderDetails(
                OrderId=order_id,
                ProductId=product_id,
                Quantity=quantity,
                UnitPrice=unit_price
            )

            # Veritabanına kaydet
            db.session.add(order_detaill)

        db.session.commit()

        return jsonify({"message": "Order details created successfully"}), 200
    except Exception as e:
      return jsonify({"message": str(e)}), 500
