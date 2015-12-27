#! /usr/bin/env python
# -*- coding: utf-8 -*-

def in_query():
  query = {"manufacturer": "Ford Motor Company",
           "assembly": {"$in": ["Germany", "United Kingdom", "Japan"]}}
  return query

def get_db():
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client.examples
  return db

if __name__ == '__main__':
  db = get_db()
  query = in_query()
  autos = db.autos.find(query, {"name": 1, "manufacturer":1, "assembly": 1, "_id": 0})

  print "Found autos", autos.count()
  import pprint
  for a in autos:
    pprint.pprint(a)
