#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_db(db_name):
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

def make_pipeline():
  pipeline = [{'$match': {'user.time_zone': 'Brasilia',
                          'user.statuses_count': {'$gte': 100}},
              {'$project': {'followers': '$user.followers_count',
                            'screen_name': '$user.screen_name',
                            'tweets': '$user.statuses_count'}},
              {'$sort': {'followers': -1}},
              {'$limit': 1}]

  return pipeline

def tweet_source(db, pipeline):
  return [doc for doc in db.tweets.aggregate(pipeline)]

if __name__ == '__main__':
  db = get_db('twitter')
  pipeline = make_pipeline()
  result = tweet_sources(db, pipeline)
  import pprint
  pprint.pprint(result[0])
