from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect('demo.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    c.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
        ("admin", "admin123"),
        ("user1", "pass1"),
        ("user2", "pass2")
    ])
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
    <h1>SQL Injection Demo</h1>
    <form action="/login" method="post">
        <label>Username: <input type="text" name="username"></label><br>
        <label>Password: <input type="password" name="password"></label><br>
        <button type="submit">Login</button>
    </form>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('demo.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Executing query: {query}")
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"Welcome, {user[1]}!"
    else:
        return "Invalid credentials. Try again."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
