# routes.py
from flask import Flask, request, jsonify
from models import db, Book, Member

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], published_date=data['published_date'], isbn=data['isbn'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"})

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "published_date": book.published_date, "isbn": book.isbn} for book in books]
    return jsonify(books_list)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_date = data.get('published_date', book.published_date)
    book.isbn = data.get('isbn', book.isbn)
    db.session.commit()
    return jsonify({"message": "Book updated successfully!"})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'], joined_date=data['joined_date'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully!"})

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    members_list = [{"id": member.id, "name": member.name, "email": member.email, "joined_date": member.joined_date} for member in members]
    return jsonify(members_list)

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"message": "Member not found!"}), 404
    data = request.get_json()
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    member.joined_date = data.get('joined_date', member.joined_date)
    db.session.commit()
    return jsonify({"message": "Member updated successfully!"})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"message": "Member not found!"}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully!"})

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Existing dashboard logic


if __name__ == '__main__':
    app.run(debug=True)
