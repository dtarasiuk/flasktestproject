# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, flash
from utils import Pagination


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


books_to_authors = db.Table('books_to_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    authors = db.relationship('Author', secondary=books_to_authors,
        backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return '<Book %r>' % self.title


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<Author %r>' % self.name


@app.route('/')
@app.route('/authors/list')
@app.route('/authors/list/page/<int:page>')
def authors_list(page=1):
    pagination = Pagination(Author, page, app.config['OBJECTS_ON_PAGE'])

    return render_template('authors_list.html', model='authors', pagination=pagination)


@app.route('/authors/create', methods=['GET', 'POST'])
@app.route('/authors/edit/<int:id>', methods=['GET', 'POST'])
def author_edit(id=None):
    if id:
        author = Author.query.get(id)
    else:
        author = None

    if request.method == 'POST':
        new_name = request.form['author-name']
        if author:
            author.name = new_name
            result_message = u'Author was successfully updated'
        else:
            author = Author(name=new_name)
            db.session.add(author)
            result_message = u'Author was successfully added'
        db.session.commit()
        flash(result_message)
        return redirect(url_for('authors_list'))
    else:
        return render_template('author_edit.html', author=author, \
            model='authors')


@app.route('/authors/delete/<int:id>', methods=['GET', 'POST'])
def author_delete(id=None):
    Author.query.filter_by(id=id).delete(False)
    db.session.commit()
    flash(u'Author was successfully deleted')

    return redirect(url_for('authors_list'))


@app.route('/books/list')
@app.route('/books/list/page/<int:page>')
def books_list(page=1):
    pagination = Pagination(Book, page, app.config['OBJECTS_ON_PAGE'])

    return render_template('books_list.html', model='books', pagination=pagination)


@app.route('/books/create', methods=['GET', 'POST'])
@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def book_edit(id=None):
    if id:
        book = Book.query.get(id)
        selected_authors = [author.id for author in book.authors]
    else:
        book = None
        selected_authors = []

    if request.method == 'POST':
        new_title = request.form['book-title']
        if book:
            book.title = new_title
            result_message = u'Book was successfully updated'
        else:
            book = Book(title=new_title)
            db.session.add(book)
            result_message = u'Book was successfully added'

        new_authors = []
        for author_id in request.form.getlist('book-authors'):
            new_authors.append(Author.query.get(author_id))
        book.authors = new_authors

        db.session.commit()

        flash(result_message)
        return redirect(url_for('books_list'))
    else:
        authors = Author.query.all()
        return render_template('book_edit.html', authors=authors, book=book, \
            model='books', selected_authors=selected_authors)


@app.route('/books/delete/<int:id>', methods=['GET', 'POST'])
def book_delete(id=None):
    Book.query.filter_by(id=id).delete(False)
    db.session.commit()
    flash(u'Book was successfully deleted')

    return redirect(url_for('books_list'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    q = request.form['q']
    books = Book.query.filter(Book.title.ilike('%' + q + '%')).all()
    authors = Author.query.filter(Author.name.ilike('%' + q + '%')).all()
    books.append([author.books for author in authors])

    return render_template('books_search.html', books=books, model='books')

if __name__ == '__main__':
    app.run()
