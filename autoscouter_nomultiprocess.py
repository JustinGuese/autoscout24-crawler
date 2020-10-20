from bs4 import BeautifulSoup, SoupStrainer #HTML parsing
import urllib.request #aufrufen von URLs
from time import sleep #damit legen wir den Scraper schlafen
import json #lesen und schreiben von JSON-Dateien
from datetime import datetime #um den Daten Timestamps zu geben
import re #regular expressions
import os #Dateipfade erstellen und lesen
import pandas as pd #Datenanalyse und -manipulation
from pathlib import Path


folders = ["data/visited/","data/autos/"]
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

path_to_visited_urls = "data/visited/visited_urls.json"
if not os.path.isfile(path_to_visited_urls):
    with open(path_to_visited_urls,"w") as file:
        json.dump([],file)


countries = {"Deutschland": "D",
             "Oesterreich": "A",
            #  "Belgien" : "B",
            #  "Spanien": "E",
            #  "Frankreich": "F",
            #  "Italien": "I",
            #  "Luxemburg": "L",
            #  "Niederlande": "NL"
             }



def getCar(URL,country,cycle_counter,multiple_cars_dict,visited_urls):
    problemURLS = ["https://www.autoscout24.de/leasing/angebote/"]
    try:
        if URL not in problemURLS:
            car_dict = {}
            car_dict["country"] = country
            car_dict["date"] = str(datetime.now())                    
            car = BeautifulSoup(urllib.request.urlopen('https://www.autoscout24.de'+URL).read(),'lxml')
            for key, value in zip(car.find_all("dt"),car.find_all("dd")):
                car_dict[key.text.replace("\n","")] = value.text.replace("\n","")
            car_dict["haendler"] = car.find("div",attrs={"class":"cldt-vendor-contact-box",
                                                            "data-vendor-type":"dealer"}) != None
            car_dict["privat"] = car.find("div",attrs={"class":"cldt-vendor-contact-box",
                                                        "data-vendor-type":"privateseller"}) != None
            car_dict["ort"] = car.find("div",attrs={"class":"sc-grid-col-12",
                                                    "data-item-name":"vendor-contact-city"}).text
            
            car_dict["price"] =  "".join(re.findall(r'[0-9]+',car.find("div",attrs={"class":"cldt-price"}).text))
            
            ausstattung = []
            for i in car.find_all("div",attrs={"class":"cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left"}):
                for span in i.find_all("span"):
                    ausstattung.append(i.text)
            ausstattung2 = []
            for element in list(set(ausstattung)):
                austattung_liste = element.split("\n")
                ausstattung2.extend(austattung_liste)
            car_dict["ausstattung_liste"] = sorted(list(set(ausstattung2)))
            q.put([URL,car_dict])
            multiple_cars_dict[URL] = car_dict
            visited_urls.append(URL)
        else: # is prob url
            q.put([URL,None])
    except Exception as e:
        print("Problem mit Detailseite: " + str(e) + " "*50)
        q.put([URL,None])
        with open("errorlog.txt","a") as file:
            err = 'https://www.autoscout24.de'+URL+ " cycle: "+str(cycle_counter)+"\n"
            file.write(err)


def run_once(cycle_counter,path_to_visited_urls,countries,folders):
    with open(path_to_visited_urls) as file:
        visited_urls = json.load(file)
    
    if len(visited_urls) > 100000:
        visited_urls = []
    
    multiple_cars_dict = {}
    
    cycle_counter+=1
    for country in countries:
        
        car_URLs = []
        
        for page in range(1,2):# this part is heavy on the ram. after x runs it saves to disk. 2 works for me (16 gb)
            try:
                url = 'https://www.autoscout24.de/lst/?sort=age&desc=1&ustate=N%2CU&size=20&page='+str(page)+ '&cy=' + countries[country] +'&atype=C&'
                only_a_tags = SoupStrainer("a")
                soup = BeautifulSoup(urllib.request.urlopen(url).read(),'lxml', parse_only=only_a_tags)
            except Exception as e:
                #print("uebersicht: " + str(e) +" "*50, end='\r')
                raise
            for link in soup.find_all("a"):
                if r"/angebote/" in str(link.get("href")):
                    car_URLs.append(link.get("href"))
            car_URLs_unique = [car for car in list(set(car_URLs)) if car not in visited_urls]
            
            #print(f'Lauf {cycle_counter} | {country} | Seite {page} | {len(car_URLs_unique)} neue URLs', end="\r")
        print("")
        if len(car_URLs_unique)>0:
            for link in car_URLs_unique:
                getCar(URL,country,cycle_counter,multiple_cars_dict,visited_urls)
                
        else:
            print("\U0001F634 will sleep bc too many requests")
            sleep(60)
    if len(multiple_cars_dict)>0:
        df = pd.DataFrame(multiple_cars_dict).T
        print("wiritng.... "+str(datetime.now())+".csv")
        df.to_csv("data/autos/"+re.sub("[.,:,-, ]","_",str(datetime.now()))+".csv",sep=";",index_label="url")
    else:
        print("Keine Daten")
    with open("data/visited/visited_urls.json", "w") as file:
        json.dump(visited_urls, file)

car_counter=1
cycle_counter=0

pxs = []

print("no multiprocessing here...")
while True:
    run_once(cycle_counter,path_to_visited_urls,countries,folders)