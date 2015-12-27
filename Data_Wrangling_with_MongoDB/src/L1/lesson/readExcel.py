#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import os
from zipfile import ZipFile
dataFile = "2013_ERCOT_Hourly_Load_Data.xls"

def open_zip(dataFile):
  with ZipFile('{0}.zip'.format(dataFile), 'r') as zipTarget:
    zipTarget.extractall()

def parse_file(dataFile):
  workbook = xlrd.open_workbook(dataFile)
  sheet = workbook.sheet_by_index(0)

  data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

  cv = sheet.col_values(1, start_rowx = 1, end_rowx = None)
  maxval = max(cv)
  minval = min(cv)
  maxpos = cv.index(maxval) + 1
  minpos = cv.index(minval) + 1

  maxvalue = sheet.cell_value(maxpos, 0)
  maxtime = xlrd.xldate_as_tuple(maxvalue, 0)
  minvalue = sheet.cell_value(minpos, 0)
  mintime = xlrd.xldate_as_tuple(minvalue, 0)
  avgcoast = sum(cv)/float(len(cv))

  data = {
        'maxtime':  maxtime,
        'maxvalue': maxval,
        'mintime':  mintime,
        'minvalue': minval,
        'avgcoast': avgcoast
      }
  return data


open_zip(dataFile)
data = parse_file(dataFile)
os.remove(dataFile)
print data
