#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import json
import pprint
import re

DATAFILE = '../data/dataSet/arachnid.csv'
FIELDS = {'rdf-schema#lable': 'labe',
          'URI': 'uri',
          'rdf-schema#comment': 'description',
          'synonym': 'synonym',
          'name': 'name',
          # classification start
          'family_label': 'familey',
          'class_label': 'class',
          'phylum_label': 'phylum',
          'order_label': 'order',
          'kingdom': 'kingdom',
          'genus_label': 'genus'
          # classification end
          }

def process_file(filename, fields):
  process_fields = fields.keys()
  data = []
  with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for i in range(3):
      l = reader.next()

    for line in reader:
      arachnid = {}
      classification = {}
      for field, val in line.items():
        if field in FIELDS:
          nKey = FIELDS[field]
          nVal = val
          if nKey in ['family', 'class', 'phylum', 'order', 'kingdom', 'genus']
            classification[nKey] = nVal
          else:
            arachnid[nKey] = nVal
      arachnid['classification'] = classification
      data.append(arachnid)

    # clean data
    for arachnid in data:
      # strip redundant text from label
      arachnid['label'] = re.sub('\(.*?\)', '', arachnid['label'].strip())

      # fix 'name' if 'NULL' or contains non-alphanumeric character
      if arachnid['name'] == 'NULL' or not arachnid['name'].isalnum():
        arachnid['name'] = arachnid['label']
      
      # if synonym is not None, convert to an array (strip '{}' and split on '|')
      if arachnid['synonym'] != 'NULL':
        arachnid['synonym'] = arachnid['synonym'].lstrip('{').rstrip('}').split('|')

      # if a value of a field is "NULL", convert it to None
      for field, val in arachnid.items():
        if val == 'NULL':
          arachnid[field] = None
        # strip leading and ending whitespace from all fields if there is any
        try:
          arachnid[field] = arachnid[field].strip()
        except AttributeError:
          continue

      # fix 'classification whitespace and 'NULL' value
      for field, val in arachnid['classification'].items():
        arachnid['classification'][field] = arachnid['classification'][field].strip()
        if val == 'NULL':
          arachnid['classification'][field] = None

  return data

