from flask import Flask, jsonify, request, Response
from bookModel import *
from settings import *

import json


from settings import *


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
    return jsonify({'books': Book.get_all_books()})

# Post /Books


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validation(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
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


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response

        invalidBook = {
            "error": "Book ISBN not found",
            "helpString": "please enter book name,price and isbn"
        }
        response = Response(json.dumps(invalidBook), status=404, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


app.run(port=500)
