from pprint import pprint
import requests
from bs4 import BeautifulSoup


class GMercedesCom:

    def __get_html_block(self, jjjj):

        response = requests.get(jjjj)
        html_block = BeautifulSoup(response.text, 'html.parser')

        return html_block

    def __get_all_lots_links_list(self, jjjj):
        all_lots_links_list = []

        html_block = self.__get_html_block(jjjj)
        lots_links_html_block = html_block.find("div", class_="row features")

        pprint(lots_links_html_block)
        return all_lots_links_list

    def __get_lot_engine_dict(self):
        pass

    def __get_one_lot_valid_data_dict(self):
        one_lot_valid_data_dict = {}





        one_lot_valid_data_dict["car_data"] = {"lot_vin": None,
                                               "lot_odometer": None,
                                               "lot_color": None,
                                               "lot_year": None,
                                               "lot_drive_type": None,
                                               "lot_fuel_type": None,
                                               "lot_make": None,
                                               "lot_model": None,
                                               "lot_transmission": None,
                                               "lot_trim": None,
                                               "lot_pictures_list": None,
                                               "lot_keys": None,
                                               "lot_title_status": None,
                                               "lot_damage_type": None,
                                               "lot_car_fax_link": None,
                                               "lot_engine_dict": {"displacement": None, "cylinders": None,
                                                                   "charge_type": None}}
        one_lot_valid_data_dict["car_auction_data"] = {"lot_link": None,
                                                       "lot_number": None}
        one_lot_valid_data_dict["lot_auction_data"] = {"lot_auction_time_dict": {'auction_status': None,
                                                                                 'date': None,
                                                                                 'month': None,
                                                                                 'time': None,
                                                                                 'time_zone': None},
                                                       "lot_bid_dict": {"lot_minimum_Bid": None,
                                                                        "lot_increment_bid": None,
                                                                        "lot_current_bid": None,
                                                                        "lot_starting_bid": None,
                                                                        "auction_fee": None,
                                                                        "lot_delivery": None,
                                                                        "lot_sell_max_offer": None,
                                                                        "lot_condition_report": None,
                                                                        "lot_buy_now_price": None,
                                                                        "lot_final_price": None}}
        one_lot_valid_data_dict["location_dict"] = {"lot_location_dict": {"lot_location_city": None,
                                                                          "lot_location_state_name": None,
                                                                          "lot_location_state_code": None,
                                                                          "lot_location_zip": None,
                                                                          "lot_Lane/Item/Grid/Row": None,
                                                                          "lot_latitude": None,
                                                                          "lot_longitude": None},
                                                    "delivery_location_dict": {'delivery_city': 'Merrillville',
                                                                               'delivery_state_code': 'IN',
                                                                               'delivery_state_name': 'Indiana',
                                                                               'delivery_zip': '46410',
                                                                               "delivery_latitude": None,
                                                                               "delivery_longitude": None}}

    def test(self):
        url = "https://g-mercedes.com/inventory-for-sale"
        self.__get_all_lots_links_list(url)

g_m_ercedes_com = GMercedesCom()
g_m_ercedes_com.test()