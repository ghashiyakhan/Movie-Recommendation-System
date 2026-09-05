# Movie Recommendation System
## Data Structures and Algorithms Project Report

### 1. Introduction

A movie recommendation system helps users discover movies that may match their interests. This project implements a simple recommendation system in Python while demonstrating important Data Structures and Algorithms concepts.

The system uses movie genres to create a similarity graph and uses user ratings to identify movies that the user likes. Candidate movies are scored and ranked to produce recommendations.

### 2. Problem Statement

Develop a movie recommendation system that uses suitable data structures and algorithms to:

- store movie and user information efficiently;
- identify similar movies;
- generate personalized recommendations;
- rank recommendations;
- compare the performance of different searching and sorting approaches.

### 3. Objectives

1. Implement a graph-based movie similarity model.
2. Store movie and user information using hash tables.
3. Generate recommendations from user ratings.
4. Use a heap for top-N recommendation selection.
5. Implement Merge Sort using recursion.
6. Compare Linear Search with Hash Table lookup.
7. Compare Merge Sort with Python's built-in sorting.
8. Analyze performance as dataset size increases.

### 4. Tools and Technologies

- Programming Language: Python
- Development Environment: Python IDLE
- Visualization: Matplotlib
- Concepts: Graphs, Hash Tables, Heaps, Searching, Sorting, Recursion, Divide and Conquer

### 5. Dataset

The project uses a small manually defined dataset containing 8 movies and 2 users.

Each movie contains:
- movie ID;
- title;
- genres;
- rating.

Each user contains:
- user ID;
- name;
- preferred genres;
- movie ratings.

Movies rated 4 or 5 by a user are treated as movies the user likes.

### 6. Data Structures

#### 6.1 Hash Table

Python dictionaries are used to store movies and users. Movie IDs and user IDs act as keys.

This provides average O(1) lookup for a known key.

#### 6.2 Graph

The `MovieGraph` class represents movies as vertices. An undirected edge is added between two movies when they have at least one genre in common.

For example, movies sharing the Sci-Fi genre are connected.

#### 6.3 Heap

The recommendation engine uses a heap to select the highest-scoring candidate movies efficiently.

The implementation stores negative scores because Python's `heapq` is a min-heap.

#### 6.4 Lists

Lists are used for movie genres, graph adjacency lists, recommendation results, and intermediate Merge Sort data.

### 7. Algorithms

#### 7.1 Graph Construction

Every pair of movies is compared. Their genre sets are intersected. If the intersection contains at least one genre, an undirected edge is created.

The graph construction uses pairwise comparison and therefore has O(V²) pair comparisons, where V is the number of movies.

#### 7.2 Recommendation Algorithm

The recommendation process is:

1. Obtain the selected user's ratings.
2. Identify movies rated 4 or higher.
3. Find their neighboring movies in the graph.
4. Ignore movies already rated by the user.
5. Increase each candidate's similarity score.
6. Add the movie's rating to the similarity score.
7. Insert candidates into a heap.
8. Extract the top N candidates.

The final recommendation score is:

`Final Score = Similarity Score + Movie Rating`

#### 7.3 Merge Sort

Merge Sort recursively divides the recommendation list into smaller lists and merges them according to recommendation score.

The implementation has O(n log n) time complexity.

### 8. Program Modules

#### `movie_data.py`

Stores the movie and user dictionaries.

#### `graph.py`

Contains the `MovieGraph` class and constructs the movie similarity graph.

#### `recommendation.py`

Contains the `RecommendationEngine` class and generates top-N recommendations.

#### `sorting.py`

Contains the recursive Merge Sort implementation.

#### `main.py`

Runs the recommendation system and displays recommendations before and after Merge Sort.

#### `performance.py`

Generates synthetic datasets and measures Linear Search, Hash Table lookup, Merge Sort, and Python built-in sorting.

### 9. Sample Result

For User 1, the program generated:

| Rank | Recommended Movie | Score |
|---:|---|---:|
| 1 | The Martian | 7.6 |
| 2 | Avatar | 7.4 |
| 3 | The Dark Knight | 6.9 |
| 4 | The Prestige | 6.7 |
| 5 | Titanic | 5.6 |

The result shows that the system successfully excludes movies already rated by the user and ranks candidate movies by their calculated recommendation scores.

### 10. Performance Analysis

#### 10.1 Searching

| Dataset Size | Linear Search | Hash Table |
|---:|---:|---:|
| 100 | 0.00000670 | 0.00000160 |
| 1,000 | 0.00005280 | 0.00000130 |
| 10,000 | 0.00051940 | 0.00000200 |
| 50,000 | 0.00273370 | 0.00000270 |
| 100,000 | 0.00590080 | 0.00000290 |

The experiment shows that Linear Search becomes slower as the dataset increases. Hash Table lookup remains almost constant in comparison. This demonstrates the practical benefit of average O(1) hash-table lookup over O(n) Linear Search.

#### 10.2 Sorting

| Dataset Size | Merge Sort | Python Built-in Sort |
|---:|---:|---:|
| 100 | 0.000301 | 0.000023 |
| 1,000 | 0.002262 | 0.000283 |
| 10,000 | 0.032105 | 0.002632 |
| 50,000 | 0.197936 | 0.013933 |
| 100,000 | 0.451380 | 0.033005 |

Both methods become slower as the dataset grows. Merge Sort maintains its theoretical O(n log n) complexity, while Python's built-in sort is considerably faster in the experiment because it is implemented and optimized for practical use.

### 11. Graphical Results

Two graphs were generated:

1. Linear Search vs Hash Table Lookup
2. Merge Sort vs Python Built-in Sort

The graphs visually demonstrate how execution time changes with increasing dataset size.

### 12. Complexity Analysis

| Component | Complexity |
|---|---:|
| Hash Table average lookup | O(1) |
| Linear Search | O(n) |
| Merge Sort | O(n log n) |
| Heap insertion | O(log n) |
| Heap extraction | O(log n) |
| Graph construction | O(V²) pair comparisons |

### 13. Advantages

- Demonstrates multiple DSA concepts in one practical application.
- Uses efficient hash-table lookup.
- Uses graph relationships to identify similar movies.
- Uses a heap for top-N selection.
- Includes explicit Merge Sort implementation.
- Includes empirical performance testing.
- Easy to extend with additional movies and users.

### 14. Limitations

- The current dataset is small and manually created.
- Movie similarity is based only on whether at least one genre is shared.
- Similarity is not weighted according to the number of common genres.
- User preferred genres are stored but are not currently used directly in the recommendation score.
- The recommendation model is rule-based rather than machine-learning-based.

### 15. Future Scope

Future versions could:

- use a larger real-world movie dataset;
- calculate weighted genre similarity;
- incorporate preferred genres into scoring;
- add collaborative filtering;
- use machine learning;
- provide a graphical user interface;
- allow users to enter ratings interactively.

### 16. Conclusion

The Movie Recommendation System successfully demonstrates how different data structures and algorithms can be combined to solve a practical problem. The graph is used to model relationships between movies, hash tables provide efficient data storage and lookup, a heap supports top-N recommendation selection, and Merge Sort demonstrates recursive divide-and-conquer sorting.

The performance analysis confirms that algorithm and data-structure selection affects practical execution time. Hash Table lookup performed much faster than Linear Search for larger datasets, while Python's optimized built-in sorting performed faster than the custom Merge Sort implementation.

Overall, the project provides a clear practical demonstration of DSA concepts through a movie recommendation application.
