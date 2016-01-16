#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tag.py
# Nan-Tsou Liu

"""
Use to check whether the tag k's value is valid or potentially problem.
"""

import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_|-)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
  if element.tag == 'tag':
    if lower.search(element.attrib['k']):
      keys['lower'] += 1
    elif lower_colon.search(element.attrib['k']):
      keys['lower_colon'] += 1
    elif problemchars.search(element.attrib['k']):
      print element.attrib['k'], element.attrib['v']
      keys['problemchars'] += 1
    else:
      keys['other'] += 1
  
  return keys

def process_map(filename):
  keys = {'lower': 0, 'lower_colon': 0, 'problemchars': 0, 'other': 0}
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
