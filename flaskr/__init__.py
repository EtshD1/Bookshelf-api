from re import error
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_cors.decorator import cross_origin
from models import db, Book
from flask_migrate import Migrate

__BOOKS_PER_SHELF__ = 5


def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * __BOOKS_PER_SHELF__
    limit = start + __BOOKS_PER_SHELF__

    if limit > len(selection):
        limit = len(selection)

    bookList = []
    for book in range(start, limit):
        bookList.append(selection[book].to_dict())

    if len(bookList) == 0:
        abort(404)

    db.session.close()

    return bookList


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://etsh:3894@127.0.0.1:5432/bookshelf'
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
        try:
            books = Book.query.order_by(Book.id).all()
            bookList = paginate_books(request, books)

            return jsonify({'success': True, 'total_books': len(bookList), 'books': bookList})
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/books/<int:book_id>')
    def view_book(book_id):
        try:
            query = Book.query.get(book_id)
            if query:
                book = query.to_dict()
                return jsonify({
                    'book': book,
                    'success': True,
                })
            else:
                abort(404)
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.get(book_id)

            if book:
                book.delete()
            else:
                abort(404)

            bookQuery = Book.query.all()
            bookList = paginate_books(request, bookQuery)

            return jsonify({
                'success': True,
                'deleted_book_id': book_id,
                'books': bookList,
                'total_books': len(bookList)
            })
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def patch_book(book_id):
        try:
            body = request.get_json()
            book = Book.query.get(book_id)
            if book is None:
                abort(404)

            contentFilled = False
            if 'author' in body:
                book.author = body.get('author')
                book.update()
                contentFilled = True

            if 'name' in body:
                book.name = body.get('name')
                book.update()
                contentFilled = True

            bookDict = book.to_dict()
            db.session.close()
            if contentFilled:
                return jsonify({
                    'success': True,
                    'book': bookDict
                })
            else:
                return jsonify({
                    'success': False,
                    'book': bookDict
                }), 400
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/books/<int:book_id>', methods=['PUT'])
    def put_book(book_id):
        try:
            body = request.get_json()
            book = Book.query.get(book_id)
            if book is None:
                abort(404)

            author = body.get('author')
            if author is None:
                return jsonify({
                    'success': False,
                    'message': 'Please supply a "Author" in the body'
                }), 400

            name = body.get('name')
            if name is None:
                return jsonify({
                    'success': False,
                    'message': 'Please supply a "Name" in the body'
                }), 400

            book.author = body.get('author')
            book.name = body.get('name')
            book.update()

            bookDict = book.to_dict()
            db.session.close()
            return jsonify({
                'success': True,
                'book': bookDict
            })
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/books', methods=['POST'])
    def create_book():
        try:
            body = request.get_json()

            newBook = Book(
                name=body.get('name', None),
                author=body.get('author', None)
            )
            newBook.insert()
            book = newBook.to_dict()
            db.session.close()

            return jsonify({"success": True, 'book': book})
        except error:
            print(error)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error. Please try again later"
        }), 500

    return app
