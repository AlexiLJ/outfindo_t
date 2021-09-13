# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import lxml
import json
import pandas as pd


def scrape_product_detail_page(product_detail_url):
    yield_=dict()
    product_page = requests.get(product_detail_url)
    soup = BeautifulSoup(product_page.content, 'lxml')
    yield_["model"] = soup.find(id="detail_page").h1.text
    yield_["url"] = product_detail_url
    yield_["main_photo_path"] = soup.find(id="nahled")["src"]

    links = [link.img['src'] for link in soup.find_all(class_="html5lightbox")]
    if len(links) == 0: yield_['additional_photo_paths']=None
    else: yield_['additional_photo_paths']=links

    price  = soup.find(class_="cena").span.text.split()[0].split('.') 
    yield_["price"] = int(''.join(price))
    yield_["model_year"] = int(''.join(price))

    #Here I manage specs in the html table through pandas
    
    tab = soup.find_all('table', class_='spec')
    table_list=[]
    for t in tab:
        table_rows = t.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            table_list.append(row[1:])
    table=pd.DataFrame(table_list, columns=['spec', 'data'])
    
    
    year = table[table['spec'] == "Ročník"]
    yield_['model_year'] = int(year.iloc[0]['data'])
    
    yield_["parameters"] ={
        "weight" : table.loc[table[(table['spec'] == "Hmotnost")].index[0]]['data'],
        "frame": table.loc[table[(table['spec'] == "Rám")].index[0]]['data']
        }
   
    return yield_


'''

model_year - celočíselná hodota modelového roky daného kola, na "Ročník" v sekci
Sekce parameters bude obsahovat tyto parametry
weight - textová hodnota, nachází pod názvem "Hmotnost" v sekci specifikace
frame - textová hodnota názvu rámu, nachází se pod názvem "Rám" v sekci specifikace
'''

if __name__ == '__main__':
    scrap = scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/spicy-cf-69/5943')
    # print(scrap)

    with open('output.json', 'w+') as f:
        # this would place the entire output on one line
        # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
        json.dump(scrap, f, indent=4)