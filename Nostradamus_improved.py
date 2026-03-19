"""
Course Number: ENGR 13300
Semester: Fall 2024

Description: A program that predicts the probability of a hurricane occurring in a determined location, 
and creates a heatmap for the history of hurricanes in that month, marking the user location on the world map.

Assignment Information:
    Assignment:     Individual Project 16 (Improved Version)
    Team ID:        LC5 - 13 
    Author:         Fabricio Giusti Oliveira Monteiro, fgiustio@purdue.edu
    Date:           12/5/2024

Contributors:
    Refactored by AI Assistant

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import pandas as pd
import folium
from folium.plugins import HeatMap
import branca.colormap 
import calendar
from location import location

def calculate_hurricane_count(lat_user, lon_user, data, month_user):
    """
    Calculates the number of unique hurricanes within a +/- 5 degree radius 
    of the user's location for a specific month.
    """
    # Define the range
    lat_min, lat_max = lat_user - 5, lat_user + 5
    lon_min, lon_max = lon_user - 5, lon_user + 5

    # Filter data for the specific month and location range
    # We assume 'data' already has a 'month' column and datetime objects
    mask = (
        (data['month'] == month_user) &
        (data['LAT'] >= lat_min) & (data['LAT'] <= lat_max) &
        (data['LON'] >= lon_min) & (data['LON'] <= lon_max)
    )
    
    nearby_data = data[mask]
    
    # Count unique hurricanes based on SID
    unique_hurricanes = nearby_data['SID'].nunique()
    
    return unique_hurricanes

def create_heatmap(data, month_user, lat_user, lon_user, out_message):
    """
    Creates and saves a heatmap of hurricane activity for the specified month.
    """
    month_name = calendar.month_name[month_user]
    
    # Filter data for the specific month
    monthly_data = data[data["month"] == month_user]
    
    # Initialize map
    world_map = folium.Map(location=[0, 0], zoom_start=3, control_scale=True)

    # Prepare data for HeatMap
    # Ensure we drop NaNs if any, though original code didn't explicitly handle them
    heat_data = monthly_data[["LAT", "LON"]].dropna().values.tolist()
    
    # Add HeatMap layer
    HeatMap(heat_data, min_opacity=0.1, max_opacity=0.8, radius=50).add_to(world_map)

    # Add User Marker
    hm_icon = folium.Icon(color="darkpurple", icon_color="red", icon="user", prefix="fa")
    hm_style_tooltip = "color:black; font-size:15px; font-weight:normal; background-color:white; padding:5px;"
    hm_tooltip = folium.Tooltip(text=out_message, style=hm_style_tooltip)
    
    folium.Marker(
        location=[lat_user, lon_user],
        popup="Your Location.",
        tooltip=hm_tooltip,
        icon=hm_icon
    ).add_to(world_map)

    # Add Title
    map_title = f"Hurricane map in the month of {month_name}"
    title_html = f'<h1 style="position:absolute;z-index:100000;left:40vw" >{map_title}</h1>'
    world_map.get_root().html.add_child(folium.Element(title_html))

    # Add Legend
    legend_colors = ["blue", "lightgreen", "yellow", "orange", "red"]
    legend = branca.colormap.LinearColormap(colors=legend_colors, caption="Hurricane Intensity")
    legend.add_to(world_map)

    # Save and Show
    filename = f"heatmap_{month_name}.html"
    world_map.save(filename)
    print(f"Heatmap saved to {filename}")
    world_map.show_in_browser()

def get_valid_location():
    """Prompts user for a city until a valid location is confirmed."""
    while True:
        city_input = input("What is your city: ")
        lat, lon, formatted_address = location(city_input)
        
        if lat is None:
            print("We couldn't find your location. Please try again. (Check spelling or add country)")
            continue
            
        print(f"We found: {formatted_address}")
        confirm = input("Is this correct? (Yes/No): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            return lat, lon, formatted_address
        elif confirm in ['no', 'n']:
            print("Please provide more details (e.g., City, Country).")
        else:
            print("Invalid response. Please answer Yes or No.")

def get_valid_month():
    """Prompts user for a month number (1-12)."""
    print("\nMonth Reference:")
    print("1: January   2: February   3: March      4: April")
    print("5: May       6: June       7: July       8: August")
    print("9: September 10: October   11: November  12: December")
    
    while True:
        user_input = input("Enter the month number you want to predict (1-12): ")
        if user_input.isdigit():
            month = int(user_input)
            if 1 <= month <= 12:
                return month
            else:
                print("Please choose a number between 1 and 12.")
        else:
            print("Invalid input. Please enter a numeric value.")

def main():
    print("Loading data... (this may take a moment)")
    # Read CSV efficiently
    try:
        # Optimizing types can save memory, but standard read is fine for this size
        data = pd.read_csv("ALL.csv", header=0, usecols=["SID", "ISO_TIME", "LAT", "LON"])
    except FileNotFoundError:
        print("Error: 'ALL.csv' not found. Please ensure the data file is in the same directory.")
        return

    # Pre-process datetime once
    data["ISO_TIME"] = pd.to_datetime(data["ISO_TIME"])
    data["month"] = data["ISO_TIME"].dt.month
    data["year"] = data["ISO_TIME"].dt.year

    print("\nWelcome to Nostradamus (Improved): Hurricane Probability Predictor!")
    print("Discover the likelihood of hurricanes in your city for a specific month.")

    # Get User Inputs
    lat_user, lon_user, location_web = get_valid_location()
    month_user = get_valid_month()

    # Calculate Statistics
    print("\nCalculating probabilities...")
    hurricane_count = calculate_hurricane_count(lat_user, lon_user, data, month_user)
    
    total_years = data["year"].max() - data["year"].min() + 1
    probability = (hurricane_count / total_years) * 100
    
    month_name = calendar.month_name[month_user]
    city_name = location_web.split(",")[0] # Simple split for display

    # Output Message
    message = f"The probability of a hurricane in {city_name} during {month_name} is {probability:.2f}%."
    print(f"\n{message}")

    # Determine Risk Level for Heatmap Message
    if probability == 0:
        risk_msg = f"Good news! Historical data suggests a very low chance of hurricanes in {city_name} during {month_name}."
    elif probability < 10:
        risk_msg = f"Low Risk: There's only a {probability:.2f}% chance of a hurricane in {city_name} during {month_name}."
    elif probability < 30:
        risk_msg = f"Moderate Risk: A {probability:.2f}% chance of hurricane activity in {city_name} during {month_name}."
    elif probability < 50:
        risk_msg = f"High Risk: A significant {probability:.2f}% chance of hurricanes in {city_name} during {month_name}!"
    else:
        risk_msg = f"Extreme Risk: A high {probability:.2f}% chance of hurricane occurrence in {city_name} during {month_name}! Stay prepared!"

    # Generate Heatmap
    print("Generating heatmap...")
    create_heatmap(data, month_user, lat_user, lon_user, risk_msg)

if __name__ == "__main__":
    main()
