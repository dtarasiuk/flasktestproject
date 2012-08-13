from flasktestproject import db
from sqlalchemy import or_


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

    def set_authors(self, author_ids):
        self.authors = Author.query.filter(Author.id.in_(author_ids)).all()

    @classmethod
    def query_search_by_title_and_author(cls, query):
        author_ids = Author.searh_author_ids_by_name(query)
        return (
            cls.query.filter(or_(
                cls.title.ilike('%' + query + '%'),
                cls.authors.any(Author.id.in_(author_ids))
            ))
        )


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return '<Author %r>' % self.name

    @classmethod
    def searh_author_ids_by_name(cls, query):
        return db.session.query(cls.id).filter(
            cls.name.ilike('%' + query + '%')
        )
