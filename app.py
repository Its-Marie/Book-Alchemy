import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from flask import render_template, request, redirect, url_for, flash

@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form["name"]
        birth_date = request.form["birth_date"]
        date_of_death = request.form["date_of_death"]

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash("Author added successfully!", "success")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    authors = Author.query.all()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        year = request.form["publication_year"]
        author_id = request.form["author_id"]

        new_book = Book(isbn=isbn, title=title, publication_year=year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    return render_template("add_book.html", authors=authors)

@app.route("/")
def home():
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        results = Book.query.filter(Book.title.like(f"%{keyword}%")).all()
    return render_template("search.html", results=results)

@app.route("/", methods=["GET"])
def home():
    sort_by = request.args.get("sort", "title")  # default sort by title
    if sort_by == "author":
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()
    return render_template("home.html", books=books, sort_by=sort_by)

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

#with app.app_context():
#    db.create_all()


if __name__ == "__main__":
    app.run(port=5005, debug=True)
