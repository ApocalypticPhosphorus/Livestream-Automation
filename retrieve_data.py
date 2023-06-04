import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

presider = ""
copy_text = ""

# Get the current date and time
now = datetime.now()
#now = datetime(2023, 2, 14)

#Get the time for the mass based on the day
mass_time = None

if now.weekday() == 5:
    mass_time = "5:00 PM"
elif now.weekday() == 6:
    mass_time = "10:00 AM"
else:
    mass_time = "8:30 AM"
    
# Format the date as "May 12, 2023"
date_string = now.strftime("%B %d, %Y")

# Check if the current day is Saturday
if now.weekday() == 5:  # Saturday is represented by 5 (Monday is 0, Sunday is 6)
    # Add one day to get tomorrow's date
    now = now + timedelta(days=1)

# Format the date as mmddyy
date_mmddyy = now.strftime("%m%d%y")

#URL of the USCCB page
url = "https://bible.usccb.org/bible/readings/"
url += date_mmddyy + ".cfm"

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the title and description elements and extract their text
title = soup.find("title").text
title = title[:-8]

def get_title():
    return title

def get_description():
    return date_string + "  " + mass_time + " Mass Presider: " + presider + " St. Norbert Catholic Church Orange, CA  USA"

# Find the first element containing the string "R."
r_element = soup.find(string=lambda text: text and "R." in text)

response_text = None

#Get the response text
if r_element:
    next_sibling = r_element.next_sibling
    if next_sibling:
        response_text = next_sibling.text.strip()

def get_psalm():
    if response_text:
        return response_text
