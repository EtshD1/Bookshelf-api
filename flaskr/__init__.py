from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__)

    return app
