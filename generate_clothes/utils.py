import random
import requests
import time


class Clothes:

    source_url = 'https://www.asos.com/api/product/search/v2/categories/' \
                 '{}?base_colour={}&channel=mobile-web&country={}&' \
                 'currency={}&keyStoreDataversion=3pmn72e-27&lang={}&limit=200&offset=0' \
                 '&rowlength=4&size_eu={}&store={}'

    def __init__(self, clothes, colours, user_settings):
        self.clothes = clothes
        self.colours = colours

        self.country = user_settings["country"]
        self.currency = user_settings["currency"]
        self.language = user_settings["language"]
        self.store = user_settings["store"]
        self.sweater_size = user_settings["sweater_size"]
        self.pants_size = user_settings["pants_size"]
        self.shoes_size = user_settings["shoes_size"]
        self.gender = user_settings["gender"]


    def get_items_by_category(self):
        """Returns a dictionary of clothing items"""

        clothes_selection = dict()
        for category_name, category_items in self.clothes.items():
            random_item = self.get_random_clothes_element(category_name, category_items)
            clothes_selection.update(random_item)
            time.sleep(0.1)
        return {"clothes": clothes_selection}

    def get_random_clothes_element(self, category_name, category_items):
        """Returns one random item from a clothes category"""

        obj = Size(self.gender, category_name, self.sweater_size, self.pants_size, self.shoes_size)
        for sub_category_id in category_items:
            size = obj.get_size(sub_category_id)
            index = random.randint(0, len(self.colours) - 1)
            colour = self.colours[index]
            url = self.source_url.format(sub_category_id, colour, self.country, self.currency, self.language, size,
                                         self.store)
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
        return {"error": "Empty"}


class Size:
    def __init__(self, gender, category_name, sweater_size, pants_size, shoes_size):
        self.gender = gender
        self.category_name = category_name
        self.sweater_size = sweater_size
        self.pants_size = pants_size
        self.shoes_size = shoes_size

    def get_clothes_size(self):
        clothes_sizes_male = {
            "shoes": {
                'EU 36': 2466, 'EU 37': 2340, 'EU 38': 2339, 'EU 39': 2332, 'EU 40': 2325, 'EU 41': 2334, 'EU 42': 2337,
                'EU 43': 2331, 'EU 44': 1855
            },
            "pants": {'XS': 2103, 'S':'2156', 'X': 2156, 'M': 2056, 'L': 1956, 'XL': 2574},
            "pants_jogers_shorts": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "shirt": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "sweater": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "jacket": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
        }
        clothes_sizes_female = {
            "shoes": {
                'EU 36': 1853, 'EU 37': 2311, 'EU 38': 2079, 'EU 39': 2317, 'EU 40': 1902, 'EU 41': 2320, 'EU 42': 2314,
                'EU 43': 2319, 'EU 44': 2322
            },
            "pants": {'XS': 1924, 'S': 1880, 'M': 2077, 'L': 1992, 'XL': 1970},
            "shirt": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "sweater": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "jacket": {'XS': 1997, 'S': 1873, 'M': 1848, 'L': 1943, 'XL': 1881},
            "dress": {'XS': 1924, 'S': 1880, 'M': 1944, 'L': 2077, 'XL': 1920},
        }
        if self.gender == 'M':
            return clothes_sizes_male
        return clothes_sizes_female

    def get_size(self, sub_category_id):
        clothes_sizes = self.get_clothes_size()
        item_sizes = clothes_sizes[self.category_name]
        a = {
            "shoes": self.shoes_size, "pants": self.pants_size, "pants_jogers_shorts": self.pants_size,
            "shirt": self.sweater_size, "sweater": self.sweater_size, "jacket": self.sweater_size,
            "dress": self.sweater_size
        }

        if self.category_name == "pants" and self.gender == 'M':
            return self.get_pant_size(sub_category_id, item_sizes, clothes_sizes["pants_jogers_shorts"])
        else:
            return item_sizes[a[self.category_name]]

    def get_pant_size(self, category_id, pants, pants_jogers_shorts):
        jogers_shorts = [14274, 13138, 20282, 13127, 25402]
        if category_id in jogers_shorts:
            return pants_jogers_shorts[self.pants_size]
        return pants[self.pants_size]