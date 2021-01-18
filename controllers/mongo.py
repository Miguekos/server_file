from pymongo import MongoClient
import os
import datetime
from bson.json_util import dumps
import logging
import uuid

client = MongoClient()
# logging.debug("Mongo Conectado a: {}".format(os.getenv("URL_MONGO")))
# mongo = MongoClient(os.getenv("URL_MONGO"))
# mongo = MongoClient("mongodb://127.0.0.1:27017")
# mongo = MongoClient("mongodb://admin:password@207.244.232.99:37018")
mongo = MongoClient(os.getenv("URL_MONGO"))
mydb = mongo["fileserver"]


class MongoConect(object):
    def __init__(self, arg):
        date = datetime.datetime.now()
        self.arg = arg
        self.namedb = "{}_{}_{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
        self.mycol = mydb["{}_{}".format("archivos", self.namedb)]

    def InsertarFile(self):
        # idregistro = "{}".format(uuid.uuid4())
        archivo = {
            **self.arg,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        self.mycol.insert_one(archivo)
        print("Seguardo correctamente")
        return True

    def BuscarFile(self):
        print("BuscarFile", self.arg)
        resultplaca = self.mycol.find_one({"idRegistro": self.arg})
        resp = resultplaca
        print("resp", resp)
        return resp
