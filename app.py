import xlwt
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
            unique_list.append(item["link"])
            new_data.append([item["name"], item["link"]])
    return new_data


def write(data, path):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("sheet")

    col_index = 0
    for col in data:
        row_index = 0
        for row in col:
            ws.write(col_index, row_index, row)
            row_index += 1
        col_index += 1

    wb.save(path)


if __name__ == "__main__":

    while True:
        word = input("请输入搜索词")
        if not word:
            continue
        try:

            google_res = google.shopping(word, 3)

            data = [{"name": i.name, "price": i.price} for i in google_res]
            print(data)
            write(data, "/home/rogers/" + word + ".xls")

        except Exception as e:
            print(e)
