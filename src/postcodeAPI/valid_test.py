#!/usr/bin/env python
# -*- coding: utf-8 -*-

ADDRNAME = ['city', 'district', 'village', 'neighborhood','road', 'street', 'section', 'lane', 'alley', 'housenumber']
ADDRSUFFIX = [u'市', u'區', u'里', u'鄰', u'路', u'街', u'段', u'巷', u'弄', u'號']

addr_order = {'city': 0,
              'district': 1,
              'village': 2,
              'neighborhood': 3,
              'road': 4,
              'street': 5,
              'section': 6,
              'lane': 7,
              'alley': 8,
              'housenumber': 9}


# This dictionary is used to add name to the terms which only have the values.
addr_value_name = {'neighborhood': u'鄰',
                   'section': u'段',
                   'lane': u'巷',
                   'alley': u'弄',
                   'housenumber': u'號'}



def valid(addr_term):
  """Return True if the term has the information corresponding to itself only"""
  key, val = addr_term.items()[0]
  if key in addr_value_name:
    try:
      int(val)
      return True
    except ValueError:
      return False
  else:
    check_len = True
    if key == 'city' or key == 'district':
      check_len = (len(val) == 3)
    return val.endswith(ADDRSUFFIX[ADDRNAME.index(key)]) and check_len





