import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import json
import random
import sys
import pandas as pd

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import shuffle

try:

    import requests
    from bs4 import BeautifulSoup
    import random

except:
    print(" Library Not Found !")

list_proxies = [
    "88.99.149.188:31288",
    "51.75.147.40:3128",
    "125.27.251.124:45861",
    "51.254.237.77:3129",
    "104.248.63.49:31583",
    "125.26.99.185:36525",
    "183.164.227.165:4216",
    "180.109.124.30:4216",
    "103.31.251.18:8080",
    "110.44.133.135:3128",
    "175.100.5.52:32721",
    "182.72.150.242:8080",
    "51.75.147.44:3128",
    "78.96.125.24:3128",
    "176.56.107.214:52184",
    "125.26.99.186:41358",
    "217.172.170.116:3838",
    "62.210.177.105:3128",
    "46.225.241.66:3128",
    "180.211.183.178:60604",
    "116.212.129.58:59557",
    "189.195.162.242:8080",
    "165.22.64.68:33874",
    "186.226.172.165:57783",
    "43.248.24.157:51166",
    "78.96.125.24:3128",
    "1.20.102.102:38816",
    "118.174.220.11:60148",
    "195.154.232.38:3838",
    "5.202.188.154:3128",
    "46.151.108.6:41171",
    "119.82.252.29:46872",
    "117.6.161.118:53281",
    "104.248.63.49:31583",
    "1.20.103.196:42792",
    "182.72.150.242:8080",
    "108.163.66.164:8080",
    "103.117.195.224:8686",
    "103.250.68.10:8080",
    "178.33.251.230:3129"
]

_headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}


def get_proxy_function():
    return {"https": list_proxies[0]}


def delete_proxy():
    if len(list_proxies) > 0:
        list_proxies.remove(list_proxies[0])


def Proxy_Request(request_type='get', url='', **kwargs):
    while True:
        try:
            proxy = get_proxy_function()
            print("Using Proxy {}".format(proxy))
            r = requests.request(request_type, url, proxies=proxy, headers=_headers, timeout=8, **kwargs)
            return r
            break
        except:
            pass

class Gsmarena():

    def __init__(self):
        self.phones = []
        self.features = ["Brand", "Model Name", "Model Image"]
        self.temp1 = []
        self.phones_brands = []
        self.url = 'https://www.gsmarena.com/'
        self.new_folder_name = 'GSMArenaDataset'
        self.absolute_path = os.popen('cd').read().strip() + '/' + self.new_folder_name

    def crawl_html_page(self, sub_url):

        url = self.url + sub_url

        try:
            request_type = "get"

            r = Proxy_Request(url=url, request_type=request_type)

            soup = BeautifulSoup(r.content, 'html.parser')
            title = soup.find('title')
            if title == "Too Many Requests":
                delete_proxy()
                self.crawl_html_page(sub_url)
            else:
                return soup

        except ConnectionError as err:
            print("Please check your network connection and re-run the script.")
            exit()

        except Exception:
            print("Please check your network connection and re-run the script.")
            exit()

    def crawl_phone_brands(self):
        phones_brands = []
        soup = self.crawl_html_page('makers.php3')
        table = soup.find_all('table')[0]
        table_a = table.find_all('a')
        for a in table_a:
            temp = [a['href'].split('-')[0], a.find('span').text.split(' ')[0], a['href']]
            phones_brands.append(temp)
        phones_brands.reverse()
        return phones_brands

    def crawl_phones_models(self, phone_brand_link):
        links = []
        nav_link = []
        soup = self.crawl_html_page(phone_brand_link)
        nav_data = soup.find(class_='nav-pages')
        if not nav_data:
            nav_link.append(phone_brand_link)
        else:
            nav_link = nav_data.findAll('a')
            nav_link = [link['href'] for link in nav_link]
            nav_link.append(phone_brand_link)
            nav_link.insert(0, nav_link.pop())
        for link in nav_link:
            soup = self.crawl_html_page(link)
            data = soup.find(class_='section-body')
            for line1 in data.findAll('a'):
                links.append(line1['href'])

        return links

    def crawl_phones_models_specification(self, link, phone_brand):
        phone_data = {}
        try:
            soup = self.crawl_html_page(link)
            model_name = soup.find(class_='specs-phone-name-title').text
            model_img_html = soup.find(class_='specs-photo-main')
            model_img = model_img_html.find('img')['src']
            phone_data.update({"Brand": phone_brand})
            phone_data.update({"Model Name": model_name})
            phone_data.update({"Model Image": model_img})
            temp = []
            for data1 in range(len(soup.findAll('table'))):
                table = soup.findAll('table')[data1]
                for line in table.findAll('tr'):
                    temp = []
                    for l in line.findAll('td'):
                        text = l.getText()
                        text = text.strip()
                        text = text.lstrip()
                        text = text.rstrip()
                        text = text.replace("\n", "")
                        temp.append(text)
                        if temp[0] in phone_data.keys():
                            temp[0] = temp[0] + '_1'
                        if temp[0] not in self.features:
                            self.features.append(temp[0])
                    if not temp:
                        continue
                    else:
                        phone_data.update({temp[0]: temp[1]})
        except:
            print("exception tamu ima")
            return phone_data

        return phone_data

    def create_folder(self):
        if not os.path.exists(self.new_folder_name):
            os.system('mkdir ' + self.new_folder_name)
            print("Creating ", self.new_folder_name, " Folder....")
            time.sleep(6)
            print("Folder Created.")
        else:
            print(self.new_folder_name, "directory already exists")

    def check_file_exists(self):
        return os.listdir(self.absolute_path)

    def save_specification_to_file(self):
        phone_brand = self.crawl_phone_brands()
        self.create_folder()
        files_list = self.check_file_exists()
        for brand in phone_brand:
            phones_data = []
            if (brand[0].title() + '.csv') not in files_list:
                link = self.crawl_phones_models(brand[2])
                model_value = 1
                print("Working on", brand[0].title(), "brand.")
                for value in link:
                    datum = self.crawl_phones_models_specification(value, brand[0])
                    datum = {k: v.replace('\n', ' ').replace('\r', ' ') for k, v in datum.items()}
                    phones_data.append(datum)
                    print("Completed ", model_value, "/", len(link))
                    model_value += 1
                with open(self.absolute_path + '/' + brand[0].title() + ".csv", "w", encoding='utf8')  as file:
                    dict_writer = csv.DictWriter(file, fieldnames=self.features)
                    dict_writer.writeheader()
                    str_phones_data = json.dumps(phones_data)
                    encoded = str_phones_data.encode('utf-8')
                    load_list = json.loads(encoded)
                    for dicti in load_list:
                        dict_writer.writerow({k: v for k, v in dicti.items()})
                print("Data loaded in the file")
            else:
                print(brand[0].title() + '.csv file already in your directory.')
                if (brand == phone_brand[-1]):
                    print('Crawling Data finished. Stored in the Dataset Folder. \n')
                    exit()

i = 1

def output_csv():
    try:
        while i == 1:
            if __name__ == "__main__":
                obj = Gsmarena()
                obj.save_specification_to_file()
    except KeyboardInterrupt:
        print("File has been stopped due to KeyBoard Interruption.")

output_csv()