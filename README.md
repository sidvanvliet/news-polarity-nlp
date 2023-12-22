# News Polarity NLP

A proof of concept project that retrieves and analyzes news articles from a given RSS feed. The project calculates both the polarity and subjectivity of each article using Natural Language Processing (NLP) techniques. The results are then visualized in a front-end for easy interpretation.

## Features

- Retrieves new articles from the specified RSS feed.
- Utilizes [NLP](https://en.wikipedia.org/wiki/Natural_language_processing) to analyze the polarity and subjectivity of each article.
- Presents the analysis results in an straight-to-the-point front-end for quick insights.

## Usage

#### Clone the Repository

```bash
$ git clone https://github.com/sidvanvliet/news-polarity-nlp.git
```

#### Install Dependencies

```bash
$ pip install -r requirements.txt
```

#### Run the Python App

Execute the main Python script to run the application. You can schedule this as needed, and the app will check for new articles every time it runs.

```bash
$ python main.py
```

#### Run the Frontend

Change directory to the 'frontend' folder and run the Flask application:

```bash
$ cd frontend
$ flask run
```

Access the frontend by navigating to http://localhost:5000 in your web browser, which presents a simple site with displaying the 10 most recent articles that the application scanned. The table includes the polarity and subjectivity of each article and also lists the combined median polarity of those articles.

## Licenses

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## TODO

- [ ] Add multilingual support
- [ ] Add tests
