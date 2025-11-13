import streamlit as st
from utils import load_data, build_similarity_matrix, recommend

st.set_page_config(page_title="Netflix Recommender", page_icon="🎬", layout="centered")

st.title("🎬 Netflix Recommender & Insights Explorer")
st.write("Discover similar movies or shows based on content — powered by Machine Learning!")

@st.cache_data
def setup():
    df = load_data()
    similarity = build_similarity_matrix(df)
    return df, similarity

df, similarity = setup()


st.header("🔍 Find Similar Shows")
selected_title = st.selectbox("Select a Movie/Show:", df['title'].values[:5000])

if st.button("Recommend"):
    recs = recommend(selected_title, df, similarity)
    st.subheader("Top Recommendations:")
    for i, r in enumerate(recs, start=1):
        st.write(f"{i}. {r}")

st.sidebar.header("📊 Explore Netflix Insights")
if st.sidebar.checkbox("Show Visuals"):
    type_counts = df['type'].value_counts()
    st.sidebar.bar_chart(type_counts)
    st.sidebar.write("Top 10 Genres:")
    st.sidebar.bar_chart(df['listed_in'].value_counts().head(10))

st.caption("Built by Vamshi Krishna Garlapati | For EONVERSE AI Challenge 2025 🚀")