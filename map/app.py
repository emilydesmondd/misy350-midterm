import os
import requests as r
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

st.title("Recipe Finder")
st.markdown("Find recipes based on ingredients you have!")
st.caption('example: "chicken, rice, broccoli"')

ingredients = st.text_input("Enter ingredients (comma separated):")
st.spinner("Searching for recipes...")

url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={api_key}"
response = r.get(url)
recipes = response.json()

for recipe in recipes:
    st.write(recipe["title"])
    st.image(recipe["image"])
    
if ingredients: 
    st.write(f"Recipes found for: {ingredients}")
else:
    st.write("Please enter some ingredients to find recipes.")




