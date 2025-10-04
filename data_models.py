from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(20))
    date_of_death = db.Column(db.String(20))

    def __str__(self):
        return f"{self.name} ({self.birth_date} - {self.date_of_death})"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.String(4))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    author = db.relationship("Author", backref="books")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
