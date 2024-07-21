from flask import Flask, request, jsonify, Blueprint
import uuid

pay = Blueprint('pay', __name__, url_prefix='/api/v1/pay')

# Simulate tokenization by generating a UUID as a token // mock
@pay.route('/tokenize', methods=['POST'])
def tokenize():
    data = request.json
    if not all(key in data for key in ("card_number", "expiry_date", "cvv", "card_holder_name")):
        return jsonify({"error": "Missing card information"}), 400

    # Generate a mock token
    token = str(uuid.uuid4())
    return jsonify({"token": token})


# Simulate detokenization
@pay.route('/detokenize', methods=['POST'])
def detokenize():
    data = request.json
    if "token" not in data:
        return jsonify({"error": "Missing token"}), 400

    # For demo purposes, return mock card info
    card_info = {
        "card_number": "4111111111111111",
        "expiry_date": "12/25",
        "cvv": "123",
        "card_holder_name": "John Doe"
    }
    return jsonify(card_info)


@pay.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    if "token" not in data or "amount" not in data:
        return jsonify({"error": "Missing payment information"}), 400

    # Simulate payment processing
    payment_status = "success" if data["token"] and data["amount"] > 0 else "failure"

    return jsonify({"status": payment_status})


@pay.route('/finalize_order', methods=['POST'])
def finalize_order():
    data = request.json
    if "order_id" not in data or "status" not in data:
        return jsonify({"error": "Missing order information"}), 400

    # Mock order finalization
    order_status = data["status"]

    # Normally, you would update the order status in your database here.
    print(f"Order ID: {data['order_id']} has been {order_status}")

    return jsonify({"order_id": data["order_id"], "status": order_status})
