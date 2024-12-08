from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
import os

# Initialize Flask App
app = Flask(__name__)

# Database Setup
DATABASE = 'library.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create Books Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )''')
        # Create Members Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            join_date TEXT NOT NULL
        )''')
        conn.commit()

def insert_sample_data():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Clear existing data to avoid duplicates
        cursor.execute('DELETE FROM books')
        cursor.execute('DELETE FROM members')
        
        # Insert unique sample books
        books = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
            ('1984', 'George Orwell', 1949)
        ]
        cursor.executemany('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', books)
        
        # Insert unique sample members
        members = [
            ('John Doe', 'john@example.com', '2023-01-15'),
            ('Jane Smith', 'jane@example.com', '2023-02-20')
        ]
        cursor.executemany('INSERT INTO members (name, email, join_date) VALUES (?, ?, ?)', members)
        
        conn.commit()

@app.route('/')
def home():
    return "Welcome to the Library Management System!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        print(f"Books: {books}")  # Debugging
        print(f"Members: {members}")  # Debugging
    return render_template('dashboard.html', books=books, members=members)

@app.route('/books', methods=['GET'])
def get_books():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
    return jsonify([{"id": row[0], "title": row[1], "author": row[2], "year": row[3]} for row in books]), 200

# Define other routes for CRUD operations...

# Run the Flask Application
if __name__ == '__main__':
    init_db()
    insert_sample_data()  # Insert sample data
    app.run(debug=True)
