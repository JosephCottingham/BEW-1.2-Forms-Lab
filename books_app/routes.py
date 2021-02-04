"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User
from books_app.forms import BookForm, AuthorForm, GenreForm

# Import app and db from events_app package so that we can run app
from books_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template('home.html', 
        all_books=all_books, all_users=all_users)

@main.route('/create_book', methods=['GET', 'POST'])
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            author=form.author.data,
            audience=form.audience.data,
            genres=form.genres.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash('New book was created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_book.id))
    return render_template('create_book.html', form=form)

@main.route('/create_author', methods=['GET', 'POST'])
def create_author():
    af=AuthorForm()
    if af.author_form_submit.data and af.validate_on_submit():
        author=Author()
        author.name=af.name.data
        author.biography=af.biography.data
        db.session.add(author)
        db.session.commit()
    
    # fields
    return render_template('create_author.html', af=af)

@main.route('/create_genre', methods=['GET', 'POST'])
def create_genre():

    gf = GenreForm()
    if gf.genre_form_submit.data and gf.validate_on_submit():
        genre = Genre(
            name=gf.name.data
        )
        db.session.add(genre)
        db.session.commit()

    # fields
    return render_template('create_genre.html', gf=gf)

@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # STRETCH CHALLENGE: Fill out the Create User route
    return "Not Yet Implemented"

@main.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)

    if form.submit.data and form.validate_on_submit():
        book.title=form.title.data
        book.publish_date=form.publish_date.data
        book.author=form.author.data
        book.audience=form.audience.data
        book.genres=form.genres.data
        db.session.commit()

    return render_template('book_detail.html', book=book, form=form)

@main.route('/profile/<username>')
def profile(username):
    user = db.session.query(User).filter_by(username=username).first()

    # STRETCH CHALLENGE: Add ability to modify a user's username or favorite 
    # books
    return render_template('profile.html', username=username, user=user)
