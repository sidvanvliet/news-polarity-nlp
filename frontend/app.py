import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    conn = sqlite3.connect("../news.db")
    cursor = conn.cursor()

    # Fetch data from the 'articles' table
    cursor.execute(
        "SELECT title, polarity, subjectivity, publishing_date FROM articles ORDER BY publishing_date DESC LIMIT 10;")
    data = cursor.fetchall()

    conn.close()

    # Calculate the median polarity
    median_polarity = 0.0
    for article in data:
        median_polarity += article[1]

    median_polarity /= len(data)

    # Render the template
    return render_template('index.html', data={
        "articles": data,
        "median_polarity": median_polarity,
    })
