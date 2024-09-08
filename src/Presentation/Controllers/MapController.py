import os
import requests
from flask import Blueprint,jsonify,request
from src.Domain.Entities.Order import Orders
from googlemaps import Client
from src.config import Config

#API_KEY = os.environ.get("API_KEY")
gmaps = Client(key=Config.API_KEY)

map = Blueprint('map', __name__, url_prefix="/api/v1/map")

@map.route('/convert', methods=['GET'])
def convert_addresses():
    address = request.args.get('address')  # Adresi al

    if not address:
        return jsonify({'error': 'Adres belirtilmedi'}), 400

    geocode_result = gmaps.geocode(address)  # Adresi Google Haritalar API'sine göndererek enlem-boylam bilgisine dönüştür

    if geocode_result and 'geometry' in geocode_result[0]:
        location = geocode_result[0]['geometry']['location']
        converted_address = {
            "latitude": location['lat'],
            "longitude": location['lng']
        }
        return jsonify(converted_address), 200
    else:
        return jsonify({'error': 'Adres dönüştürülemedi'}), 500

@map.route('/send', methods=['POST'])
def send_to_server():
    orders = Orders.query.all()

    converted_addresses = []
    for order in orders:
        # Her bir siparişin adresini al
        address = order.Address
        # Adresi Google Haritalar API'sine göndererek enlem-boylam bilgisine dönüştür
        geocode_result = gmaps.geocode(address)
        if geocode_result and 'geometry' in geocode_result[0]:
            location = geocode_result[0]['geometry']['location']
            # Dönüştürülmüş adresi listeye ekle
            converted_addresses.append({
                "latitude": location['lat'],
                "longitude": location['lng']
               })

    if converted_addresses:
        # Dönüştürülmüş adresleri başka bir sunucuya POST et
        server_url = "https://8r0c8h02-4000.euw.devtunnels.ms/location"
        response = requests.post(server_url, json=converted_addresses)
        if response.status_code == 200:
            return jsonify({"message": "Addresses sent to server successfully"}), 200
        else:
            return jsonify({"error": "Failed to send addresses to server"}), 500
    else:
        return jsonify({"error": "No addresses to send"}), 400

@map.route('/get', methods=['GET'])
def get_locations():
        # The URL from which to fetch the data
        server_url = "https://8r0c8h02-4000.euw.devtunnels.ms/location"  # Replace with the actual URL

        try:
            # Perform a GET request to the server to fetch location data
            response = requests.get(server_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                locations_data = response.json()

                # Dönen yanıtın expected formatta olup olmadığını kontrol ediyoruz
                if 'latitude' in locations_data and 'longitude' in locations_data:
                    return jsonify(locations_data), 200
                else:
                    return jsonify({"error": "Drone location data is invalid"}), 500
            else:
                return jsonify({"error": "Failed to fetch drone location from server"}), response.status_code

        except requests.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"An error occurred: {e}")
            return jsonify({"error": "An error occurred while fetching locations"}), 500


