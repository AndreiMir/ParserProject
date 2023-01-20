import site
from pprint import pprint
import requests
from bs4 import BeautifulSoup


# todo - we need to import CARVANNA database (Vlad know what to do)
# todo - connect files

# I can do it
# todo - create a list that contains lots dictionaries


class CapitalauctionCom:
    def __init__(self):
        self.base_page_url = "https://www.capitalautoauction.com/inventory?per_page=100&sort=make&page=1"  # In this section we can put any data for calling in any methods in any places

    # returns html block of www page
    def __get_html_block(self, url):

        response = requests.get(url)
        html_block = BeautifulSoup(response.text, 'html.parser')

        return html_block

    # returns list with all lots links from one page (all_lots_links_list_from_one_page)
    def __get_one_page_lots_links_list(self, url):
        one_page_lot_links_list = []

        html_block = self.__get_html_block(url)
        one_page_all_lots_links_html_block = html_block.find("div", class_="catalog__cards")
        one_page_all_lots_links_html_block_list = one_page_all_lots_links_html_block.findAll("div", class_="card__main")

        for html_block_link in one_page_all_lots_links_html_block_list:
            lot_link = html_block_link.find("a").get("href")
            one_page_lot_links_list.append(lot_link)

        # pprint(one_page_lot_links_list)
        # print(len(one_page_lot_links_list))

        return one_page_lot_links_list

    # returns last page number
    def __get_last_page_number(self):

        html_block = self.__get_html_block(self.base_page_url)
        last_page_html_block = html_block.find("div", class_="pagination catalog__top-pagination")
        last_page_number = last_page_html_block.findAll("a")[-1].text
        last_page_number = int(last_page_number)
        return last_page_number

    # returns list of all pages links
    def __get_all_pages_links_list(self):
        all_pages_links_list = []

        last_page_number = self.__get_last_page_number()
        # print(last_page_number)
        for page_number in range(1, last_page_number + 1):
            one_page_link = 'https://www.capitalautoauction.com/inventory?per_page=100&sort=make&page=' + str(page_number)
            all_pages_links_list.append(one_page_link)

        return all_pages_links_list

    # returns list of all lots from all pages of www site
    def __get_all_pages_lots_links_list(self):
        all_pages_lots_links_list = []

        all_pages_links_list = self.__get_all_pages_links_list()

        for one_page_link in all_pages_links_list:
            print('working on', one_page_link)
            one_page_lots_links_list = self.__get_one_page_lots_links_list(one_page_link)
            all_pages_lots_links_list.extend(one_page_lots_links_list)
            print('done')
        print('----------------------------------------------------------------')

        # print(all_pages_lots_links_list)  #why PPRINT CAN NOT PRINT IT?????????????

        return all_pages_lots_links_list


    def test(self):
        print('===========================================START====================================================')
        self.__get_all_pages_lots_links_list()
        print('============================================END====================================================')


capitalauctioncom = CapitalauctionCom()
capitalauctioncom.test()
# Returns dict - car_data = {lot_car_fax_link': None, 'lot_color': None,...........}
# def (self, one_lot_html_block, lot_link):
#     one_lot_valid_data_dict = {}
#
#     one_lot_valid_data_dict = ["car_data"] = {"lot_vin": None,
#                                            "lot_type": None,
#                                            "lot_odometer": None,
#                                            "lot_color": None,
#                                            "lot_year": None,
#                                            "lot_drive_type": None,
#                                            "lot_make": None,
#                                            "lot_model": None,
#                                            "lot_transmission": {"transmission_type": None,
#                                                                 "transmission_speeds": None},
#                                            "lot_trim": None,
#                                            "lot_pictures": {"lot_pictures_list": None,
#                                                             "lot_base_pictures_list": None},
#                                            "lot_keys": None,
#                                            "lot_title_status": None,
#                                            "lot_damage_type": None,
#                                            "lot_car_fax_link": None,
#                                            "lot_factory_body_code": None,
#                                            "lot_truck_cab_type": None,
#                                            "lot_engine_dict": {"displacement": None, "cylinders": None,
#                                                                "charge_type": None, "hp": None, "fuel_type": None,
#                                                                "configuration": None, "engine_id": None}}
#     one_lot_valid_data_dict["car_auction_data"] = {"lot_link": None,
#                                                    "lot_number": None,
#                                                    "best_buyer_name": None}
#     one_lot_valid_data_dict["lot_auction_data"] = {"lot_auction_time_dict": {'auction_status': None,
#                                                                              'auction_date': None,
#                                                                              'auction_month': None,
#                                                                              'auction_time': None,
#                                                                              'auction_time_zone': None},
#                                                    "lot_bid_dict": {"lot_minimum_bid": None,
#                                                                     "lot_increment_bid": None,
#                                                                     "lot_current_bid": None,
#                                                                     "lot_starting_bid": None,
#                                                                     "auction_fee": None,
#                                                                     "lot_delivery_price": None,
#                                                                     "lot_sell_max_offer": None,
#                                                                     "lot_condition_report": 134,
#                                                                     "lot_buy_now_price": None,
#                                                                     "lot_clear_profit": None,
#                                                                     "buy_now_fee": None,
#                                                                     "buy_now_clear_profit": None}}
#     one_lot_valid_data_dict["location_dict"] = {"lot_location_dict": {"lot_location_city": None,
#                                                                       "lot_location_state_name": None,
#                                                                       "lot_location_state_code": None,
#                                                                       "lot_location_zip": None,
#                                                                       "lot_Lane/Item/Grid/Row": None,
#                                                                       "lot_latitude": None,
#                                                                       "lot_longitude": None},
#                                                 "delivery_location_dict": {'delivery_city': 'Merrillville',
#                                                                            'delivery_state_code': 'IN',
#                                                                            'delivery_state_name': 'Indiana',
#                                                                            'delivery_zip': '46410',
#                                                                            "delivery_latitude": None,
#                                                                            "delivery_longitude": None}}

# printing results here