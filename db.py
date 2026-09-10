"""
MySQL database layer for the Movie Recommendation System.

EDIT THE CONFIG BELOW to match your local MySQL login before running the app.
"""

import mysql.connector

# ---------------------------------------------------------------
# EDIT THIS to match your MySQL setup
# ---------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "bebo",      # <-- change to your real MySQL password
    "database": "movie_rec_db",
}


def get_connection(with_db=True):
    config = DB_CONFIG.copy()
    if not with_db:
        config.pop("database")
    return mysql.connector.connect(**config)


def init_db():
    """Create the database and tables if they don't already exist."""
    conn = get_connection(with_db=False)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.commit()
    cur.close()
    conn.close()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            genres VARCHAR(300) NOT NULL,
            rating FLOAT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            preferred_genres VARCHAR(300)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            rating_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            movie_id INT NOT NULL,
            rating FLOAT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def seed_if_empty():
    """Populate the original 8 movies / 2 users / their ratings, only if tables are empty."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM movies")
    movies_empty = cur.fetchone()[0] == 0

    cur.execute("SELECT COUNT(*) FROM users")
    users_empty = cur.fetchone()[0] == 0

    movie_id_map = {}
    if movies_empty:
        seed_movies = [
            ("Inception", ["Sci-Fi", "Thriller"], 4.8),
            ("Interstellar", ["Sci-Fi", "Drama"], 4.7),
            ("The Dark Knight", ["Action", "Crime", "Drama"], 4.9),
            ("The Martian", ["Sci-Fi", "Adventure", "Drama"], 4.6),
            ("Avengers: Endgame", ["Action", "Adventure", "Sci-Fi"], 4.5),
            ("The Prestige", ["Drama", "Mystery", "Thriller"], 4.7),
            ("Avatar", ["Action", "Adventure", "Sci-Fi"], 4.4),
            ("Titanic", ["Drama", "Romance"], 4.6),
        ]
        for title, genres, rating in seed_movies:
            cur.execute(
                "INSERT INTO movies (title, genres, rating) VALUES (%s, %s, %s)",
                (title, ",".join(genres), rating),
            )
            movie_id_map[title] = cur.lastrowid

    user_id_map = {}
    if users_empty:
        seed_users = [
            ("User1", ["Sci-Fi", "Adventure"]),
            ("User2", ["Drama", "Thriller"]),
        ]
        for name, prefs in seed_users:
            cur.execute(
                "INSERT INTO users (name, preferred_genres) VALUES (%s, %s)",
                (name, ",".join(prefs)),
            )
            user_id_map[name] = cur.lastrowid

    conn.commit()

    if movies_empty and users_empty:
        seed_ratings = [
            ("User1", "Inception", 5),
            ("User1", "Interstellar", 5),
            ("User1", "Avengers: Endgame", 4),
            ("User2", "The Dark Knight", 5),
            ("User2", "The Prestige", 5),
            ("User2", "Titanic", 4),
        ]
        for user_name, movie_title, rating in seed_ratings:
            cur.execute(
                "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
                (user_id_map[user_name], movie_id_map[movie_title], rating),
            )
        conn.commit()

    cur.close()
    conn.close()


def load_movies():
    """Returns {movie_id: {"title":..., "genres": [...], "rating": ...}} - same shape as movie_data.py."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM movies ORDER BY movie_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    movies = {}
    for row in rows:
        movies[row["movie_id"]] = {
            "title": row["title"],
            "genres": [g.strip() for g in row["genres"].split(",") if g.strip()],
            "rating": float(row["rating"]),
        }
    return movies


def load_users():
    """Returns {user_id: {"name":..., "preferred_genres": [...], "ratings": {movie_id: rating}}}."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users ORDER BY user_id")
    user_rows = cur.fetchall()
    cur.execute("SELECT * FROM ratings")
    rating_rows = cur.fetchall()
    cur.close()
    conn.close()

    users = {}
    for row in user_rows:
        prefs = row["preferred_genres"] or ""
        users[row["user_id"]] = {
            "name": row["name"],
            "preferred_genres": [g.strip() for g in prefs.split(",") if g.strip()],
            "ratings": {},
        }

    for r in rating_rows:
        if r["user_id"] in users:
            users[r["user_id"]]["ratings"][r["movie_id"]] = float(r["rating"])

    return users


def add_movie(title, genres_list, rating):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO movies (title, genres, rating) VALUES (%s, %s, %s)",
        (title, ",".join(genres_list), rating),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def add_user(name, preferred_genres_list):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, preferred_genres) VALUES (%s, %s)",
        (name, ",".join(preferred_genres_list)),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def add_rating(user_id, movie_id, rating):
    """Insert a new rating, or update it if this user already rated this movie."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT rating_id FROM ratings WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id),
    )
    existing = cur.fetchone()

    if existing:
        cur.execute("UPDATE ratings SET rating = %s WHERE rating_id = %s", (rating, existing[0]))
    else:
        cur.execute(
            "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            (user_id, movie_id, rating),
        )

    conn.commit()
    cur.close()
    conn.close()
