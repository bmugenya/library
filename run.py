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
