import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="fun_map")

st.title("Budget-friendly College Life Map!")

user_location = st.text_input("Enter city or zip")

# ✅ Always create a map first (default center if user enters nothing)
default_center = [39.7392, -104.9903]  # Denver as default
m = folium.Map(location=default_center, zoom_start=5)

# ✅ If user types a location, recenter map
if user_location:
    location = geolocator.geocode(user_location)

    if location:
        lat = location.latitude
        lon = location.longitude

        # recreate map centered on the user location
        m = folium.Map(location=[lat, lon], zoom_start=10)

        folium.Marker(
            [lat, lon],
            popup=f"You searched: {user_location}",
            tooltip="Your location"
        ).add_to(m)
    else:
        st.warning("Couldn't find that location. Try adding state (e.g., 'Hockessin, DE').")

# ✅ Add your example pin (always)
folium.Marker(
    [39.7392, -104.9903],
    popup="Night Life Spot",
    tooltip="Click for more info"
).add_to(m)

# ✅ Display the map
st_folium(m, width=700)

st.sidebar.title("Your Favorites")