import bs4 as bs
from urllib.request import Request, urlopen
import csv
import json
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

DATA = []

def extract_questions(url):
    try:
        q = Request(url ,None,hdr)
        source = urlopen(q).read()
        c = url.split('/')[3]
        sc = url.split('/')[4]
        ssc = url.split('/')[-1].split('.')[0][4:]
        soup1 = bs.BeautifulSoup(source , "html5lib")
        article1 = soup1.find("div", {"class":"detail-body"}).findAll('li' ,{"class":["even", "alt"]})
        # print(article)
        for a in article1:
            q = a.find('h3').text
            a = a.find('p').text
            data_obj = {
                'class' : c,
                'sub_class' : sc,
                'sub_sub_class' : ssc,
                'question' : q,
                'answer' : a
            }
            DATA.append(data_obj)

    except:
        print(url)

urls = [
        'http://info.maybank2u.com.sg/personal/customer-service/faq/faq-personal.aspx',
        'http://info.maybank2u.com.sg/business/customer-service/faq/faq-business.aspx',
        'http://info.maybank2u.com.sg/eservices/faq/faq-eservices.aspx#personal',
        ]
for u in urls:

    site = u
    q = Request(site ,None,hdr)
    source = urlopen(q).read()

    soup = bs.BeautifulSoup(source , "html5lib")
    article = soup.find("div", {"class":"detail-content"}).findAll('a'  , href = True)

    for a in article:
        extract_questions('http://info.maybank2u.com.sg' + a['href'])

f = open('maybank1.json', 'w')
f.write(json.dumps(DATA))
f.close()
