#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the MongoClient class
from pymongo import MongoClient
# from Convert import ConvertirEnviar
# import the Pandas library
import pandas

# these libraries are optional
import json
import time

#VARIABLES
# IP = "10.3.3.122"
# PORT = 27017
# ADMIN = ''
# PASSWORD = ''

IP = "192.168.44.72"
PORT = 27017
ADMIN = 'admin'
PASSWORD = 'password'

nombre_del_reporte = "central"

# build a new client instance of MongoClient
# mongo_client = MongoClient('192.168.44.72', 27017, username="admin", password="password")
mongo_client = MongoClient(IP, PORT, username=ADMIN, password=PASSWORD)

db = mongo_client.landing
col = db.reprogramacion_update

# db = mongo_client.testmongoNew
# col = db.repro2

# start time of script
start_time = time.time()

# make an API call to the MongoDB server
cursor = col.find()

# extract the list of documents from cursor obj
mongo_docs = list(cursor)

# restrict the number of docs to export
mongo_docs = mongo_docs[:]  # slice the list
print("total docs:", len(mongo_docs))

# create an empty DataFrame for storing documents
docs = pandas.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate(mongo_docs):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]

    # create a Series obj from the MongoDB dict
    series_obj = pandas.Series(doc, name=doc_id)

    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)

    # only print every 10th document
    if num % 10 == 0:
        print(type(doc))
        print(type(doc["_id"]))
        print(num, "--", doc, "\n")

"""
EXPORTAR LOS DOCUMENTOS DEL MONGODB
EN DIFERENTES FORMATOS
"""
# print("\nexporting Pandas objects to different file types.")
print("\nCantidad de DataFrame (len):", len(docs))

# export the MongoDB documents as a JSON file
docs.to_json("{}.json".format(nombre_del_reporte))

# have Pandas return a JSON string of the documents
json_export = docs.to_json()  # return JSON data
print("\nJSON data:", json_export)

# export MongoDB documents to a CSV file
docs.to_csv("{}.csv".format(nombre_del_reporte), ",")  # CSV delimited by commas

# export MongoDB documents to CSV
csv_export = docs.to_csv(sep=",")  # CSV delimited by commas
print("\nCSV data:", csv_export)

# create IO HTML string
import io

html_str = io.StringIO()

# export as HTML
docs.to_html(
    buf=html_str,
    classes='table table-striped'
)

# print out the HTML table
print(html_str.getvalue())

# save the MongoDB documents as an HTML table
docs.to_html("{}.html".format(nombre_del_reporte))

print("\n\ntime elapsed:", time.time() - start_time)

import os
import glob
import csv
import xlwt  # from http://www.python-excel.org/
from config import *

# ifile  = open('sample.csv', "rt", encoding=<theencodingofthefile>)

def ConvertirEnviar(name):
    try:
        print('{}.csv'.format(name))
        for csvfile in glob.glob(os.path.join('.', '{}.csv'.format(name))):
            print("csvfile", csvfile)
            wb = xlwt.Workbook()
            ws = wb.add_sheet('data')
            with open(csvfile, 'rt', encoding="utf8") as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    # print(row)
                    for c, val in enumerate(row):
                        ws.write(r, c, val)
            wb.save(csvfile + '.xls')
            os.remove(csvfile)
        return True
    except:
        return False


ConvertirEnviar("{}".format(nombre_del_reporte))
