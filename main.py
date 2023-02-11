import requests
from bs4 import BeautifulSoup
import lxml
import os
import json
from fake_useragent import UserAgent
from progress.bar import Bar
from time import sleep
ua = UserAgent()

if os.path.exists('files'):
    pass
elif not os.path.exists('files'):
    os.mkdir('files')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'
}
try:
    response = requests.get('https://s106.skladchina.biz/', headers = headers).text
    
except Exception as e:
    print('ошбика:\n', e)

else:
    tag_li_s = BeautifulSoup(response, 'lxml').find_all('ol', class_ = 'nodeList')[2].find_all('li')
    for li in tag_li_s:
        link = li.find('h3', class_ = 'nodeTitle').find('a')
        txt = link.text.strip()
        print(txt)
        os.mkdir(f'files/{txt}')
        headers = {
            'user-agent': ua.random
        }
        link = 'https://s106.skladchina.biz/' + link.get('href')
        response2 = requests.get(link + '?tt=dostupno', headers = headers).text
        try:
            max_page = int(BeautifulSoup(response2, 'lxml').find('span', class_ = 'pageNavHeader').text.split(' ')[-1].strip())
        except Exception as e:
            max_page = 1
        with Bar('Обработано страниц: ', max = max_page) as bar:
            page_names = []
            for page in range(1, max_page + 1):
                try:
                    bar.next()
                    headers = {
                        'user-agent': ua.random
                    }
                    response3 = requests.get(link + f'page-{page}?tt=dostupno', headers = headers).text
                    all_names = BeautifulSoup(response3, 'lxml').find_all('div', class_ = 'title')
                    for name in all_names:
                        name = name.find('a').text.strip()
                        page_names.append(
                            {
                            'name_course': name
                            }
                        )

                except Exception as e:
                    sleep(200)
            json.dump(page_names, open(f'files/{txt}/data.json', 'w', encoding = 'utf-8'), ensure_ascii = False, indent = 4)
            

