#!/usr/bin/env python
# -*- coding: utf-8 -*-

def isInt(val):
  try:
    int(val)
    return True
  except ValueError:
    return False

def get_postcode(address):
  """Return postcode with 5 digits if exists. Otherwise return None"""
  postcode = ''
  if 'postcode' in address:
    if len(address['postcode']) == 5:
      postcode = address['postcode']
    else:
      postcode = None
  
  if not postcode and 'full' in address:
    if isInt(address['full'][:5]):
      postcode = address['full'][:5]
    else:
      postcode = None
  
    return postcode


address = {'full': u'106臺北市大安區羅斯福路四段1號',
           'postcode':u'106'
           }

print get_postcode(address)
