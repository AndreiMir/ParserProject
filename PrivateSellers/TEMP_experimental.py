import site
from pprint import pprint
import requests
from bs4 import BeautifulSoup

url = 'https://www.capitalautoauction.com/inventory?per_page=100&sort=make&page=1'

def get_html_block(url):
    response = requests.get(url)
    html_block = BeautifulSoup(response.text, 'html.parser')

    return html_block

html_block = get_html_block(url)
last_page_html_block = html_block.find("div", class_="pagination catalog__top - pagination")

pprint(last_page_html_block)
