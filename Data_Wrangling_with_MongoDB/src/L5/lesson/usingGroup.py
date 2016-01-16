#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_db(db_name):
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

def make_pipeline():
  pipeleine = [{'$group': {'_id': '$source', 'count': {'$sum': 1}}},
               {'$sort': {'count': -1}}]
  return pipeline

def tweet_source(db, pipeline):
  return [doc for doc in db.tweets.aggregate(pipeline)]

if __name__ == '__main__':
  db = get_db('twitter')
  pipeline = make_pipeline()
  result = tweet_sources(db, pipeline)
  import pprint
  pprint.pprint(result[0])
