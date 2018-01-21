import requests

from app import db
from app.models import Book

key = "AIzaSyCZDeUzMo21vkKpPQBAFwSdle6RkkACWKA"
key1 = "AIzaSyCsTHxXG4ZlMqCEzc3MT8ZG_u48ehLUCxM"


def search_isbn(isbn):
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=+isbn:" + isbn + "&key=" + key1)
    rj = r.json()
    print(rj)
    info = rj["items"][0]["volumeInfo"]

    book = Book(isbn=isbn, title=info["title"], author=info["authors"][0], description=info["description"],
                thumbnail=info["imageLinks"]["thumbnail"], category_id=1)

    db.session.add(book)
    db.session.commit()

    return book
