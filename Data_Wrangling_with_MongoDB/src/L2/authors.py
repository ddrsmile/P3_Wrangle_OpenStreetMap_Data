import xml.etree.ElementTree as ET

article_file = r'./exampleResearchArticle.xml'

def get_root(fName):
  tree = ET.parse(fName)
  return tree.getroot()

def get_authors(root):
  authors = []
  for author in root.findall('./fm/bibl/aug/au'):
    data = {
            'fnm': None,
            'snm': None,
            'email': None,
            'insr': []
           }
    data["fnm"] = author.find('./fnm').text if author.find('./fnm').text else None
    data["snm"] = author.find('./snm').text if author.find('./snm').text else None
    data["email"] = author.find('./email').text if author.find('./email').text else None
    for i in author.findall('./insr'):
      data["insr"].append(i.attrib["iid"])

    authors.append(data)
  
  return authors

def test():
  solution = [{'insr': ['I1'], 'fnm': 'Omer', 'snm': 'Mei-Dan', 'email': 'omer@extremegate.com'},
              {'insr': ['I2'], 'fnm': 'Mike', 'snm': 'Carmont', 'email': 'mcarmont@hotmail.com'},
              {'insr': ['I3', 'I4'], 'fnm': 'Lior', 'snm': 'Laver', 'email': 'laver17@gmail.com'},
              {'insr': ['I3'], 'fnm': 'Meir', 'snm': 'Nyska', 'email': 'nyska@internet-zahav.net'},
              {'insr': ['I8'], 'fnm': 'Hagay', 'snm': 'Kammar', 'email': 'kammarh@gmail.com'},
              {'insr': ['I3', 'I5'], 'fnm': 'Gideon', 'snm': 'Mann', 'email': 'gideon.mann.md@gmail.com'},
              {'insr': ['I6'], 'fnm': 'Barnaby', 'snm': 'Clarck', 'email': 'barns.nz@gmail.com'},
              {'insr': ['I7'], 'fnm': 'Eugene', 'snm': 'Kots', 'email': 'eukots@gmail.com'}]

  root = get_root(article_file)
  data = get_authors(root)

  assert data[0] == solution[0]
  assert data[1]["insr"] == solution[1]["insr"]

  print data[0]
  print data[1]['fnm']

if __name__ == '__main__':
  test()
