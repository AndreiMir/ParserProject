import requests
from pprint import pprint
from bs4 import BeautifulSoup
import webbrowser
import json

zzzzz
xxxx



# возвращает HTML-block объект типа BS
def get_html_block(germancars_link):
    response = requests.get(germancars_link)
    html_block = BeautifulSoup(response.text, 'html.parser')

    return html_block


# Возвращает список lot_links_list = [] ссылок в "грязном" виде
def get_all_lots_links_from_one_page_list(germancars_link):
    # dirty_lot_links_list = []

    html_block = get_html_block(germancars_link)

    one_lot_html_links_list = html_block.findAll("div", class_="post-content")
    for html_link in one_lot_html_links_list:
        lot_link = html_link.find("a").get("href")
        if lot_link != ' ' and lot_link != '' and lot_link != '  ' and lot_link != None and 'mailto:' not in lot_link:
            dirty_lot_links_list.append(lot_link)
    # pprint(lot_link)
    return dirty_lot_links_list


# Возвращает список чистых ссылок web_page_links_list = []
def get_clear_all_links_list(germancars_link):
    # web_page_links_list = []
    dirty_lot_links_list = get_all_lots_links_from_one_page_list(germancars_link)
    for dirty_lot_link in dirty_lot_links_list:
        if 'http://https://' not in dirty_lot_link:
            cuted_link = dirty_lot_link.split("/")[2]
            web_page_links_list.append('https://' + cuted_link)
        else:
            if dirty_lot_link not in broken_links_list:
                broken_links_list.append(dirty_lot_link)

    return web_page_links_list


# Возвращает список уникальных ссылок unique_links_list = []
def get_unique_links_list(germancars_link):
    # unique_links_list = []  # Тут создаем пустой список, в который положим только уникальные сайты

    web_page_links_list = get_clear_all_links_list(germancars_link)

    for web_page_link in web_page_links_list:
        if 'craigslist' in web_page_link:
            web_page_link = 'https://www.craigslist.org'
        if web_page_link not in unique_links_list:
            unique_links_list.append(web_page_link)

    return unique_links_list  # Тут возвращаем результат функции



print('=========================START=================================')

dirty_lot_links_list = []
web_page_links_list = []
unique_links_list = []
broken_links_list = []

start_page_number = int(input('Enter first desired page: '))
finish_page_number = int(input('Enter last desired page number: '))

for www_page_number in range(start_page_number, finish_page_number + 1):
    germancars_link = "https://germancarsforsaleblog.com/page/" + str(www_page_number)
    print(germancars_link, '...done!')
    get_unique_links_list(germancars_link)


total_unique_links_count = len(unique_links_list)


print('Amount of unique links found:', total_unique_links_count, end='.')
print()
print('Result from pages', start_page_number, 'till', finish_page_number, end='.')
print('----------------------------------------------------------------')
print()
print(*get_unique_links_list(germancars_link), sep = "\n")  # Main string for function summoning
# pprint(get_all_lots_links_from_one_page_list(germancars_link))  # Main string for function summoning
print('----------------------------------------------------------------')
print('broken links:', *broken_links_list, sep = "\n")  #List with brocken links
print('=========================FINISH=================================')

for link in unique_links_list:
    webbrowser.open_new_tab(link)
