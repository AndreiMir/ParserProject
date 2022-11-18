from pprint import pprint
import requests
from bs4 import BeautifulSoup


class GMercedesCom:

    def __get_html_block(self, url):

        response = requests.get(url)
        html_block = BeautifulSoup(response.text, 'html.parser')

        return html_block

    def __get_all_lots_links_list(self, url):
        all_lots_links_list = []

        html_block = self.__get_html_block(url)
        lots_links_html_block_list = html_block.findAll("div", class_="contentinventory")
        for html_lot_link in lots_links_html_block_list:
            # print('BEFORE-------------------------------------------------------------------------------------------------------------------')
            # print(html_lot_link)
            str_html_lot_link = html_lot_link.text
            # print('AFTER----------------------------------------------------------------------------------------------------------------')
            # print(str_html_lot_link)

            if "(SOLD)" not in str_html_lot_link:
                lot_link = html_lot_link.find("a").get("href")
                all_lots_links_list.append(lot_link)

        # pprint(all_lots_links_list)
        return all_lots_links_list

    def __get_one_lot_pictures_list(self, one_lot_html_block):
        lot_pictures_list = []

        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")

        pictures_html_block = lot_data_html_block_list[0]
        picture_html_list = pictures_html_block.findAll("a", class_="example-image-link")
        for picture_html_line in picture_html_list:
            lot_link = picture_html_line.get("href")
            lot_pictures_list.append(lot_link)

        return lot_pictures_list

    def __get_one_lot_valid_data_dict(self, lot_link):
        lot_fuel_type_list = []
        displacement_list = []
        lot_transmission_list = []
        lot_cylinder_list = []
        one_lot_valid_data_dict = {}

        displacement = None
        fuel_type = None
        cylinders = None
        transmission = None

        one_lot_html_block = self.__get_html_block(lot_link)
        lot_pictures_list = self.__get_one_lot_pictures_list(one_lot_html_block)


        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")

        lot_description_html_block = lot_data_html_block_list[1]

        lot_trim = lot_description_html_block.find("h2").text

        paragraph_html_list = lot_description_html_block.findAll("p")
        lot_year = paragraph_html_list[0].text.split()[1]
        lot_price = lot_description_html_block.text.split("Price:")[-1].strip()

        paragraph_html_txt = lot_description_html_block.text
        if "*" in paragraph_html_txt:
            lot_description_html_list = " ".join(paragraph_html_list[1].text.split()).split("*")
        elif ", " in paragraph_html_txt:
            lot_description_html_list = " ".join(paragraph_html_list[1].text.split()).split(", ")

        # print(paragraph_html_txt)
        # print('99999999999999999999999999999999999999999999999999999999999999999999')
        # pprint(lot_description_html_list)
        # print('99999999999999999999999999999999999999999999999999999999999999999999')

        for element in lot_description_html_list:
            if "L" in element:
                displacement_list = element.split()
                for displacement_element in displacement_list:
                    if "L" in displacement_element:
                        engine_displacement = displacement_element
                        displacement = engine_displacement.replace("L", "")
            element = element.lower()
            if "diesel" in element or "gas" in element:
                lot_fuel_type_list = element.split()
                for fuel_type_line in lot_fuel_type_list:
                    if "diesel" in fuel_type_line:
                        fuel_type = "Diesel"
                    if "gas" in fuel_type_line:
                        fuel_type = "Gas"
            if "transmission" in element:
                lot_transmission_list = element.split()
                for transmission_type in lot_transmission_list:
                    if "Speed" in transmission_type or "speed" in transmission_type:
                        transmission = transmission_type
            if "cylinder" in element:
                lot_cylinder_list = element.split()
                for cylinders_line in lot_cylinder_list:
                    if "cylinder" in cylinders_line:
                        cylinders = cylinders_line.split("-")[0]


        one_lot_valid_data_dict["car_data"] = {
                                                "lot_vin": None,
                                               "lot_odometer": None,
                                               "lot_color": None,
                                               "lot_year": lot_year,
                                               "lot_drive_type": None,
                                               "lot_fuel_type": fuel_type,
                                               "lot_make": "Mercedes-Benz",
                                               "lot_model": "G-Klasse",
                                               "lot_transmission": transmission,
                                               "lot_trim": lot_trim,
                                               "lot_pictures_list": lot_pictures_list,
                                               "lot_keys": None,
                                               "lot_title_status": None,
                                               "lot_damage_type": None,
                                               "lot_car_fax_link": None,
                                               "lot_engine_dict": {"displacement": displacement, "cylinders": cylinders,
                                                                   "charge_type": None}}
        one_lot_valid_data_dict["car_auction_data"] = {"lot_link": lot_link,
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
                                                                        "lot_buy_now_price": lot_price,
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

        pprint(one_lot_valid_data_dict)

    def test(self):
        url = "https://g-mercedes.com/inventory-for-sale"
        lot_link = "https://g-mercedes.com/inventory-for-sale/&detail=J&id=123&JGALL_DIR=DALE.Pinzgauer/"
        # lot_link = "https://g-mercedes.com/inventory-for-sale/&detail=J&id=171&JGALL_DIR=234b/"

        self.__get_one_lot_valid_data_dict(lot_link)
        # self.__get_all_lots_links_list(url)


print("========================================start==============================================================")

g_m_ercedes_com = GMercedesCom()
g_m_ercedes_com.test()

print("========================================end================================================================")
