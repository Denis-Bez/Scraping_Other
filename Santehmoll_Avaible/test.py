from Class_API_Yandex import API_Requests
from Class_product_card import Product
import csv

import main_Smoll

def checkAvaible():

    current_data = main_Smoll.Groups_Ads.Scrap_current_data()
    new = []
    for i in range(0, 2):
        for row in current_data:
            items = Product.getSoup(row.clearurl)         
            new.append(row.id)
            new.append(Product.getAvaible(items))
            new.append(Product.getPrice(items))
            new.append(Product.getOldPrice(items))

            with open('checking.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(new)


if __name__ == "__main__":
    checkAvaible()