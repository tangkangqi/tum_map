import requests
import scrapy
from bs4 import BeautifulSoup
import pandas as pd

def save_html(url):
    html = get_html(url)
    with open('%s.html'%(url.split('/')[-1]), 'w') as f:
        f.write(html)

def get_html(url):
    r = requests.get(url)
    html = r.text
    return html

def get_html1(url):
    fpath = '%s.html'%(url.split('/')[-1])
    data = [v for v in open(fpath, 'r').readlines()]
    data = ''.join(data)
    return data

def func(region):
    url = 'http://legacy.lib.utexas.edu/maps/ams/%s'%(region)
    #save_html(url)

    html = get_html(url)
    # html = get_html1(url)
    soup = BeautifulSoup(html, "html.parser")
    vals = []
    for t in soup.find_all('a'):
        print(t)
        # print(t.get('href'))
        # print(t.contents)
        vals.append([t.get('href'), t.contents])
    df = pd.DataFrame(data=vals, columns=['href', 'contents'])
    df['href'] = df['href'].apply(lambda x: x if type(x) == str else '')
    df['map_flag'] = df['href'].apply(lambda x: 1 if 'http://legacy.lib.utexas.edu/maps/ams/' in x else 0)
    df = df[df['map_flag'] == 1].reset_index()
    df['content'] = df['contents'].apply(lambda x: x[0] if len(x)>0 else '')
    df['content'] = df['content'].apply(lambda x: x.upper() if len(x) > 0 else '')
    #df['flag'] = df['content'].apply(lambda x: 1 if 'NK ' in x else 0)

    df['VICINITY_flag'] = df['content'].apply(lambda x: 1 if 'VICINITY' in x else 0)
    vicinity_list = df[df['VICINITY_flag'] == 1].reset_index()['content'].apply(lambda x: ' '.join(x.split(' ')[:2])).values
    print(vicinity_list)
    def judege_vicinity(name):
        for v in vicinity_list:
            if v in name and 'VICINITY' not in name:
                if ' '.join(name.split(' ')[:2]) == v:
                    return v
        return 0


    df['VICINITY_city'] = df['content'].apply(lambda x: 1 if judege_vicinity(x) !=0 else 0)
    df.to_excel('%s.xls'%(region))
    return

if __name__ == '__main__':
    regions = ['china', 'manchuria', 'taiwan',  'japan', 'korea',
               'indonesia', 'philippines', 'indochina_and_thailand',
               'india','south_africa', 'france']
    # 依次是中国（美帝的恶意叫法，前三个是中国华北华南、中国东北、中国台湾）、日本、 韩国
    # 印度尼西亚、菲律宾、中南半岛、印度、南非、法国

    for region in regions:
        func(region)