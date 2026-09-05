# Movie data stored using a hash table (dictionary)

movies = {
    1: {
        "title": "Inception",
        "genres": ["Sci-Fi", "Thriller"],
        "rating": 4.8
    },

    2: {
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Drama"],
        "rating": 4.7
    },

    3: {
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "rating": 4.9
    },

    4: {
        "title": "The Martian",
        "genres": ["Sci-Fi", "Adventure", "Drama"],
        "rating": 4.6
    },

    5: {
        "title": "Avengers: Endgame",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "rating": 4.5
    },

    6: {
        "title": "The Prestige",
        "genres": ["Drama", "Mystery", "Thriller"],
        "rating": 4.7
    },

    7: {
        "title": "Avatar",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "rating": 4.4
    },

    8: {
        "title": "Titanic",
        "genres": ["Drama", "Romance"],
        "rating": 4.6
    }
}


# User data stored using a hash table

users = {
    1: {
        "name": "User1",
        "preferred_genres": ["Sci-Fi", "Adventure"],
        "ratings": {
            1: 5,
            2: 5,
            5: 4
        }
    },

    2: {
        "name": "User2",
        "preferred_genres": ["Drama", "Thriller"],
        "ratings": {
            3: 5,
            6: 5,
            8: 4
        }
    }
}
