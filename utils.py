import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.dropna(subset=['description'], inplace=True)
    df['combined'] = (df['listed_in'].fillna('') + ' ' +
                      df['cast'].fillna('') + ' ' +
                      df['description'].fillna(''))
    return df

def build_similarity_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df['combined'])
    similarity = cosine_similarity(tfidf_matrix)
    return similarity

# def recommend(title, df, similarity):
#     if title not in df['title'].values:
#         return ["Sorry, title not found."]
#     idx = df[df['title'] == title].index[0]
#     scores = list(enumerate(similarity[idx]))
#     scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
#     recs = [df.iloc[i[0]].title for i in scores]
#     return recs

def recommend(title, df, similarity, top_n=5):
    title = title.lower().strip()
    df['title'] = df['title'].str.lower().str.strip()

    if title not in df['title'].values:
        return [{"error": "Sorry, title not found."}]
    idx = df[df['title'] == title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_scores = scores[1:top_n + 1]
    recommendations = []
    for i, score in top_scores:
        recommendations.append({
            "title": df.iloc[i]['title'],
            "score": round(score, 3),
            "genre": df.iloc[i].get('genre', 'Unknown'),
            "description": df.iloc[i].get('description', 'No description available')
        })
    return recommendations