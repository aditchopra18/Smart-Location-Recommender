import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.osm_utils import get_city_data
import geopandas as gpd

st.set_page_config(page_title="Smart Residential Map Viewer", layout="wide")

st.title("🏡 Smart Residential Location Viewer")
city_name = st.text_input("Enter a city or town name:", placeholder="e.g., San Francisco, USA")

if city_name:
    with st.spinner(f"Fetching map data for {city_name}..."):
        boundary, streets, buildings = get_city_data(city_name)

    if isinstance(buildings, str):  # error message
        st.error(buildings)
    elif boundary is not None:
        st.success("Data loaded successfully!")

        # Initialize Folium map
        centroid = boundary.geometry.centroid.iloc[0]
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13)

        # Add layers
        folium.GeoJson(boundary.geometry, name="City Boundary", style_function=lambda x: {
            "color": "blue", "weight": 2, "fillOpacity": 0.1
        }).add_to(m)

        folium.GeoJson(streets.geometry, name="Streets", style_function=lambda x: {
            "color": "black", "weight": 1
        }).add_to(m)

        folium.GeoJson(buildings.geometry, name="Buildings", style_function=lambda x: {
            "color": "gray", "weight": 0.5, "fillOpacity": 0.3
        }).add_to(m)

        folium.LayerControl().add_to(m)

        # Show map in Streamlit
        st_folium(m, width=1000, height=600)
    else:
        st.warning("Could not retrieve data. Please check the city name.")