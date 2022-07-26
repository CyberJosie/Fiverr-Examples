import requests
from bs4 import BeautifulSoup
from src.DatabaseManager import DBManager

class WebCrawler:

    def __init__(self):
        self.root_url = "https://www.whiskyshopusa.com/"
    
    # Returns a list of featured booze
    def get_featured_booze(self):
        featured_booze = []
        page = None

        try:
            page = requests.session().get(self.root_url).content
        except Exception as e:
            print(e)
            return
        
        page_soup = BeautifulSoup(page, 'html.parser')
        product_block = page_soup.find("div", id="HomeFeaturedProducts").find("div", class_="BlockContent").find_all("li")

        for block in product_block:
            try:
                block_soup = BeautifulSoup(str(block), 'html.parser')

                product_price = block_soup.find("em", class_="p-price").text
                product_name = block_soup.find("a", class_="pname").text
                product_link = block_soup.find("a", class_="pname")['href']
                product_img_link = block_soup.find("img")['src']

                product_data = {
                    "name": product_name,
                    "price": product_price,
                    "link": product_link,
                    "image": product_img_link
                }
                featured_booze.append(product_data)
            except:
                pass
        return featured_booze
    
    # Retrives top telling booze from url
    def get_top_sellers(self):
        top_sellers = []
        page = None

        try:
            page = requests.session().get(self.root_url).content
        except Exception as e:
            print(e)
            return
        
        page_soup = BeautifulSoup(page, 'html.parser')
        product_block = page_soup.find("div", id="SideTopSellers").find("div", class_="BlockContent").find_all("li")

        for block in product_block:
            try:
                block_soup = BeautifulSoup(str(block), 'html.parser')

                product_price = block_soup.find("em", class_="p-price").text
                product_name = block_soup.find("a", class_="pname").text
                product_link = block_soup.find("a", class_="pname")['href']
                product_img_link = block_soup.find("img")['src']

                product_data = {
                    "name": product_name,
                    "price": product_price,
                    "link": product_link,
                    "image": product_img_link
                }
                top_sellers.append(product_data)
            except:
                pass
        return top_sellers
    
    # Retrives new booze from url
    def get_new_products(self):
        new_products = []
        page = None

        try:
            page = requests.session().get(self.root_url).content
        except Exception as e:
            print(e)
            return
        
        page_soup = BeautifulSoup(page, 'html.parser')
        product_block = page_soup.find("div", id="HomeNewProducts").find("div", class_="BlockContent").find_all("li")

        for block in product_block:
            try:
                block_soup = BeautifulSoup(str(block), 'html.parser')

                product_price = block_soup.find("em", class_="p-price").text
                product_name = block_soup.find("a", class_="pname").text
                product_link = block_soup.find("a", class_="pname")['href']
                product_img_link = block_soup.find("img")['src']

                product_data = {
                    "name": product_name,
                    "price": product_price,
                    "link": product_link,
                    "image": product_img_link
                }
                new_products.append(product_data)
            except:
                pass
        return new_products
    
    def run(self, db_conn):
        # Get products
        print("Getting Featured Booze...", end=" ", flush=True)
        featured = self.get_featured_booze()
        print(f"Done. [{len(featured)} Elements]")

        print("Getting Top Selling Booze...", end=" ", flush=True)
        top_selling = self.get_top_sellers()
        print(f"Done. [{len(top_selling)} Elements]")

        print("Getting New Booze...", end=" ", flush=True)
        new_products = self.get_new_products()
        print(f"Done. [{len(new_products)} Elements]")

        # Add featured products to database
        [db_conn.add_product(p["name"], p["price"], p["link"], p["image"], "FEATURED") for p in featured]

        # Add top products to database
        [db_conn.add_product(p["name"], p["price"], p["link"], p["image"], "TOP") for p in top_selling]

        # Add new_products to database
        [db_conn.add_product(p["name"], p["price"], p["link"], p["image"], "NEW") for p in new_products]

# Call this to run the crawler
def init():
    # Define
    cralwer = WebCrawler()
    db = DBManager()
    
    # Create any missing defined tables
    db.ensure_content_table()

    # Run the crawler
    cralwer.run(db)
