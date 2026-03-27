import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def fetch_poster(movie_id):
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

movies['tags'] = movies['tags'].fillna('')

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
movies['title'].values)

if st.button('Recommend'):
    names,posters= recommendations = recommend(selected_movie_name)

    col1,col2,col3, col4, col5 = st.columns(5)
    with col1:
        st.caption(names[0])
        st.image(posters[0])
    with col2:
        st.caption(names[1])
        st.image(posters[1])
    with col3:
        st.caption(names[2])
        st.image(posters[2])
    with col4:
        st.caption(names[3])
        st.image(posters[3])
    with col5:
        st.caption(names[4])
        st.image(posters[4])