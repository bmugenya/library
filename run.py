from flask import Flask, jsonify, request, Response
from datetime import datetime, timedelta
from bookModel import *
from userModel import User
from functools import wraps
from settings import *
import jwt
import json


app.config['SECRET_KEY'] = 'library'
books = Book.get_all_books()


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.utcnow() + timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', status=401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Need a valid token to view page %s' % e})
    return wrapper


def validation(book):
    if ("name" in book and "price" in book and "isbn" in book):
        return True
    else:
        return False


def updateValidation(book):
    if ("name" in book and "price" in book):
        return True
    else:
        return False
# Get /Books


@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# Post /Books


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if(validation(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBook = {
            "error": "Invalid book object in request",
            "helpString": "please enter book name,price and isbn"
        }
        response = Response(json.dumps(invalidBook), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if(not updateValidation(request_data)):
        invalidBook = {
            "error": "Invalid book object in request",
            "helpString": "please enter book name,price and isbn"
        }
        response = Response(json.dumps(invalidBook), status=400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    for book in books:
        if book['isbn'] == isbn:
            Book.delete_book(isbn)
            response = Response("", status=204)
            return response

        invalidBook = {
            "error": "Book ISBN not found",
            "helpString": "please enter book name,price and isbn"
        }
        response = Response(json.dumps(invalidBook), status=404, mimetype='application/json')
        return response


app.run(port=500)
