#!/usr/bin/env python
# -*- coding: utf-8 -*-

# audit.py
# Nan-Tsou Liu

"""
- Audit the city name only.
  it will make the city name into u'臺北市' and u'新北市' if the non expecting word which
  represent '臺北市' or '新北市'.
"""

mapping = {u'台北市': u'臺北市',
           u'台灣台北市': u'臺北市',
           u'Taipei': u'臺北市',
           u'Taipei City': u'臺北市',
           u'台北市(Taipei City)': u'臺北市',
           u'Taipai': u'臺北市',
           u'台北': u'臺北市',
           u'臺北': u'臺北市',
           u'台灣新北市': u'新北市'}

def update(name, mapping):
  """
  Return the updated city name
  Implement in data_updated.py
  """
  if name in mapping:
    name = mapping[name]

  return name
