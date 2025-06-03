import osmnx as ox
import geopandas as gpd

def get_city_data(city_name: str):
    try:
        # Get all geocoding matches
        gdf = ox.geocode_to_gdf(city_name, which_result=None)

        # Filter: Only city-level results
        city_gdf = gdf[gdf['type'].isin(['city', 'administrative'])]  # 'administrative' often includes cities
    
        if city_gdf.empty:
            return None, None, "No city-level match found."

        # Pick the best (first) city match
        selected_city = city_gdf.iloc[0]
        location_point = selected_city.geometry.centroid
        display_name = selected_city['display_name']

        # Street network and buildings
        graph = ox.graph_from_point((location_point.y, location_point.x), dist=3000, network_type="walk")
        street_gdf = ox.graph_to_gdfs(graph, nodes=False)

        tags = {'building': True}
        buildings = ox.features_from_point((location_point.y, location_point.x), tags=tags, dist=3000)
        buildings = buildings[['geometry']]
        buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]

        return selected_city.to_frame().T, street_gdf, buildings, display_name

    except Exception as e:
        return None, None, None, f"Error fetching data: {e}"