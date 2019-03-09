from flask import Flask, jsonify


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

#Get /Books


@app.route('/books')
def get_books():
    return jsonify({
        'books': books
    })


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
