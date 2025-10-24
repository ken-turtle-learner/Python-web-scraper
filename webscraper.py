import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import requests
from bs4 import BeautifulSoup

page_num = 0
status_code = 0
link_list = []
book_data = {}
# Step 1: Parse index pages and extract the links to the book pages and append to link_list
while(status_code != 404): # Loop until the site returns a 404 meaning we've reached the last of the index pages
    page_num = page_num + 1
    index_url = (f'https://books.toscrape.com/catalogue/page-{page_num}.html')
    page = requests.get(index_url)
    status_code = page.status_code 

    if (status_code == 200): # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, 'lxml')
        articles = soup.find_all('article', class_='product_pod') 
        logging.debug(f'Page number: {page_num}')

        for article in articles: 
            find_link = article.find('a')['href']
            book_link = (f'https://books.toscrape.com/catalogue/{find_link}')
            
            if not(book_link in link_list): #Checks if  link is a duplicate
                link_list.append(book_link)

logging.debug('link_list is completed')

count = 1
##Step 2: Go through each link in link_list
for link in link_list:
    page = requests.get(link)
    status_code = page.status_code
    if (status_code == 200): # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, 'lxml')
        book_info = soup.find('article', class_='product_page')
        title = book_info.h1.text
        price = book_info.find('p', class_='price_color').text.replace("£","")
        
        ## Parse table
        table = soup.find('table')
        row = table.find_all('tr')

        upc = row[0].find('td').text
        availability = row[5].find('td').text
        
        book_data[upc] = {'Title' : title, 'Price' : price, 'Availability' : availability}
    count += 1
    logging.debug(f'book: {count}')

logging.debug(book_data)
logging.debug('End	of	program')
