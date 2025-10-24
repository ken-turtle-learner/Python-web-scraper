import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import requests
from bs4 import BeautifulSoup

page_num = 0
status_code = 0
book_data = {}
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
            
            title = books.find('h3').text
            rating = books.find('p')['class'][1]

            ##Parce Price and availability
            book_price = books.find('div', class_='product_price')
            price = book_price.find('p', class_='price_color').text.replace("£","")
            availability = book_price.find('p', class_='instock availability').get_text(strip=True)
            
            book_data[title] = {'Price' : price, 'Rating': rating, 'Availability' : availability}
            logging.debug(f'Title: {title}, Price: {price}, Rating: {rating}, Availability: {availability}')
            count += 1
            logging.debug(f'Book: {count}')

logging.debug(book_data)
logging.debug(f'Total books: {count}')
logging.debug('End	of	program')
