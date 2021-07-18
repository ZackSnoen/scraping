#-------------------------------------------------
#                  Zack Snoen
#              ZackSnoen@gmail.com
# Copyright 2021, Zack Snoen, All rights reserved.
#-------------------------------------------------

# Scraping libararies
from bs4 import BeautifulSoup
import requests

# To create dirs
import os, sys

# url to scrap, this code only works with fcc
url = 'https://www.freecodecamp.org'
start = '/learn/responsive-web-design/'

# Apparently wont work in the interactive interpreter
# Sets cwd to ... current working directory
cwd = os.path.dirname(__file__)

# ---------------------------------------------------------------
# Variables to change depending where you want to put solutions!! 
# ---------------------------------------------------------------
# dumpPath => Where to create new files, I'm choosing sibling folder fcc which will be automatically made!
# solutionsFile => Name of file to place course headings in
# I then manually copy my code while going through fcc under corresponding heading
dumpPath = '../fcc/'
solutionsFile = 'mySolutions.txt'
# ---------------------------------------------------------------

# Get page content into var r
r = requests.get(url + start)

# Parse page content with BeautifulSoup
html = BeautifulSoup(r.content, 'html.parser')

# Grabs all the list items on page which hold certification names
rows = html.select('.map-ui ul li a')

# Dictionary to hold all data we scrape
# Will be {cert:{course titles : [courses], ...}, ...}
data = {}

# Appends starting url which is a certification
data[start[7:]] = {}

# Loop through each list item, grab the link, cut it to take off /learn/
# append to directories array
for row in rows:

    # Appends cert name in href to dict 
    data[row['href'][7:]] = {}

# Loop through each cert title
for key in data:
    # request with dict keys
    r = requests.get(url + '/learn/' + key)

    # Parse page content with BeautifulSoup
    html = BeautifulSoup(r.content, 'html.parser')
    
    # Grabs all course title blocks
    rows = html.select('.block .block-title-wrapper a')

    # Loop through each course title block
    # Exclude last row
    for row in rows[:-1]:
        # Append each title to data inside dict of parent certificate
        data[key][row['href'][1:]] = []

# Loop through the course titles inside each certificate
for cert, value in data.items():
    for title, courses in value.items():
        # Requests json page of each course title in each cert to get courses
        r = requests.get(url + '/page-data/learn/' + cert + title + '/page-data.json')
        rows = r.json()['result']['data']['allChallengeNode']['edges']
        
        # Loop through each row of json that holds courses
        for row in rows:
            courses.append(row['node']['title'])

# Now I need to make directories
# ../fcc/cert/title/mySolutions.txt
for cert, value in data.items():
    for title, courses in value.items():
        # Make ~/projects/fcc/cert/title/mySolutions.txt
        # Make header comment
        # /n/n
        # Make line comment with course
        # /n/n
        # Repeat the 2 lines above

        # Directory to create
        path = dumpPath + cert + title + '/'

        # join with cwd
        newPath = os.path.join(cwd, path)

        # makedirs() can create both cert and title dirs at once
        os.makedirs(path)
        
        # Make mySolutions.txt and open for writing
        with open(newPath + solutionsFile, 'w') as f:
            # Write my header
            f.write("-------------------------------------------------\n                  Zack Snoen\n              ZackSnoen@gmail.com\n Copyright 2021, Zack Snoen, All rights reserved.\n-------------------------------------------------\n\n")
            # Write courses with \n inbetween
            # Loop through all courses relevant to title
            for course in courses:
                f.write("// " + course + "\n\n")
