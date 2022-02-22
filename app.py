import pickle
import streamlit as st
import requests
import pandas as pd


st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values
def fecth_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b75fc3d67305d46871cbf94c08050357&language=en-US'.format(movie_id))
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def get_recommendations(title,cosine_sim=similarity):
    # Get the index of the movie that matches the title
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scorex = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scored = sorted(sim_scorex, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scored[1:6]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    ###
    recommendation=[]
    for i in sim_scores:
        movie_id=movies['id'].iloc[i[0]]
        recommendation.append(fecth_poster(movie_id))
    # Return the top 10 most similar movies
    return movies['title'].iloc[movie_indices],recommendation
Selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = get_recommendations(Selected_movie_name,similarity)
    st.image(recommended_movie_posters[0])
    st.image(recommended_movie_posters[1])
    st.image(recommended_movie_posters[2])
    st.image(recommended_movie_posters[3])
    st.image(recommended_movie_posters[4])











