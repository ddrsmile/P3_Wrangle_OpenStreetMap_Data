#!/usr/bin/env python
# -*- coding: utf8 -*-

import re

FILE = r'examples.txt'
utfCheck = re.compile('[^\d]')
f = open(FILE, 'r')
msg = f.read().strip()

msgList = list(msg)
words = []
tmp = []
cnt = 0
for i in range(len(msgList)):
  if utfCheck.search(msgList[i]):
    tmp.append(msgList[i])
    cnt += 1
    if cnt == 3:
      word = ''.join(tmp)
      words.append(word)
      tmp = []
      cnt = 0
  else:
    words.append(msgList[i])

for word in words:
  print word,
