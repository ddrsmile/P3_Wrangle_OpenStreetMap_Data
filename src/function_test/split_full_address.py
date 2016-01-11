#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import pprint


ADDRSUFFIX = [u'市', u'區', u'里', u'鄰', u'路', u'段', u'街', u'巷', u'弄', u'號', u'樓']
ADDRNAME = ['city', 'district', 'village', 'neighborhood','road', 'section', 'street', 'lane', 'alley', 'housenumber', 'floor']
ADDR_VALUE_NAME = [u'鄰', u'段', u'巷', u'弄', u'號', u'樓']
def get_index(s):
  index_dict = {}
  for name in ADDRSUFFIX:
    if name in s:
      index_dict[name] = s.index(name)
  index_arr = [x[0] for x in sorted(index_dict.items(), key=lambda x: x[1])]
  return index_arr

full_addr = ur'羅斯福路四段25巷3弄1號4-11樓台灣大學'
index_arr = get_index(full_addr)

address = {}
for name in index_arr:
  print name,
  tmp, full_addr = full_addr.split(name, 1)
  if not name in ADDR_VALUE_NAME:
    address[ADDRNAME[ADDRSUFFIX.index(name)]] = tmp + name
  else:
    address[ADDRNAME[ADDRSUFFIX.index(name)]] = tmp
if full_addr:
  address['housename'] = full_addr
print '\n'
for k, v in address.items():
  print k, v
