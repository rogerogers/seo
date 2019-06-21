from bing import bing
from google import google
import pandas as pd

if __name__=='__main__':

    while True:
        word = input('请输入搜索词')
        if not word:
            continue
        try:

            bing_res = bing.search(word)
            google_res = google.search(word)
            bing_recommands = bing_res[0].recommand
            if bing_recommands:
                print(bing_recommands)
                for recommand in bing_recommands:
                    bing_res = bing_res.extend(bing.search(recommand))

            df = pd.DataFrame([{'name': i.name, 'link': i.link} for i in bing_res])
            print(df)
            df.to_excel('/home/sense/' + word + '.xls')


        except Exception as e:
            print(e)

