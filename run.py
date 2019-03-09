from flask import Flask, jsonify, request, Response
import json


app = Flask(__name__)

books = [
    {
        'name': 'English book',
        'price': 7.99,
        'isbn': 1

    },
    {
        'name': 'Computer book',
        'price': 10.99,
        'isbn': 2
    }
]


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

# Post /Books


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validation(request_data)):

        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': request_data['isbn']
    }

    i = 0
    for book in books:
        curresntIsbn = book['isbn']
        if curresntIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBook = {
        "error": "Book ISBN not found",
        "helpString": "please enter book name,price and isbn"
    }
    response = Response(json.dumps(invalidBook), status=404, mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}

    if('name' in request_data):
        updated_book['name'] = request_data['name']
    if("price" in request_data):
        updated_book['price'] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


app.run(port=500)
