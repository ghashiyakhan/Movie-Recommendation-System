import heapq
from movie_data import movies, users


class RecommendationEngine:

    def __init__(self, movie_graph):
        self.movie_graph = movie_graph

    def recommend(self, user_id, top_n=5):

        user = users[user_id]

        # Movies already rated by the user
        rated_movies = user["ratings"]

        # Store recommendation scores
        recommendation_scores = {}

        # Find movies the user liked
        for movie_id, rating in rated_movies.items():

            # We consider ratings 4 or 5 as liked
            if rating >= 4:

                # Find similar movies from the graph
                similar_movies = self.movie_graph.graph[movie_id]

                for similar_id in similar_movies:

                    # Don't recommend a movie already rated
                    if similar_id in rated_movies:
                        continue

                    # Give one point for similarity
                    recommendation_scores[similar_id] = (
                        recommendation_scores.get(similar_id, 0) + 1
                    )

        # Use a heap to find the top recommendations
        heap = []

        for movie_id, score in recommendation_scores.items():

            movie_rating = movies[movie_id]["rating"]

            # Combine similarity and movie rating
            final_score = score + movie_rating

            heapq.heappush(
                heap,
                (-final_score, movie_id)
            )

        # Extract top N movies
        recommendations = []

        while heap and len(recommendations) < top_n:

            negative_score, movie_id = heapq.heappop(heap)

            recommendations.append(
                (movie_id, -negative_score)
            )

        return recommendations
