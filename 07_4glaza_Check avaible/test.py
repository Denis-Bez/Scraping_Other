from Class_API_Yandex import API_Requests
import csv, re
from Class_Scraping import Product


a = ['1er1443896462', '1144er3896463', '11re443896464']
b = API_Requests(a)
print(b.GetStatus_Ads())











# Creating Tables SQLAlchemy
# Base.metadata.create_all(engine)


# i = 0
# with open('4glaza_available.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=';')   
#     with open('avaible.csv', 'a', encoding='utf-8', newline='') as file:
#         for row in reader:
#             req = API_Requests(row['Ads_id'])
#             response = req.GetStatus_Ads()
#             response = response['result']['Ads']
#             writer = csv.writer(file, delimiter=';')
#             writer.writerow([row['product_id'], response])
#             print(f'Проверено {i}-позиций')


# Filling database
    # session = Session(engine)
    # i=0
    # with open('4glaza_available.csv', encoding='utf-8', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile, delimiter=';')
    #     for row in reader:
    #         input = Groups_Ads(
    #             product_id=row['product_id'], 
    #             clear_url=row['clear_url'],
    #             available=row['Status'],
    #             price=0,
    #             ads_Id=row['Ads_id']
    #         )
    #         session.add_all([input])
    #         print(f'Обработано {i}-позиций')
    #     session.commit()

     
  