from pprint import pprint
import requests
from bs4 import BeautifulSoup


# todo - create a list that contains lots dictionaries
# todo - we need to import CARVANNA database (Vlad know what to do)
# todo - connect files


class GMercedesCom:

    #
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

    def __get_one_lot_pictures_list(self, lot_link):
        lot_pictures_list = []

        one_lot_html_block = self.__get_html_block(lot_link)

        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")

        pictures_html_block = lot_data_html_block_list[0]
        picture_html_list = pictures_html_block.findAll("a", class_="example-image-link")
        for picture_html_line in picture_html_list:
            lot_link = picture_html_line.get("href")
            lot_pictures_list.append(lot_link)

        return lot_pictures_list

    def __lot_description_html_list(self, lot_link):
        lot_description_html_list = []

        one_lot_html_block = self.__get_html_block(lot_link)

        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")

        lot_description_html_block = lot_data_html_block_list[1]
        paragraph_html_list = lot_description_html_block.findAll("p")
        paragraph_html_txt = lot_description_html_block.text

        if "*" in paragraph_html_txt:
            lot_description_html_list = " ".join(paragraph_html_list[1].text.split()).split("*")
        elif ", " in paragraph_html_txt:
            lot_description_html_list = " ".join(paragraph_html_list[1].text.split()).split(", ")
        pprint(lot_description_html_list)
        return lot_description_html_list

    def __lot_engine_dict(selfself, lot_link):
        displacement_list = []
        lot_cylinder_list = []
        lot_engine_dict = {}
        displacement = None
        cylinders = None

        lot_description_html_list = []

        for element in lot_description_html_list:
            if "L" in element:
                displacement_list = element.split()
                for displacement_element in displacement_list:
                    if "L" in displacement_element:
                        engine_displacement = displacement_element
                        displacement = engine_displacement.replace("L", "")

            element = element.lower()
            if "cylinder" in element:
                lot_cylinder_list = element.split()
                for cylinders_line in lot_cylinder_list:
                    if "cylinder" in cylinders_line:
                        cylinders = cylinders_line.split("-")[0]

            return lot_engine_dict

    def __lot_bid_dict(self, lot_link):
        one_lot_html_block = self.__get_html_block(lot_link)

        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")

        lot_description_html_block = lot_data_html_block_list[1]
        lot_price = lot_description_html_block.text.split("Price:")[-1].strip()

        if "$" in lot_price:
            lot_price = lot_price.replace("$", "")
        if "." in lot_price:
            lot_price = lot_price.split(".")[0]

        return lot_price

    # Returns dict - car_data = {lot_car_fax_link': None, 'lot_color': None,...........}
    def __get_car_data_dict(self, one_lot_html_block, lot_link):
        lot_fuel_type_list = []
        lot_transmission_list = []

        fuel_type = None
        lot_trim = None
        lot_pictures_list = None
        lot_year = None
        fuel_type = None
        transmission = None


        lot_pictures_list = self.__get_one_lot_pictures_list(lot_link)
        lot_description_html_list = self.__lot_description_html_list(lot_link)
        lot_price = self.__lot_bid_dict(lot_link)
        lot_engine_dict = self.__lot_engine_dict(lot_link)

        one_lot_html_block = self.__get_html_block(lot_link)
        lot_data_html_block = one_lot_html_block.find("div", class_="row")
        lot_data_html_block_list = lot_data_html_block.findAll("div", class_="column")
        lot_description_html_block = lot_data_html_block_list[1]

        lot_trim = lot_description_html_block.find("h2").text

        lot_year_paragraph = lot_description_html_block.find("p").text
        lot_year = lot_year_paragraph.split(" ")[1]

        for element in lot_description_html_list:
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


        car_data = {"lot_vin": None,
                   "lot_type": None,
                   "lot_odometer": None,
                   "lot_color": None,
                   "lot_year": lot_year,
                   "lot_drive_type": None,
                   "lot_make": None,
                   "lot_model": None,
                   "lot_transmission": {"transmission_type": None,
                                        "transmission_speeds": None},
                   "lot_trim": None,
                   "lot_pictures": {"lot_pictures_list": lot_pictures_list, "lot_base_pictures_list": None},
                   "lot_keys": None,
                   "lot_title_status": None,
                   "lot_damage_type": None,
                   "lot_car_fax_link": None,
                   "lot_factory_body_code": None,
                   "lot_truck_cab_type": None,
                   "lot_engine_dict": {"displacement": None, "cylinders": None,
                                       "charge_type": None, "hp": None, "fuel_type": None,
                                       "configuration": None, "engine_id": None}}

        pprint(car_data)
        return car_data

    def __get_one_lot_valid_data_dict(self, lot_link):
        one_lot_valid_data_dict = {}

        car_data = self.__get_car_data_dict(one_lot_html_block, lot_link)

        one_lot_valid_data_dict["car_data"] = car_data

        pprint(one_lot_valid_data_dict)


    def test(self):
        url = "https://g-mercedes.com/inventory-for-sale"
        lot_link = "https://g-mercedes.com/inventory-for-sale/&detail=J&id=123&JGALL_DIR=DALE.Pinzgauer/"
        # lot_link = "https://g-mercedes.com/inventory-for-sale/&detail=J&id=171&JGALL_DIR=234b/"

        one_lot_html_block = self.__get_html_block(lot_link)
        self.__get_car_data_dict(one_lot_html_block, lot_link)


        # self.__get_one_lot_valid_data_dict(lot_link)
        # self.__get_all_lots_links_list(url)

print("========================================start==============================================================")

g_m_ercedes_com = GMercedesCom()
g_m_ercedes_com.test()

print("========================================end================================================================")
