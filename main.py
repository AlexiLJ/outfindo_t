from bs4 import BeautifulSoup
import requests
import lxml
import json
import pandas as pd


def scrape_product_detail_page(product_detail_url):
    yield_=dict()                                           #init dinct
    product_page = requests.get(product_detail_url)         
    soup = BeautifulSoup(product_page.content, 'lxml')      #get bs4 representation of the page 
    
    yield_["model"] = soup.find(id="detail_page").h1.text   # getting requsted data
    yield_["url"] = product_detail_url
    yield_["main_photo_path"] = soup.find(id="nahled")["src"]

    links = [link.img['src'] for link in soup.find_all(class_="html5lightbox")]
    if len(links) == 0: yield_['additional_photo_paths']=None
    else: yield_['additional_photo_paths']=links

    price  = soup.find(class_="cena").span.text.split()[0].split('.')  #formating price
    yield_["price"] = int(''.join(price))                               #
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
    table=pd.DataFrame(table_list, columns=['spec', 'data']) # get pandas data frame
    
    
    
    year = table[table['spec'] == "Ročník"]
    yield_['model_year'] = int(year.iloc[0]['data'])
    
    yield_["parameters"] ={
        "weight" : table.loc[table[(table['spec'] == "Hmotnost")].index[0]]['data'],
        "frame": table.loc[table[(table['spec'] == "Rám")].index[0]]['data']
        }
   
    return yield_

def main(name, url_links):
    with open(name, 'a') as f:
        data=[scrape_product_detail_page(task) for task in url_links] #brute force
        json.dump(data, f, indent=4)                                    #
       
if __name__ == '__main__':
    tasks = [
        "https://www.lapierre-bike.cz/produkt/aircode-drs-80/5934", 
        "https://www.lapierre-bike.cz/produkt/spicy-cf-79/5993",
        "https://www.lapierre-bike.cz/produkt/lapierre-crosshill-50/6037",
        "https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-ltd-ultimate/5951",
        "https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-90-ultimate/5950"

    ]

    main("top-5-bikes.json", tasks)


    


        
   
