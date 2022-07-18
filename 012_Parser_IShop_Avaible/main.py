import random
import requests
from bs4 import BeautifulSoup
import csv
import time

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36', 'accept': '*/*'}

def get_content(url):

    # Protection if link don't open
    try:
        html = requests.get(url, headers=HEADERS, timeout=20)

    # If url did't open
    except Exception:
        print("Something went wrong. Repeat")
        time.sleep(60)

        # Try open url again
        try:
            html = requests.get(url, headers=headers, timeout=120)
        except Exception:
            print("Something went wrong Again")
            avaible = 'Ссылка не работает'
        else:
            avaible = read_avaible(html)
    else:
        avaible = read_avaible(html)

    return avaible

def read_avaible(html):

    # Check url for Error
    if html.status_code == 200:

        # Reading avaible information from url
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find('div', class_='wrap')
        avaible = items.find('h1').find_next('p').find_next('span').getText(strip=True)

        
    else:
        avaible = 'Ссылка не работает'

    return avaible


def main():

    i = 0  # Just counter

    # Create title new "csv"
    with open('avaible.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'url', 'avaible'])

    # Open file with all url
    with open('Ishop_avaible_all.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Check all product
        for row in reader:
            avaible = get_content(row['url'])
            i += 1  # Just Couter

            # Write avaible infomation into file "avaible.csv"
            with open('avaible.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([row['id'], row['url'], avaible])
            print(f'Проверенно: {i} позиций. Статус: {avaible}')
            time.sleep(random.randint(5, 10))
            file.close()

    csvfile.close()

if __name__ == "__main__":
    main()