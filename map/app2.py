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
    "Cinemark Christiana": {"lat": 39.6778, "lon": -75.6570},
    "Fred Rust Ice Arena": {"lat": 39.6632, "lon": -75.7508},
    "Newark Reservoir": {"lat": 39.6948, "lon": -75.7745},
    "College Square": {"lat": 39.6809, "lon": -75.7192},
    "Main Event": {"lat": 39.6816, "lon": -75.6507},
}

# -----------------------------
# DEALS DATA
# -----------------------------
deals = [
    {
        "name": "Klondike Kate's",
        "deal": "20% off all items",
        "lat": 39.6839,
        "lon": -75.7496,
        "category": "Restaurant",
        "card_color": "#DFF4FF"
    },
    {
        "name": "Santa Fe",
        "deal": "Buy one get one free margaritas",
        "lat": 39.6833,
        "lon": -75.7490,
        "category": "Restaurant",
        "card_color": "#DFF4FF"
    },
    {
        "name": "The Greenhouse",
        "deal": "Free appetizer with any entree",
        "lat": 39.6827,
        "lon": -75.7513,
        "category": "Restaurant",
        "card_color": "#DFF4FF"
    },
    {
        "name": "Grain Craft Bar",
        "deal": "15% off drinks on Wednesdays",
        "lat": 39.6844,
        "lon": -75.7497,
        "category": "Restaurant",
        "card_color": "#DFF4FF"
    },
    {
        "name": "Christiana Mall Food Court",
        "deal": "Free drink with any combo meal",
        "lat": 39.6788,
        "lon": -75.6585,
        "category": "Restaurant",
        "card_color": "#DFF4FF"
    },
    {
        "name": "Target Christiana",
        "deal": "10% off school supplies",
        "lat": 39.6769,
        "lon": -75.6547,
        "category": "Shopping",
        "card_color": "#EEE0FF"
    },
    {
        "name": "Barnes & Noble Cafe",
        "deal": "Buy a coffee, get a pastry half off",
        "lat": 39.6817,
        "lon": -75.7468,
        "category": "Shopping",
        "card_color": "#EEE0FF"
    },
    {
        "name": "College Square Shopping Center",
        "deal": "Free tote bag with $25 purchase",
        "lat": 39.6809,
        "lon": -75.7192,
        "category": "Shopping",
        "card_color": "#EEE0FF"
    },
    {
        "name": "Starbucks Newark",
        "deal": "Half-price iced drinks after 3 PM",
        "lat": 39.6848,
        "lon": -75.7495,
        "category": "Other",
        "card_color": "#FFF4CC"
    },
    {
        "name": "Fred Rust Ice Arena",
        "deal": "Student skate night: 2-for-1 admission",
        "lat": 39.6632,
        "lon": -75.7508,
        "category": "Other",
        "card_color": "#FFF4CC"
    },
    {
        "name": "Cinemark Christiana",
        "deal": "Student discount movie tickets on Thursdays",
        "lat": 39.6778,
        "lon": -75.6570,
        "category": "Other",
        "card_color": "#FFF4CC"
    },
    {
        "name": "Newark Reservoir Trail Stop",
        "deal": "Free smoothie upgrade on weekends",
        "lat": 39.6948,
        "lon": -75.7745,
        "category": "Other",
        "card_color": "#FFF4CC"
    },
    {
        "name": "Main Event",
        "deal": "Buy one arcade card, get one half off",
        "lat": 39.6816,
        "lon": -75.6507,
        "category": "Other",
        "card_color": "#FFF4CC"
    }
]

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected_deal" not in st.session_state:
    st.session_state.selected_deal = None

# -----------------------------
# HELPER FOR MARKER COLORS
# -----------------------------
def get_marker_color(category):
    if category == "Restaurant":
        return "lightblue"
    elif category == "Shopping":
        return "purple"
    else:
        return "beige"

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

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.55rem 0.8rem;
        font-weight: 600;
        background-color: #F7F3FF;
        color: #5A4E63;
    }

    div.stButton > button:hover {
        background-color: #EEE6FA;
        color: #4D4056;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='main-title'>Budget Hangout Map</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Find fun places and local deals around Newark</div>", unsafe_allow_html=True)

# -----------------------------
# DROPDOWN AT TOP
# -----------------------------
selected_place = st.selectbox("Choose a location", list(places.keys()))

# -----------------------------
# MAP LOCATION LOGIC
# -----------------------------
if st.session_state.selected_deal is not None:
    map_lat = st.session_state.selected_deal["lat"]
    map_lon = st.session_state.selected_deal["lon"]
    map_zoom = 18
else:
    map_lat = places[selected_place]["lat"]
    map_lon = places[selected_place]["lon"]
    map_zoom = 16

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([3, 1], gap="large")

# -----------------------------
# MAP PANEL
# -----------------------------
with col1:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    if st.session_state.selected_deal is not None:
        st.subheader(f"Showing: {st.session_state.selected_deal['name']}")
        if st.button("Back to dropdown view"):
            st.session_state.selected_deal = None
            st.rerun()
    else:
        st.subheader("Hangout Map")

    m = folium.Map(location=[map_lat, map_lon], zoom_start=map_zoom)

    # dropdown location marker
    if st.session_state.selected_deal is None:
        folium.Marker(
            [places[selected_place]["lat"], places[selected_place]["lon"]],
            popup=selected_place,
            tooltip="Selected Location",
            icon=folium.Icon(color="blue")
        ).add_to(m)

    # saved markers
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
        <div style="width:215px; font-family:Arial, sans-serif;">
            <h4 style="margin-bottom:6px;">{deal['name']}</h4>
            <p style="margin:0 0 4px 0;"><b>Category:</b> {deal['category']}</p>
            <p style="margin:0;"><b>Deal:</b> {deal['deal']}</p>
        </div>
        """

        marker_color = get_marker_color(deal["category"])

        if st.session_state.selected_deal is not None and deal["name"] == st.session_state.selected_deal["name"]:
            marker_color = "orange"

        folium.Marker(
            [deal["lat"], deal["lon"]],
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=deal["name"],
            icon=folium.Icon(color=marker_color)
        ).add_to(m)

    st_folium(m, width=900, height=520)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# DEALS PANEL
# -----------------------------
with col2:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Local Deals")

    try:
        deals_box = st.container(height=500)
    except TypeError:
        deals_box = st.container()

    with deals_box:
        for i, deal in enumerate(deals):
            st.markdown(
                f"""
                <div style='
                    background-color:{deal["card_color"]};
                    padding:12px;
                    border-radius:12px;
                    margin-bottom:8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                '>
                    <div style='font-weight:700; font-size:15px; margin-bottom:4px;'>{deal["name"]}</div>
                    <div style='font-size:13px; color:#6B6470; margin-bottom:4px;'>{deal["category"]}</div>
                    <div style='font-size:14px; color:#4F4A4A; margin-bottom:8px;'>{deal["deal"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(f"Show {deal['name']} on map", key=f"deal_btn_{i}"):
                st.session_state.selected_deal = deal
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)