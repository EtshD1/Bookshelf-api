from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_cors.decorator import cross_origin
from models import db, Book
from flask_migrate import Migrate

__BOOKS_PER_SHELF__ = 5


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://etsh:3894@127.0.0.1:5432/libraryapi'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    db.init_app(app)
    migrate = Migrate(app, db)

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

    @app.route('/books')
    def get_books():
        page = request.args.get('page', 1, type=int)
        start = (page-1) * __BOOKS_PER_SHELF__
        books = Book.query.all()

        limit = start + __BOOKS_PER_SHELF__
        if limit > len(books):
            limit = len(books)

        bookList = []
        for book in range(start, limit):
            bookList.append(books[book].to_dict())

        if len(bookList) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': bookList,
            'total_books': len(books)
        })

    return app
