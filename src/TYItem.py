import re
import requests
from bs4 import BeautifulSoup as BS


class TYItem:
    DEFAULT_PRICE_CLASS_NAME = 'prc-slg'
    NORMAL_DISCOUNT_PRICE_CLASS_NAME = 'prc-org'
    CARTBOX_DISCOUNT_PRICE_CLASS_NAME = 'prc-dsc'
    DETAILS_CLASS_NAME = 'pr-in-br'
    IMAGE_CLASS_NAME = 'ph-gl-img'

    def __init__(self, item_url, threshold):
        self.url = item_url
        self.threshold = float(threshold)
        self.details = None
        self.old_price = None
        self.default_price = None
        self.cartbox_price = None
        self.normal_discount = None
        self.cartbox_discount = None
        self.image_url = None
        self.informed = False
        self.update()

    def __iter__(self):
        yield 'url', self.url
        yield 'threshold', self.threshold
        yield 'details', self.details
        yield 'old_price', self.old_price
        yield 'default_price', self.default_price
        yield 'cartbox_price', self.cartbox_price
        yield 'normal_discount', self.normal_discount
        yield 'cartbox_discount', self.cartbox_discount
        yield 'image_url', self.image_url
        yield 'informed', self.informed

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        space = 17
        if self.normal_discount and self.cartbox_discount:
            return (
                f'{"Brand":<{space}}: {self.details["brand"]}\n'
                f'{"Description":<{space}}: {self.details["description"]}\n'
                f'{"Original Price":<{space}}: {self.old_price}₺\n'
                f'{"Default Price":<{space}}: {self.default_price}₺\n'
                f'{"Normal Discount":<{space}}: {self.normal_discount*100:.0f}%\n'
                f'{"Cartbox Price":<{space}}: {self.cartbox_price}₺\n'
                f'{"Cartbox Discount":<{space}}: {self.cartbox_discount*100:.0f}%\n'
                f'{"URL":<{space}}: {self.url}\n'
                f'{"Threshold":<{space}}: {self.threshold}₺\n'
            )
        elif self.normal_discount:
            return (
                f'{"Brand":<{space}}: {self.details["brand"]}\n'
                f'{"Description":<{space}}: {self.details["description"]}\n'
                f'{"Original Price":<{space}}: {self.old_price}₺\n'
                f'{"Default Price":<{space}}: {self.default_price}₺\n'
                f'{"Normal Discount":<{space}}: {self.normal_discount*100:.0f}%\n'
                f'{"URL":<{space}}: {self.url}\n'
                f'{"Threshold":<{space}}: {self.threshold}₺\n'
            )
        elif self.cartbox_discount:
            return (
                f'{"Brand":<{space}}: {self.details["brand"]}\n'
                f'{"Description":<{space}}: {self.details["description"]}\n'
                f'{"Original Price":<{space}}: {self.default_price}₺\n'
                f'{"Cartbox Price":<{space}}: {self.cartbox_price}₺\n'
                f'{"Cartbox Discount":<{space}}: {self.cartbox_discount*100:.0f}%\n'
                f'{"URL":<{space}}: {self.url}\n'
                f'{"Threshold":<{space}}: {self.threshold}₺\n'
            )
        else:
            return (
                f'{"Brand":<{space}}: {self.details["brand"]}\n'
                f'{"Description":<{space}}: {self.details["description"]}\n'
                f'{"Price":<{space}}: {self.default_price}₺\n'
                f'{"Discount":<{space}}: {self.normal_discount}\n'
                f'{"URL":<{space}}: {self.url}\n'
                f'{"Threshold":<{space}}: {self.threshold}₺\n'
            )

    def update(self):
        soup = self.__getParsedHTML(self.url)
        self.details = self.__getItemDetails(soup, TYItem.DETAILS_CLASS_NAME)

        self.default_price = self.__getFloatValue(
            soup, TYItem.DEFAULT_PRICE_CLASS_NAME)
        self.old_price = self.__getFloatValue(
            soup, TYItem.NORMAL_DISCOUNT_PRICE_CLASS_NAME)
        self.cartbox_price = self.__getFloatValue(
            soup, TYItem.CARTBOX_DISCOUNT_PRICE_CLASS_NAME)
        self.image_url = self.__getItemImageURL(soup, TYItem.IMAGE_CLASS_NAME)

        if self.old_price:
            self.normal_discount = 1 - (self.default_price / self.old_price)
        else:
            self.normal_discount = None

        if self.cartbox_price:
            self.cartbox_discount = 1 - \
                (self.cartbox_price / self.default_price)
        else:
            self.cartbox_discount = None

    def setThreshold(self, new_threshold):
        self.threshold = new_threshold

    def setInformed(self, state):
        self.informed = state

    def __getParsedHTML(self, url):
        response = requests.get(url)
        soup = BS(response.text, 'html.parser')
        return soup

    def __getItemDetails(self, parsed_html, class_name):
        bs_info = parsed_html.find(class_=class_name)
        brand = bs_info.contents[0].get_text()
        description = bs_info.contents[1].get_text()
        return {'brand': brand, 'description': description}

    def __getFloatValue(self, parsed_html, class_name):
        try:
            str_price = parsed_html.find(class_=class_name).get_text()
            pattern = re.compile(r'(\d+)([\,\.]*)(\d*)')
            search_result = pattern.search(str_price)
            return float(search_result.group().replace(',', '.'))
        except:
            return None

    def __getItemImageURL(self, parsed_html, class_name):
        image_info = parsed_html.find(class_=class_name)
        return image_info['src']


def main():
    url = input('Enter item URL: ')
    threshold = input('Enter price threshold: ')
    print()
    item = TYItem(url, threshold)
    print(item)


if __name__ == "__main__":
    main()
