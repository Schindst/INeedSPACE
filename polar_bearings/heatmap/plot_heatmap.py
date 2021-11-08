from folium import Map, Marker
from folium.plugins import HeatMap


def plot_heatmap(
    plot_data,
    axis_min_lat,
    axis_max_lon,
    start_location,
    destination_location,
    zoom_start=6,
):
    heatmap = Map(location=[axis_min_lat, axis_max_lon], zoom_start=zoom_start)
    hm_wide = HeatMap(
        list(zip(plot_data.latitude.values, plot_data.longitude.values)),
        min_opacity=0.2,
        radius=17,
        blur=15,
        max_zoom=1,
    )
    heatmap.add_child(hm_wide)
    Marker(
        [destination_location.longitude, destination_location.latitude],
        popup=destination_location.name,
    ).add_to(heatmap)
    Marker(
        [start_location.longitude, start_location.latitude], popup=start_location.name
    ).add_to(heatmap)
    return heatmap
