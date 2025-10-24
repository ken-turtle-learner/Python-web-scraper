import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all('article', class_='product_pod') 

        for article in articles: 
            find_link = article.find('a')['href']
            book_link = (f'https://books.toscrape.com/catalogue/{find_link}')
            
            if not(book_link in link_list): #Checks if  link is a duplicate
                link_list.append(book_link)


## Step 2: Go through each link in link_list
for link in link_list:
    page = requests.get(link)
    status_code = page.status_code

    if (status_code == 200): # 200 means a valid page was returned
        soup = BeautifulSoup(page.content, 'html.parser')
        book_info = soup.find('article', class_='product_page')
        book_title = book_info.find('h1')
        print (book_title.text)