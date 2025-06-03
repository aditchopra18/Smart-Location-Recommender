import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from utils.osm_utils import get_city_data

st.set_page_config(page_title="Smart Residential Location Viewer", layout="wide")

st.title("📍 Smart Residential Location Viewer")
st.markdown("Enter a city name below to view its streets and buildings from OpenStreetMap.")

# Input field
city = st.text_input("Enter city name (e.g., New York, Paris, Tokyo):")

# Map render
if city:
    with st.spinner("Fetching data..."):
        city_boundary, streets, buildings, result_info = get_city_data(city)

        if isinstance(result_info, str) and result_info.startswith("Error"):
            st.error(result_info)
        elif city_boundary is None:
            st.warning("No results found.")
        else:
            st.success(f"Showing results for: {result_info}")

            # Center map on city centroid
            centroid = city_boundary.geometry.iloc[0].centroid
            m = folium.Map(location=[centroid.y, centroid.x], zoom_start=14, tiles="cartodbpositron")

            # City boundary
            folium.GeoJson(city_boundary.geometry.iloc[0], name="City Boundary", style_function=lambda x: {
                'fillColor': 'blue', 'color': 'blue', 'fillOpacity': 0.1
            }).add_to(m)

            # Streets
            folium.GeoJson(streets, name="Streets", style_function=lambda x: {
                'color': 'gray', 'weight': 1
            }).add_to(m)

            # Buildings
            folium.GeoJson(buildings, name="Buildings", style_function=lambda x: {
                'fillColor': 'orange', 'color': 'orange', 'weight': 0.5, 'fillOpacity': 0.4
            }).add_to(m)

            folium.LayerControl().add_to(m)

            st_data = st_folium(m, width=1200, height=600)