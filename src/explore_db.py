#!/usr/bin/env python
# -*- coding: utf-8 -*-

# explore_db.py
# Nan-Tsou Liu

"""
Use to get the information from MongoDB with expecting conditions.
pprint's pretty printer class is modified to be capable of showing chinese characters in utf-8 format.
"""

def get_db(db_name):
  """Return the conntected db"""
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

def make_pipeline():
  """Return the well-defined pipline statement."""
  pipeline = [{'$match': {'shop':{'$exists':1}, 'shop':'convenience'}}, 
              {'$group': {'_id': {'city':'$address.city'}, 'count':{'$sum':1}}},
              {'$project': {'_id':0,'city':'$_id.city', 'count': '$count'}},
              {'$sort': {'count':-1}}, 
              ]  

 
  '''
pipeline = [{'$match': {'amenity':{'$exists':1}, 'amenity':'fast_food'}},
              {'$group': {'_id': {'name':'$name'}, 'count':{'$sum':1}}},
              {'$project': {'_id':0,'name':'$_id.name', 'count': '$count'}},
              {'$sort': {'count':-1}},
              {'$limit':5}]

  pipeline = [{'$match': {'amenity': {'$exists':1}}}, 
              {'$group': {'_id': {'amenity': '$amenity'}, 'count':{'$sum':1}}},
              {'$project': {'_id':0, 'amenity': '$_id.amenity', 'count': '$count'}},
              {'$sort': {'count':-1}}, 
              {'$limit':5}]

  pipeline = [{'$match': {'amenity':{'$exists':1}, 'cuisine': {'$exists':1}}}, 
              {'$group': {'_id': {'cuisine': '$cuisine'}, 'count':{'$sum':1}}},
              {'$project': {'_id':0,'cuisine':'$_id.cuisine', 'count': '$count'}},
              {'$sort': {'count':-1}}, 
              {'$limit':5}]

  pipeline = [{'$match': {'created.user':{'$exists':1},
                          'address.postcode':{'$exists':1}}},
              {'$group': {'_id':{'user':'$created.user'},
                                 'count':{'$sum':1}}},
              {'$project':{'_id':0, 'User':'$_id.user', 'count':'$count'}},
              {'$sort':{'count':-1}},
              {'$limit':5}]
  
  

  pipeline = [{'$match': {'address.district':{'$exists':1},
                          'amenity': {'$exists':1},
                          'amenity':'place_of_worship'}},
              {'$group': {'_id':{'city':'$address.city','district':'$address.district'},
                          'count': {'$sum':1}}},
              {'$project': {'_id':0,'City':'$_id.city', 'District':'$_id.district', 'count':'$count'}},
              {'$sort': {'count': -1}},
              ]
  '''
  return pipeline

def get_info(db, pipeline):
  """Extract the information based on pipeline from MongoDB and return the result."""
  return [doc for doc in db.api.aggregate(pipeline)]

def show_data():
  """Print the extract result"""
  db = get_db('mydb')
  pipeline = make_pipeline()
  result = get_info(db, pipeline)
  import pprint
  # modified the pretty printer to show chinese character.
  class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
      if isinstance(object, unicode):
        return (object.encode('utf8'), True, False)
      return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
  
  MyPrettyPrinter().pprint(result)

if __name__ == '__main__':
  show_data()
