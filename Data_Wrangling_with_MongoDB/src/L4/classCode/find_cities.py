from datetime import datetime

def rane_query():
  query = {'foundingDate' : {'$gte': datetime(2001,1,1), '$lt':datetime(2101,1,1)}}
  return query

def get_db():
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client.examples
  return db

if __name__ == '__main__':
  db = get_db()
  query = range_query()
  cities = db.cities.find(query)

  print "Found cities", cities.count()
  import pprint
  pprint.pprint(cities[0])
