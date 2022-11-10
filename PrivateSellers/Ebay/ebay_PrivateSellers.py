import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import time

class Ebay:

    def __get_html_block(self, url):
        headers_dict = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers_dict)
        response_text = response.text
        html_block = BeautifulSoup(response_text, 'html.parser')

        return html_block


    def __get_one_lot_valid_data_dict(self):
        one_lot_valid_data_dict = {}


        one_lot_valid_data_dict["lot_vin"] = None
        one_lot_valid_data_dict["lot_odometer"] = None

        one_lot_valid_data_dict["lot_link"] = None
        one_lot_valid_data_dict["lot_title_status"] = None
        one_lot_valid_data_dict["lot_engine_dict"] = {"displacement": None, "cylinders": None, "charge_type": None}
        one_lot_valid_data_dict["lot_color"] = None
        one_lot_valid_data_dict["lot_year"] = None
        one_lot_valid_data_dict["lot_damage_type"] = None
        one_lot_valid_data_dict["lot_drive_type"] = None
        one_lot_valid_data_dict["lot_fuel_type"] = None
        one_lot_valid_data_dict["lot_number"] = None
        one_lot_valid_data_dict["lot_make"] = None
        one_lot_valid_data_dict["lot_model"] = None
        one_lot_valid_data_dict["lot_transmission"] = None
        one_lot_valid_data_dict["lot_keys"] = None
        one_lot_valid_data_dict["lot_pictures_list"] = None
        one_lot_valid_data_dict["lot_auction_time_dict"] = {'auction_status': None,
                                                            'date': None,
                                                            'month': None,
                                                            'time': None,
                                                            'time_zone': None}
        one_lot_valid_data_dict["lot_trim"] = None
        one_lot_valid_data_dict["lot_car_fax_link"] = None
        one_lot_valid_data_dict["lot_bid_dict"] = {"lot_minimum_Bid": None,
                                                   "lot_increment_bid": None,
                                                   "lot_current_bid": None,
                                                   "lot_starting_bid": None,
                                                   "auction_fee": None,
                                                   "lot_delivery": None,
                                                   "lot_sell_max_offer": None,
                                                   "lot_condition_report": None,
                                                   "lot_buy_now_price": None,
                                                   "lot_final_price": None}
        one_lot_valid_data_dict["lot_location_dict"] = {"lot_location_city": None,
                                                        "lot_location_state_name": None,
                                                        "lot_location_state_code": None,
                                                        "lot_location_zip": None,
                                                        "lot_Lane/Item/Grid/Row": None,
                                                        "delivery_location_dict": {'delivery_city': 'Merrillville',
                                                                                   'delivery_state_code': 'IN',
                                                                                   'delivery_state_name': 'Indiana',
                                                                                   'delivery_zip': '46410'}}



        return one_lot_valid_data_dict




    # def test(self):
    #     eBay_lot_url= "http://"
    #     html_block = self.__get_html_block(eBay_lot_url)
    #     self.__get_one_lot_valid_data_dict()


ebay_parser = Ebay()
# ebay_parser.test()

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313&_nkw=car&_sacat=6001'

print(url)