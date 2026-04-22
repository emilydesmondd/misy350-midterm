import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from pathlib import Path

st.set_page_config(page_title="Hangout Map", layout="wide")

# -----------------------------
# LOAD SAVED LOCATIONS
# -----------------------------
json_location = Path("location.json")

saved_locations = []
if json_location.exists():
    try:
        with open(json_location, "r", encoding="utf-8") as f:
            saved_locations = json.load(f)
    except json.JSONDecodeError:
        saved_locations = []

# -----------------------------
# PRESET PLACES
# -----------------------------
places = {
    "Main Street Newark": {"lat": 39.6837, "lon": -75.7497},
    "Christiana Mall": {"lat": 39.6785, "lon": -75.6582},
    "University of Delaware": {"lat": 39.6780, "lon": -75.7506},
    "Barnes & Noble": {"lat": 39.6817, "lon": -75.7468},
    "Starbucks Newark": {"lat": 39.6848, "lon": -75.7495},
    "Cinemark Christiana": {"lat": 39.6778, "lon": -75.6570},
    "Fred Rust Ice Arena": {"lat": 39.6632, "lon": -75.7508},
    "Newark Reservoir": {"lat": 39.6948, "lon": -75.7745},
    "College Square": {"lat": 39.6809, "lon": -75.7192},
}

# -----------------------------
# DEALS DATA
# -----------------------------
deals = [
    {"name": "Klondike Kate's", "deal": "20% off all items", "lat": 39.6839, "lon": -75.7496, "color": "#F9C6C9"},
    {"name": "Santa Fe", "deal": "Buy one get one free margaritas", "lat": 39.6833, "lon": -75.7490, "color": "#F7D6BF"},
    {"name": "The Greenhouse", "deal": "Free appetizer with any entree", "lat": 39.6827, "lon": -75.7513, "color": "#D8EFCF"},
    {"name": "Grain Craft Bar", "deal": "15% off drinks on Wednesdays", "lat": 39.6844, "lon": -75.7497, "color": "#DDD6F3"},
    {"name": "Christiana Mall Food Court", "deal": "Free drink with any combo meal", "lat": 39.6788, "lon": -75.6585, "color": "#F5D3E2"},
    {"name": "Target Christiana", "deal": "10% off school supplies", "lat": 39.6769, "lon": -75.6547, "color": "#CFE3F6"},
    {"name": "Barnes & Noble Cafe", "deal": "Buy a coffee, get a pastry half off", "lat": 39.6817, "lon": -75.7468, "color": "#F4E7BE"},
    {"name": "Starbucks Newark", "deal": "Half-price iced drinks after 3 PM", "lat": 39.6848, "lon": -75.7495, "color": "#D7EFD9"},
    {"name": "Fred Rust Ice Arena", "deal": "Student skate night: 2-for-1 admission", "lat": 39.6632, "lon": -75.7508, "color": "#D3EAF7"},
    {"name": "Cinemark Christiana", "deal": "Student discount movie tickets on Thursdays", "lat": 39.6778, "lon": -75.6570, "color": "#E7D4F4"},
    {"name": "College Square Shopping Center", "deal": "Free tote bag with $25 purchase", "lat": 39.6809, "lon": -75.7192, "color": "#D9E6F2"},
    {"name": "Newark Reservoir Trail Stop", "deal": "Free smoothie upgrade on weekends", "lat": 39.6948, "lon": -75.7745, "color": "#D3EFE7"},
]

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #6B5B73;
        margin-bottom: 6px;
    }

    .sub-text {
        text-align: center;
        font-size: 17px;
        color: #8A7F88;
        margin-bottom: 24px;
    }

    .panel {
        background-color: #FFFDFB;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }

    .deal-card {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='main-title'>Budget Hangout Map</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Find fun places and fake local deals around Newark</div>", unsafe_allow_html=True)

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([3, 1], gap="large")

# -----------------------------
# MAP PANEL
# -----------------------------
with col1:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    selected_place = st.selectbox("Choose a location", list(places.keys()))
    coords = places[selected_place]

    m = folium.Map(location=[coords["lat"], coords["lon"]], zoom_start=13)

    # selected location
    folium.Marker(
        [coords["lat"], coords["lon"]],
        popup=selected_place,
        tooltip="Selected Location",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # saved locations
    for loc in saved_locations:
        if isinstance(loc, dict) and "lat" in loc and "lon" in loc:
            folium.Marker(
                [loc["lat"], loc["lon"]],
                popup=loc.get("name", "Saved Location"),
                tooltip=loc.get("name", "Saved Location"),
                icon=folium.Icon(color="red")
            ).add_to(m)

    # deal markers
    for deal in deals:
        popup_html = f"""
        <div style="width:210px; font-family:Arial, sans-serif;">
            <h4 style="margin-bottom:6px;">{deal['name']}</h4>
            <p style="margin:0;"><b>Deal:</b> {deal['deal']}</p>
        </div>
        """

        folium.Marker(
            [deal["lat"], deal["lon"]],
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=deal["name"],
            icon=folium.Icon(color="green")
        ).add_to(m)

    st_folium(m, width=900, height=520)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# DEALS PANEL
# -----------------------------
with col2:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Local Deals")

    # This is the key fix
    try:
        deals_box = st.container(height=380)
    except TypeError:
        deals_box = st.container()

    with deals_box:
        for deal in deals:
            st.markdown(
                f"""
                <div class='deal-card' style='background-color:{deal["color"]};'>
                    <div style='font-weight:700; font-size:15px; margin-bottom:4px;'>{deal["name"]}</div>
                    <div style='font-size:14px; color:#4F4A4A;'>{deal["deal"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)