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

# req = session.get(base_url + "?page=" + str(150))
# print(req.status_code)


def get_company(base_url, cnt):

    urls.append(base_url + '?page=' + str(cnt))
    req = session.get(urls[-1], headers=headers)

    if req.status_code == 200:
        bsObj = BS(req.content, 'html.parser')
        div_list = bsObj.find_all('div', attrs={'class': 'job-link'})
        for div in div_list:
            title = div.find('a').text
            href = div.a['href']
            short = div.p.text
            short = re.sub(pattern, ' ', short)
            short = short.strip()
            span_list = div.find_all('span')
            company = 'No name'
            for span in span_list:
                b = span.find('b')
                if b:
                    company = b.text
                    break
            jobs.append({'title': title,
                         'href': domain + href,
                         'description': short,
                         'company': company})

        return True
    return


cnt = 1
while cnt < 16:
    if not get_company(base_url, cnt):
        break
    cnt += 1

handle = open('jobs.html', 'w', encoding='utf-8')
handle.write(str(jobs))
handle.close()

# for i in jobs:
#     print(i)
