import streamlit as st
import requests

TMDB_API_KEY = "cc45eb418523213195d914267d63ae15"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_movie(query):
    url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()
    if response["results"]:
        return response["results"][0]  # best match
    return None

def get_similar(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/similar?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()
    return response.get("results", [])

def get_poster(path):
    if path:
        return f"https://image.tmdb.org/t/p/w500{path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

st.set_page_config(page_title="Netflix Recommender", layout="wide")
st.title("Real-Time Netflix-Style Recommender")
st.write("Enter a movie/show name and get real-time recommendations!")

query = st.text_input("🔍 Search for a Movie:", "")

if query:
    movie = search_movie(query)

    if movie:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(get_poster(movie.get("poster_path")), width=300)

        with col2:
            st.subheader(movie["title"])
            st.write(f"Rating: {movie.get('vote_average', 'N/A')}")
            st.write(f"Release Date: {movie.get('release_date', 'N/A')}")
            st.write("**Overview:**")
            st.write(movie.get("overview", "No description available"))

        st.markdown("---")
        st.subheader("Similar Titles You May Like:")

        similar = get_similar(movie["id"])

        if similar:
            cols = st.columns(4)
            for i, m in enumerate(similar[:8]):
                with cols[i % 4]:
                    st.image(get_poster(m["poster_path"]), width=200)
                    st.caption(m["title"])
        else:
            st.write("No recommendations found.")

    else:
        st.error("Movie not found. Try another name!")
