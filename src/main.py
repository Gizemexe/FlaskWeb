from flask import Flask, make_response, jsonify
import os
import pymssql
from src.Presentation.Controllers.UsersController import users
from src.Presentation.Controllers.ProductsController import products
from src.Presentation.Controllers.CategoriesController import categories
from src.Presentation.Controllers.FavoritesController import favorites
from src.Presentation.Controllers.CartsController import carts
from src.Presentation.Controllers.AuthController import auth
from src.Presentation.Controllers.OrdersController import orders
from src.Presentation.Controllers.OrdersDetailsController import orderDetails
from src.Presentation.Controllers.MapController import map
from src.Infrastructure.Database.database import db,ma
from src.config import Config
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv

socketio = SocketIO()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    load_dotenv()



    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")

        )
    else:
       app.config.from_mapping(test_config)

    db.init_app(app)
    ma.init_app(app)
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

    print(os.environ.get("SERVER_USERNAME"))
    print(os.environ.get("PASSWORD"))
    print(os.environ.get("DATABASE_NAME"))
    print(os.environ.get("SERVER_NAME"))
    print(os.environ.get("SQLALCHEMY_DATABASE_URI"))
    # MSSQL bağlantısı
    try:
        conn = pymssql.connect(
            server=os.environ.get("SERVER_NAME"),
            user=os.environ.get("SERVER_USERNAME"),
            password=os.environ.get("PASSWORD"),
            database=os.environ.get("DATABASE_NAME")
        )
        print("MSSQL veritabanına başarıyla bağlandı.")
    except Exception as e:
        print("MSSQL veritabanına bağlanırken bir hata oluştu:", e)

    socketio.init_app(app)
    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)


