import os
import pprint
import csv
'''
def parse_file(dataFile):
  data = []
  with open(dataFile, "rb") as f:
    header = f.readline().split(',')
    cnt = 0
    for line in f:
      if cnt == 0:
        break

      values = line.split(',')
      ins = {}

      for field, value in zip(header, values):
        ins[field.rstrip()] = value.rstrip()

      data.append(ins)
      cnt += 1

    return data
'''

def parse_file(dataFile):
  data = []
  n = 0
  with open(dataFile, 'rb') as sd:
    r = csv.DictReader(sd)
    for line in r:
      data.append(line()
    return data
