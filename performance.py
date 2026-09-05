import time
import random
import matplotlib.pyplot as plt

from sorting import merge_sort


# ---------------------------------------------------
# 1. Generate Synthetic Movie Data
# ---------------------------------------------------

def generate_movies(size):

    movie_list = []

    for i in range(1, size + 1):

        movie_list.append({
            "id": i,
            "title": f"Movie {i}",
            "rating": random.uniform(1, 5)
        })

    return movie_list


# ---------------------------------------------------
# 2. Linear Search
# ---------------------------------------------------

def linear_search(movies, target_id):

    for movie in movies:

        if movie["id"] == target_id:
            return movie

    return None


# ---------------------------------------------------
# 3. Hash Table Lookup
# ---------------------------------------------------

def hash_lookup(movie_table, target_id):

    return movie_table.get(target_id)


# ---------------------------------------------------
# 4. Measure Search Performance
# ---------------------------------------------------

def measure_search_time(size):

    movies = generate_movies(size)

    # Create hash table
    movie_table = {}

    for movie in movies:

        movie_table[movie["id"]] = movie

    # Worst-case target for linear search
    target_id = size

    # Measure Linear Search
    start = time.perf_counter()

    linear_search(movies, target_id)

    linear_time = time.perf_counter() - start

    # Measure Hash Table Lookup
    start = time.perf_counter()

    hash_lookup(movie_table, target_id)

    hash_time = time.perf_counter() - start

    return linear_time, hash_time


# ---------------------------------------------------
# 5. Measure Sorting Performance
# ---------------------------------------------------

def measure_sort_time(size):

    movies = generate_movies(size)

    # Create (movie_id, rating) tuples
    movie_scores = [
        (movie["id"], movie["rating"])
        for movie in movies
    ]

    # Measure Merge Sort
    start = time.perf_counter()

    merge_sort(movie_scores.copy())

    merge_time = time.perf_counter() - start

    # Measure Python Built-in Sort
    start = time.perf_counter()

    sorted(
        movie_scores.copy(),
        key=lambda x: x[1],
        reverse=True
    )

    builtin_time = time.perf_counter() - start

    return merge_time, builtin_time


# ---------------------------------------------------
# 6. Main Performance Test
# ---------------------------------------------------

def main():

    # Dataset sizes
    dataset_sizes = [100, 1000, 10000, 50000, 100000]

    # Lists to store results
    linear_times = []
    hash_times = []

    merge_times = []
    builtin_times = []

    print("======================================")
    print("       PERFORMANCE ANALYSIS")
    print("======================================")

    # ------------------------------------------------
    # Search Performance
    # ------------------------------------------------

    print("\nSearch Performance")
    print("------------------")

    for size in dataset_sizes:

        linear_time, hash_time = measure_search_time(size)

        linear_times.append(linear_time)
        hash_times.append(hash_time)

        print(
            f"{size:>6} movies | "
            f"Linear: {linear_time:.8f} sec | "
            f"Hash: {hash_time:.8f} sec"
        )

    # ------------------------------------------------
    # Sorting Performance
    # ------------------------------------------------

    print("\nSorting Performance")
    print("-------------------")

    for size in dataset_sizes:

        merge_time, builtin_time = measure_sort_time(size)

        merge_times.append(merge_time)
        builtin_times.append(builtin_time)

        print(
            f"{size:>6} movies | "
            f"Merge Sort: {merge_time:.6f} sec | "
            f"Built-in: {builtin_time:.6f} sec"
        )

    # ------------------------------------------------
    # Graph 1: Search Performance
    # ------------------------------------------------

    plt.figure()

    plt.plot(
        dataset_sizes,
        linear_times,
        marker="o",
        label="Linear Search"
    )

    plt.plot(
        dataset_sizes,
        hash_times,
        marker="o",
        label="Hash Table"
    )

    plt.xlabel("Number of Movies")
    plt.ylabel("Search Time (seconds)")
    plt.title("Linear Search vs Hash Table Lookup")

    plt.legend()
    plt.grid(True)

    plt.savefig("search_performance.png")

    # ------------------------------------------------
    # Graph 2: Sorting Performance
    # ------------------------------------------------

    plt.figure()

    plt.plot(
        dataset_sizes,
        merge_times,
        marker="o",
        label="Merge Sort"
    )

    plt.plot(
        dataset_sizes,
        builtin_times,
        marker="o",
        label="Python Built-in Sort"
    )

    plt.xlabel("Number of Movies")
    plt.ylabel("Sorting Time (seconds)")
    plt.title("Merge Sort vs Python Built-in Sort")

    plt.legend()
    plt.grid(True)

    plt.savefig("sorting_performance.png")

    # Display both graphs
    plt.show()


# ---------------------------------------------------
# 7. Run Program
# ---------------------------------------------------

if __name__ == "__main__":
    main()
