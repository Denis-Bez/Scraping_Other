import csv, re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import declarative_base, Session

from Class_Scraping import Product
from Class_API_Yandex import API_Requests

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
                    # print(f"Checking {i}-rows. Ads {row.product_id} Doesn't changed") 
            else:
                if row.available == 'Идут показы.':
                    save_to_Databse(session, row.available, row)
                    # print(f"Checking {i}-rows. Ads {row.product_id} Doesn't changed") 
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

                

def save_to_Databse(session, status, row):
    row.available=status
    row.update_date=datetime.utcnow()
    session.commit()


# --- START ---
if __name__ == "__main__":
    print('\n1.Checking available\n2.Filter feed (in development)\n')
    type_algorithm = input('Input script number that you want to do:')
    # print(type_algorithm)
    if type_algorithm == '1':
        Check_avaible()
    elif type_algorithm == '2':
        print("TODO: Creating csv-file of products that there aren't in database and filtering on price and available")