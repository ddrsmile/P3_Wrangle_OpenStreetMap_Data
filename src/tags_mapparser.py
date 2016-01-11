#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'\w*$')
lower_colon = re.compile(r'\w*(:\w*)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
  excludes = ['',
              'addr',
              'wheelchair',
              'via',
              'to',
              'start_date',
              'source',
              'ISO3166-1',
              'website',
              'web',
              'name', 
              'alt_name', 
              'abandoned', 
              'brand', 
              'building', 
              'disused',
              'is_in', 
              'note',
              'aerialway',
              'capacity',
              'construction',
              'contact',
              'description',
              'emergency',
              'internet_access',
              'offical_name',
              'official_name',
              'old_addr',
              'old_name',
              'payment',
              'ref',
              'roof',
              'restriction',
              'short_name',
              'GNS',
              'FIXME',
              'access',
              'activity',
              'ISO3166-2',
              'Note',
              '_description_',
              'address',
              'aeroway',
              'agricultural',
              'alcohol',
              'ally',
              'alt_name2',
              'alt_name1',
              'alt_name3',
              'amount',
              'animal',
              'aprox',
              'archway',
              'area',
              'artisit_name',
              'atm',
              'attribution',
              'baby_feeding',
              'backrest',
              'barrier',
              'bench',
              'bic',
              'bicycle',
              'bicycle_parking',
              'lood_donation',
              'board_type',
              'boat',
              'bollard',
              'books',
              'bottle',
              'bridge',
              'bridge_name',
              'brownfield',
              'builder',
              'bus',
              'button_operated',
              'by_night',
              'cables',
              'comment',
              'wikipedia',
              'branch']
  if element.tag == 'tag':
    # collect tag's k attribution
    prefix = ''
    if lower_colon.search(element.attrib['k']):
      prefix = element.attrib['k'].strip().split(':')[0]
    else:
      prefix = element.attrib['k']

    if not prefix in excludes:
      if element.attrib['k'] in keys:
        keys[element.attrib['k']].add(element.attrib['v'])
      else:
        keys[element.attrib['k']] = set()
        keys[element.attrib['k']].add(element.attrib['v'])
  return keys

def process_map(filename):
  keys = {}
  parsed = ET.iterparse(filename)
  for _, element in parsed:
    keys = key_type(element, keys)
    element.clear()

  del parsed
  return keys

def main():
  FILE = r'../data/inputFile/taipei_taiwan.osm'
  keys = process_map(FILE)
  pprint.pprint(keys)

if __name__ == '__main__':
  main()
