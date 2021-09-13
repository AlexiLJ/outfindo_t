from bs4 import BeautifulSoup
import requests
import lxml
import json


def scrape_product_detail_page(product_detail_url):
    yield_=dict()
    product_page = requests.get(product_detail_url).text
    soup = BeautifulSoup(product_page, 'lxml')
    yield_["model"] = soup.find(id="detail_page").h1.text
    yield_["url"] = product_detail_url
    yield_["main_photo_path"] = soup.find(id="nahled")["src"]

    links = [link.img['src'] for link in soup.find_all(class_="html5lightbox")]
    if len(links) == 0: yield_['additional_photo_paths']=None
    else: yield_['additional_photo_paths']=links
      
    # yield_["additional_photo_paths"] = soup.find_all(class_="pohledy").a.text
    return yield_


'''
model - textový název modelu

url - textový název detailu stránky
main_photo_path - cesta k hlavní fotce o největších rozměrech
additional_photo_paths - textové pole s dalšími cestami fotek opět v největší kvalitě.
price - celočíselná hotnota
model_year - celočíselná hodota modelového roky daného kola, na "Ročník" v sekci
Sekce parameters bude obsahovat tyto parametry
weight - textová hodnota, nachází pod názvem "Hmotnost" v sekci specifikace
frame - textová hodnota názvu rámu, nachází se pod názvem "Rám" v sekci specifikace
'''

if __name__ == '__main__':
    scrap = scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/spicy-cf-69/5943')
    # print(scrap)
    print(scrap["additional_photo_paths"])
    with open('output.json', 'w+') as f:
        # this would place the entire output on one line
        # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
        json.dump(scrap, f, indent=4)