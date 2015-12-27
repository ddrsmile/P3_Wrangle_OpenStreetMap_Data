#!/usr/bin/env python
# -*- coding: utf-8 -*-

from autos import process_file
import os
from zipfile import ZipFile

def open_zip(dataFile):
  with ZipFile('{0}.zip'.format(dataFile), 'r') as zipTarget:
    zipTarget.extractall("../data/dataSet")

def insert_autos(infile, db):
  data = process_file(infile)
  db.autos.insert(data)

if __name__ == '__main__':
  from pymongo import MongoClient
  client = MongoClient("mongodb://localhost:27017")
  db = client.examples
  dataFile = "../data/dataSet/autos.csv"
  open_zip(dataFile)
  insert_autos(dataFile, db)
  os.remove(dataFile)
  print db.autos.find_one()
