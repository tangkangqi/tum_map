import scrapy
import pandas as pd
import os, sys
import threading
import urllib


def get_urls():
    vals = []
    for f in os.listdir('./'):
        if '.xls' in f:
            df = pd.read_excel(f)
            df = df[df['VICINITY_city'] == 1].reset_index()
            for v in df[['content','href']].values:
                vals.append([f.split('.')[0], v[0], v[1]])
    return vals

def func():
    data = get_urls()
    df = pd.DataFrame(data=data, columns=['region','content','href'])
    df['name'] = df.apply(lambda x: x['region'] + '-' + x['content'] + '-' + x['href'].split('/')[-1], axis=1)
    vals = df[['href', 'name']].values
    vals = [v for v in vals]
    download(vals)


def download(val_list):
    glock = threading.Lock()
    def download_picture():
        while True:
            glock.acquire()
            if len(val_list) == 0:
                glock.release()
                continue
            else:
                tp  = val_list.pop()
                glock.release()
                # 修改文件名
                url = tp[0]
                filename = tp[1]
                path = os.path.join("img", filename)
                # 下载图片，保存本地
                urllib.request.urlretrieve(url, filename=path)

    for x in range(10):
        product = threading.Thread(target=download_picture)
        product.start()

if __name__ == '__main__':
    func()