import os
from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Für Flash-Nachrichten

# Datenbank konfigurieren
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

# ---------------- Routes ---------------- #

# Add Author
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

# Add Book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    authors = Author.query.all()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        year = request.form["publication_year"]
        rating = request.form.get("rating")
        rating = int(rating) if rating else None
        author_id = request.form["author_id"]

        new_book = Book(isbn=isbn, title=title, publication_year=year, rating=rating, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    return render_template("add_book.html", authors=authors)

# Homepage mit Sortierung
@app.route("/", methods=["GET"])
def home():
    sort_by = request.args.get("sort", "title")
    if sort_by == "author":
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()
    return render_template("home.html", books=books)

# Suche
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    results = Book.query.filter(Book.title.like(f"%{keyword}%")).all()
    return render_template("home.html", books=results)

# Buch Detailseite
@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)

# Autor Detailseite
@app.route("/author/<int:author_id>")
def author_detail(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template("author_detail.html", author=author)

# Autor löschen (inkl. Bücher)
@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    flash("Author and their books deleted successfully!", "success")
    return redirect(url_for("home"))

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    app.run(port=5005, debug=True)
