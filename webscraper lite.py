import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv #import lib to read dotenv file with the supabase url and key
load_dotenv()
import os
from supabase import create_client, Client  #Create client to connect with Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

##Setup variables
page_num = 0
status_code = 0
book_data = []
count = 0

# Step 1: Parse index pages and extract the links to the book pages and append to link_list
while(status_code != 404): # Loop until the site returns a 404 meaning we've reached the last of the index pages
    page_num += 1
    index_url = (f'https://books.toscrape.com/catalogue/page-{page_num}.html')
    page = requests.get(index_url)
    status_code = page.status_code 

    if (status_code == 200): # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, 'lxml')
        book_info = soup.find_all('article', class_='product_pod') 

        for books in book_info:
            
            ##Parse link, title and rating
            find_link = books.find("div")
            book_link = f"http://books.toscrape.com/catalogue/{find_link.find('a')['href']}"
            title = books.find('h3').text
            rating = books.find('p')['class'][1]

            ##Parse price and availability
            book_price = books.find('div', class_='product_price')
            price = book_price.find('p', class_='price_color').text.replace("£","")
            availability = book_price.find('p', class_='instock availability').get_text(strip=True)
            
            ##Add Book info to book_data dictionary
            book_row = {'title' : title, 'price' : price, 'rating': rating, 'availability' : availability, 'link' : book_link}
            book_data.append(book_row)
            count += 1
            logging.debug(f'Book: {count}')

logging.debug(book_data)
logging.debug(f'Total books: {count}')

##Send data to books database in Supabase
response = supabase.table("books").insert(book_data).execute()
print(response)

logging.debug('End	of	program')