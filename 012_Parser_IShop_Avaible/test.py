from Class_API_Yandex import API_Requests
from Class_Scraping import Product
import csv, sys


print('Working!')
sys.exit()


# i = 0
# with open('IS_available.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=';')   
#     with open('avaible.csv', 'a', encoding='utf-8', newline='') as file:
#         for row in reader:
#             i += 1
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
    #             ads_Id=row['Ads_id']
    #         )
    #         session.add_all([input])
    #         print(f'Обработано {i}-позиций')
    #     session.commit()