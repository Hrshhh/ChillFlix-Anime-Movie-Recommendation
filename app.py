import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_movie(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=25cb0e4dcc3e28854e30f65173067d31&language=en-US'.format(movie_id))
     return response.json()

def fetch_poster(movie_id):
     data = fetch_movie(movie_id)
     # st.text(data)
     return 'https://image.tmdb.org/t/p/original/' + data['poster_path']


def fetch_overview(movie_id):
     data = fetch_movie(movie_id)
     # st.text(data)
     return data['overview']

def fetch_genre(movie_id):
     data = fetch_movie(movie_id)
     sd = data['genres']
     L = ""
     for i in sd:
          L += i['name']
          L += "  "

     # st.text(data)
     return L

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
     index = movies[movies['title'] == movie].index[0]
     distances = similarity[index]
     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]
     recom_mov = []
     recom_mov_posters = []
     recom_mov_overview = []
     recom_mov_genre = []
     for i in movies_list:
          recom_mov.append(movies.iloc[i[0]].title)
          recom_mov_posters.append(fetch_poster(movies.iloc[i[0]].id))
          recom_mov_overview.append(fetch_overview(movies.iloc[i[0]].id))
          recom_mov_genre.append(fetch_genre(movies.iloc[i[0]].id))
          # st.text(fetch_overview(movies.iloc[i[0]].id))
          # st.text(i)
     return recom_mov, recom_mov_posters, recom_mov_overview, recom_mov_genre

st.title("MovieFlex")
st.header("Movie Recommendation System")
selected_movie_name = st.selectbox(
'Type or select the movie from the dropdown',
movies['title'].values)

if st.button('Recommend Kr'):
     m_name, m_posters, m_overview, m_genre = recommend(selected_movie_name)
     co1, co2 = st.columns([0.35,1])
     with co1:
          st.image(m_posters[0])
          # st.text(m_name[0])
          # print(m_name['overview'])

     with co2:
          # st.image(m_posters[1])
          st.header(m_name[0])
          st.write("**Overview** : " +" "+  m_overview[0])
          st.write("**Genres** : " +" "+ m_genre[0])

     col1, col2, col3, col4 = st.columns(4)

     with col1:
          st.image(m_posters[1])
          st.write(m_name[1])
          # print(m_name['overview'])

     with col2:
          st.image(m_posters[2])
          st.write(m_name[2])

     with col3:
          st.image(m_posters[3])
          st.write(m_name[3])

     with col4:
          st.image(m_posters[4])
          st.write(m_name[4])

     # with col5:
     #      st.image(m_posters[4])
     #      st.text(m_name[4])


# col1, col2, col3 = st.columns([1,1,1])

# with col1:
#     st.button('1')
# with col2:
#     st.button('2')
# with col3:
#     st.button('3')
    
# if st.button('Overview'):
#      m_posters, m_overview = recommend(selected_movie_name)
#      col1 = st.columns(1)

#      with col1:
#           st.image(m_posters[0])
#           st.text(m_overview[0])
