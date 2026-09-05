class MovieGraph:

    def __init__(self):
        self.graph = {}

    def build_graph(self, movies):
        # Create an empty list for every movie
        for movie_id in movies:
            self.graph[movie_id] = []

        # Compare every pair of movies
        movie_ids = list(movies.keys())

        for i in range(len(movie_ids)):
            for j in range(i + 1, len(movie_ids)):

                movie1_id = movie_ids[i]
                movie2_id = movie_ids[j]

                genres1 = set(movies[movie1_id]["genres"])
                genres2 = set(movies[movie2_id]["genres"])

                common_genres = genres1.intersection(genres2)

                if len(common_genres) > 0:
                    self.graph[movie1_id].append(movie2_id)
                    self.graph[movie2_id].append(movie1_id)

    def display_graph(self, movies):
        print("\nMOVIE SIMILARITY GRAPH")
        print("-----------------------")

        for movie_id, neighbours in self.graph.items():
            movie_name = movies[movie_id]["title"]

            print(f"\n{movie_name} is similar to:")

            for neighbour_id in neighbours:
                print(f" - {movies[neighbour_id]['title']}")
