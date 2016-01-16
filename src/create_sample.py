#!/usr/bin/env python
# -*- coding: utf-8 -*-

# create_sample.py
# Nan-Tsou Liu

"""
- extract the data from original OSM file to make the sample osm file.
  This code is written by consulting the code on the lession.
"""

import xml.etree.cElementTree as ET
OSM_FILE = r'../data/inputFile/taipei_city_taiwan.osm'
SAMPLE_FILE = r'../data/inputFile/sample.osm'

def get_element(osm_file, tags=('node', 'way', 'relation')):
  """Return the information of an element by yield"""
  context = ET.iterparse(osm_file, events=('start', 'end'))
  _, root = next(context)
  for event, elem in context:
    if event == 'end' and elem.tag in tags:
      yield elem
      root.clear()

with open(SAMPLE_FILE, 'w') as output:
  output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  output.write('<osm>\n')

  # Write every 10th top level element
  for i, element in enumerate(get_element(OSM_FILE)):
    if i%10 == 0:
      # chinese characters exist therefore encoding is set to utf-8
      output.write(ET.tostring(element, encoding='utf-8'))

  output.write('</osm>')
