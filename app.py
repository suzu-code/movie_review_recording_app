from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('app.db')
    db.row_factory = sqlite3.Row
    return db

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
SEARCH_URL = 'https://api.themoviedb.org/3/search/movie?include_adult=false&language=ja-JP&page=1'

def get_api_data(query):
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'ja-JP',
        'query': query,
        'page': 1,
        'include_adult': False
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    cinema_data = []
    keyword = ''
    if request.method == 'POST':
        keyword = request.form.get('title', '')
        if keyword:
            items = get_api_data(keyword)
            for item in items:
                cinema_data.append({
                    'title': item.get('title', 'N/A'),
                    'image': item.get('poster_path', ''),
                    'release_date': item.get('release_date', 'N/A'),
                    'id': item.get('id', '')
                })
    return render_template('main.html', cinema_data=cinema_data, keyword=keyword)

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ja-JP'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def save_movie_to_db(movie):
    db = get_db()
    query = """
        INSERT INTO movies (movie_id, poster_path, title, release_date, genre, overview)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    genre = ", ".join([g['name'] for g in movie.get('genres', [])])
    with db:
        db.execute(query, (
            movie.get('id'),
            movie.get('poster_path', ''),
            movie.get('title', 'Unknown Title'),
            movie.get('release_date', 'Unknown Date'),
            genre,
            movie.get('overview', 'No overview available')
        ))
    db.close()



@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    db = get_db()
    query = """
        SELECT * FROM movies WHERE movie_id = ?
    """
    movie = db.execute(query, (movie_id,)).fetchone()
    db.close()

    if not movie:
        movie_details = get_movie_details(movie_id)
        if not movie_details:
            return "Movie not found", 404
        save_movie_to_db(movie_details)
        db = get_db()
        movie = db.execute(query, (movie_id,)).fetchone()
        db.close()
        
    print("*************", dict(movie))
    return render_template('movie_details.html',movie=movie )



@app.route('/create', methods=['POST'])
def create():
    movie_id = request.form.get('movie_id')
    if not movie_id:
        return "Movie ID is required", 400
    
    movie_details = get_movie_details(movie_id)
    list_choice = request.form.get('list')
    overall_rating = request.form.get('overall_rating')
    story_rating = request.form.get('story_rating')
    acting_rating = request.form.get('acting_rating')
    visuals_rating = request.form.get('visuals_rating')
    music_rating = request.form.get('music_rating')
    review = request.form.get('review')

    db = get_db()
    existing_movie = db.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,)).fetchone()

    if existing_movie:
        query = """
            UPDATE movies
            SET list = ?, overall_rating = ?, story_rating = ?, acting_rating = ?, visuals_rating = ?, music_rating = ?, review = ?
            WHERE movie_id = ?
        """
        params = (list_choice, overall_rating, story_rating, acting_rating, visuals_rating, music_rating, review, movie_id)
    else:
        query = """
            INSERT INTO movies (movie_id, poster_path, title, release_date, genre, overview, list, overall_rating, story_rating, acting_rating, visuals_rating, music_rating, review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            movie_id,
            movie_details.get('poster_path', ''),
            movie_details.get('title', 'Unknown Title'),
            movie_details.get('release_date', 'Unknown Date'),
            ", ".join([genre['name'] for genre in movie_details.get('genres', [])]),
            movie_details.get('overview', 'No overview available'),
            list_choice,
            overall_rating,
            story_rating,
            acting_rating,
            visuals_rating,
            music_rating,
            review
        )

    with db:
        db.execute(query, params)
    db.close()

    return redirect(url_for('index'))



@app.route('/favorite', methods=['GET'])
def favorite_index():
    db = get_db()
    query = """ SELECT movie_id, poster_path, title, release_date, genre, overview
                FROM movies
                WHERE list = 1
                ORDER BY id DESC
            """
    movies = db.execute(query).fetchall()
    db.close()
    return render_template('favorite.html', movies=movies)

@app.route('/already', methods=['GET'])
def already_index():
    db = get_db()
    query = """ SELECT movie_id, poster_path, title, release_date, genre, overview
                FROM movies
                WHERE list = 2
                ORDER BY id DESC
            """
    movies = db.execute(query).fetchall()
    db.close()
    return render_template('already.html', movies=movies)

@app.route('/want_to_watch', methods=['GET'])
def want_to_watch_index():
    db = get_db()
    query = """ SELECT movie_id, poster_path, title, release_date, genre, overview
                FROM movies
                WHERE list = 3
                ORDER BY id DESC
            """
    movies = db.execute(query).fetchall()
    db.close()
    return render_template('want_to_watch.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
