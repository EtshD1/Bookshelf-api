from flask import Flask, jsonify
from flask_cors import CORS
from flask_cors.decorator import cross_origin


def create_app(test_config=None):
    app = Flask(__name__)

    cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-METHODS',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({"message": "hello world!"})

    @app.route('/smiley')
    @cross_origin
    def smile():
        return ":)"

    return app
