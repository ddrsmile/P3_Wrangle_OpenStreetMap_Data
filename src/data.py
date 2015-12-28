#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


wer = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

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
  file_out = '{0}.json'.format(file_in)
  data = []
  with codecs.open(file_out, 'w') as fo:
    for _, elem in ET.iterparse(file_in):
      el = shape_element(elem)
      if el:
        data.append(el)
        if pretty:
          fo.write(json.dumps(el, indent = 2) + '\n')
        else:
          fo.write(json.dumps(el) + '\n')
  return data

def test():
  data = process_map('example.osm' True)
  pprint.pprint(data)

if __name__ == '__main__':
  test()
