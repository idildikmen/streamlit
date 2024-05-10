import pandas as pd
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
from streamlit_folium import folium_static


def read_data():
    data = pd.read_csv("data.csv")
    data['Sene'] = data['Sene'].apply(lambda x: "Unknown" if pd.isna(x) else x[-4:])
    return data

def filter_data():
    data = read_data()
    data_filtered = data[data['Sene'] != 'Unknown']

    # Then, convert the year column back to numeric if it was in string format
    data_filtered['Sene'] = pd.to_numeric(data_filtered['Sene'])

    # Define the custom epoch
    custom_epoch = 1000

    # Convert milliseconds since custom epoch back to years
    data_filtered['Date'] = pd.to_datetime((data_filtered['Sene'] * (365.25 * 24 * 60 * 60 * 1000)) + (custom_epoch * (365.25 * 24 * 60 * 60 * 1000)))

    # Optionally, you can set the "date" column as the index if needed
    # df_filtered.set_index('date', inplace=True)

    # Display the filtered DataFrame
    #print(data_filtered)
    return data_filtered


def points_data():
    points = []
    data_filtered = filter_data()
    # Iterate over each row in the DataFrame
    for index, row in data_filtered.iterrows():
        # Extract data from the current row
        #print(row['Sene'])
        year =  row['Date'].to_pydatetime()# Convert year to string
        place_name = row['Yerin Adı']
        latitude = row['lat']
        longitude = row['lon']

        year_isoformat = year.isoformat()
        # Create a dictionary for the current data point
        point = {
            "time": year_isoformat,
            "popup": f"<h1>{place_name}</h1>",
            "coordinates": [longitude, latitude]  # Note: Longitude first, then latitude
        }

        # Append the dictionary to the list
        points.append(point)
    return points
        #return points
    

def features_data():
    points = points_data()
    features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"],
        },
        "properties": {
            "time": point["time"],
            "popup": point["popup"],
            "id": "house",
            "icon": "point",
             "iconstyle": {
            #     "iconUrl": "https://leafletjs.com/examples/geojson/baseball-marker.png",
                 "iconSize": [2, 2],
             },
        },
    }
    for point in points
    ]

    return features






def main():
    st.title("Simple Streamlit App with Folium Map")
    data = read_data()
    features = features_data()
    points = points_data()
    # Set up initial map center and zoom level
    map_plot = folium.Map(location=[data["lat"].mean()-1, data["lon"].mean()+5], zoom_start=6, zoom_control= False,
    max_zoom = 6,
    min_zoom = 6,
    tiles="cartodbpositron")
    # Add a marker to the map
    #marker_text = "Ottoman"
    folium.plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT45S",  # Specify the time period between each frame (in this case, 30 seconds)
    max_speed=10,  # Maximum speed of animation (default is 1)
    auto_play=False,  # Whether to automatically play the animation (default is True)
    loop_button=True,  # Show loop button to restart animation (default is False)
    time_slider_drag_update=True,  # Update map as slider is dragged (default is False)
    ).add_to(map_plot)
    
    #folium.Marker(location=initial_location, popup=marker_text).add_to(my_map)
    # Render the map in the Streamlit app
    #st_folium(map_plot, width =  2000)
    #folium_static(map_plot)
    folium_static(map_plot, width=1000)

if __name__ == "__main__":
    main()