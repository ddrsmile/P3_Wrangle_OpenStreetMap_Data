def porsche_query():
  query = {'manufacturer':'Porsche'}
  return query

def get_db(db_name):
  from pymongo import MongoClient
  client = MongoClient('localhost:27017')
  db = client[db_name]
  return db

def find_porsche(db, query):
  return db.autos.find(query)

if __name__ == '__main__':
  db = get_db('examples')
  query = porsche_query()
  results = find_porshce(db, query)

  print 'Printing first 3 results\n'
  import pprint
  for car in results[:3]:
    pprint.pprint(car)
