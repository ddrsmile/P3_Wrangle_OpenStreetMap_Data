#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def update_phone(val):
  """Return an array of phone number"""
  val = val.replace(' ','')
  vals = []
  
  if ';' not in val and u'、' not in val:
    vals = [val]
  else:
    if ';' in val:
      vals = val.split(';')
    elif u'、' in val:
      tmp = val.index(u'、')
      if len(val[tmp + 1:]) >= 8:
        vals = val.split(u'、')
      else:
        vals = [val]
  
  print 'vals', vals
  for i, v in enumerate(vals):
    extension = []
    tmp = None 
    if '#' not in v and u'轉' not in v:
      tmp = [v]
    else:
      if '#' in v:
        tmp = v.split('#')
      elif u'轉' in v:
        tmp = v.split(u'轉')
      
      print 'tmp[1]', tmp[1]
      if u'、' in tmp[1]:
        extension = tmp[1].split(u'、')
      else:
        extension.append(tmp[1])
    print 'ext', extension
    # 
    tmp = tmp[0]  
    tmp = re.sub('\D', '', tmp)
    
    # 8860212345678
    if len(tmp) == 13:
      vals[i] = '+' + tmp[:3] + '-' + tmp[4] + '-' + tmp[5:9] + '-' + tmp[9:]
    # 886212345678 886937123456
    elif len(tmp) == 12:
      if tmp[3] == '2':
        vals[i] = '+' + tmp[:3] + '-' + tmp[3] + '-' + tmp[4:8] + '-' + tmp[8:]
      else:
        vals[i] = '+' + tmp[:3] + '-' + tmp[3:6] + '-' + tmp[6:9] + '-' + tmp[9:]
    # 0212345678 0937123456
    elif len(tmp) == 10:
      if tmp[1] == 2:
        vals[i] = '+886' + '-' + tmp[1] + '-' + tmp[2:6] + '-' + tmp[6:]
      else:
        vals[i] = '+886' + '-' + tmp[1:4] + '-' + tmp[4:7] + '-' + tmp[7:]
    elif len(tmp) == 8:
      vals[i] = '+886' + '-2-' + tmp[0:4] + '-' + tmp[4:]
    
    print 'vals', vals

    if extension:
      for j, ext in enumerate(extension):
        if j == 0:
          vals[i] += '#' + ext
        else:
          vals[i] += ':' + ext

  return vals


def test():
  
  val1 = '+886 2 1234 5678;02 12345678;+886-937123456;+886(02)12345678'
  val2 = u'2631-3507、0935-434-088'
  val3 = '+886-2 1234-5678#467'
  val4 = u'+886 4 2873-6548#101、107'
  val5 = u'+886-2-33169908轉0252'
  val6 = u'(02)2236-8225#63302、63304'
  val7 = '+886-2-5678-1234'
  print update_phone(val7)

if __name__ == '__main__':
  test()


