import time

import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36', 'accept': '*/*'}

 
# Object is certain product in catalog
class Product:

    def __init__(self, url_product):  
        self.clear_url = url_product
        self.items = self.getSoup()
    

# --- Getting page content ---

    # Getting 'html' and object 'soup' and checking link working and server response. Try 2 times open link
    def getSoup(self):        
        for i in range(1, 3):
            try:
                html = requests.get(self.clear_url, headers=HEADERS)
                if html.status_code == 200:
                    soup = BeautifulSoup(html.text, 'html.parser')
                    items = soup.find('div', class_='wrap')
                    return items
                return False
            except Exception as e:
                print(f"Something went wrong, {e}. Repeat {i}")
                time.sleep(i*15)          
        return False
 

# --- Scraping data for create ads ---
    
    def getAvaible(self):
        if self.items:
            try:
                avaible = self.items.find('h1').find_next('p').find_next('span').getText(strip=True)
            except Exception:
                avaible = False
            return avaible
        else:
            return False