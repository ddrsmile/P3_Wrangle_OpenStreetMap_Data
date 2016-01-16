#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mapparser.py
# Nan-Tsou Liu

"""
Uses to invstigate how many of each tag there are.
Print the dictionary with tag name as keys and the number of times as the value.
"""

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
  tags = {}
  parsed = ET.iterparse(filename)
  
  for _, elem in parsed:
    if elem.tag in tags:
      tags[elem.tag] += 1
    else:
      tags[elem.tag] = 1

    elem.clear()
  del parsed
  return tags

def test():
    FILE = r'../data/inputFile/taipei_city_taiwan.osm'
    tags = count_tags(FILE)
    pprint.pprint(tags)

if __name__ == '__main__':
  test()
