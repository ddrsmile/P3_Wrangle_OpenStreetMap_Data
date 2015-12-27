#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import json
import pprint
import re

DATAFILE = "../data/dataSet/arachnid.csv"
FIELDS = {'rdf-schema#label' : 'label',
          'binomialAuthority_label': 'binomialAuthority'}

def add_field(filename, fields):
  process_fields = fields.keys()
  data = {}

  with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for i in range(3):
      l = reader.next()

    for line in reader:
      if line['binomialAuthority_label'] != 'NULL':
        # clean up the label
        label = re.sub('\(.*?\)', '', line['rdf-schema#label']).strip()
        value = line['binomialAuthority_label']
        data[label] = value
    return data

def update_db(data,db):
  labels = data.keys()
  for item in labels:
    db.arachnid.update({'label': item},
                       {'$set': {'classification.binomialAuthority': data[item]}})

def test():
  data = add_field(DATAFILE, FIELDS)
  from pymongo import MongoClient
  client = MongoClient("mongodb://localhost:27017")
  db = client.examples

  update_db(data,db)

  updated = db.arachnid.find_one({'label': 'Opisthoncana'})
  pprint.pprint(data)
if __name__ == '__main__':
  test()
