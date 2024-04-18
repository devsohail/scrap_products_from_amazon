import requests
from bs4 import BeautifulSoup

class Product:
    def __init__(self, product_name: str):
        self.product_name = product_name

    def get_products(self):
        try:
            product_name = self.product_name
            product_name = product_name.replace(" ", "+")
            url = f"https://amazon.in/s?k={product_name}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
            products = soup.find_all("div", {"class": "s-product-image-container"})
            product_links = []
            for product in products:
                product_link = product.find("a", {"class": "a-link-normal"})["href"]
                product_links.append("https://amazon.in" + product_link)
            return {
                "data": product_links,
                "message": f"All product links have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product links: {e}",
            }

    # Get product details
    def get_product_details(self):
        try:
            product_links = self.get_products()["data"]
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
            products_details = []
            for product_link in product_links:
                r = requests.get(product_link, headers=headers)
                soup = BeautifulSoup(r.content, "html.parser")
                product_name = soup.find("span", {"id": "productTitle"}).text.strip()
                product_price = soup.find("span", {"class": "a-price-whole"}).text.strip()
                product_rating = soup.find("span", {"class": "a-size-base a-color-base"}).text.strip()
                product_detail = {
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_rating": product_rating,
                    "product_link": product_link,
                }
                products_details.append(product_detail)
            return {
                "data": products_details,
                "message": f"All product details have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product details: {e}",
            }
