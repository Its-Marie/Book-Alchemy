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

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

#with app.app_context():
#    db.create_all()


if __name__ == "__main__":
    app.run(port=5005, debug=True)
