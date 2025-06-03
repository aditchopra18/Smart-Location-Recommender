import osmnx as ox
import geopandas as gpd

def get_city_data(city_name: str):
    try:
        # Get city boundary
        city_boundary = ox.geocode_to_gdf(city_name)

        # Get street network
        graph = ox.graph_from_place(city_name, network_type="walk")
        street_gdf = ox.graph_to_gdfs(graph, nodes=False)

        # Get buildings
        tags = {'building': True}
        buildings = ox.geometries_from_place(city_name, tags)

        # Clean up columns
        buildings = buildings[['geometry']]
        buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]

        return city_boundary, street_gdf, buildings

    except Exception as e:
        return None, None, f"Error fetching data: {e}"