import xlwt
from bing import bing
from google import google
from urllib.parse import urlparse
from time import sleep
from os import path

def get_netloc(url):
    return urlparse(url).netloc


def data_unique(data):
    new_data = []
    unique_list = []
    for item in data:
        if item not in unique_list:
            unique_list.append(item['link'])
            new_data.append([item['name'], item['link']])
    return new_data


def write(data, path):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sheet')

    col_index = 0
    for col in data:
        row_index = 0
        for row in col:
            print(type(row), row)
            ws.write(col_index, row_index, row)
            row_index += 1
        col_index += 1

    wb.save(path)


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
            google_res = []
            google_res.extend(bing_res)
            data = data_unique([{'name': i.name, 'link': get_netloc(i.link)} for i in google_res])
            write(data, '/home/rogers/' + word + '.xls')



        except Exception as e:
            print(e)

