#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re

def process_map(filename):
  users = set()
  parsed = ET.iterparse(filename)
  for _, element in parsed:
    if 'uid' in element.attrib:
      users.add(element.attrib['uid'])
    element.clear()
  del parsed
  return users

def main():
  FILE = r'../data/inputFile/taipei_taiwan.osm'

  users = process_map(FILE)
  pprint.pprint(len(users))

if __name__ == '__main__':
  main()
