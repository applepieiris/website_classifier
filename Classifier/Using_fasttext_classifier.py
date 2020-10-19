import fasttext as ft
from os import path
import json

def pre_process(JsonName):
    f = open(JsonName,'r',encoding='utf-8')
    data = json.load(f)
    train = open('training.txt','a',encoding='utf-8')
    print(len(data.keys()))
    for key,value in data.items():
        for item in value:
            label = '__label__'+ key + ' '
            line = ','.join((label,' ' + item.replace('\"','')))
            train.write(line + '\n')

def classify(filename):
    classifier = ft.train_supervised(filename,label_prefix='__label__')
    texts = ['coupons, cash back, rakuten, promo codes, online rebates, discounts, deals, coupon codes','Sky, Sky TV, Sky Broadband, Sky Fibre, Sky Mobile, Sky Entertainment, Sky Sports, Sky Cinema']
    labels = classifier.predict(texts)
    print(labels)

classify('training.txt')
