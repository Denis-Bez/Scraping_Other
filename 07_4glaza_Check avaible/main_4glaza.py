import csv, re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import declarative_base, Session

from Class_Scraping import Product
from Class_API_Yandex import API_Requests

from Dictionary_UrlCorrection import cleaning_url

engine = create_engine('sqlite:///DB_4glaza.db', future=True)
Base = declarative_base()


class Groups_Ads(Base):
    __tablename__ = "DB_4glaza"
    id = Column(Integer, unique=True, primary_key=True)
    product_id = Column(Integer, unique=True, nullable=False)
    clear_url = Column(String, unique=True, nullable=False)
    available = Column(String)
    ads_Id = Column(String)
    update_date = Column(DATETIME, default=datetime(2022, 8, 8, 8, 50, 16, 59198))

    def __repr__(self):
         return f"DB_4glaza(id={self.id!r}, available={self.available!r}, product_id={self.product_id!r})"


def Check_avaible():
    i = 0   # Conter rows
    c = 0   # Conter changes
    e = 0   # Conter errors

    session = Session(engine)
    db_rows = session.query(Groups_Ads).order_by(Groups_Ads.update_date)

    for row in db_rows:
        i += 1
        available = Product(row.clear_url).getAvaible()
        if available:
            if re.search(r"К сожалению", available) or re.search(r"Товар поступит", available):
                if row.available == 'Идут показы.':
                    request = API_Requests(row.ads_Id)
                    response = request.Stop_ads()
                    if response[0]:
                        save_to_Databse(session, 'Остановлено.', row)
                        c += 1
                        print(f"Checking {i}-rows. Ads {row.product_id} was stopped. count of changes: {c}") 
                    else:
                        e += 1
                        print(f"Checking {i}-rows. Error stoping ads: {response[1]}. Error count: {e}")    
                    
                else:
                    save_to_Databse(session, row.available, row)
            else:
                if row.available == 'Идут показы.':
                    save_to_Databse(session, row.available, row)
                else:
                    request = API_Requests(row.ads_Id)
                    response = request.Start_ads()
                    if response[0]:
                        save_to_Databse(session, 'Идут показы.', row)
                        c += 1
                        print(f"Checking {i}-rows. Ads {row.product_id} was started. count of changes: {c}")
                    else:
                        e += 1
                        print(f"Checking {i}-rows. Error starting ads: {response[1]}. Error count: {e}")
        else:
            e += 1
            print(f"Checking {i}-rows. Ads {row.product_id} Error scraping. Error count: {e}")
    
    print(f"Sum of the checks: {i}, Sum of the chnges: {c}, Sum of the errors: {e}")


# Getting file with new products (id, name, url, vendor, cleanurl)
# Input file: 'new_catalog.csv', Output file: 'new_products.csv'
def Feed_filter():
    i = 0 # New product counter
    e = 0 # Error counter
    avail = 0 # Noе available counter
    with open('new_products.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'name', 'url', 'vendor', 'clean_url'])
        with open('new_catalog.csv', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            session = Session(engine)
            for row in reader:
                # Cheking price >= 10000
                if float(row['price']) >= 10000:
                    db_id = session.query(Groups_Ads).filter(Groups_Ads.product_id == int(row['id'])).first()
                    # Checking if database already has product
                    if not db_id:
                        # Checking new product's available (table)
                        if row['available'] == 'true':
                            clean_url = getClean_url(row['url'])
                            if clean_url:
                                available = Product(clean_url).getAvaible()
                                # Checking new product's available (scraping)
                                if not re.search(r"К сожалению", available) or re.search(r"Товар поступит", available):
                                    i += 1
                                    writer.writerow([row['id'], row['name'], row['url'], row['vendor'], clean_url])
                                    print(f'Was found New product! id: {row["id"]}. In total: {i}')
                                elif not available:
                                    e += 1
                                    print(f'Error scrapping available! Sum of errors: {e}')
                                else:
                                    avail += 1
                                    print(f"Product {row['id']} don't available. Counter:{avail}")
                            else:
                                e += 1
                                print(f'Error cleaning URL! Sum of errors: {e}')
            print(f'Finish! Sum of new products: {i}. Sum of errors: {e}. Sum not available: {avail}')


# Filling datavase new ads (input: new_ads.csv(id, clean_url))
def Filling_base():
    session = Session(engine)
    i=0 # Data inputting counter
    with open('new_ads.csv', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            input = Groups_Ads(
                product_id=row['id'], 
                clear_url=row['clean_url'],
                available='Идут показы.',
                ads_Id=row['ads_id']
            )
            session.add_all([input])
            i += 1
        session.commit()
        print(f'Inputting {i}-positions')


# Is being cleared url from partner's id
def getClean_url(url):
    try:
        cleanurl = re.findall(r"&ulp=(.+)(?=%3F)", url)[0]
    except:
        return False
    # Replacement reserved url-symbols
    for symbol in cleaning_url:
        cleanurl = re.sub(symbol, cleaning_url[symbol], cleanurl)
    return cleanurl


def save_to_Databse(session, status, row):
    row.available=status
    row.update_date=datetime.utcnow()
    session.commit()


# --- START ---
if __name__ == "__main__":
    print('\n1.Checking available\n2.Filter new products (input: new_catalog.csv)\n3.Filling database (input: new_ads.csv)')
    type_algorithm = input('Input script number that you want to do:')
    if type_algorithm == '1':
        Check_avaible()
    elif type_algorithm == '2':
        Feed_filter()
    elif type_algorithm == '3':
        Filling_base()