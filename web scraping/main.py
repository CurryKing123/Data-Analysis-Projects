from bs4 import BeautifulSoup
import requests
import csv
import re

url = 'https://store.steampowered.com/search/?filter=topsellers'

#send a get rq
response = requests.get(url)

steam_web_page = response.text

soup = BeautifulSoup(steam_web_page, "html.parser")

new_trending_games = soup.find_all('a', {'data-gpnav' : 'item'})

#create scraper component to save results as a CSV file
with open('games_topsellers.csv', mode = 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Pubished Date', 'Original Price', 'Discount Price', 'Reviews', 'Tags'])
    
    #loop through each game and extract info
    for game in new_trending_games:
        name = game.find('span', {'class': 'title'}).text
        published_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text
        
        #check of element is present before accessing text attribute
        original_price_elem = game.find('div', {'class': 'discount_original_price'})
        original_price = original_price_elem.text.strip() if original_price_elem else 'N/A'
        
        discount_price_elem = game.find('div', {'class': 'discount_final_price'})
        discount_price = discount_price_elem.text.strip() if discount_price_elem else 'N/A'
        
        #extract review info
        review_summary = game.find('span', {'class': 'search_review_summary'})
        reviews_html = review_summary['data-tooltip-html'] if review_summary else 'N/A'
        
        #use regular expressions to extract the number of reviews
        match = re.search(r'(\d+,*\d*)\s+user reviews', reviews_html)
        reviews_number = match.group(1).replace(',', '') if match else 'N/A'
        
        #find all tags for each game
        game_page_url = game.get("href")
        game_page_response = requests.get(game_page_url)
        game_page_contents = game_page_response.text
        game_page_doc = BeautifulSoup(game_page_contents, 'html.parser')
        game_page_tags_elem = game_page_doc.find_all('a', {'class' : 'app_tag'})
        tag_list = []
        #add found tags into a list
        for tags in game_page_tags_elem:
            game_page_tags = tags.text.strip() if game_page_tags_elem else 'N/A'
            tag_list.append(game_page_tags)
        
        #write the extracted information to the CSV file
        writer.writerow([name, published_date, original_price, discount_price, reviews_number, tag_list])
        

# List of search filters
search_filters = ['topsellers', 'mostplayed', 'newreleases', 'upcomingreleases']

# Create a CSV file to store the scraped data
with open('games_all.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Published_Year', 'Original Price', 'Discount Price', 'Reviews', 'Search Query', 'Tags'])

    # Loop through each search query
    for filter in search_filters:
        # URL of the website to be scraped for the current search query
        url = f'https://store.steampowered.com/search/?filter={filter}'

        # Send a GET request to the specified URL
        response = requests.get(url)

        # Parse the HTML content of the page using BeautifulSoup
        webpage = BeautifulSoup(response.content, 'html.parser')

        # Find the total number of pages
        total_pages = int(webpage.find('div', {'class': 'search_pagination_right'}).find_all('a')[-2].text)

        # Counter to keep track of the number of lines written
        line_count = 0

        # Loop through each page and extract the relevant information
        for page in range(1, total_pages + 1):
            # Send a GET request to the specified URL
            response = requests.get(url + '&page=' + str(page))

            # Parse the HTML content of the page using BeautifulSoup
            doc = BeautifulSoup(response.content, 'html.parser')

            # Find all the games on the page
            games = doc.find_all('a', {'data-gpnav' : 'item'})

            # Loop through each game and extract the relevant information
            for game in games:
                name = game.find('span', {'class': 'title'}).text
                published_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip().split()
                year = published_date[2]

                # Check if the element is present before accessing the text attribute
                original_price_elem = game.find('div', {'class': 'discount_original_price'})
                original_price = original_price_elem.text.strip() if original_price_elem else 'N/A'

                discount_price_elem = game.find('div', {'class': 'discount_final_price'})
                discount_price = discount_price_elem.text.strip() if discount_price_elem else 'N/A'

                # Extract review information using regular expressions
                review_summary = game.find('span', {'class': 'search_review_summary'})
                reviews_html = review_summary['data-tooltip-html'] if review_summary else 'N/A'

                # Use regular expressions to extract the number of reviews
                match = re.search(r'(\d+,*\d*)\s+user reviews', reviews_html)
                reviews_number = match.group(1).replace(',', '') if match else 'N/A'
                
                #get tags from games
                game_page_url = game.get("href")
                game_page_response = requests.get(game_page_url)
                game_page_contents = game_page_response.text
                game_page_doc = BeautifulSoup(game_page_contents, 'html.parser')
                game_page_tags_elem = game_page_doc.find_all('a', {'class' : 'app_tag'})
                tag_list = []
                #add found tags into a list
                for tags in game_page_tags_elem:
                    game_page_tags = tags.text.strip() if game_page_tags_elem else 'N/A'
                    tag_list.append(game_page_tags)

                # Write the extracted information to the CSV file
                writer.writerow([name, year, original_price, discount_price, reviews_number, filter, tag_list])

                # Increment the line count
                line_count += 1

                # Stop scraping if we have reached the minimum data requirement
                if line_count > 100:
                    break

            # Stop scraping if we have reached the minimum data requirement
            if line_count > 100:
                break
            

# Create a function that takes url and get the total page
def get_total_pages(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.content, 'html.parser')
    total_pages = int(doc.find('div', {'class': 'search_pagination_right'}).find_all('a')[-2].text)
    return total_pages

# Create a function that extracts game info from the webpage
def extract_game_info(game):
    name = game.find('span', {'class': 'title'}).text
    published_date = game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip().split()
    year = published_date[2]
    
    original_price_elem = game.find('div', {'class': 'discount_original_price'})
    original_price = original_price_elem.text.strip() if original_price_elem else 'N/A'

    discount_price_elem = game.find('div', {'class': 'discount_final_price'})
    discount_price = discount_price_elem.text.strip() if discount_price_elem else 'N/A'

    review_summary = game.find('span', {'class': 'search_review_summary'})
    reviews_html = review_summary['data-tooltip-html'] if review_summary else 'N/A'

    match = re.search(r'(\d+,*\d*)\s+user reviews', reviews_html)
    reviews_number = match.group(1).replace(',', '') if match else 'N/A'
    
    game_page_url = game.get("href")
    game_page_response = requests.get(game_page_url)
    game_page_contents = game_page_response.text
    game_page_doc = BeautifulSoup(game_page_contents, 'html.parser')
    game_page_tags_elem = game_page_doc.find_all('a', {'class' : 'app_tag'})
    tag_list = []
    
    for tags in game_page_tags_elem:
        game_page_tags = tags.text.strip() if game_page_tags_elem else 'N/A'
        tag_list.append(game_page_tags)

    return name, year, original_price, discount_price, reviews_number, tag_list

# Create a function that scrapes the webpage
def scrape_page(url, filter, writer):
    # Invoking get total page function
    total_pages = get_total_pages(url)

    line_count = 0

    for page in range(1, total_pages + 1):
        response = requests.get(f"{url}&page={page}")
        doc = BeautifulSoup(response.content, 'html.parser')
        games = doc.find_all('a', {'data-gpnav' : 'item'})

        for game in games:
            # Invoking the extract game info function
            game_info = extract_game_info(game)
            writer.writerow([*game_info, filter])

            line_count += 1
            if line_count > 100:
                break

        if line_count > 100:
            break


# Creating the main function that takes the scrape page function and do the actual scraping
def main(search_queries=["topsellers"]):

    with open('games_all.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Year', 'Original Price', 'Discount Price', 'Reviews', 'Tags', 'Search Filter'])

        for filter in search_filters:
            url = f'https://store.steampowered.com/search/?filter={filter}'
            # Invoking the scrape page function
            scrape_page(url, filter, writer)
    remove_brackets_from_csv('games_all.csv', 'games_all_new.csv')

#remove brackets from csv file
def remove_brackets_from_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            modified_row = []
            for cell in row:
                modified_cell = cell.replace('[', '').replace(']', '')
                modified_row.append(modified_cell)
            writer.writerow(modified_row)



# Invoking the main function
search_queries = ['topsellers', 'mostplayed', 'newreleases', 'upcomingreleases']
main(search_queries)