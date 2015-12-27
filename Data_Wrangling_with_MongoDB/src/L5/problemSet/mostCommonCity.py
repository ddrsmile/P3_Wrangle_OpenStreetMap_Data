#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_db(db_name):
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

def make_pipeline():
  pipeline = [{'$match': {'name': {'$exists': 1}}},
              {'$group': {'_id': '$name', 'count': {'$sum': 1}}},
              {'$sort': {'count': -1}},
              {'$limit': 1}]
  return pipeline

def aggregate(db, pipeline):
  return [doc for doc in db.cities.aggregate(pipeline)]

if __name__ == '__main__':
  db = get_db('examples')
  pipeline = make_pipeline()
  result = aggregate(db, pipeline)
  import pprint
  pprint.pprint(result[0])

