from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TEXT,
            color TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        color = request.form['color']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO journals (title, content, created_at, color) VALUES (?, ?, ?, ?)',
                  (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), color))
        conn.commit()
        conn.close()
        return redirect(url_for('journals'))
    return render_template('new.html')

@app.route('/journals')
def journals():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM journals ORDER BY id DESC')
    journals = c.fetchall()
    conn.close()
    return render_template('journals.html', journals=journals)

@app.route('/journal/<int:journal_id>')
def journal_view(journal_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM journals WHERE id=?', (journal_id,))
    journal = c.fetchone()
    conn.close()
    return render_template('view_journal.html', journal=journal)



from flask import request

@app.route('/delete/<int:journal_id>', methods=['POST'])
def delete_journal(journal_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM journals WHERE id=?', (journal_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('journals'))



if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
