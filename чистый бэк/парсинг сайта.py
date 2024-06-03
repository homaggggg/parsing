import sqlite3
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import pymongo
import pprint

def CreateDocDB(doc):
    print('-подгрузка в бд-', doc)
    x = collection.insert_one(doc)

def readDB():
    printer = pprint.PrettyPrinter()
    find_all = collection.find()
    for i in find_all:
        printer.pprint(i)

def DeleteAllDocsDB():
    collection.drop()

def DeleteDocDB(doc):
    collection.delete_one(doc)
    documents = collection.find()
    for x in documents:
        print(x)    

def UpdateDB(doc, newDoc):
    collection.update_one(doc, newDoc)
    documents = collection.find()
    for x in documents:
        print(x)

client = pymongo.MongoClient("localhost", 27017)
db = client.Sites
collection = db.News

conn = sqlite3.connect("ietr.db")
cursor = conn.cursor()


url = 'https://www.defenseadvancement.com/news/section/technology/'
page = requests.get(url)
print(page.status_code)

soup = BeautifulSoup(page.text, "html.parser")
news = soup.findAll(class_='product-card full-bkg category')

# print("----------------------news-------------------------")
name_news = []
link_news = []
date_news = []
text_news = []

for i in range(len(news)):
    if news[i].find(class_='news-card-heading') is not None:
        new = news[i].text.split('\n')
        if i == 0:
            new.pop(0)
            new.pop(7)

        link = news[i].find('a').get('href')
        newurl = link
        newpage = requests.get(newurl)
        newpage.encoding = 'utf8'
        news_inlink = soup.findAll('div', class_='container')

        name_news.append(new[5])
        date_news.append(new[9])
        link_news.append(link)
        text_news.append('')

# createDB()


# print("----------------------news-------------------------")
for i in range(len(link_news)):
    data = []
    data = {"title" : name_news[i], "date": date_news[i], "link": link_news[i]}
    CreateDocDB(data)
    # print('------------------------------------------------------')

readDB()