#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:42:20 2026

@author: evangelinemadhumitha
"""

import streamlit as st
import json
import os
import requests
import random

st.markdown("""
<style>
.stApp {
background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
background-size: cover;
background-position: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<h1 style='text-align: center;'>🎬 What's Your Vibe</h1>
""",
unsafe_allow_html=True
)

PASSWORD = "movie123"

st.markdown(
"""
<p style='text-align: center; font-size:18px;'>Enter password to access the app</p>
""",
unsafe_allow_html=True
)

password = st.text_input("", type="password")

if password != PASSWORD:
    st.warning("🔒 Enter the correct password to continue")
    st.stop()
        
def get_movie_poster(title, language=""):
    api_key = "a837a8ca"

    url = f"https://www.omdbapi.com/?t={title}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    print(data)   # temporary check

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]
    
        return None


st.markdown("""
<style>
.stApp {
    background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                      url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
    background-size: cover;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 10em;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="What's Your Vibe?", page_icon="🎬", layout="centered")

FILE_NAME = "movies.json"

def load_movies():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_movies(movies):
    with open(FILE_NAME, "w") as file:
        json.dump(movies, file, indent=4)

st.markdown(
"""
<h1 style='text-align: center; font-size:50px;'>
🎬 What's Your Vibe?
</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<h6 style='text-align:center;'>Find movies based on your mood</h6>
""",
unsafe_allow_html=True
)

if "movies" not in st.session_state:
    st.session_state.movies = load_movies()

with st.container():
    st.subheader("Add a Movie")

    title = st.text_input("Movie Name")
    language = st.text_input("Language (optional)")
    genre = st.text_input("Genre")
    rating = st.slider("Rating", 0.0, 10.0, 5.0, 0.1)
    
    if rating <= 3:
      slider_color = "red"
    elif rating <= 5:
      slider_color = "#ff6666"
    elif rating <= 7:
      slider_color = "orange"
    else:
      slider_color = "green"
      
    st.markdown(f"""
    <style>
    div[data-baseweb="slider"] > div > div > div {{
      background: {slider_color} !important;
    }}

    div[data-baseweb="slider"] [role="slider"] {{
      background: {slider_color} !important;
      border: 2px solid {slider_color} !important;
    }}
    
    div[data-baseweb="slider"] [data-testid="stSliderThumbValue"] {{
      color: {slider_color} !important;
      font-weight: bold;
    }}

    </style>
    """, unsafe_allow_html=True)
      
    review = st.text_input("One Liner: ")

    vibes = st.multiselect(
        "Select vibes",
        [
            "funny","scary","emotional","epic","romantic","dark",
            "adventurous","mind-blowing","playful","thrilling",
            "mysterious","dramatic","heartwarming","sad",
            "intense","action-packed","fantasy","suspenseful",
            "inspiring","feel-good"
        ]
        )   

    poster = get_movie_poster(title, language)

    if st.button("Add Movie"):

        movie = {
            "title": title,
            "genre": genre,
            "rating": rating,
            "one-liner": review,
            "vibe": vibes,
            "poster": poster
        }

        st.session_state.movies.append(movie)
        save_movies(st.session_state.movies)
        st.success(f"{title} added successfully!")

st.divider()

st.subheader("Search by Vibe")
search_vibe = st.text_input("What's your vibe?")

if search_vibe:
    search_vibe = search_vibe.lower()
    found = False

    for movie in st.session_state.movies:

        if (search_vibe in movie["vibe"] or
            search_vibe in movie["genre"].lower() or
            search_vibe in movie.get("one-liner","").lower()):

            col1, col2 = st.columns([1.2, 3])

            with col1:
                if movie.get("poster"):
                    st.image(movie["poster"], width=350)

            with col2:
                st.markdown(f"## 🎬 {movie['title']}")
                st.write(f"**Genre:** {movie['genre']}")

                rating = movie["rating"]

                if rating <= 3:
                    color = "red"
                elif rating <= 5:
                    color = "#ff6666"
                elif rating <= 7:
                    color = "orange"
                else:
                    color = "green"

                st.markdown(
                    f"<h4 style='color:{color}'>⭐ Rating: {rating}/10</h4>",
                    unsafe_allow_html=True
                )

                st.write(f"**One Liner:** {movie['one-liner']}")
                st.write(f"**Vibes:** {', '.join(movie['vibe'])}")

            st.divider()
            found = True

    if not found:
        st.warning("Sorry, no movies matched your vibe.")
        
st.divider()
st.subheader("🎲 Random Movie Suggestion")

if st.button("Suggest a Movie"):
    if st.session_state.movies:
        movie = random.choice(st.session_state.movies)

        col1, col2 = st.columns([1.2, 3])

        with col1:
            if movie.get("poster"):
                st.image(movie["poster"], width=300)

        with col2:
            st.markdown(f"## 🎬 {movie['title']}")
            st.write(f"**Genre:** {movie['genre']}")

            rating = movie["rating"]

            if rating <= 3:
                color = "red"
            elif rating <= 5:
                color = "#ff6666"
            elif rating <= 7:
                color = "orange"
            else:
                color = "green"

            st.markdown(
                f"<h4 style='color:{color}'>⭐ Rating: {rating}/10</h4>",
                unsafe_allow_html=True
            )
            st.write(f"**One Liner:** {movie['one-liner']}")
            st.write(f"**Vibes:** {', '.join(movie['vibe'])}")
    else:
        st.warning("No movies added yet.")