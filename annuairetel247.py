import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import sys
from utils import printProgressBar


def scrapping(name, location=None):
    url = f"https://www.annuairetel247.com/search.php?q={name}&loc={location if location else ''}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    search_list= soup.find('div', {'class', 'search-list'})
    li_s = search_list.find_all('li')
    anchors = [f"https://www.annuairetel247.com{item.find('a')['href']}" for item in li_s]
    data = []
    printProgressBar(0, len(anchors), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for index, anchor in enumerate(anchors):
        data.append(get_detail(anchor))
        printProgressBar(index + 1, len(anchors), prefix = 'Progress:', suffix = 'Complete', length = 50)

    export_data(filename=f"{name}_{location if location else ''}_result.csv", data=data)


def get_detail(anchor):
    sleep(0.4)
    page = requests.get(anchor)
    soup = BeautifulSoup(page.content, 'html.parser')
    vcard = soup.find('div', {'class', 'vcard'})
    name = vcard.find('span', {'class', 'fn'}).text.strip()
    address = vcard.find('div', {'class', 'street-address'}).text.strip()
    city = vcard.find('div', {'class', 'locality'}).text.strip()
    postal_code = vcard.find('div', {'class', 'postal-code'}).text.strip()
    country = vcard.find('div', {'class', 'country-name'}).text.strip()
    tel_numbers = vcard.find_all('li', {'class', 'tel'})
    tel = " / ".join(tel for tel in tel_numbers[0].find('span', {'class', 'value'}).text.split(','))
    tel2 = tel_numbers[1].find('span', {'class', 'value'}).text
    fax = tel_numbers[2].find('span', {'class', 'value'}).text
    return [name, address, city, postal_code, country, tel, tel2, fax]


def export_data(filename, data):
    # field names
    fields = ['NOM/PRENOM', 'ADDRESSE', 'VILLE', 'CODE_POSTAL', 'PAYS', 'SITE_INTERNET', 'TELEPHONES', 'TELEPHONE_CELLULAIRES', 'FAX']
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # writing the fields
        csvwriter.writerow(fields)
        
        # writing the data rows
        csvwriter.writerows(data)


if __name__ == '__main__':
    location = None
    if len(sys.argv) >= 2:
        name = sys.argv[1]
    if len(sys.argv) == 3:
        location = sys.argv[2]
    scrapping('albert', 'paris')
