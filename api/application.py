"""
Author: John Sharp

File: application.py

Description: API for GET/PUSH/DELETE request on a custom database for books

"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f'{self.book_name} - {self.author}'


@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Books.query.all()
    output = []
    for book in books:
        books_data = {'Title':  book.book_name, 'Author': book.author, 'Publisher': book.publisher}
        output.append(books_data)
    return {'books': output}

@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {'Title': book.book_name, 'Author': book.author}

@app.route('/books', methods=['POST'])
def add_book():
    book = Books(book_name=request.json['Title'], author=request.json['Author'], publisher=request.json['Publisher'])
    db.session.add(book)
    db.session.commit()
    return{'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {'ERROR': "Not Found"}
    db.session.delete(book)
    db.session.commit()
    return {"Message": "Burned"}
