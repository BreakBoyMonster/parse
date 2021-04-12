import requests
from bs4 import BeautifulSoup as BS
# import codecs
import string
import re

# 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36}'
session = requests.session()
headers = {'User-Agent':
            'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }
base_url = 'https://www.work.ua/jobs-kyiv-%D0%BA%D0%BE%D0%BD%D0%B4%D0%B8%D1%82%D0%B5%D1%80/'
domain = 'https://www.work.ua'
jobs = []
urls = []
pattern = r'\s{2,}|\xa0|\u2060'


def get_company(base_url, cnt):

    urls.append(base_url + '?page=' + str(cnt))
    req = session.get(urls[-1], headers=headers)
    # if req.status_code == 200:
        # bsObj = BS(req.content, 'html.parser')
        # pagination = bsObj.find('ul', attrs={'class': 'pagination'})
        # if pagination:
        #     pages = pagination.find_all('li', attrs={'class': False})
        #     for page in pages:
        #         urls.append(domain + page.a['href'])

    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        div_list = bsObj.find_all('div', attrs={'class': 'job-link'})
        for div in div_list:
            title = div.find('a').text
            href = div.a['href']
            short = div.p.text
            short = re.sub(pattern, ' ', short)
            short = short.strip()
            company = 'No name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({'cnt': cnt,
                         'title': title,
                         'href': domain + href,
                         'description': short,
                         'company': company})

        # print(cnt)
        return True
    return False

cnt = 1
while get_company(base_url, cnt):
    cnt += 1

handle = open('jobs.html', 'w', encoding='utf-8')
handle.write(str(jobs))
handle.close()

for i in jobs:
    print(i)
