# Import necessary libraries

import requests
from bs4 import BeautifulSoup

# Import csv module
import csv

# Import regex
import re



# Download the webpage using requests

# URL of the website to be scraped for the current search query
url = 'https://store.steampowered.com/search/?filter=topsellers'

# Send a GET request to the specified URL
response = requests.get(url)

# Get the content of the downloaded page and save in a variable
page_content = response.text

# Convert the file to a beautiful soup file
doc = BeautifulSoup(page_content, 'html.parser')

# Find all the games on the page
games = doc.find_all('a', {'data-gpnav' : 'item'})

#name = games.find('span', {'class': 'title'}).text

# published_date = games.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip().split()
# print(published_date[2])

#for game in games:
    # game_page_url = game.get("href")
    # game_page_response = requests.get(game_page_url)
    # game_page_contents = game_page_response.text
    # game_page_doc = BeautifulSoup(game_page_contents, 'html.parser')
    # game_page_tags_elem = game_page_doc.find_all('a', {'class' : 'app_tag'})
    # tag_list = []
    
    # for tags in game_page_tags_elem:
    #     game_page_tags = tags.text.strip() if game_page_tags_elem else 'N/A'
    #     tag_list.append(game_page_tags)
    
    
    
    
for game in games:
    game_page_url = game.get("href")
    game_page_response = requests.get(game_page_url)
    game_page_contents = game_page_response.text
    game_page_doc = BeautifulSoup(game_page_contents, 'html.parser')
    
    if game_page_doc.find('div', {'id' : 'genresAndManufacturer'}):    
        game_page_genre_elem = game_page_doc.find('div', {'id' : 'genresAndManufacturer'})
        genre_ = game_page_genre_elem.find('span').find('a')
    else:
        genre_ = ''
    game_page_genre = genre_.text.strip() if genre_ else 'N/A'
    print(game_page_genre)





#remove brackets from csv file

# with open('games_all.csv', 'r', encoding='utf-8') as infile, \
#         open('games_all_new.csv', 'w', newline='', encoding='utf-8') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)

#     for row in reader:
#         modified_row = []
#         for cell in row:
#             modified_cell = cell.replace('[', '').replace(']', '')
#             modified_row.append(modified_cell)
#         writer.writerow(modified_row)