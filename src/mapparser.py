#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
  tag = {}
  for event, elem in ET.iterparse(filename):
    if elem.tag in tag:
      tag[elem.tag] += 1
    else:
      tag[elem.tag] = 1
  return tag

