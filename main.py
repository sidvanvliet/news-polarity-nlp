from bs4 import BeautifulSoup as bs
import requests
import sqlite3
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer


def get_rss_feed(rss_feed: str = "https://tweakers.net/feeds/mixed.xml", index: int = 0):
    """
    Retrieves the RSS feed and returns the latest item
    """
    content = requests.get(rss_feed)
    xml = bs(content.text, 'xml')
    latest_article = xml.find_all('item')[index]

    print(f"Found article: {latest_article.find('title').text}")

    # Return dictionary with information we want to store
    return {
        "title": latest_article.find('title').text,
        "content": latest_article.find('description').text,
        "sentiment": get_polarity(latest_article.find('description').text),
        "publishing_date": latest_article.find('pubDate').text,
    }


def is_new_item(article: dict) -> bool:
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    # Check if the "articles" table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='articles';"
    )

    if not cursor.fetchone():
        # If the "articles" table doesn't exist, create it
        create_table_if_not_exist()

    # Check if the article is already in the database
    check_query = """
    SELECT COUNT(*)
    FROM articles
    WHERE title = ? AND publishing_date = ?
    """

    # Execute query to check if the article is already in the database
    cursor.execute(check_query, (article['title'], article['publishing_date']))
    count = cursor.fetchone()[0]

    conn.close()

    # If the article is not in the database, return True
    return count == 0


def get_polarity(text: str) -> float:
    """
    Calculate the polarity of the news item, using the SpaCy NLP library
    """
    blob = TextBlob(text,
                    pos_tagger=PatternTagger(),
                    analyzer=PatternAnalyzer()
                    )

    # Return the polarity and subjectivity of the news item
    return {
        "polarity": blob.sentiment[0],
        "subjectivity": blob.sentiment[1]
    }


def create_table_if_not_exist() -> None:
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    # Define the SQL query to create the 'articles' table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        publishing_date DATETIME,
        polarity REAL,
        subjectivity REAL
    )
    """

    # Execute the SQL query to create the table
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return


def add_to_db(title: str, content: str, publish_date: str, polarity: float, subjectivity: float) -> None:
    """
    Add the news item to the database
    """
    # Connect to the database
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    # Query to insert the article into the database
    query = """
    INSERT INTO articles (title, content, publishing_date, polarity, subjectivity)
    VALUES (?, ?, ?, ?, ?)
    """

    # Execute the SQL query with the provided values
    cursor.execute(query, (
        title, content, publish_date, polarity, subjectivity
    ))

    # Commit & close the connection
    connection.commit()
    connection.close()

    return


"""
Retrieve latest article and, if it's new, add it to the database
"""

# First, validate that the table exists, otherwise create it
create_table_if_not_exist()

# Retrieve the latest article
latest_article = get_rss_feed(index=0)

# Check if the article is new, if so, add it to the database
if (is_new_item(latest_article) is True):
    print(f"New article found: {latest_article['title']}")
    add_to_db(
        latest_article["title"],
        latest_article["content"],
        latest_article["publishing_date"],
        latest_article["sentiment"]["polarity"],
        latest_article["sentiment"]["subjectivity"]
    )

else:
    print("No new articles found")
