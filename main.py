import grequests
from bs4 import BeautifulSoup
import csv
import time


def get_urls():
    urls = []
    for x in range(1, 51):
        urls.append(f'https://books.toscrape.com/catalogue/page-{x}.html')
    return urls


def get_data(urls_list):
    reqs = [grequests.get(url) for url in urls_list]
    resp = grequests.map(reqs)
    return resp


def parse_data(responses):
    for r in responses:
        soup = BeautifulSoup(r.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            data = []
            title = book.find('h3').text
            price = book.find('p', class_='price_color').text
            data.append(title)
            data.append(price)
            print(title, price)
            write_to_csv(data)


def write_to_csv(data_list):
    with open('books.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_list)



if __name__ == '__main__':
    start = time.perf_counter()
    all_urls = get_urls()
    response = get_data(all_urls)
    parse_data(response)
    finish = time.perf_counter()
    print(finish - start)
