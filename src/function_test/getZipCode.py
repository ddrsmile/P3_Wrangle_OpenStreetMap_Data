#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
import pprint
import codecs
import xml.etree.cElementTree as ET
from  urllib import quote, unquote
from valid_test import valid

BASE_URL = "http://zip5.5432.tw/zip5json.py?adrs="
FILE = "examples.osm"

def getAddr(osmfile):
  f = open(osmfile, 'r')
  parsed = ET.iterparse(f, events=('start',))
  
  addrClass = {'lane':u'巷','housenumber': u'號'}
  addrOrder = {'city':0, 'district': 1, 'street':2, 'lane':3, 'housenumber':4}
  addr = ['']*5
  getposcode = False
  for event, elem in parsed:
    if elem.tag == 'node' or elem.tag == 'way':
      for tag in elem.iter('tag'):
        print tag.attrib['k'], ':', tag.attrib['v']
        if ':' not in tag.attrib['k']:
          continue
        addrtag = tag.attrib['k'].strip().split(':')[1]
        if addrtag == 'postcode':
          if len(tag.attrib['v']) == 3:
            getpostcode = True
          continue

        if addrtag in addrClass:
          addr[addrOrder[addrtag]] = tag.attrib['v'] + addrClass[addrtag]
        else:
          addr[addrOrder[addrtag]] = tag.attrib['v']
        aa = {addrtag:tag.attrib['v']}
        print aa
        print valid(aa)

  print ''.join(addr)
  return getpostcode, ''.join(addr)

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
  getpostcode, addr = getAddr(FILE)
  print getpostcode
  print addr
  if getpostcode:
    addrurl = quote(addr.encode('utf8'))
    result = query_site(addrurl) 
    zipcode = ''
    addr = ''
    if isinstance(result, dict):
      zipcode = result['zipcode']
      addr = u'{0}'.format(result['new_adrs2'])

  print('zipcode: %s' % zipcode)
  print('address: %s' % addr)

if __name__ == '__main__':
  main()
