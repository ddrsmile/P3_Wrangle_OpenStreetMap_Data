#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
#import audit #local python file, used to make the value consistent

#OSM_FILE = r'../data/inputFIle/sample.osm'
#JSON_FILE = r'../data/outputFile/sample.json'

OSM_FILE = r'../data/inputFIle/taipei_taiwan.osm'
JSON_FILE = r'../data/outputFile/taipei_taiwan.json'

wer = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
lower_two_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def get_pos(elem):
  '''return the latitude and longitude of the elem'''
  lat = float(elem.attrib['lat'])
  lon = float(elem.attrib['lon'])
  return [lat, lon]

def ignoring(k):
  """Return true if k should be ignored"""
  IGNORESTR = ['wikipedia', 'source', 'old_name','int_name', 'alt_name']
  IGNOREPRE1 = ['name:', 'is_in']
  IGNOREPRE2 = ['old_name:']
  if k in IGNORESTR:
    return True
  return False

def shape_element(elem):
  node = {}
  if elem.tag == 'node' or elem.tag == 'way':
    node['type'] = elem.tag
    
    for a in elem.attrib:
      if a in CREATED:
        if 'created' not in node:
          node['created'] = {}
        node['created'][a] = elem.attrib[a]
      elif a in ['lat', 'lon']:
        if 'pos' not in node:
          node['pos'] = [None, None]

        if a == 'lat':
          node['pos'][0] = float(elem.attrib[a])
        else:
          node['pos'][1] = float(elem.attrib[a])
      else:
        node[a] = elem.attrib[a]

    for tag in elem.iter('tag'):
      if not problemchars.search(tag.attrib['k']):
        if lower_colon.search(tag.attrib['k']):
          if tag.attrib['k'].find('addr') == 0:
            if 'address' not in node:
              node['address'] = {}
            sub_attr = tag.attrib['k'].split(':', 1)
            node['address'][sub_attr[1]] = tag.attrib['v']
          else:
            node[tag.attrib['k']] = tag.attrib['v']
        elif tag.attrib['k'].find(':') == -1:
          node[tag.attrib['k']] = tag.attrib['v']
    
    for nd in elem.iter('nd'):
      if 'node_refs' not in node:
        node['node_refs'] = []
      node['node_refs'].append(nd.attrib['ref'])

    return node
  else:
    return None

def process_map(file_in, pretty = False):
  file_out = JSON_FILE
  # data = []
  with codecs.open(file_out, 'w') as fo:
    for _, elem in ET.iterparse(file_in):
      print type(elem)
      el = shape_element(elem)
      if el:
        # data.append(el)
        if pretty:
          fo.write(json.dumps(el, indent = 2, ensure_ascii=False).encode("utf-8") + '\n')
        else:
          fo.write(json.dumps(el, ensure_ascii=False).encode("utf-8") + '\n')
  # return data

class MyPrettyPrinter(pprint.PrettyPrinter):
  def format(self, object, context,  maxlevels, level):
    if isinstance(object, unicode):
      return (object.encode('utf8'), True, False)
    return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def test():
  # data = process_map('../data/inputFile/taipei_taiwan.osm', True)
  process_map(OSM_FILE, True)  

if __name__ == '__main__':
  test()
