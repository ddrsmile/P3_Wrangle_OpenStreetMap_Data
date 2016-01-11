#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

pattern = re.compile(ur'..市..區(.+里)?(.+鄰)?(.+路(.+段)?|.+街)(.+巷)?(.+弄)?(\d+號)', re.UNICODE)
m = pattern.match(u'台中市東勢區延平里4鄰豐勢路104巷35號')



a = u'B1asdjfhajkl'
m = re.search(ur'B[0-9]+', a, re.IGNORECASE| re.UNICODE)

if m:
  print m.group()
else:
  print None
