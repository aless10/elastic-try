from bs4 import BeautifulSoup
import requests
import urllib
import json

base_url = 'http://milan2017.codemotionworld.com'
speakers_url = '/speakers/'

r = urllib.request.urlopen(base_url + speakers_url)
soup = BeautifulSoup(r)

info = {"speaker_list": []}

articles = soup.find_all("article", class_="post col")
n = 1

for element in articles[:-1]:
    href = element.a['href']
    new_r = urllib.request.urlopen(href)
    soup = BeautifulSoup(new_r)
    headers = soup.find("article", id="speaker")
    name = headers.h1.text
    job = headers.h2.text
    try:
        talk_title_div = soup.find("div", class_= "eight_col")
        talk_title_html = talk_title_div.find_all('p')[1]
        talk_title = talk_title_html.text
        talk_link = talk_title_html.a['href']
        last_r = urllib.request.urlopen(base_url + talk_link)
        last_soup = BeautifulSoup(last_r)
        talk_desc_p = last_soup.find("p")
        talk_desc = talk_desc_p.text
        talk_info = last_soup.find_all('h3')
        talk_lang = talk_info[1].text.split(" ")[1]
        talk_level = talk_info[2].text.split(" ")[1]
        id = str(n)
        n += 1
        print(n)
        print(talk_title)
        info["speaker_list"].append({'id': id,
                     'speaker': name,
                     'job': job,
                     'title': talk_title,
                     'description': talk_desc,
                     'language': talk_lang,
                     'level': talk_level
                      })
    except:
        print('No link')
        pass

with open('codemotion_info.txt', 'w') as outfile:
    json.dump(info, outfile)

with open('codemotion_info.json', 'w') as jsonfile:
    json.dump(info, jsonfile)



