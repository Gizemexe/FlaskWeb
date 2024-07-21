from flask import Flask, make_response, jsonify
import os
import pyodbc
from src.Presentation.Controllers.UsersController import users
from src.Presentation.Controllers.ProductsController import products
from src.Presentation.Controllers.CategoriesController import categories
from src.Presentation.Controllers.FavoritesController import favorites
from src.Presentation.Controllers.CartsController import carts
from src.Presentation.Controllers.AuthController import auth
from src.Presentation.Controllers.OrdersController import orders
from src.Presentation.Controllers.OrdersDetailsController import orderDetails
from src.Presentation.Controllers.MapController import map
from src.Infrastructure.Database.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from googlemaps import Client
from flask_socketio import SocketIO
from dotenv import load_dotenv

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()
    socketio = SocketIO(app)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = r'mssql+pyodbc://DenemeUser:123@GizemASUS\SQLEXPRESS/Deneme?driver=ODBC+Driver+17+for+SQL+Server'

        )
    else:
       app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)
    CORS(app)
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(categories)
    app.register_blueprint(favorites)
    app.register_blueprint(carts)
    app.register_blueprint(auth)
    app.register_blueprint(orders)
    app.register_blueprint(orderDetails)
    app.register_blueprint(map)

    #swagger configs
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINTS = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config= {
            'app_name': 'Test API'
        }
    )
    app.register_blueprint(SWAGGER_BLUEPRINTS,url_prefix=SWAGGER_URL)

    @app.route('/')
    def index():
        return "websocket server is running!"

    # error handeling
    @app.errorhandler(400)
    def handle_400_error(_error):
        """Return a http 400 error to client"""
        return make_response(jsonify({'error': 'Misunderstood'}), 400)

    @app.errorhandler(401)
    def handle_401_error(_error):
        """Return a http 401 error to client"""
        return make_response(jsonify({'error': 'Unauthorised'}), 401)

    @app.errorhandler(404)
    def handle_404_error(_error):
        """Return a http 404 error to client"""
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(500)
    def handle_500_error(_error):
        """Return a http 500 error to client"""
        return make_response(jsonify({'error': 'Server error'}), 500)

    @socketio.on('connect')
    def handle_connect():
        print("Client connected")

    @socketio.on('location_update')
    def handle_location_update(data):
        print(f"Location update: {data}")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")

    # MSSQL bağlantısı
    DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
    SERVER_NAME = 'GizemASUS\\SQLEXPRESS'
    DATABASE_NAME = 'Deneme'
    USERNAME = 'DenemeUser'  # Veritabanı kullanıcı adı
    PASSWORD = '123'  # Veritabanı parolası

    connection_string = f"""
          DRIVER={{{DRIVER_NAME}}};
          SERVER={SERVER_NAME};
          DATABASE={DATABASE_NAME};
          UID={USERNAME};
          PWD={PASSWORD};
          Trust_Connection=yes;
       """

    # Veritabanı bağlantısını oluştur
    try:
        conn = pyodbc.connect(connection_string)
        print("MSSQL veritabanına başarıyla bağlandı.")
    except Exception as e:
        print("MSSQL veritabanına bağlanırken bir hata oluştu:", e)

    return app

if __name__ == '__main__':
    app = create_app()
    #app.run(host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)


