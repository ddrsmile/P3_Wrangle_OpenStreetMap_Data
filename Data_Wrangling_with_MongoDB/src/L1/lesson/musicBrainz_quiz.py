#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.

query_type = {
    "simple" : {},
    "atr" : {"inc": "aliases+tags+ratings"},
    "aliases": {"inc": "aliases"},
    "releases": {"inc": "releases"}
    }

def query_site(url, params, uid="", fmt="json"):
  # This is the main function for making queries to the musicbrainz API.
  # A json document should be returned by the query.
  params["fmt"] = fmt
  r = requests.get(url + uid, params=params)
  print "requesting", r.url

  if r.status_code == requests.codes.ok:
    return r.json()
  else:
    r.raise_for_status()

def query_by_name(url, params, name):
  # This adds an artist name to the query parameters before making
  # an API call to the function above.
  params["query"] = "artist:" + name
  return query_site(url, params)

def pretty_print(data, indent=4):
  # After we get our output, we can format it to be more readable
  # by using this function
  if type(data) == dict:
    print json.dumps(data, indent=indent, sort_keys=True)
  else:
    print data


def main():
  '''
  Modify the function calls and indexing below to answer the question on
  the next quiz. HINT: Note how the output we get from the site is a 
  multi-level JSON document, so try making print statments to step through
  the structure one level at a time or copy the output to a separate output file.
  '''
  
  # question 1: how many bands named "FIRST AID KIT"
  target_name = "first aid kit"
  results = query_by_name(ARTIST_URL, query_type["simple"], target_name)
  cnt = 0
  for artist in results["artists"]:
    if artist["name"].lower() == target_name:
      cnt += 1
  print cnt

  #question 2: begin area name for Queen
  target_name = "queen"
  results = query_by_name(ARTIST_URL, query_type["simple"], target_name)
  for artist in results["artists"]:
    if artist["name"].lower() == target_name:
      try:
        print artist["begin-area"]["name"]
      except:
        None
  
  #question 3: spanish alias for beatles
  target_name = "the beatles"
  results = query_by_name(ARTIST_URL, query_type["simple"], target_name)
  for artist in results["artists"]:
    if artist["name"].lower() == target_name:
      for alias in artist["aliases"]:
        if alias["locale"] == "es":
          try:
            print alias["name"]
          except:
            None

  #question 4: Nirvana disambiguation
  target_name = "nirvana"
  results = query_by_name(ARTIST_URL, query_type["simple"], target_name)
  for artist in results["artists"]:
    if artist["name"].lower() == target_name:
      try:
        print artist["disambiguation"]
      except:
        None
  
  #question 5: when was one direction formed
  target_name = "one direction"
  results = query_by_name(ARTIST_URL, query_type["simple"], target_name)
  for artist in results["artists"]:
    if artist["name"].lower() == target_name:
      try:
        print artist["life-span"]["begin"]
      except:
        None

if __name__ == '__main__':
  main()
