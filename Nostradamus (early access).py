"""
Course Number: ENGR 13300
Semester: Fall 2024

Description: A porgram that predicts the chance of happening a hurricane in a determined location, 
and creates a heatmap for the history of the hurricane in each month marking the user location on the world map.

Assignment Information:
    Assignment:     Individual Project 16
    Team ID:        LC5 - 13 
    Author:         Fabricio Giusti Oliveira Monteiro, fgiustio@purdue.edu
    Date:           12/5/2024

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import pandas as pd
import folium
from folium.plugins import HeatMap
#https://python-visualization.github.io/folium/latest/user_guide/plugins/heatmap.html
#https://python-visualization.github.io/folium/latest/reference.html
import branca.colormap 
from location import location

#function to find the number of hurricanes per month in a determine location
def quant_month(lat_user,lon_user,lat_data,lon_data,month,month_user,ID):
    
    #range of the latitude and longitude of user
    lat_user_upper = lat_user + 5
    lat_user_lower = lat_user - 5
    lon_user_upper = lon_user + 5
    lon_user_lower = lon_user - 5

    #loop to discover how many individual hurricanes go into the range of the user
    i = 0
    hurr_month = 0
    while i < len(lat_data):
        if month[i] == month_user:
            if float(lat_data[i]) >= lat_user_lower and float(lat_data[i]) <= lat_user_upper:
                if str(ID[i]) == str(ID[i - 1]):
                    i += 1
                    continue 
                else:
                    if float(lon_data[i]) >= lon_user_lower and float(lon_data[i]) <= lon_user_upper:
                        if str(ID[i]) == str(ID[i - 1]):
                            i += 1
                            continue 
                        else:
                            hurr_month += 1
            else:
                i +=1
        else:
            i += 1
            continue
        i += 1
    return hurr_month

def heatmap(data,month_user,lat_user,lon_user,out_message):#function to create the heatmap

    data["month"] = pd.to_datetime(data["ISO_TIME"]).dt.month
    new_data = data.loc[data["month"] == month_user]          
    month_out = out_month(month_user)
    world_map = folium.Map(location=[0,0],zoom_start=3, control_scale=True,)#create the map

    lon_lat = new_data[["LAT","LON"]]#take the latitude and longitude collumn from the data
    data_hm = lon_lat.values.tolist()#tranform the data for the library be able to read it
    hm = HeatMap(data_hm,min_opacity=0.1,max_opacity=0.8, radius = 50).add_to(world_map)#create the heatmap
    hm_icon = folium.Icon(color="darkpurple",icon_color="red",icon="user", prefix="fa")#create the marker
    hm_style_tooltip = "color:black; font-size:15px; font-weight:normal; background-color:white; padding:5px;" #format of the message displayed
    hm_tooltip = folium.Tooltip(text=out_message,style=hm_style_tooltip)#create the message inside the map
    folium.Marker(location=[lat_user,lon_user],popup="Your Location.",tooltip=hm_tooltip, icon=hm_icon).add_to(world_map)#create the marker into the map

    map_title = f"Hurricane map in the month of {month_out}"
    title_html = f'<h1 style="position:absolute;z-index:100000;left:40vw" >{map_title}</h1>'#create the title into the map
    world_map.get_root().html.add_child(folium.Element(title_html))

    legend_colors = ["blue","lightgreen", "yellow","orange","red"]
    legend_name = "Hurricane Intensity"
    legend = (branca.colormap.LinearColormap( colors=legend_colors,caption=legend_name)).add_to(world_map)#legend of the heatmap

    world_map.save(f"heatmap_{month_out}.html")
    world_map.show_in_browser()

def out_month(month_user):# function to transform the number of the month to the name of the month
    if month_user == 1:
        month_out = "January"
    elif month_user == 2:
        month_out = "February"
    elif month_user == 3:
        month_out = "March"
    elif month_user == 4:
        month_out = "April"
    elif month_user == 5:
        month_out = "May"
    elif month_user == 6:
        month_out = "June"
    elif month_user == 7:
        month_out = "July"
    elif month_user == 8:
        month_out = "August"
    elif month_user == 9:
        month_out = "September"
    elif month_user == 10:
        month_out = "October"
    elif month_user == 11:
        month_out = "November"
    elif month_user == 12:
        month_out = "December"
    return month_out

def main():

    data = pd.read_csv("ALL.csv",header=0,usecols=["SID", "ISO_TIME", "LAT", "LON"])#read the data, only the collumns that I will use
    #separate between individual variables each collumn
    ID = data["SID"]
    time = data["ISO_TIME"]
    lat_data = data["LAT"]
    lon_data = data["LON"]

    print("Welcome to Nostradamus (early access): Hurricane probability predictor !!! ")
    print("Discover the likelihood of hurricanes in your city for a specific month!")
    local_user = input("What is your city: ")#input for the location of the user

    local_right = False
    while local_right == False:#error check for the location
        lat_user, lon_user, location_web = location(local_user)
        if lat_user == None:
            print("We couldn't find your location. Please try again. (Check the spelling of your location or provide a broader description.)")
            local_user = input("What is your city: ")
        else:
            print(f"We found {location_web}. Is this correct?")
            conf_loc = input("Yes or No: ")
            if conf_loc == "No" or conf_loc == "no" or conf_loc == "N" or conf_loc == "n":
                print("Try giving more details (example: after the city give the name of the country)")
                local_user = input("What is your city: ")
            elif conf_loc == "Yes" or conf_loc == "yes" or conf_loc == "Y" or conf_loc == "y":
                local_right = True     
            else:
                local_right = False

    month_right = False
    while month_right == False:   #error check month
        print(" January = 1 | February = 2 | March = 3 | April = 4 | May = 5 | June = 6 ")
        print(" July = 7 | August = 8 | September = 9 | October = 10 | November = 11 | December = 12")
        month_user = input("What is the month you want to predict (digit a number from: 1 - 12): ")#input for the month of the user 
        if month_user.isdigit():
            month_user = int(month_user)
            if 1 <= month_user <= 12:
                month_right = True
                break
            else:
                print("That's not a valid month. Please choose a number from 1 to 12.")
        else:
            print("Invalid input. Please enter the number in numeric value")

    
    #Take the month from the data
    month = pd.to_datetime(time).dt.month 
    hurr_month = quant_month(lat_user,lon_user,lat_data,lon_data,month,month_user,ID)

    year_data = pd.to_datetime(time).dt.year#calculate how many years are on the data
    start_year = year_data.min()
    end_year = year_data.max()
    years_all = end_year - start_year + 1

    #probability based on how many times happens the hurricane on the month of the user
    prob_happ = (hurr_month/years_all)*100 
    
    month_out = out_month(month_user)
    
    loc_out = location_web.split(",", 1)

    if len(loc_out) > 1: #output for the vs code
        out_message = f"The probability of happening a hurricane in {loc_out[0]} ({loc_out[1]}) during the month of {month_out} is {prob_happ:.2f}%."
    else:
        out_message = f"The probability of happening a hurricane in {loc_out[0]} during the month of {month_out} is {prob_happ:.2f}%."
    print(out_message)

    if prob_happ == 0: #output for the heatmap
        out_message_hm = f"Good news! Historical data suggests a very low chance of hurricanes in {loc_out[0]} during {month_out}."
    elif prob_happ < 10:
        out_message_hm = f"Low Risk: There's only a {prob_happ:.2f}% chance of a hurricane in {loc_out[0]} during {month_out}."
    elif prob_happ < 30:
        out_message_hm = f"Moderate Risk: A {prob_happ:.2f}% chance of hurricane activity in {loc_out[0]} during {month_out}."
    elif prob_happ < 50:
        out_message_hm = f"High Risk: A significant {prob_happ:.2f}% chance of hurricanes in {loc_out[0]} during {month_out}!"
    else:
        out_message_hm = f"Extreme Risk: A high {prob_happ:.2f}% chance of hurricane occurrence in {loc_out[0]} during {month_out}! Stay prepared!"

    heatmap(data,month_user,lat_user,lon_user,out_message_hm)

if __name__ == "__main__":
    main()