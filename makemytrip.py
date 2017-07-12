import bs4 as bs
from urllib.request import Request, urlopen
import json
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 \
    (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;\
        q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

DATA = []


def extract_items(url):
    url = 'https:' + url
    print(url)
    q = Request(url, None, hdr)
    source = urlopen(q).read()
    soup1 = bs.BeautifulSoup(source, "html5lib")
    article1 = soup1.find("div", {"class": "destInfoWrap"}).findAll('li')
    for a in article1:
        item = {
            'image_source': a.find('img')['src'],
            'name': a.find('h4').text,
            'details': a.find('p').text,
            'tags': []
        }
        spans = a.findAll('span')
        item['tags'] = [span.get_text() for span in spans]
        DATA.append(item)


url = 'https://www.makemytrip.com/travel-guide/singapore/places-to-visit.html'

q = Request(url, None, hdr)
source = urlopen(q).read()
soup = bs.BeautifulSoup(source, "html5lib")
article = soup.find("ul", {"class": "lftNavList"}).findAll('a', href=True)
for a in article[1:]:
    extract_items(a['href'])
f = open('maybank1.json', 'w')
f.write(json.dumps(DATA))
f.close()
