import pandas as pd
from bing import bing
from google import google
from urllib.parse import urlparse
from time import sleep

def get_netloc(url):
    return urlparse(url).netloc

if __name__=='__main__':

    while True:
        word = input('请输入搜索词')
        if not word:
            continue
        try:

            bing_res = bing.search(word)
            google_res = google.search(word, 3)
            google_recommands = google_res[0].recommand
            bing_recommands = bing_res[0].recommand
            if bing_recommands:
                for recommand in bing_recommands:
                    bing_res.extend(bing.search(recommand))
                    sleep(3)

            if google_recommands:
                for recommand in google_recommands:
                    google_res.extend(google.search(recommand, 3))
                    sleep(3)
            google_res.extend(bing_res)

            df = pd.DataFrame([{'name': i.name, 'link': get_netloc(i.link)} for i in google_res]).groupby('link').first()
            df.to_excel('/home/sense/' + word + '.xls')


        except Exception as e:
            print(e)

