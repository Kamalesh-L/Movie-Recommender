import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, number):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:number+1]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def get_director_movies(director_name):
    director_movies = moviess[moviess['director'] == director_name]
    director_movies_sorted = director_movies.sort_values(by="rating", ascending=False)
    return director_movies_sorted['title'].tolist()

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
moviess=pickle.load(open('movie_lists.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies)
moviess = pd.DataFrame(moviess)
print(movies.head)
print(movies.columns)
print(moviess.head)
print(moviess.columns)


# Set background image
page_bg_img = '''
<style>
.stApp {
background-image: url("/Users/kamaleshl/Desktop/ML-REVIEW-2/Review 1/pink.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Set page title and header
st.title('Movie Recommender System 🚨 ▶ 🎥 ▶ 🎬')
st.sidebar.header('USER INPUT:🍿🕶️', divider='blue')

# User input and recommendation logic
with st.sidebar:
    option = st.radio("Select an option:", ["Movie Recommendation", "Director's Movies"])

    if option == "Movie Recommendation":
        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown👇🏻",
            movie_list
        )
        button = st.button('✨Show Recommendation✨')
        st.divider()
        number = st.number_input('Number of recommendations needed:', step=1, value=6)

    else:  # Director's Movies
        director_list = moviess['director'].unique()
        selected_director = st.selectbox(
            "Select a director from the dropdown👇🏻",
            director_list
        )
        button = st.button('✨Show Movies✨')

# Display recommendations or director's movies on button click
if button:
    if option == "Movie Recommendation":
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, number)
        st.image(recommended_movie_posters, width=150, caption=recommended_movie_names)

    else:  # Director's Movies
        director_movies = get_director_movies(selected_director)
        st.success(f"{selected_director}'s Movies:")
        # st.write(director_movies)
        # st.table(pd.DataFrame({"Movies": director_movies}))
        st.table(pd.DataFrame({"Movies": director_movies}).style.set_properties(**{'text-align': 'left', 'font-size': '16px'}))

        

