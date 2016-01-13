#!usr/bin/env python
# -*- coding: utf-8 -*-

# shape_addr.py
# Nan-Tsou Liu

"""
- shape the address dictionary in expecting structure as follows:
  'address': {'city':         'city name',
              'district':     'district name',
              'village':      'village name',
              'neighborhood': 'neighborhood value',
              'road':         'road name',
              'street':       'street name',
              'lane':         'lane value',
              'alley':        'alley value',
              'housenumber':  'housenumber value',
              'floor':        'floor value',
              'housename':    'house name',
              'postcode':     'postcode value (5 digits)'
- 'city', 'distrit', 'road'/'street', 'housenumber' are necessary to get the postal code from API.
"""

import re
import get_postcode_API #Local python file

pattern = re.compile(ur'..市..區(.+里)?(.+鄰)?(.+路(.+段)?|.+街)(.+巷)?(.+弄)?(\d+號)', re.UNICODE)

# floor and house name is not necessary to get the post code.
ADDR_NAME = ['city', 'district', 'village', 'neighborhood','road', 'section', 'street', 'lane', 'alley', 'housenumber', 'floor']
ADDR_SUFFIX = [u'市', u'區', u'里', u'鄰', u'路', u'段', u'街', u'巷', u'弄', u'號', u'樓']
ADDR_VALUE_NAME = ['village', 'section', 'lane', 'alley', 'housenumber', 'floor']
ADDR_VALUE_SUFFIX = [u'鄰', u'段', u'巷', u'弄', u'號', u'樓']

def isInt(val):
  """Return True if val is in Integer format"""
  try:
    int(val)
    return True
  except ValueError:
    return False

def get_index(full_addr):
  """Return the index array of each term in a address string"""
  index_dict={}
  for name in ADDR_SUFFIX:
    if name in full_addr:
      index_dict[name] = full_addr.index(name)
  index_arr = [x[0] for x in sorted(index_dict.items(), key=lambda x: x[1])]
  return index_arr 

def get_postcode(address):
  """Return postcode with 5 digits if exists. Otherwise return None"""
  postcode = ''
  if 'postcode' in address:
    if len(address['postcode']) == 5:
      postcode = address['postcode']
    else:
      postcode = None
    del address['postcode']

  if not postcode and 'full' in address:
    if isInt(address['full'][:5]):
      postcode = address['full'][:5]
    else:
      postcode = None

  return postcode

def split_addr(full_addr):
  """Return the dictionary content information in the given str."""
  address = {}
  full_addr = full_addr.replace(' ', '')
  index_arr = get_index(full_addr)
  for name in index_arr:
    tmp, full_addr = full_addr.split(name, 1)
    if not name in ADDR_VALUE_SUFFIX:
      # the info of name not in ADDR_VALUE_NAME containss chinese characters only.
      address[ADDR_NAME[ADDR_SUFFIX.index(name)]] = re.sub(ur'\d', '', tmp) + name
    else:
      # On the other hand, it contains integer digits only except the one of section (u'段').
      address[ADDR_NAME[ADDR_SUFFIX.index(name)]] = tmp
  if full_addr and 'floor' not in address:
    # The floor info of basement 1 doesn't content u'樓', so it should be treated separately.
    m=re.search(ur'B/d+', full_addr, re.IGNORECASE | re.UNICODE)
    if m:
      address['floor'] = m.group()

  return address

def unite_addr(address):
  full_addr = ''
  for name in ADDR_NAME:
    if name in address and address[name]:
      if not name in ADDR_VALUE_NAME:
        full_addr += address[name]
      else:
        full_addr += address[name] + ADDR_VALUE_SUFFIX[ADDR_VALUE_NAME.index(name)]
  return full_addr

def shape(addr_dict):
  """Return the shaped address dictionary"""
  address = {}
  postcode = get_postcode(addr_dict)
  if postcode:
    address['postcode'] = postcode

  if 'full' in addr_dict:
    full_addr = addr_dict['full']
    address.update(split_addr(full_addr))
  else:
    if 'city' in addr_dict:
      if re.match( u'..市$', addr_dict['city'], re.UNICODE):
        address['city'] = addr_dict['city']
      elif re.match( u'..市..區$', addr_dict['city'], re.UNICODE):
        address['city'] = addr_dict['city'][:3]
        address['district'] = addr_dict['city'][3:]
      elif re.match( u'..區$', addr_dict['city'], re.UNICODE):
        address['district'] = addr_dict['city']
      else:
        address['city'] = None
      del addr_dict['city']

    if 'district' in addr_dict and 'dictrict' not in address:
      if re.match( u'..區$', addr_dict['district'], re.UNICODE):
        address['district'] = addr_dict['district']
      else:
        address['district'] = None
      del addr_dict['district']
    # The info of lane and alley is contained in that of road or street originally.
    # Basically, the address dictionary contains either road or street.
    if 'road' in addr_dict:
      full_addr = addr_dict['road']
      address.update(split_addr(full_addr))
      del addr_dict['road']
    if 'street' in addr_dict:
      full_addr = addr_dict['street']
      address.update(split_addr(full_addr))
      del addr_dict['street']
    address.update(addr_dict)

  if 'postcode' not in address:
    full_addr = unite_addr(address)
    if pattern.match(full_addr):
      postcode = get_postcode_API.get_postcode(full_addr)
      if postcode:
        address['postcode'] = postcode


  return address

def test():
  addr1 = {'postcode': '106',
               'city': u'臺北市大安區',
               'road': u'羅斯福路四段',
               'housenumber': '1'
               }

  addr2 = {'postcode':'106',
                'full':u'臺北市大同區長安西路226號1-4樓'}

  addr3 = {
           'city' : u'大安區',
           'street' : u'長興街24巷3弄',
           'housenumber' : '3',
          'housename' : u'台大宿舍'}
  address = shape(addr2)
  for k, v in address.items():
    print k, ':', v
  print unite_addr(address)

if __name__ == '__main__':
  test()
