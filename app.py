import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from collections import Counter

from graph import MovieGraph
from recommendation import RecommendationEngine
from sorting import merge_sort
from performance import measure_search_time, measure_sort_time
import db


# ---------------------------------------------------------------
# Category tags used to color-code the network graph
# ---------------------------------------------------------------
CATEGORY_TAGS = [
    "Hollywood", "Marvel", "DC", "Bollywood", "Tollywood",
    "Bhojpuri", "K-Drama", "Ghibli", "Anime", "Turkish",
]
CATEGORY_COLORS = {
    "Hollywood": "#a6402c",
    "Marvel": "#e74c3c",
    "DC": "#2c3e50",
    "Bollywood": "#d4a017",
    "Tollywood": "#8e44ad",
    "Bhojpuri": "#16a085",
    "K-Drama": "#2980b9",
    "Ghibli": "#27ae60",
    "Anime": "#e67e22",
    "Turkish": "#c2185b",
    "Other": "#95a5a6",
}


def get_category(genres):
    for tag in CATEGORY_TAGS:
        if tag in genres:
            return tag
    return "Other"


st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")


# ---------------------------------------------------------------
# Connect to MySQL, create tables, seed on first run (once per session)
# ---------------------------------------------------------------
@st.cache_resource
def setup_database():
    db.init_db()
    db.seed_if_empty()
    return True


try:
    setup_database()
except Exception as e:
    st.error(
        "❌ Could not connect to MySQL.\n\n"
        f"Error: `{e}`\n\n"
        "Check that: MySQL is running, and the username/password/host in **db.py** "
        "(top of the file, `DB_CONFIG`) match your MySQL login."
    )
    st.stop()


# ---------------------------------------------------------------
# Load current data fresh from MySQL on every run
# (small dataset — no caching needed, always shows the latest data)
# ---------------------------------------------------------------
movies = db.load_movies()
users = db.load_users()

movie_graph = MovieGraph()
movie_graph.build_graph(movies)
engine = RecommendationEngine(movie_graph, movies, users)


# ---------------------------------------------------------------
# Sidebar: page switcher
# ---------------------------------------------------------------
st.sidebar.title("🎬 Movie Rec System")
page = st.sidebar.radio("Navigate", ["Recommendations", "Analytics Dashboard", "Manage Data"])
st.sidebar.divider()


# =================================================================
# PAGE 1: RECOMMENDATIONS
# =================================================================
def render_recommendations_page():
    st.title("🎬 Movie Recommendation System")
    st.caption("DSA CIA2 Project — Graph traversal, Heap (priority queue), and Merge Sort — data from MySQL")
    st.divider()

    if not users:
        st.warning("No users yet. Go to 'Manage Data' to add one.")
        return
    if not movies:
        st.warning("No movies yet. Go to 'Manage Data' to add one.")
        return

    st.sidebar.header("Select User")
    user_id = st.sidebar.selectbox(
        "Choose a user",
        options=list(users.keys()),
        format_func=lambda uid: users[uid]["name"],
    )
    top_n = st.sidebar.slider("Number of recommendations", min_value=1, max_value=8, value=5)

    st.sidebar.divider()
    st.sidebar.markdown("**Preferred genres:**")
    st.sidebar.write(", ".join(users[user_id]["preferred_genres"]) or "None set")

    st.subheader(f"📋 {users[user_id]['name']}'s Ratings")
    rated = users[user_id]["ratings"]

    if not rated:
        st.info("This user hasn't rated any movies yet — add ratings in 'Manage Data'.")
    else:
        rated_df = pd.DataFrame(
            [{"Movie": movies[mid]["title"], "Genres": ", ".join(movies[mid]["genres"]), "Rating": r}
             for mid, r in rated.items() if mid in movies]
        )
        st.dataframe(rated_df, hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("✨ Recommendations")

    if st.button("Generate Recommendations", type="primary"):
        recommendations = engine.recommend(user_id, top_n=top_n)

        if not recommendations:
            st.warning("No recommendations found — this user needs ratings of 4+ on some movies first.")
        else:
            before_df = pd.DataFrame(
                [{"Movie": movies[mid]["title"], "Genres": ", ".join(movies[mid]["genres"]), "Score": round(score, 2)}
                 for mid, score in recommendations]
            )
            sorted_recommendations = merge_sort(recommendations)
            after_df = pd.DataFrame(
                [{"Movie": movies[mid]["title"], "Genres": ", ".join(movies[mid]["genres"]), "Score": round(score, 2)}
                 for mid, score in sorted_recommendations]
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Before Sorting** (heap order)")
                st.dataframe(before_df, hide_index=True, use_container_width=True)
            with col2:
                st.markdown("**After Merge Sort** (ranked)")
                st.dataframe(after_df, hide_index=True, use_container_width=True)

            st.markdown("### 🏆 Top Pick")
            top_movie_id, top_score = sorted_recommendations[0]
            st.success(f"**{movies[top_movie_id]['title']}** — score {round(top_score, 2)}")
    else:
        st.info("Click the button above to generate recommendations for this user.")

    st.divider()
    with st.expander("🕸️ View Movie Similarity Graph (text)"):
        for movie_id, neighbours in movie_graph.graph.items():
            movie_name = movies[movie_id]["title"]
            similar_titles = ", ".join(movies[n]["title"] for n in neighbours) if neighbours else "None"
            st.markdown(f"**{movie_name}** is similar to: {similar_titles}")

    with st.expander("🎞️ View All Movies"):
        all_df = pd.DataFrame(
            [{"Movie": m["title"], "Genres": ", ".join(m["genres"]), "Rating": m["rating"]}
             for m in movies.values()]
        )
        st.dataframe(all_df, hide_index=True, use_container_width=True)


# =================================================================
# PAGE 2: ANALYTICS DASHBOARD
# =================================================================
def render_analytics_page():
    st.title("📊 Analytics Dashboard")
    st.caption("Dataset stats, graph structure, and algorithm performance — live from MySQL")
    st.divider()

    if not movies:
        st.warning("No movies yet. Go to 'Manage Data' to add some.")
        return

    st.subheader("📌 Basic Stats")

    all_ratings = [m["rating"] for m in movies.values()]
    all_genres = [g for m in movies.values() for g in m["genres"]]
    genre_counts = Counter(all_genres)
    degrees = {mid: len(neighbours) for mid, neighbours in movie_graph.graph.items()}
    total_edges = sum(degrees.values()) // 2

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Movies", len(movies))
    c2.metric("Total Users", len(users))
    c3.metric("Avg Movie Rating", f"{sum(all_ratings) / len(all_ratings):.2f}")
    c4.metric("Similarity Connections", total_edges)

    if degrees:
        most_connected_id = max(degrees, key=degrees.get)
        c5, c6 = st.columns(2)
        if genre_counts:
            c5.metric("Most Common Genre", genre_counts.most_common(1)[0][0])
        c6.metric("Most Connected Movie", movies[most_connected_id]["title"], f"{degrees[most_connected_id]} links")

    st.divider()

    st.subheader("🎭 Genre & Rating Distribution")
    col1, col2 = st.columns(2)

    with col1:
        if genre_counts:
            genre_df = pd.DataFrame(genre_counts.items(), columns=["Genre", "Count"]).sort_values("Count", ascending=False)
            st.markdown("**Movies per Genre**")
            st.bar_chart(genre_df.set_index("Genre"))

    with col2:
        rating_df = pd.DataFrame(
            [{"Movie": m["title"], "Rating": m["rating"]} for m in movies.values()]
        ).sort_values("Rating", ascending=False)
        st.markdown("**Rating per Movie**")
        st.bar_chart(rating_df.set_index("Movie"))

    st.divider()

    st.subheader("🕸️ Movie Similarity Graph (Network View)")
    st.caption("Node size = connections. Node color = category. Hover any node for details — zoom/pan with your mouse. Use the filter below to reduce clutter.")

    all_categories = sorted({get_category(m["genres"]) for m in movies.values()})
    selected_categories = st.multiselect(
        "Filter by category", options=all_categories, default=all_categories
    )

    filtered_ids = {mid for mid, m in movies.items() if get_category(m["genres"]) in selected_categories}

    G = nx.Graph()
    for mid in filtered_ids:
        G.add_node(mid)
    for mid in filtered_ids:
        for n in movie_graph.graph.get(mid, []):
            if n in filtered_ids:
                G.add_edge(mid, n)

    if G.number_of_nodes() == 0:
        st.info("No movies match the selected filters.")
    else:
        node_count = G.number_of_nodes()
        pos = nx.spring_layout(G, seed=42, k=2.2 / (node_count ** 0.5), iterations=150)
        node_degrees = dict(G.degree())

        # Only label the top ~15 most-connected nodes to avoid a wall of overlapping text
        degree_values = sorted(node_degrees.values(), reverse=True)
        label_threshold = degree_values[min(14, len(degree_values) - 1)]

        edge_x, edge_y = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.6, color="rgba(221, 208, 184, 0.35)"),
            hoverinfo="none", mode="lines",
        )

        node_x, node_y, node_color, node_size, node_hover, node_label = [], [], [], [], [], []
        for mid in G.nodes():
            x, y = pos[mid]
            node_x.append(x)
            node_y.append(y)
            cat = get_category(movies[mid]["genres"])
            node_color.append(CATEGORY_COLORS.get(cat, "#95a5a6"))
            deg = node_degrees[mid]
            node_size.append(11 + deg * 1.6)
            node_hover.append(
                f"{movies[mid]['title']}<br>Category: {cat}<br>Rating: {movies[mid]['rating']}<br>Connections: {deg}"
            )
            node_label.append(movies[mid]["title"] if deg >= label_threshold else "")

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            text=node_label,
            textposition="top center",
            textfont=dict(size=9, color="white"),
            hovertext=node_hover,
            hoverinfo="text",
            marker=dict(size=node_size, color=node_color, line=dict(width=1, color="#211a15")),
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="#211a15",
            paper_bgcolor="#211a15",
            height=620,
        )
        st.plotly_chart(fig, use_container_width=True)

        legend_html = " ".join(
            f'<span style="background:{CATEGORY_COLORS.get(c, "#95a5a6")}; color:white; '
            f'padding:3px 11px; border-radius:12px; font-size:0.8em; margin-right:6px;">{c}</span>'
            for c in all_categories
        )
        st.markdown(legend_html, unsafe_allow_html=True)

    st.divider()

    st.subheader("⚡ Algorithm Performance")
    st.caption("Reuses the exact functions from your performance.py.")

    dataset_sizes = [100, 1000, 10000, 50000, 100000]

    if st.button("Run Live Benchmark", type="primary"):
        with st.spinner("Running benchmark across dataset sizes..."):
            linear_times, hash_times = [], []
            merge_times, builtin_times = [], []

            for size in dataset_sizes:
                lt, ht = measure_search_time(size)
                mt, bt = measure_sort_time(size)
                linear_times.append(lt)
                hash_times.append(ht)
                merge_times.append(mt)
                builtin_times.append(bt)

            search_df = pd.DataFrame({
                "Dataset Size": dataset_sizes,
                "Linear Search (s)": linear_times,
                "Hash Table (s)": hash_times,
            }).set_index("Dataset Size")

            sort_df = pd.DataFrame({
                "Dataset Size": dataset_sizes,
                "Merge Sort (s)": merge_times,
                "Built-in Sort (s)": builtin_times,
            }).set_index("Dataset Size")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Linear Search vs Hash Table Lookup**")
                st.line_chart(search_df)
            with col2:
                st.markdown("**Merge Sort vs Python Built-in Sort**")
                st.line_chart(sort_df)
    else:
        st.info("Click the button above to benchmark your search & sort algorithms live.")

    import os
    if os.path.exists("search_performance.png") or os.path.exists("sorting_performance.png"):
        st.divider()
        st.subheader("🖼️ Previously Saved Performance Charts")
        col1, col2 = st.columns(2)
        if os.path.exists("search_performance.png"):
            col1.image("search_performance.png", caption="Search Performance")
        if os.path.exists("sorting_performance.png"):
            col2.image("sorting_performance.png", caption="Sorting Performance")


# =================================================================
# PAGE 3: MANAGE DATA
# =================================================================
def render_manage_data_page():
    st.title("🗄️ Manage Data")
    st.caption("Add new movies, users, and ratings — saved directly to your MySQL database.")

    tab1, tab2, tab3 = st.tabs(["🎬 Add Movie", "👤 Add User", "⭐ Add Rating"])

    with tab1:
        with st.form("add_movie_form", clear_on_submit=True):
            title = st.text_input("Movie Title")
            genres_input = st.text_input("Genres (comma-separated)", placeholder="e.g. Sci-Fi, Drama")
            rating = st.slider("Rating", 1.0, 5.0, 4.0, 0.1)
            submitted = st.form_submit_button("Add Movie")

            if submitted:
                if not title.strip() or not genres_input.strip():
                    st.error("Please fill in both the title and genres.")
                else:
                    genres_list = [g.strip() for g in genres_input.split(",") if g.strip()]
                    db.add_movie(title.strip(), genres_list, rating)
                    st.success(f"✅ Added '{title}' to the database.")
                    st.rerun()

    with tab2:
        with st.form("add_user_form", clear_on_submit=True):
            name = st.text_input("User Name")
            pref_input = st.text_input("Preferred Genres (comma-separated, optional)", placeholder="e.g. Action, Comedy")
            submitted = st.form_submit_button("Add User")

            if submitted:
                if not name.strip():
                    st.error("Please enter a name.")
                else:
                    pref_list = [g.strip() for g in pref_input.split(",") if g.strip()]
                    db.add_user(name.strip(), pref_list)
                    st.success(f"✅ Added user '{name}'.")
                    st.rerun()

    with tab3:
        if not users or not movies:
            st.info("Add at least one user and one movie first (other tabs above).")
        else:
            with st.form("add_rating_form", clear_on_submit=True):
                user_choice = st.selectbox("User", options=list(users.keys()), format_func=lambda uid: users[uid]["name"])
                movie_choice = st.selectbox("Movie", options=list(movies.keys()), format_func=lambda mid: movies[mid]["title"])
                rating_val = st.slider("Rating", 1.0, 5.0, 4.0, 0.5)
                submitted = st.form_submit_button("Save Rating")

                if submitted:
                    db.add_rating(user_choice, movie_choice, rating_val)
                    st.success("✅ Rating saved.")
                    st.rerun()

    st.divider()
    st.subheader("Current Data Snapshot")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Movies**")
        if movies:
            st.dataframe(
                pd.DataFrame([{"ID": mid, "Title": m["title"], "Genres": ", ".join(m["genres"]), "Rating": m["rating"]}
                              for mid, m in movies.items()]),
                hide_index=True, use_container_width=True,
            )
        else:
            st.caption("No movies yet.")

    with col2:
        st.markdown("**Users**")
        if users:
            st.dataframe(
                pd.DataFrame([{"ID": uid, "Name": u["name"], "Preferred Genres": ", ".join(u["preferred_genres"])}
                              for uid, u in users.items()]),
                hide_index=True, use_container_width=True,
            )
        else:
            st.caption("No users yet.")


# =================================================================
# ROUTER
# =================================================================
if page == "Recommendations":
    render_recommendations_page()
elif page == "Analytics Dashboard":
    render_analytics_page()
else:
    render_manage_data_page()