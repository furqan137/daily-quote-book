from flask import Flask, render_template, request, redirect, url_for
from models import db, Quote
import os
import random

app = Flask(__name__)

# Database config from env vars
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "quotes")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    quotes = Quote.query.all()
    random_quote = random.choice(quotes) if quotes else None
    return render_template('index.html', quote=random_quote)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        text = request.form['text']
        author = request.form['author']
        new_quote = Quote(text=text, author=author)
        db.session.add(new_quote)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
