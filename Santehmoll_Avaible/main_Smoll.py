# --- MAIN SCRAPING SANTEHMOLL --
# --- Input data: csv file name: ".csv"---
import csv, re
from datetime import datetime

from sqlalchemy import create_engine, select, update
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import declarative_base, Session

from .Class_API_Yandex import API_Requests
from .Class_product_card import Product

import os.path
import sys
#sys.path.append('C:\\Users\\v4174\\git\\Scraping_Other\\Santehmoll_Avaible')
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(BASE_DIR, "DB_Santehmoll_scraping.db")

engine = create_engine('sqlite:///DB_Santehmoll_scraping.db', future=True)

# engine = create_engine("sqlite:///C:\\Users\\v4174\\git\\Scraping_Other\\Santehmoll_Avaible\\DB_Santehmoll_scraping.db", future=True)
Base = declarative_base()


class Groups_Ads(Base):
    __tablename__ = "groups_ads"
    id = Column(Integer, unique=True, primary_key=True)
    clearurl = Column(String, unique=True, nullable=False)
    name = Column(String)
    product_id = Column(Integer, unique=True, nullable=False)
    price =  Column(Integer)
    old_price =  Column(String)
    picture = Column(String)
    avaible = Column(String(25))
    vCardId = Column(Integer, nullable=False)
    CampaignId = Column(Integer, nullable=False)
    time = Column(DATETIME, default=datetime.utcnow())
    compaign_number = Column(Integer, nullable=False)
    Ads_Id = Column(String)
    update_date = Column(DATETIME, default=datetime(2022, 8, 8, 8, 50, 16, 59198))

    def __repr__(self):
         return f"Group_Ads(id={self.id!r}, name={self.name!r}, product_id={self.product_id!r})"

    def Get_last_data_update():
        with Session(engine) as session:
            last_data = session.query(Groups_Ads).order_by(Groups_Ads.update_date).first()
        return last_data.update_date
    
    def Scrap_current_data():
        with Session(engine) as session:
            return session.query(Groups_Ads).order_by(Groups_Ads.id)


# --- MAIN PROGRAMM SCRIPTS ---
def creatingNewAds(current_ad, csv_file='all.csv'):
    count = 0
    # Reading csv feed
    with open(csv_file, encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:

            if int(row['Number']) >= current_ad and int(row['Number']) < current_ad + 1000:
                # Exctrction last ad's data from database
                with Session(engine) as session:
                    last_Ad = session.query(Groups_Ads).order_by(Groups_Ads.id.desc()).first()
                    
                    # Checking available id in database
                    if not session.query(Groups_Ads).filter(Groups_Ads.product_id==int(row['id'])).all():
                        # Filtering Feed. Only if price >= 40000 and skipping SETs
                        if int( re.search(r"^[0-9]*", row['price']).group(0) ) >= 60000: # Deleted from price number after the dot
                            if re.search(r"SET", row['vendorCode']) and len(re.findall(r'\w+', row['vendorCode'])) > 2:
                                print(f"Product doesn't match (SET): Vendor Code: {row['vendorCode']}, Price: {row['price']}")
                            else:
                                scrapingProduct = Product(row)
                                adTexts = scrapingProduct.DataForNewAd()
                                if adTexts[0]:
                                    # Checking available product
                                    if adTexts[1]['avaible'] == 'В наличии':
                                        API_Req = API_Requests(adTexts[1])
                                        response = API_Req.add_Compaign(last_Ad)
                                        if response[0]:
                                            save_to_Databse(response, session, adTexts[1])
                                            print(f'Successfully create company: {row["name"]} Id: {row["id"]}')
                                            # Sending to moderation TODO May be do it in method 'add_Compaign'?
                                            try:
                                                API_Req.Moderation_Send(response[2])
                                                count += 1
                                            except:
                                                print('Error sending group on moderation')
                                        else:
                                            addErrorToCSV(adTexts[1], response[1])
                                    else:
                                        print("Product isn't avaible")    
                                else:
                                    addErrorToCSV(adTexts[1])
                                    print('Error scraping data')
                        else:
                            print(f"Product doesn't match (Price): Vendor Code: {row['vendorCode']}, Price: {row['price']}")    
                    else:
                        print(f"Product already exist: Id: {row['id']}, Name: {row['name']}")
    return count


def errorsCorrection():
    creatingNewAds('Errors_Correct.csv')


def checkAvaible():
    check = 0
    error = 0
    change = 0

    # sorting database on 'update_date' and start loop of checking
    session = Session(engine)
    # TODO Don't get all data from base, only necessary
    check_rows = session.query(Groups_Ads).order_by(Groups_Ads.update_date)
    
    # Getting clearurl, Ads_Id, avaible, price, old price from database
    for row in check_rows:
        check += 1
        check_data = {}
        Error = False

        items = Product.getSoup(row.clearurl)
        
        check_data['old_avaible'] = row.avaible
        check_data['old_price'] = row.price
        check_data['old_oldprice'] =  row.old_price
        check_data['Ads_Id'] = row.Ads_Id 
    
        # Scrapping avaible, price and old price
        check_data['new_avaible'] = Product.getAvaible(items)
        check_data['new_price'] = Product.getPrice(items)
        check_data['new_oldprice'] = Product.getOldPrice(items)

        # Check for errors. If error created 'Log_Errors_Avaible.csv'
        for data in check_data:
            if re.search(r'Error!', data):
                addErrorToCSV(check_data, 'None', 'Log_Errors_Avaible.csv')
                error += 1
                Error = True
                print('Error of scrapping!')
                break

        if not Error:
            if check_data['new_avaible'] != check_data['old_avaible']:
                row.time = datetime.utcnow()
                session.commit() # TODO May be deleted this row?
                if check_data['new_avaible'] == 'В наличии':
                    API_Requests(check_data['Ads_Id']).Start_ads()
                    row.avaible = 'В наличии'
                    session.commit()
                    change += 1
                    print(f'Checked: {check}. Available of product ID: {row.product_id} was changed!(Was Started). Count of the changes: {change}')
                else:
                    API_Requests(check_data['Ads_Id']).Stop_ads()
                    row.avaible = check_data['new_avaible']
                    session.commit()
                    change += 1
                    print(f'Checked: {check}. Available of product ID: {row.product_id} was changed!(Was Stopped). Count of the changes: {change}')
        
            if int(check_data['new_price']) != int(check_data['old_price']):
                API_Requests(check_data['Ads_Id']).Update_Price(check_data['new_price'])
                row.price = check_data['new_price']
                session.commit()
                change += 1
                print(f'Checked: {check}. Price of product ID: {row.product_id} changed! Count of the changes: {change}')

            if check_data['new_oldprice'] != check_data['old_oldprice']:
                API_Requests(check_data['Ads_Id']).Update_OldPrice(check_data['new_oldprice'])
                row.old_price = check_data['new_oldprice']
                session.commit()
                change += 1
                print(f'Checked: {check}. Old price of product ID: {row.product_id} changed! Count of the changes: {change}')
                
        
            row.update_date = datetime.utcnow()
            session.commit()
    
    print(f"Finish! Checked positions: {check}, Changes: {change}, Errors: {error}")
    return f"Finish! Checked positions: {check}, Changes: {change}, Errors: {error}"


# --- OTHER FUNCTIONS ---

def save_to_Databse(new_adGroup, session, adTexts):
    newAdGrpoup = Groups_Ads(
        clearurl=adTexts['clearurl'], 
        name=adTexts['name'], 
        product_id=adTexts['id'], 
        price=adTexts['price'], 
        old_price=adTexts['oldprice'], 
        picture=adTexts['picture'], 
        avaible=adTexts['avaible'], 
        vCardId=new_adGroup[1], 
        CampaignId=new_adGroup[0], 
        compaign_number=new_adGroup[3],
        Ads_Id=str(new_adGroup[2])
    )

    session.add_all([newAdGrpoup])
    session.commit()

# Create Error log csv file for correction
def addErrorToCSV(error_data, error_API='None', Log_file = 'Log_Errors.csv'):

    # Create table for 'Error log'. If table headers don't exist they will created
    # !!!!Not good design. Think!
    try:
        # Will except if 'Log_Errors.csv' don't exist
        with open(Log_file, encoding='utf-8', newline='') as csvfile:
            csv.DictReader(csvfile, delimiter=';')
        with open(Log_file, 'a', encoding='utf-8', newline='') as file:
            table_value = []
            writer = csv.writer(file, delimiter=';')
            for i in error_data:
                table_value.append(error_data[i])
            table_value.append(error_API)
            writer.writerow(table_value)
    except:
        with open(Log_file, 'a', encoding='utf-8', newline='') as file:
            table_title = []
            table_value = []
            writer = csv.writer(file, delimiter=';')
            for i in error_data:
                table_title.append(i)
                table_value.append(error_data[i])
            table_title.append('API_Error')
            table_value.append(error_API)
            writer.writerow(table_title)
            writer.writerow(table_value)


# --- START --
if __name__ == "__main__":
    print('\n1.Creating new ads\n2.Check avaible\n3.Errors Correction (File name - "Errors_Correct.csv")\n')
    type_algorithm = input('Input script number that you want to do:')
    print(type_algorithm)
    if type_algorithm == '1':
        creatingNewAds()
    elif type_algorithm == '2':
        checkAvaible()
    elif type_algorithm == '3':
        errorsCorrection()
