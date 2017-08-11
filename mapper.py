import os
import pandas as pd
import numpy as np
import folium


fte_df = pd.read_csv('csv_data/fte_location.csv',
                     names=['fte', 'fte_id', 'city', 'country',
                            'address', 'long', 'lat'])
sites_df = pd.read_csv('csv_data/jnj_sites.csv',
                       names=['site_id', 'city', 'country', 'long', 'lat'])
site_dict = {}
for row in sites_df.values.tolist():
    site_dict[row[0]] = {'lat': row[-1], 'long': row[-2]}
fte_dict = {}
for row in fte_df.values.tolist():
    fte_dict[row[1]] = {'name': row[0], 'lat': row[-1], 'long': row[-2]}


def haversine(lat1, lon1, lat2, lon2):
    radius = 6371  # km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1))
         * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = radius * c
    return d * .62137119  # convert to miles


def add_sites_to_map(map_obj):
    for site_id in site_dict:
        site_lat = site_dict[site_id]['lat']
        site_long = site_dict[site_id]['long']
        folium.RegularPolygonMarker(location=[site_long, site_lat],
                                    popup=str(site_id), fill_color='orange',
                                    number_of_sides=6, radius=5).add_to(map_obj)


def set_default_map(map_file):
    default_map = folium.Map(zoom_start=1)
    for fte_id in fte_dict:
        fte_lat = fte_dict[fte_id]['lat']
        fte_long = fte_dict[fte_id]['long']
        folium.Marker(location=[fte_long, fte_lat],
                      popup=fte_dict[fte_id]['name'],
                      icon=folium.Icon(color='blue')).add_to(default_map)
    add_sites_to_map(default_map)
    try:
        os.remove('templates/' + map_file)
    except:
        pass
    default_map.save('templates/' + map_file)


def make_map(site_id, travel_distance, map_file):
    site_lat = site_dict[site_id]['lat']
    site_long = site_dict[site_id]['long']
    distance_map = folium.Map(location=[site_long, site_lat], zoom_start=2)
    folium.CircleMarker(location=[site_long, site_lat], radius=travel_distance * 1609.344,
                        popup=str(site_id), color='#3186cc',
                        fill_color='#3186cc').add_to(distance_map)
    for fte_id in fte_dict:
        fte_lat = fte_dict[fte_id]['lat']
        fte_long = fte_dict[fte_id]['long']
        name = fte_dict[fte_id]['name']
        if haversine(site_lat, site_long, fte_lat, fte_long) < travel_distance:
            folium.Marker(location=[fte_long, fte_lat],
                          popup=name,
                          icon=folium.Icon(color='green', icon='ok-sign')).add_to(distance_map)
        else:
            folium.Marker(location=[fte_long, fte_lat],
                          popup=name,
                          icon=folium.Icon(color='red', icon='remove-sign')).add_to(distance_map)
    add_sites_to_map(distance_map)
    try:
        os.remove('templates/' + map_file)
    except:
        pass
    distance_map.save('templates/' + map_file)
