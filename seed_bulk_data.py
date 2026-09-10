"""
Bulk-seeds the movie_rec_db database with:
  - ~70 diverse movies across 9 categories (Hollywood, Marvel/DC, Bollywood,
    Tollywood, Bhojpuri, K-Drama, Ghibli, Anime, Turkish)
  - 150 users with randomly assigned preferred genres
  - Realistic ratings per user (weighted toward their preferred genres,
    so the recommendation engine has real signal to work with)

Run this ONCE:
    python seed_bulk_data.py

Safe to re-run: it only ADDS new users/movies, it never deletes your
existing 2 users or their ratings.
"""

import random
import db

random.seed(42)  # remove this line if you want different random data each run


# =====================================================================
# 1. MOVIE CATALOG — ~70 movies across 9 categories
#    (category name is included as one of the "genres" so the
#    similarity graph naturally clusters movies from the same category)
# =====================================================================
MOVIES_SEED = [
    # ---- Hollywood ----
    ("The Shawshank Redemption", ["Hollywood", "Drama"], 4.9),
    ("Pulp Fiction", ["Hollywood", "Crime", "Drama"], 4.8),
    ("Fight Club", ["Hollywood", "Drama", "Thriller"], 4.7),
    ("The Matrix", ["Hollywood", "Sci-Fi", "Action"], 4.8),
    ("Forrest Gump", ["Hollywood", "Drama", "Romance"], 4.7),
    ("Gladiator", ["Hollywood", "Action", "Drama"], 4.6),
    ("The Social Network", ["Hollywood", "Drama", "Biography"], 4.4),
    ("La La Land", ["Hollywood", "Romance", "Musical"], 4.5),
    ("Whiplash", ["Hollywood", "Drama", "Music"], 4.7),
    ("The Grand Budapest Hotel", ["Hollywood", "Comedy", "Drama"], 4.4),

    # ---- Marvel / DC ----
    ("Avengers: Infinity War", ["Marvel", "Action", "Sci-Fi"], 4.7),
    ("Spider-Man: No Way Home", ["Marvel", "Action", "Adventure"], 4.7),
    ("Black Panther", ["Marvel", "Action", "Adventure"], 4.5),
    ("Guardians of the Galaxy Vol. 3", ["Marvel", "Action", "Comedy"], 4.5),
    ("Doctor Strange", ["Marvel", "Action", "Fantasy"], 4.3),
    ("Wonder Woman", ["DC", "Action", "Fantasy"], 4.4),
    ("The Batman", ["DC", "Action", "Crime", "Thriller"], 4.6),
    ("Man of Steel", ["DC", "Action", "Sci-Fi"], 4.0),
    ("Aquaman", ["DC", "Action", "Fantasy"], 4.0),
    ("Joker", ["DC", "Drama", "Thriller"], 4.6),

    # ---- Bollywood ----
    ("Dangal", ["Bollywood", "Drama", "Sport"], 4.8),
    ("3 Idiots", ["Bollywood", "Comedy", "Drama"], 4.8),
    ("Lagaan", ["Bollywood", "Drama", "Sport"], 4.6),
    ("Zindagi Na Milegi Dobara", ["Bollywood", "Drama", "Adventure"], 4.5),
    ("Gully Boy", ["Bollywood", "Drama", "Music"], 4.4),
    ("Queen", ["Bollywood", "Comedy", "Drama"], 4.5),
    ("Andhadhun", ["Bollywood", "Thriller", "Comedy"], 4.6),
    ("Pink", ["Bollywood", "Drama", "Thriller"], 4.5),
    ("Barfi!", ["Bollywood", "Romance", "Drama"], 4.3),
    ("Kabhi Khushi Kabhie Gham", ["Bollywood", "Drama", "Romance"], 4.0),

    # ---- Tollywood (Telugu cinema) ----
    ("Baahubali: The Beginning", ["Tollywood", "Action", "Fantasy"], 4.6),
    ("Baahubali 2: The Conclusion", ["Tollywood", "Action", "Fantasy"], 4.8),
    ("RRR", ["Tollywood", "Action", "Drama"], 4.9),
    ("Pushpa: The Rise", ["Tollywood", "Action", "Drama"], 4.4),
    ("Arjun Reddy", ["Tollywood", "Romance", "Drama"], 4.3),
    ("Magadheera", ["Tollywood", "Action", "Fantasy"], 4.2),
    ("Eega", ["Tollywood", "Fantasy", "Action"], 4.3),
    ("Jersey", ["Tollywood", "Drama", "Sport"], 4.5),

    # ---- Bhojpuri ----
    ("Nirahua Hindustani", ["Bhojpuri", "Drama", "Romance"], 3.8),
    ("Sasura Bada Paisa Wala", ["Bhojpuri", "Drama", "Family"], 3.7),
    ("Border", ["Bhojpuri", "Action", "Drama"], 3.6),
    ("Dulhin Ganga Paar Ke", ["Bhojpuri", "Romance", "Drama"], 3.7),
    ("Ganga", ["Bhojpuri", "Action", "Drama"], 3.6),
    ("Deewane Ishq Ke", ["Bhojpuri", "Romance", "Drama"], 3.5),

    # ---- K-Drama / Korean cinema ----
    ("Parasite", ["K-Drama", "Thriller", "Drama"], 4.9),
    ("Train to Busan", ["K-Drama", "Horror", "Action"], 4.7),
    ("Squid Game: The Movie Edit", ["K-Drama", "Thriller", "Drama"], 4.6),
    ("The Handmaiden", ["K-Drama", "Thriller", "Romance"], 4.5),
    ("Oldboy", ["K-Drama", "Thriller", "Mystery"], 4.6),
    ("Burning", ["K-Drama", "Mystery", "Drama"], 4.3),
    ("Extreme Job", ["K-Drama", "Comedy", "Action"], 4.4),
    ("Crash Landing on You: The Movie", ["K-Drama", "Romance", "Comedy"], 4.7),

    # ---- Studio Ghibli ----
    ("Spirited Away", ["Ghibli", "Fantasy", "Adventure"], 4.9),
    ("My Neighbor Totoro", ["Ghibli", "Fantasy", "Family"], 4.8),
    ("Princess Mononoke", ["Ghibli", "Fantasy", "Adventure"], 4.8),
    ("Howl's Moving Castle", ["Ghibli", "Fantasy", "Romance"], 4.7),
    ("Kiki's Delivery Service", ["Ghibli", "Fantasy", "Family"], 4.5),
    ("Ponyo", ["Ghibli", "Fantasy", "Family"], 4.4),
    ("The Wind Rises", ["Ghibli", "Drama", "Historical"], 4.5),

    # ---- Anime (non-Ghibli) ----
    ("Demon Slayer: Mugen Train", ["Anime", "Action", "Fantasy"], 4.7),
    ("Your Name", ["Anime", "Romance", "Fantasy"], 4.9),
    ("Jujutsu Kaisen 0", ["Anime", "Action", "Fantasy"], 4.6),
    ("Attack on Titan: Chronicle", ["Anime", "Action", "Drama"], 4.6),
    ("One Piece Film: Red", ["Anime", "Action", "Adventure"], 4.5),
    ("Naruto Shippuden: The Movie", ["Anime", "Action", "Adventure"], 4.3),
    ("Weathering With You", ["Anime", "Romance", "Fantasy"], 4.6),
    ("Suzume", ["Anime", "Fantasy", "Adventure"], 4.7),

    # ---- Turkish ----
    ("Winter Sleep", ["Turkish", "Drama"], 4.4),
    ("Mustang", ["Turkish", "Drama"], 4.3),
    ("Three Monkeys", ["Turkish", "Drama", "Thriller"], 4.2),
    ("Ayla: The Daughter of War", ["Turkish", "Drama", "War"], 4.6),
    ("The Butterfly's Dream", ["Turkish", "Drama", "Romance"], 4.1),
    ("Miracle in Cell No. 7", ["Turkish", "Drama", "Comedy"], 4.7),
]


# =====================================================================
# 2. USER NAME POOL — mixed culturally to match the movie catalog
# =====================================================================
FIRST_NAMES = [
    "James", "Emma", "Michael", "Olivia", "Daniel", "Sophia", "Chris", "Ava",
    "Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Neha", "Arjun", "Kavya",
    "Minjun", "Jiwoo", "Seojun", "Hana", "Jihoon", "Yuna",
    "Haruto", "Sakura", "Ren", "Aoi", "Sora", "Yui",
    "Emir", "Elif", "Baran", "Zeynep", "Kaan", "Defne",
    "Charan", "Sruthi", "Naveen", "Divya",
    "Rajesh", "Sunita", "Manoj", "Kiran",
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Sharma", "Verma", "Reddy", "Kumar", "Iyer",
    "Kim", "Park", "Lee", "Choi", "Tanaka", "Sato", "Yamamoto", "Suzuki",
    "Yilmaz", "Demir", "Kaya", "Celik", "Gupta", "Singh", "Rao", "Nair",
    "Patel", "Das", "Roy", "Malhotra",
]


def generate_user_pool(count=150):
    """Generate `count` unique (first, last) name pairs."""
    names = set()
    while len(names) < count:
        names.add((random.choice(FIRST_NAMES), random.choice(LAST_NAMES)))
    return list(names)


def main():
    print("Connecting to MySQL and ensuring schema exists...")
    db.init_db()

    all_genres = sorted({g for _, genres, _ in MOVIES_SEED for g in genres})

    conn = db.get_connection()
    cur = conn.cursor()

    # -----------------------------------------------------------
    # Insert movies (skip any title that already exists, so this
    # script is safe to re-run without creating duplicates)
    # -----------------------------------------------------------
    cur.execute("SELECT title FROM movies")
    existing_titles = {row[0] for row in cur.fetchall()}

    new_movie_rows = [
        (title, ",".join(genres), rating)
        for title, genres, rating in MOVIES_SEED
        if title not in existing_titles
    ]

    if new_movie_rows:
        cur.executemany(
            "INSERT INTO movies (title, genres, rating) VALUES (%s, %s, %s)",
            new_movie_rows,
        )
        conn.commit()
        print(f"Inserted {len(new_movie_rows)} new movies.")
    else:
        print("All movies already present — skipping movie insert.")

    # -----------------------------------------------------------
    # Insert 150 new users
    # -----------------------------------------------------------
    cur.execute("SELECT COUNT(*) FROM users")
    users_before = cur.fetchone()[0]

    user_pool = generate_user_pool(150)
    new_user_rows = []
    for first, last in user_pool:
        name = f"{first} {last}"
        prefs = random.sample(all_genres, k=random.randint(1, 3))
        new_user_rows.append((name, ",".join(prefs)))

    cur.executemany(
        "INSERT INTO users (name, preferred_genres) VALUES (%s, %s)",
        new_user_rows,
    )
    conn.commit()
    print(f"Inserted {len(new_user_rows)} new users.")

    # -----------------------------------------------------------
    # Generate ratings for the newly added users only
    # (existing users/ratings are left untouched)
    # -----------------------------------------------------------
    cur.execute("SELECT movie_id, genres FROM movies")
    movie_rows = cur.fetchall()  # [(movie_id, "genre1,genre2"), ...]
    movies_with_genres = [(mid, set(g.split(","))) for mid, g in movie_rows]

    cur.execute(
        "SELECT user_id, preferred_genres FROM users ORDER BY user_id"
    )
    all_users = cur.fetchall()
    new_users = all_users[users_before:]  # only the ones we just inserted

    rating_rows = []
    for user_id, prefs in new_users:
        preferred = set((prefs or "").split(","))
        num_ratings = random.randint(3, 8)
        chosen_movies = random.sample(movies_with_genres, k=min(num_ratings, len(movies_with_genres)))

        for movie_id, movie_genres in chosen_movies:
            if preferred & movie_genres:          # overlaps with their taste
                rating = random.choice([4, 4, 5, 5, 5])
            else:                                  # random / exploratory watch
                rating = random.choice([2, 3, 3, 4])
            rating_rows.append((user_id, movie_id, rating))

    cur.executemany(
        "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
        rating_rows,
    )
    conn.commit()
    print(f"Inserted {len(rating_rows)} new ratings.")

    cur.close()
    conn.close()
    print("\n✅ Done! Restart your Streamlit app to see the new data.")


if __name__ == "__main__":
    main()
