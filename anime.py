import streamlit as st
import pickle
import pandas as pd

anime_dict = pickle.load(open('anime_dict.pkl', 'rb'))
animes = pd.DataFrame(anime_dict)

similar = pickle.load(open('similar.pkl', 'rb'))

def recommend(movie):
     index = animes[animes['Name'] == movie].index[0]
     distances = similar[index]
     anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
     recommended_anime = []
     for i in anime_list:
          recommended_anime.append(animes.iloc[i[0]].Name)
     return recommended_anime

st.title("Anime Recommendation System")

selected_anime_name = st.selectbox(
'How would you like to be contacted?',
animes['Name'].values)

if st.button('Recommend'):
     recommendations = recommend(selected_anime_name)
     for i in recommendations:
          st.write(i)
