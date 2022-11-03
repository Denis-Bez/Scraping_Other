import time, random, re

from .Dictionary_User_agent import user_agent_data
from .Dictionary_shortName import titles_pattern, correct_shortName_utf8
from .Dictionary_TextCorrecting import cleaning_url, correct_vendor, correct_vendorCode, correct_Text, correct_Serie, correct_Suburl

import requests
from bs4 import BeautifulSoup


# Object is certain product in catalog
class Product:

    
    def __init__(self, product):
        self.product = product
        self.cleanurl = self.getCleanurl()
        self.items = self.getSoup(self.cleanurl)
        self.series = self.getSeries()
        self.shortName = self.getShortName()
        self.vendor = product['vendor']
        self.vendorCode = product['vendorCode']

        # Clear 'vendor' from prohibited simbols
        for v in correct_vendor:
            self.vendor = re.sub(v, correct_vendor[v], self.vendor)
        
        # vendorCode is being Cleaned from prohibited symbols
        for v in correct_vendorCode:
            self.vendorCode = re.sub(f'\{v}', correct_vendorCode[v], self.vendorCode)


# --- Different methods ---


    # Getting 'html' and object 'soup' and checking link working and server response. Try 3 times open link
    @staticmethod
    def getSoup(cleanurl):        
        for i in range(1, 4):
            try:
                headers = {'user-agent': random.choice(user_agent_data), 'accept': '*/*'}
                html = requests.get(cleanurl, headers=headers)
                if html.status_code == 200:
                    soup = BeautifulSoup(html.text, 'html.parser')
                    items = soup.find('div', class_='content')
                    return items
                return f'Status code {html.status_code}'    
            except Exception as e:
                print(f"Something went wrong, {e}. Repeat {i}")
                time.sleep(i*5)            
        return False


    # Is Generated and return dictionary with all necessay data for creating ads
    def DataForNewAd(self):
        self.all_data = {
            'url': self.product['url'],
            'clearurl': self.cleanurl,
            'name': self.product['name'],
            'shortname': self.shortName,
            'id': self.product['id'],
            'vendor': self.vendor,
            'vendorCode': self.product['vendorCode'],
            'price': self.getPrice(self.items),
            'oldprice': self.getOldPrice(self.items),
            'picture': self.product['picture'],
            'serie': self.series,
            'avaible': self.getAvaible(self.items),

            'groupName': self.nameAdGroup(),
            'keyPhrases': self.keyPhrases(),
            'mainTitle': self.header_main(),
            'subTitle': ['В Наличии. Доставка', 'Быстрая доставка. В Наличии'],
            'text': self.ad_Text(),
            'suburl': self.Suburl(),
        }


        for key in self.all_data:
            # TODO CRUTCH Need to thinking
            try:
                if re.search(r'Error', self.all_data[key]):
                    return [False, self.all_data]
            except:
                for i in self.all_data[key]:
                    if re.search(r'Error', i):
                        return [False, self.all_data]
        
        return [True, self.all_data]
 

# --- Scraping data for create ads ---
    
    # Checking avaible of item (no optional)
    @staticmethod
    def getAvaible(items):
        try:
            avaible = items.find('div', class_='p-available').get_text(strip=True)
        except Exception:
            avaible = "Error! Couldn't scraping avaible"
        return avaible
    

    # Getting series of product (optional)
    def getSeries(self):
        try:
            series = self.items.find(itemprop='model').get_text(strip=True)
            # Deleting prohibited symbols from 'serie'
            for s in correct_Serie:
                series = re.sub(f'\{s}', correct_Serie[s], series)
            return series
        except Exception:
            return "Don't exist Series"


    # Getting current product price (no optional)
    @staticmethod
    def getPrice(items):
        try:
            price = items.find(itemprop='price').get_text(strip=True)
            # Clean 'price' and 'oldprice' from ' ' and '₽'
            for i in [' ', '₽']:
                price = re.sub(i, '', price)
        except:
            price = "Error! Don't reading 'price'"
        
        return price


    # Getting past product price (optional)
    @staticmethod
    def getOldPrice(items):
        try:
            oldprice = items.find('span', class_='p-price__compare-at-price').get_text(strip=True)
            # Clean 'price' and 'oldprice' from ' ' and '₽'
            for i in [' ', '₽']:
                oldprice = re.sub(i, '', oldprice)
            return oldprice
        except Exception:
            return "Don't exist 'oldprice'"
    

    # Is being cleared url from partner's id (no optional)
    def getCleanurl(self):
        try:
            cleanurl = re.findall(r"&ulp=(.+)(?=%3F)", self.product['url'])[0]
        except:
            return "Error! Couldn't get cleanurl"

        # Replacement reserved url-symbols
        for v in cleaning_url:
            cleanurl = re.sub(v, cleaning_url[v], cleanurl)

        return cleanurl


    # Getting short product's name (no optional)
    def getShortName(self):
        
        # Searching short pattern in long name
        for title in titles_pattern:
            result = re.search(r'{}'.format(title), self.product['name'])
            if result:
                result = result.group(0)
                # Checking for non-Cyrillic symbols: 
                for c in correct_shortName_utf8:
                    result = re.sub(c, correct_shortName_utf8[c], result)
                return result.capitalize()

        return "Error! Product Is not found in 'Dictionary_shortName'"  


# --- Ad texts create and validation ---  

    # Return ad's group name
    def nameAdGroup(self):
        try:
            nameAdGroup = '_' + self.product['id'] + '_' + self.product['name']
            return nameAdGroup
        except:
            return "Error! Couldn't extract 'id' or 'name'"
    

    # Return a list of key phreses for the ad group
    def keyPhrases(self):
        keyPhrases = []       

        # For phrase's algorithm 'Vendor + VendorCode'
        keyPhrases.append(self.vendor + ' ' + self.vendorCode)
        
        # !It 'if' isn't good design. Need to think
		# For phrase's algorithm 'VendorCode'. Checking length of VendorCode for a separate phrase
        if (re.findall('[a-zA-Zа-яА-я]', self.vendorCode) and len(self.vendorCode) > 5) or (
            not re.findall('[a-zA-Zа-яА-я]', self.vendorCode) and len(self.vendorCode) > 8):
            keyPhrases.append(self.vendorCode)
            
        # For phrase's algorithm 'series + VendorCode' (if 'series' exist)
        if not re.search(r"Don't", self.series):
            keyPhrases.append(self.series + ' ' + self.vendorCode)

        # For phrase's algorithm  'shortName + vendorCode'
        keyPhrases.append(self.shortName + ' ' + self.vendorCode)

        # Cheking sum words in phrase
        for phrase in enumerate(keyPhrases):    
            if len(re.findall(r'\w+', phrase[1])) > 7:
                keyPhrases[phrase[0]] = re.sub('\.', "", keyPhrases[phrase[0]]) # Replace '.' to '' in phrase
                if len(re.findall(r'\w+', keyPhrases[phrase[0]])) > 7:
                    keyPhrases[phrase[0]]  = re.sub('-', "", keyPhrases[phrase[0]]) # Replace '-' to '' in phrase
                    if len(re.findall(r'\w+', keyPhrases[phrase[0]])) > 7:
                        return 'Error! Phrase has more 7 words'

        return keyPhrases


    # Generate two versions of main headers ('shortName + vendorCode + vendor' and 'shortName + vendorCode + series')
    def header_main(self):
        main_headers = []

        if re.search(r"Don't", self.series):
            header1 = self.shortName + " " + self.vendorCode
            # Checking main_header length
            if len(header1) > 56:
                return 'Error! Too long main_headers'
        else:
            header1 = self.shortName + " " + self.series + " " + self.vendorCode
            if len(header1) > 56:
                header1 = self.shortName + " " + self.vendorCode
                if len(header1) > 56:
                    return 'Error! Too long main_headers'
        
        header2 = self.shortName + " " + self.product['vendor'] + " " + self.vendorCode
        # Checking main_header length
        if len(header2) > 56:
            header2 = self.shortName + " " + self.vendorCode
            if len(header2) > 56:
                return 'Error! Too long main_headers'
        
        main_headers.extend([header1, header2])

        return main_headers


    # Create two versions ad's text (product['name'] and 'shortName + vendor + serie + vendorCode')
    def ad_Text(self):
        ad_text = []
        product_name1 = self.product['name']
        
        # 'name' is being Cleaned from prohibited simbols
        for t in correct_Text:
            product_name1 = re.sub(f'\{t}', correct_Text[t], product_name1)
        
        if re.search(r"Don't", self.series):
            product_name2 = self.shortName + " " + self.vendor + " " + self.vendorCode
        else:
            product_name2 = self.shortName + " " + self.vendor + " " + self.series + " " + self.vendorCode

        ad_text.extend([product_name1, product_name2])

        # Checking leigh of ad's text (max 81 symbols)
        for i, t in enumerate(ad_text):
            if len(ad_text[i]) > 81:
                ad_text[i] = re.sub(f' {self.series}', "", ad_text[i]) # Deleted 'serie' from text
                if len(ad_text[i]) > 81:
                    ad_text[i] = re.sub(f' {self.vendor}', "", ad_text[i]) # Deleted 'vendor' from text
                    if len(ad_text[i]) > 81:
                        return "Error! Ad's text is too long"
        
        return ad_text


    # Create suburl
    def Suburl(self):
        for s in correct_Suburl:
            self.vendor = re.sub(f'\{s}', correct_Suburl[s], self.vendor)
        if len(self.vendor) > 20:
            self.vendor = 'В-Наличии'

        return '#' + self.vendor + '#'

