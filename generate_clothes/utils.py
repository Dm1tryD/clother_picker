import random
import requests
import time


class Clothes:

    source_url = 'https://www.asos.com/api/product/search/v2/categories/' \
                 '{}?base_colour={}&channel=desktop-web&country={}&' \
                 'currency={}&keyStoreDataversion=3pmn72e-27&lang={}&limit=200&offset=0' \
                 '&rowlength=4&size_eu={}&store={}'

    def __init__(self, clothes, colours, user_settings):
        self.clothes = clothes
        self.colours = colours

        self.country = user_settings["country"]
        self.currency = user_settings["currency"]
        self.language = user_settings["language"]
        self.store = user_settings["store"]
        self.clothes_size = user_settings["clothes_size"]
        self.shoes_size = user_settings["shoes_size"]
        self.gender = user_settings["gender"]


    def get_items_by_category(self):
        """Returns a dictionary of clothing items"""

        clothes_selection = dict()
        for category_name, category_items in self.clothes.items():
            category_size = self.get_size(category_name)
            random_clothes_element = self.get_random_clothes_element(category_name, category_items, category_size)
            clothes_selection.update(random_clothes_element)
            time.sleep(0.1)
        return {"clothes": clothes_selection}

    def get_random_clothes_element(self, category_name, category_items, size):
        """Returns one random item from a clothes category"""

        for category_id in category_items:
            index = random.randint(0, len(self.colours) - 1)
            colour = self.colours[index]
            url = self.source_url.format(category_id, colour, self.country, self.currency, self.language, size, self.store)
            items = requests.get(url).json()
            count = items["itemCount"] if int(items["itemCount"]) < 200 else 200
            if count > 1:
                item = items["products"][random.randint(0, count - 1)]
                category_item = {
                        category_name: {
                            "subcategory": items["categoryName"],
                            "name": item["name"],
                            "brandName": item["brandName"],
                            "price": item["price"]["current"]["text"],
                            "url": str('https://www.asos.com/' + item["url"]),
                            "img": str('http://' + item["imageUrl"])
                        }
                    }
                return category_item
        return {"error":"Empty"}

    def get_size(self, category_name):
        if category_name == "shoes":
            return self.shoes_size
        else:
            return self.clothes_size