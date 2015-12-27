#!/usr/bin/env python

import csv
import os

DATADIR = ""
DATAFILE = "745090.csv"

def parse_file(dataFile):
  name = ""
  data = []
  with open(dataFile, 'rb') as f:
    header = f.readline().split(',')
    name = header[1].replace('"', '')
    f.next()
    for line in f:
      data.append(line.split(','))

    return (name, data)

def main():
  dataFile = os.path.join(DATADIR, DATAFILE)
  name, data = parse_file(dataFile)

  assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
  assert data[0][1] == "01:00"
  assert data[2][0] == "01/01/2005"
  assert data[2][5] == "2"

  print 'done'


if __name__ == "__main__":
  main()
