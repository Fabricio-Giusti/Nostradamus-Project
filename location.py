"""
Course Number: ENGR 13300
Semester: Fall 2024

Description: Function that gives based on the user input the latitude, longitude, and information about it.

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

import requests

def location(local_user):
    #function to get the exact latitude and longitude of the location of the user
    url = "https://nominatim.openstreetmap.org/search?q="+ local_user +"&format=json" #the URL to search on the internet
    headers = {'User-Agent': 'MyGeocodingApp/1.0'} #necessary to access the website, the client making the request
    response = requests.get(url,headers=headers).json() #serach the URL and get the resonse into python dictionary
    if not response:#if the website cannot find resulst
        lat_user, lon_user, location_web = None, None, None
    else: #if the website find a result and take the values for latitude, longitude and the full name of the location
        lat_user = float(response[0]["lat"])
        lon_user = float(response[0]["lon"])
        location_web = str(response[0]["display_name"])
    return lat_user, lon_user, location_web