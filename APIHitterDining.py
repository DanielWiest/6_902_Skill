import requests
import re, json
import sys

class Menu:
    def __init__(self, cafe_name):
        self.cafe_name = cafe_name
        self.meals = []
    
    def add_meal(self, meal):
        self.meals.append(meal)

    def __str__(self):
        printout = ""
        for meal in self.meals:
            meal_string = '\033[4m{:^30}\033[0m\n\n'.format((meal.name).upper())
            printout += meal_string
            for station in meal.stations:
                meal_string = '{:^20}\n'.format((meal.stations[station].name).title())
                #printout += "\t" + meal.stations[station].name + "\n"
                printout += meal_string
                for special in meal.stations[station].specials:
                    printout += "\t\t" + special["label"] + "\t" + special["price"] + "\n"
            printout += "\n"
        return printout
    
    def returnForAlexaReadout(self,mealType):
        
        NUMBER_OF_ITEMS_TO_RETURN = 12
        
        output = ""
        
        itemSet = set()
        allMeals = [i.name for i in self.meals]
        if self.meals[-1].name == "Late Night":
            del self.meals[-1]

        if self.cafe_name == "The Howard Dining Hall at Maseeh":
            if mealType == "Breakfast" and len(self.meals) == 2:
                output += "There is no breakfast today, so I will read the brunch menu instead. "
                mealType = "Brunch"
            
            elif mealType == "Lunch" and len(self.meals) == 2:
                output += "There is no lunch today, so I will read the brunch menu instead. "
                mealType = "Brunch"
                
            elif mealType == "Brunch" and len(self.meals) == 3:
                output += "There is no brunch today, so I will read the lunch menu instead. "
                mealType = "Lunch"
        else:
            
            if "Brunch" in allMeals and mealType == "Breakfast":
                output += "There is no breakfast today, so I will read the brunch menu instead. "
                mealType = "Brunch"
                
            elif "Breakfast" in allMeals and mealType == "Brunch":
                output += "There is no Brunch today, so I will read the breakfast menu instead. "
                mealType = "Breakfast"
                
            if mealType == "Lunch":
                output += "Lunch is not served at this dorm, so I will read the dinner menu instead. "
                mealType = "Dinner"
            
        for meal in self.meals:
            if meal.name == mealType:
                for station in meal.stations:
                    for special in meal.stations[station].specials:
                        itemSet.add(special["label"])
                        
        allItemsList = list(itemSet)
        numberItems = len(allItemsList)
        
        if numberItems > NUMBER_OF_ITEMS_TO_RETURN:
            output += "Because of the large number of items available at "+self.cafe_name+" for "+mealType+", only "+ str(NUMBER_OF_ITEMS_TO_RETURN)+" out of "+str(numberItems)+" menu items will be listed. "
        
        output += "For "+mealType+" "+self.cafe_name+" has "
        for menuItem in allItemsList[:NUMBER_OF_ITEMS_TO_RETURN]:
            output += menuItem+" and "
                        
        return output[:-5]+"."

class Meal:
    def __init__(self, name):
        self.name = name
        self.stations = {}

    def add_station(self, station):
        self.stations[station.name] = station


class Station:
    def __init__(self, name):
        self.name = name
        # List of objects with properties
        self.specials = []

    def add_special(self, dish):
        self.specials.append(dish)

# Constants
CAFE_URL = 'https://mit.cafebonappetit.com/cafe/{cafe_name}/{date}/'
RE_CAFE_NAME = r'Bamco.current_cafe\s+=\s+(?:[^;]+)name:\s+\'(.*?)\'(?:[^;]+);'
RE_MENU_ITEMS = r'Bamco.menu_items\s+=\s+(.+);'
RE_DAYPARTS = r'Bamco.dayparts\[\'(\d+)\'\]\s+=\s+([^;]+);'
RE_STATION_EXTRA = r'<(.*?)>@?'
RE_SPACE = r'(&nbsp;)?'

# Constants for parsing menu
NAME_FIELDS = [u'id', u'label']
INFO_FIELDS = [u'description', u'cor_icon', u'price']
EXTRA_FIELDS = [u'nutrition_details']
MENU_FIELDS = NAME_FIELDS + INFO_FIELDS + EXTRA_FIELDS

def get_page(cafe_name, date):
    """Doc"""
    url = CAFE_URL.format(cafe_name=cafe_name, date=date.isoformat())
    response = requests.get(url, timeout=10.0)
    return response.text

def get_data_from_page(page):
    name_data = re.findall(RE_CAFE_NAME, page)
    name = name_data[0]

    menu_data = re.findall(RE_MENU_ITEMS, page)
    menu = json.loads(menu_data[0]) if menu_data else None

    dayparts = {}
    dayparts_nodes = re.findall(RE_DAYPARTS, page)
    for part in dayparts_nodes:
        part_num, data = part
        dayparts[int(part_num)] = json.loads(data)

    return name, menu, dayparts

def combine(data):
    """ Get the specials of the day, under correct daypart and station """
    menu_data = data[1]
    dayparts = data[2]

    final_menu = Menu(data[0])

    # list of meal objects
    meal_list = []
    # first index = meal name, second is list of item ids in meal
    meal_id_list = []
    # Get Daypart and make meal
    for daypart_id in dayparts:
        label = dayparts[daypart_id]["label"]
        meal = Meal(label)
        meal_list.append(meal)
        # get daypart -> stations -> ids and put all in list (three lists)
        meal_items = []
        meal_items.append(label)
        for station in dayparts[daypart_id]["stations"]:
            for item_id in station["items"]:
                meal_items.append(item_id)
        meal_id_list.append(meal_items)

    # Get specials
    specials = get_specials(menu_data)
    for item in specials:
        # Make shortened item
        short_item = {}
        for field in MENU_FIELDS:
            if field == "price":
                price = re.sub(RE_SPACE, "", item[field])
                # print(price)
                short_item[field] = price
            else:
                short_item[field] = item[field]
        # Check under which of the three meal lists
        for meal_items in meal_id_list:
            if short_item["id"] in meal_items:
                station_name = re.sub(RE_STATION_EXTRA, "", item["station"])
                for meal in meal_list:
                    if meal.name == meal_items[0]:
                        # create Station obj for special if not already under meal, if under meal add station
                        if meal.stations.get(station_name):
                            meal.stations[station_name].add_special(short_item)
                        else:
                            station = Station(station_name)
                            station.add_special(short_item)
                            meal.add_station(station)
    
    for meal in meal_list:
        final_menu.add_meal(meal)
    return final_menu
                        
def get_specials(menu):
    specials = []
    for item_id in menu:
        if menu[item_id]["special"]:
            specials.append(menu[item_id])
    return specials

# Bullseye cafe = CC, Cafe Target = TPS / TPN, TNC
def get_menu(cafe_name):
    from datetime import date
    response = get_page(cafe_name, date.today())
    data = get_data_from_page(response)
    return combine(data)

# arg0 = cafe-name, arg1 = bool show price
def callableThing(meal,cafe):
    menu = get_menu(cafe)
    return menu.returnForAlexaReadout(meal)
