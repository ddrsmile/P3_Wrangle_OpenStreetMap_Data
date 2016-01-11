#! /usr/bin/env python
# -*- encoding:utf-8 -*-
import json
import requests
import pprint
import codecs
from  urllib import quote, unquote

BASE_URL = "http://zip5.5432.tw/zip5json.py?adrs="
FILE = "examples.txt"

def getAddr(fileName):
  with codecs.open(fileName, 'r', encoding='utf8') as f:
    text = f.read()
    return text.strip()

def query_site(addr):
  # This is the main function for making queries to the musicbrainz API.
  # A json document should be returned by the query.
  r = requests.get(BASE_URL+addr)

  if r.status_code == requests.codes.ok:
    return r.json()
  else:
    r.raise_for_status()

def customisedPrint(data):
  if type(data) == dict:
    for k, v in data.items():
      print u'{0}:{1}'.format(k,v)

def main():
  addr = getAddr(FILE)
  addrurl = quote(addr.encode('utf8'))
  result = query_site(addrurl) 
  zipcode = ''
  addr = ''
  if type(result) == dict:
    zipcode = result['zipcode']
    addr = u'{0}'.format(result['new_adrs2'])

    print('zipcode: %s' % zipcode)
    print('address: %s' % addr)
  

if __name__ == '__main__':
  main()
