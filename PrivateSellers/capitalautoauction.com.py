import site
from logging import info
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
        self.one_page_url = 'https://www.capitalautoauction.com/inventory/details/b38cdc6c-439d-41b8-ad8c-c27295d64776'  #Without bid
        # self.one_page_url = 'https://www.capitalautoauction.com/inventory/details/f8f83897-c985-49e8-9568-37b90dff9167'  #Wit bid

    # returns html block of www page
    def __get_html_block(self, one_page_url):

        response = requests.get(one_page_url)
        html_block = BeautifulSoup(response.text, 'html.parser')
        print(f'html_block of {one_page_url} is done')  # This string is for testing ONLY

        return html_block

    # returns last page number
    def __get_last_page_number(self):

        html_block = self.__get_html_block(self.base_page_url)
        last_page_html_block = html_block.find("div", class_="pagination catalog__top-pagination")
        last_page_number = last_page_html_block.findAll("a")[-1].text
        last_page_number = int(last_page_number)

        return last_page_number

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

        print(all_pages_lots_links_list)
        return all_pages_lots_links_list

    #returns information block of one lot WITHOUT active bid
    def __get_one_lot_information_block_without_bid(self, html_block):
        one_lot_information_block_list = []

        one_lot_information_block = html_block.find("div", class_="options options--frame")
        one_lot_information_block_list = one_lot_information_block.findAll("li", class_="options__item")

        print('PUTIN HUILO')
        return one_lot_information_block_list

    #returns information block of one lot WITH active bid
    def __get_one_lot_information_block_with_bid(self, html_block):
        one_lot_information_block_list = []

        one_lot_information_block = html_block.find("div", class_="options options--frame vehicle__options")
        one_lot_information_block_list = one_lot_information_block.findAll("li", class_="options__item")

        return one_lot_information_block_list


    # returns engine dict of one lot
    def __get_lot_engine_dict(self, info_line):
        lot_engine_dict = {}

        info_line = "Engine: 3.2L V8 SOHC 24V"

        lot_engine_dict = {"displacement": None, "cylinders": None,
                           "charge_type": None, "hp": None, "fuel_type": None,
                           "configuration": None, "engine_id": None}

        info_line_list = info_line.split()

        displacement = info_line_list[1].replace("L", "")
        configuration_and_cylinders = info_line_list[2]
        cylinders = configuration_and_cylinders[1::]
        configuration = configuration_and_cylinders[0]

        lot_engine_dict["displacement"] = displacement
        lot_engine_dict["cylinders"] = cylinders
        lot_engine_dict["configuration"] = configuration

        # pprint(lot_engine_dict)

        return lot_engine_dict

    # returns transmission dict of one lot
    def __get_lot_transmission_dict(self, one_lot_information_block_list):
        lot_transmission = {}

        lot_transmission: {"transmission_type": None,
                           "transmission_speeds": None}

        for html_line in one_lot_information_block_list:
            info_line = " ".join(html_line.text.split())

            if "Transmission:" in info_line:
                lot_transmission_string_with_number = info_line[-1]

                if lot_transmission_string_with_number.isdigit():
                    transmission_speeds = lot_transmission_string_with_number
                    transmission_type = info_line.replace(lot_transmission_string_with_number, '')
                    transmission_type = transmission_type.strip()
                else:
                    transmission_type = info_line.split(':')[-1]
                    transmission_speeds = None

        lot_transmission["transmission_type"] = transmission_type
        lot_transmission["transmission_speeds"] = transmission_speeds

        return lot_transmission



    # returns one car information block
    def __get_one_car_data_dict(self, html_block):
        car_data = {}


        one_lot_information_block = html_block.find("div", class_="options options--frame")
        one_lot_information_block_list = one_lot_information_block.findAll("li", class_="options__item")
        # print('one_lot_information_block_list = ')
        # pprint(one_lot_information_block_list)

        lot_vin = None
        lot_type = None
        lot_odometer = None
        lot_color: None
        lot_year = None
        lot_drive_type: None
        lot_make = None
        lot_model = None

        # lot_pictures: {"lot_pictures_list": None,
        #                 "lot_base_pictures_list": None}


        for html_line in one_lot_information_block_list:
            info_line = " ".join(html_line.text.split())
            if "VIN: " in info_line:
                lot_vin = info_line.split("VIN: ")[1]
            # elif "Type:" in info_line:
            #     lot_type = info_line.split("Type:")[1]
            elif "Odo:" in info_line:
                lot_odometer = info_line.split("Odo:")[1]
                if 'ACTUAL' in lot_odometer:
                    lot_odometer = lot_odometer.split()[0]
            elif "Ext color:" in info_line:
                lot_color = info_line.split("Ext color:")[1]
            elif "Year:" in info_line:
                lot_year = info_line.split("Year:")[1]
            elif "Drive:" in info_line:
                lot_drive_type = info_line.split("Drive:")[1]
            elif "Make:" in info_line:
                lot_make = info_line.split("Make:")[1]
            elif "Model:" in info_line:
                lot_model = info_line.split("Model:")[1]
            elif "Transmission:" in info_line:
                lot_transmission = self.__get_lot_transmission_dict(info_line)
            elif "Engine:" in info_line:
                lot_engine_dict = self.__get_lot_engine_dict(info_line)

        car_data["lot_vin"] = lot_vin
        # car_data["lot_type"] = lot_type
        car_data["lot_odometer"] = lot_odometer
        car_data["lot_color"] = lot_color
        car_data["lot_year"] = lot_year
        car_data["lot_drive_type"] = lot_drive_type
        car_data["lot_make"] = lot_make
        car_data["lot_model"] = lot_model
        car_data["lot_transmission"] = lot_transmission
        # car_data["lot_pictures"] = lot_pictures
        car_data["lot_engine_dict"] = lot_engine_dict



       # lot_pictures": {"lot_pictures_list": None,
       #                  "lot_base_pictures_list": None}



        return car_data

    # returns one car auction time dict
    def __get_lot_auction_time_dict(self):
        pass

    # returns one car bid dict
    def __get_lot_bid_dict(self):
        pass

    # returns one car auction data dict (takes data from lot_auction_time_dict AND lot_bid_dict)
    def __get_lot_auction_data(self):
        pass

    # returns car auction data (depending on Bid or NOT Bid in the lot)
    def __get_car_auction_data(self, one_lot_link, html_block):
        car_auction_data = {}

        car_auction_data = {"lot_link": None,
                            "lot_number": None,
                            "best_buyer_name": None}

        lot_link = one_lot_link
        lot_number = None  # Can we put lot number into dictionary using another method (where all data is in)?
        best_buyer_name = None


        return car_auction_data

    # returns dict with ALL data for one lot from all mini-dictionaries
    def __get_one_lot_valid_data_dict(self, one_page_url):
        one_lot_valid_data_dict = {}

        html_block = self.__get_html_block(one_page_url)

        bid_in_lot_checker = html_block.find(id="bid_now")
        if bid_in_lot_checker:  # Here we can put just if without any True or 'in' check. How it works: if bid_in_lot_checker = html_block.find(id="bid_now") found something with id = 'bid now', it will works like True. But it will be BS4 object, not boolean.
            self.__get_one_lot_information_block_with_bid(html_block)
        else:
            self.__get_one_lot_information_block_without_bid(html_block)

        one_lot_valid_data_dict["car_data"] = self.__get_one_car_data_dict(html_block)
        one_lot_valid_data_dict["car_auction_data"] = self.__get_car_auction_data(one_page_url, html_block)
        one_lot_valid_data_dict["lot_auction_data"] = self.__get_lot_auction_data()
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
        print('--------------------------------FINAL RESULT--------------------------------')
        pprint(one_lot_valid_data_dict)
        print('--------------------------------FINAL RESULT--------------------------------')



    def test(self):
        print('===========================================START====================================================')
        self.__get_one_lot_valid_data_dict(self.one_page_url)
        print('============================================END====================================================')


capitalauctioncom = CapitalauctionCom()


capitalauctioncom.test()





# LEARNING WITH VLAD:
#
# class Copart:
#     def get_html(self, url):
#         pass
#
#     def get_all_links(self):
#         url = 'https://www.capitalautoauction.com/inventory?f%5Bmake_id%5D%5B%5D=&f%5Bmodel_id%5D%5B%5D=&f%5Byear_from%5D=&f%5Byear_to%5D='
#
#         html = self.get_html(url)
#         pass
#
#     def get_car_data(self, html):
#         pass
#
#     def get_car_auction_data(self, html):
#         pass
#
#     def get_one_lot_full_info(self, url):
#         one_lot_full_info = {}
#
#         html = self.get_html(url)
#
#         car_data_html = html.find("A")
#
#         car_data = self.get_car_data(car_data_html)
#         one_lot_full_info['car_data'] = car_data
#
#         car_auction_data_html = html.find("A")
#
#         car_auction_data = self.get_car_auction_data(car_auction_data_html)
#         one_lot_full_info['car_auction_data'] = car_auction_data
#
#         # ///////
#
#         # ///////
#
#         return one_lot_full_info
#
#     def parser(self):
#         all_links_list = self.get_all_links()
#
#         all_lots_full_info = []
#
#         for link in all_links_list:
#             one_lot_full_info = self.get_one_lot_full_info(link)
#             all_lots_full_info.append(one_lot_full_info)
#
#         return all_lots_full_info




