from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'  # For managing session and flash messages

# Initialize the database and create the books table
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Display the list of books (Home page)
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']

        if not title or not author or not genre or not year:
            flash('Please fill out all fields.')
            return redirect(url_for('add_book'))

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)',
                       (title, author, genre, year))
        conn.commit()
        conn.close()
        flash('Book successfully added.')
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
