from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from requests.exceptions import ConnectionError


def get_soup(url):
    # Requests HTML
    # other header:  (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3

    headers = {'User-Agent':
         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }

    time.sleep(1)

    success = False
    while not success:
        try:
            request = requests.get(url, headers=headers)
            success = True
        except ConnectionError:
            print("Connection failed, retrying...")

    # HTML parser
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup


def get_pages(start, end):
    pages = []

    # Generates URLs of pages that contain transfer records between start and end
    for season in range(start, end + 1):
        for i in range(1, 11):
            url = 'https://www.transfermarkt.us/transfers/transferrekorde/statistik/top/saison_id/' + str(season) + \
                  '/land_id//ausrichtung//spielerposition_id//altersklasse//jahrgang/0/leihe//w_s//plus/1/galerie/0' \
                  '/page/' + str(i)
            pages.append(url)
    return pages


def get_details(link):
    url = 'https://www.transfermarkt.us' + link
    doc = get_soup(url)

    table = doc.find('div', id=link.split('/')[-1]).find('table')

    # Rows containing desired information
    rows = table.find_all('tr')

    # Access the information
    old_club_league = rows[2].find_all('td')[0].text.strip()
    new_club_league = rows[2].find_all('td')[2].text.strip()
    old_club_league_type = rows[3].find_all('td')[0].text.strip()
    new_club_league_type = rows[3].find_all('td')[2].text.strip()
    age_at_transfer = ''
    contract_remaining = ''

    for row in rows:
        cells = row.find_all('td')

        for cell in cells:
            if 'Age at time of transfer' in cell.text:
                age_at_transfer = cell.text.split('Age at time of transfer')[1].strip()
            if 'Remaining contract duration' in cell.text:
                s = cell.text.split('Remaining contract duration at')
                contract_remaining = s[1].split('\n')[2].split(' (')[0].strip()

    details = [old_club_league, new_club_league,
            old_club_league_type, new_club_league_type,
            age_at_transfer, contract_remaining]

    return details


def get_info(pages):

    info = []

    # Accesses each page
    for url in pages:
        doc = get_soup(url)
        table = doc.find('table', class_='items')
        rows = table.find_all('tr')[1::7]

        players = []

        #Accesses each individual player transfer on the page
        for row in rows:
            name = row.find('td', {'class': 'hauptlink'}).find('a').text
            position = row.find_all('table', {'class': 'inline-table'})[0].find_all('tr')[1].find('td').text.strip()
            country = row.find_all('img', {'class': 'flaggenrahmen'})[0]['title']

            season = row.find_all('a')[1].text
            market_value = row.find_all('td', {'class': 'rechts'})[0].text
            transfer_fee = row.find_all('td', {'class': 'rechts'})[1].text
            left = row.find_all('table', {'class': 'inline-table'})[1].find('a')['title']
            joined = row.find_all('table', {'class': 'inline-table'})[2].find('a')['title']

            general_info = [name, position, country, season, market_value, transfer_fee, left, joined]

            detail_link = row.find('td', {'class': 'rechts hauptlink'}).find('a').get('href')
            details = get_details(detail_link)

            players.append(general_info + details)

        info += players

    return info


if __name__ == "__main__":
    cols = ['name', 'position', 'country', 'season', 'market value', 'transfer fee', 'left', 'joined',
               'old club league', 'new club league', 'old club league type', 'new club league type',
               'age', 'contract remaining']


    print('Obtaining data')
    pages = get_pages(2021, 2022)
    data = get_info(pages)
    print('Data obtained...')


    df = pd.DataFrame(data, columns=cols)
    df.to_csv('transfer_data3.csv', index=False)
