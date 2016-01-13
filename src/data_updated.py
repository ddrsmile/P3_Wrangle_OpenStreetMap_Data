#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data_updated.py
# Nan-Tsou Liu


import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit #local python file
import shape_addr #local python file

#OSM_FILE = r'../data/inputFIle/sample.osm'
#JSON_FILE = r'../data/outputFile/sample.json'

#OSM_FILE = r'../data/inputFIle/taipei_city_taiwan.osm'
#JSON_FILE = r'../data/outputFile/taipei_city_taiwan.json'

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

def ignoring(kval):
  """Return true if k should be ignored"""
  IGNORESTR = ['wikipedia', 'source', 'old_name','int_name', 'alt_name']
  IGNOREPRE1 = ['name:', 'is_in']
  IGNOREPRE2 = ['old_name:']
  if kval in IGNORESTR or kval[:5] in IGNOREPRE1 or kval[:9] in IGNOREPRE2:
    return True
  return False

def update_phone(val):
  """Return an array of phone number"""
  val = val.replace(' ','')
  vals = []
  # confrim the separator is comma or semi-colon.
  # if both characters are not detected, recognize val as a single phone number.
  if ';' not in val and u'、' not in val:
    vals = [val]
  else:
    if ';' in val:
      vals = val.split(';')
    elif u'、' in val:
      # check the comman separate the phone number or extension.
      # recognize it as the phone number if its length is larger or equal to 8.
      tmp = val.index(u'、')
      if len(val[(tmp+1):]) >= 8:
        vals = val.split(u'、')
      else:
        # to make vals is an array
        vals = [val]

  for i, v in enumerate(vals):
    extension = []
    tmp = None
    # check wether the phone number contains the extension code or not.
    if '#' not in v and u'轉' not in v:
      tmp = [v]
    else:
      if '#' in v:
        tmp = v.split('#')
      elif u'轉' in v:
        tmp = v.split(u'轉')
      # check wether the phone number contains more than 1 extension code.
      if u'、' in tmp[1]:
        extension = tmp[1].split(u'、')
      else:
        extension.append(tmp[1])
        
    #reset the tmp to the phone number for the following process.
    tmp = tmp[0]
    tmp = re.sub('\D', '', tmp)
    
    # cases like 8860212345678
    if len(tmp) == 13:
      vals[i] = '+' + tmp[:3] + '-' + tmp[4] + '-' + tmp[5:9] + '-' + tmp[9:]
    # cases like 886212345678 886937123456
    elif len(tmp) == 12:
      if tmp[3] == '2':
        vals[i] = '+' + tmp[:3] + '-' + tmp[3] + '-' + tmp[4:8] + '-' + tmp[8:]
      else:
        vals[i] = '+' + tmp[:3] + '-' + tmp[3:6] + '-' + tmp[6:9] + '-' + tmp[9:]
    # cases like 0212345678 0937123456
    elif len(tmp) == 10:
      if tmp[1] == 2:
        vals[i] = '+886' + '-' + tmp[1] + '-' + tmp[2:6] + '-' + tmp[6:]
      else:
        vals[i] = '+886' + '-' + tmp[1:4] + '-' + tmp[4:7] + '-' + tmp[7:]
    # cases like 1234-5678
    elif len(tmp) == 8:
      vals[i] = '+886' + '-2-' + tmp[0:4] + '-' + tmp[4:]
    
    if extension:
      for j, ext in enumerate(extension):
        # add the first extension code with #
        # use : as the separatorfrom the second extension code
        if j == 0:
          vals[i] += '#' + ext
        else:
          vals[i] += ':' + ext

  return vals

def update_node(node, kval, tag):
  """Adds 'k' and 'v' values from the tag as new key: value pair to node."""
  k = kval
  v = tag.attrib['v']
  if k.startswith('addr'):
    # Ignore addr with 2 colon
    if k.count(':') == 1:
      if 'address' not in node:
        node['address'] = {}
      sub_attr = k.split(':')[1]
      # if address:full exists, then the other information of address is skipped except postal code.
      if sub_attr not in ['postcode', 'full'] and 'full' in node['address']:
        return node
      else:
        # audit the value of city with function audit.update
        if sub_attr == 'city':
          v = audit.update(v, audit.mapping)

        # audit the value of district if the value has 2 character only
        # 大安=>大安區(Da'an => Da'an District)
        if sub_attr == 'district':
          if len(v) == 2:
            v = v + u'區'
        node['address'][sub_attr] = v
  # check for highway exit number nodes     
  elif k == 'ref' and node['type'] == 'node':
    node['exit_number'] = v
  
  elif k == 'phone':
    node['phone'] = update_phone(v)

  # check whether k's value is 'type' or not
  # if it is, change it to other_type to avoid overwritting node['type']
  elif k == 'type':
    node['other_type'] = v
  else:
    node[k] = v

  return node


def shape_element(elem):
  """
  Return cleaned and reshaped dictionary as JSON output.
  Reshape the address after necessary address information is collected.
  The information which is not concerned would be ignored.
  """
  node = {}
  if elem.tag == 'node' or elem.tag == 'way':
    node['type'] = elem.tag
    node['created'] = {}
    if 'lat' in elem.attrib:
      node['pos'] = get_pos(elem)

    # start iterating all the sub tags.
    for tag in elem.iter():
      for k, kval in tag.items():
        if k in CREATED:
          node['created'][k] = kval

        # check 2nd-level tag k's value
        elif k == 'k' and not re.search(problemchars, kval):
          if not ignoring(kval):
            node = update_node(node, kval, tag)

        # create/update 'node_refs'
        elif k == 'ref':
          if 'node_refs' not in node:
            node['node_refs'] = []
          node['node_refs'].append(kval)
        
        # remaining tags
        elif k not in ['k', 'lat', 'lon']:
          node[k] = kval

    elem.clear()
    if 'address' in node:
      #for k, v in node['address'].items():
        #print k, v
      node['address'] = shape_addr.shape(node['address'])
    return node
  else:
    return None

def process_map(file_in, pretty = False):
  """Output a JSON file or return the data as a list of dictionaries"""
  file_out = "{0}.json".format(file_in)
  # data = []
  with codecs.open(file_out, 'w') as fo:
    for _, elem in ET.iterparse(file_in):
      el = shape_element(elem)
      if el:
        # data.append(el)
        if pretty:
          fo.write(json.dumps(el, indent = 2, ensure_ascii=False).encode("utf-8") + '\n')
        else:
          fo.write(json.dumps(el, ensure_ascii=False).encode("utf-8") + '\n')
  # return data


def test():
  # data = process_map('../data/inputFile/taipei_taiwan.osm', True)
  #OSM_FILE = r'../data/inputFIle/sample.osm'

  OSM_FILE = r'../data/inputFIle/taipei_city_taiwan.osm'
  process_map(OSM_FILE, True)  

if __name__ == '__main__':
  test()
