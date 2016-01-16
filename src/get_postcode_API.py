#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get_postcode_API.py
# Nan-Tsou Liu

"""
- The given address is assumed to be valided for the API website, which match following regex format:
  ur'..市..區(.+里)?(.+鄰)?(.+路(.+段)?|.+街)(.+巷)?(.+弄)?(\d+號)'
- The return is the postal code only.
"""

import json
import requests
import time
from  urllib import quote, unquote


BASE_URL = "http://zip5.5432.tw/zip5json.py?adrs="

def query_site(addr):
  """Return a json document (dictionary) if API work normally."""
  r = requests.get(BASE_URL+addr)

  if r.status_code == requests.codes.ok:
    return r.json()
  else:
    r.raise_for_status()

def get_postcode(full_addr):
  """Return the postal code if exists. Otherwise, return None."""
  
  # to avoid sending large amount requests in a short time
  time.sleep(2)
  # convert utf-8 string into urlencoding string
  addrurl = quote(full_addr.encode('utf8'))
  result = query_site(addrurl)
  postcode = ''
  if isinstance(result, dict):
    if 'zipcode' in result:
      postcode = result['zipcode']
    else:
      postcode = None
  else:
    postcode = None
  return postcode

def test():
  full_addr = u'臺北市大安區羅斯福路四段1號'

  print get_postcode(full_addr)

if __name__ == '__main__':
  test()
