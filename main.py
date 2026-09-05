from movie_data import movies
from graph import MovieGraph
from recommendation import RecommendationEngine
from sorting import merge_sort


print("===================================")
print("   MOVIE RECOMMENDATION SYSTEM")
print("===================================")


# Build graph
movie_graph = MovieGraph()
movie_graph.build_graph(movies)


# Create recommendation engine
engine = RecommendationEngine(movie_graph)


# Generate recommendations
user_id = 1

recommendations = engine.recommend(user_id, top_n=5)


print("\nRecommendations Before Sorting")
print("--------------------------------")

for movie_id, score in recommendations:
    print(
        movies[movie_id]["title"],
        "→",
        round(score, 2)
    )


# Sort recommendations
sorted_recommendations = merge_sort(recommendations)


print("\nRecommendations After Merge Sort")
print("----------------------------------")

for movie_id, score in sorted_recommendations:

    print(
        movies[movie_id]["title"],
        "→",
        round(score, 2)
    )
