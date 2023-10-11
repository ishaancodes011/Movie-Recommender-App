import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests . get("https://api.themoviedb.org/3/movie/{}?api_key=7e2189de88a09696562706c7efda5d89&language=en-US". format(movie_id))
    data = response . json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    i = movies[movies['title'] == movie].index[0]  # Getting the index of the movie
    distances = similarity[i]
    # Sorting the distances will require enumerating to cover up for the shuffling while sorting.
    movies_lst = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    # First element will be skipped as it is the movie itself

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_lst:
        movie_id = movies.iloc[i[0]] . movie_id
        # Fetch the movie poster from API
        recommended_movies_posters . append(fetch_poster(movie_id))

        recommended_movies . append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

st.set_page_config(
    page_title= "Movie Recommender App",
    page_icon = "🧊"
)

st . title("Movie Recommender System")

movies_list = pickle . load(open('movies.pkl','rb'))
movies = pd . DataFrame(movies_list)

similarity = pickle . load(open('similarity.pkl','rb'))

selected_movie_name = st . selectbox(
    "Select the movie:",
    movies['title'] . values
)

if st . button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

