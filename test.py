def validation(book):
    if ("name" in book and "price" in book and "isbn" in book):
        return True
    else:
        return False


valid_book = {
    'name': 'F',
    'price': 6.9,
    'isbn': 1
}


missing_name = {
    'price': 6.9,
    'isbn': 1
}


missing_price = {
    'name': 'F',
    'isbn': 1
}


missing_isbn = {
    'name': 'F',
    'price': 6.9
}

missing = {}
