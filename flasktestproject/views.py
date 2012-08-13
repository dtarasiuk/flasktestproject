# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from utils import Pagination
from flasktestproject import app
from flasktestproject.models import *


@app.route('/')
@app.route('/authors/list')
@app.route('/authors/list/page/<int:page>')
def authors_list(page=1):
    pagination = Pagination(Author.query, page, app.config['OBJECTS_ON_PAGE'])

    return render_template(
        'authors_list.html', model='authors', pagination=pagination
    )


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
    pagination = Pagination(Book.query, page, app.config['OBJECTS_ON_PAGE'])

    return render_template(
        'books_list.html',
        model='books',
        pagination=pagination,
        url='/books/list'
    )


@app.route('/books/create', methods=['GET', 'POST'])
@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def book_edit(id=None):
    if id:
        book = Book.query.get(id)
        selected_authors_ids = [author.id for author in book.authors]
    else:
        book = None
        selected_authors_ids = []

    if request.method == 'POST':
        new_title = request.form['book-title']
        if book:
            book.title = new_title
            result_message = u'Book was successfully updated'
        else:
            book = Book(title=new_title)
            db.session.add(book)
            result_message = u'Book was successfully added'

        book.set_authors(request.form.getlist('book-authors'))

        db.session.commit()

        flash(result_message)
        return redirect(url_for('books_list'))
    else:
        authors = Author.query.all()
        return render_template('book_edit.html', authors=authors, book=book, \
            model='books', selected_authors_ids=selected_authors_ids)


@app.route('/books/delete/<int:id>', methods=['GET', 'POST'])
def book_delete(id=None):
    Book.query.filter_by(id=id).delete(False)
    db.session.commit()
    flash(u'Book was successfully deleted')

    return redirect(url_for('books_list'))


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/page/<int:page>', methods=['GET', 'POST'])
def search(page=1):
    if request.method == 'GET':
        q = request.args['q']
    else:
        q = request.form['q']

    pagination = Pagination(Book.query_search_by_title_and_author(q), \
        page, app.config['OBJECTS_ON_PAGE'], q)

    return render_template(
        'books_list.html', pagination=pagination, model='books', url='/search'
    )
