
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
OSM_FILE = "miami_florida.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample1.osm"

k = 20 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# In[2]:

import xml.etree.cElementTree as ET
    
def count_tags(filename):
    tags = {}
    with open(filename, 'r') as f:
        
            for event, elem in ET.iterparse(filename, events=('start',)):
                if elem.tag not in tags.keys():
                    tags[elem.tag]=1
                else:
                    tags[elem.tag]+=1
            elem.clear()
    return tags
print count_tags(SAMPLE_FILE)            


# In[4]:

import re
import pprint

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
def key_type(filename):
    keys={'lower': 0, 'lower_colon': 0, 'problemchars': 0, 'other': 0}
    for event, elem in ET.iterparse(filename):
        if elem.tag == 'note' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                k = tag.attrib['k']
                if re.search(lower, k):
                    keys['lower'] += 1
                elif re.search(lower_colon, k):
                    keys['lower_colon'] += 1
                elif re.search(problemchars, k):
                    keys['problemchars'] += 1
                else:
                    keys['other'] += 1  
    return keys


    
print key_type(SAMPLE_FILE)
        


# In[22]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample1.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Way", "Terrace",
            "Trail", "Parkway","Highway","Loop", "Circle" ,"Plaza","West",'North',
            'Vista','Ridge', 'Section','Heights','Gate','Augusta', 'Birkdale', 'Wentworth','Westbrook',
            'Alley','Division','Plateau', '7','11','15' ,'337', '441', '5979','Bend','Charleston',
            'Broadway','Center','Point','Grove', 'Gardens', 'Capistrano', 'Esplanade','Holw','Isle','Passage','Path',
             'Lake','Spgs', 'Columbia','Huntington','Longview', 'Muirfield','Real', 'Rey','Rouge','Row','Run',
             'Oakmont','Sacramento','Spinnaker','Spyglass'
           
           ]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            elem.clear()
    osm_file.close()
    return street_types
pprint.pprint(dict(audit(OSMFILE)))

mapping = { "St": "Street", "street": "Street",'Sr':'Street', "Rd": "Road", "Rd.": "Road", "RD":"Road","AVE": "Avenue",
           "Ave": "Avenue", "avenue": "Avenue", "Pl": "Place", "Hwy": "Highway", "Ct": "Court", "Blvd.": "Boulevard", "Mnr":"MANOR",
           "Blvd": "Boulevard",'Dr': "Drive",'Ter':'Terrace','Trl':"Trail",'Ln':"Lane",'Bnd':"Bend",'PL':"Plaza",
           'Cir':"Circle",'Pkwy':"Parkway","S.": "South","S": "South", "W": "West", "NW": "Northwest", 
           "E": "East", "N": "North"
          }

def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            new_name = re.sub(street_type, mapping[street_type], name)
        else:
            new_name = name
        return new_name

st_types = audit(OSMFILE)
for ways in st_types.values():
    for item in ways:
        better_name = update_name(item, mapping)
        print item, "=>", better_name


# In[15]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample1.osm"

postcodes = {}
   

def is_postcode(elem):  
    return (elem.attrib['k']== 'addr:postcode')
    

    
OSM_FILE = open(OSMFILE, "r")

for event, elem in ET.iterparse(OSM_FILE, events=("start",)):

    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if is_postcode(tag):
                postcodes[tag.attrib['v']]=tag.attrib['v']
OSM_FILE.close()

pprint.pprint(dict(postcodes))

post_code_re = re.compile(r'^\D*(\d{5}).*')

clear_postcodes = defaultdict(set)

def update_postcode(postcode):
    m = post_code_re.search(postcode)
    if m:
        better_pc = m.group(1)
    
        return better_pc
    
for orig, pc in postcodes.items():
    
    clear_postcodes[orig].add(update_postcode(pc))
    
pprint.pprint(dict(clear_postcodes))
            


# In[24]:

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus


OSM_PATH = "sample1.osm"

NODES_PATH = "sample_nodes.csv"
NODE_TAGS_PATH = "sample_nodes_tags.csv"
WAYS_PATH = "sample_ways.csv"
WAY_NODES_PATH = "sample_ways_nodes.csv"
WAY_TAGS_PATH = "sample_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

schema = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}

SCHEMA = schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Way", "Terrace",
            "Trail", "Parkway","Highway","Loop", "Circle" ,"Plaza","West",'North',
            'Vista','Ridge', 'Section','Heights','Gate','Augusta', 'Birkdale', 'Wentworth','Westbrook',
            'Alley','Division','Plateau', '7','11','15' ,'337', '441', '5979','Bend','Charleston',
            'Broadway','Center','Point','Grove', 'Gardens', 'Capistrano', 'Esplanade','Holw','Isle','Passage','Path',
             'Lake','Spgs', 'Columbia','Huntington','Longview', 'Muirfield','Real', 'Rey','Rouge','Row','Run',
             'Oakmont','Sacramento','Spinnaker','Spyglass'
           
           ]


mapping = { "St": "Street", "street": "Street",'Sr':'Street', "Rd": "Road", "Rd.": "Road", "RD":"Road","AVE": "Avenue",
           "Ave": "Avenue", "avenue": "Avenue", "Pl": "Place", "Hwy": "Highway", "Ct": "Court", "Blvd.": "Boulevard", "Mnr":"MANOR",
           "Blvd": "Boulevard",'Dr': "Drive",'Ter':'Terrace','Trl':"Trail",'Ln':"Lane",'Bnd':"Bend",'PL':"Plaza",
           'Cir':"Circle",'Pkwy':"Parkway","S.": "South","S": "South", "W": "West", "NW": "Northwest", 
           "E": "East", "N": "North"
          }

def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            new_name = re.sub(street_type, mapping[street_type], name)
        else:
            new_name = name
        return new_name

post_code_re = re.compile(r'^\D*(\d{5}).*')


def update_postcode(postcode):
    m = post_code_re.search(postcode)
    if m:
        better_pc = m.group(1)
    
        return better_pc


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    
    if element.tag == 'node':
        for node in NODE_FIELDS:
            
            node_attribs[node] = element.attrib[node]
            
            
        for child in element:
            
            node_tags_dict = {}
            node_tags_dict['id'] = element.attrib['id']
            
            if child.attrib['k']== 'addr:street':
                node_tags_dict['value'] = update_name(child.attrib['v'],mapping)
            elif child.attrib['k'] == 'addr:postcode':
                node_tags_dict['value'] = update_postcode(child.attrib['v'])
            else:
                node_tags_dict['value'] = child.attrib['v']
            
                
            m = PROBLEMCHARS.search(child.attrib['k'])
            if m:
                continue
            else:
                if ':' in child.attrib['k']:
                    key_split = child.attrib['k'].split(":", 1)
                    node_tags_dict['type'] = key_split[0]
                    node_tags_dict['key'] = key_split[1]
                else:
                    node_tags_dict['type'] = "regular"
                    node_tags_dict['key'] = child.attrib['k']
                    
            tags.append(node_tags_dict)
            
                    
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field]
        
        position  = 0       
        for child in element:
            if child.tag == 'tag':
                way_tags_dict = {}
                way_tags_dict['id'] = element.attrib['id']
        
                if child.attrib['k']== 'addr:street':
                    way_tags_dict['value'] = update_name(child.attrib['v'],mapping)
                elif child.attrib['k'] == 'addr:postcode':
                    way_tags_dict['value'] = update_postcode(child.attrib['v'])
                else:
                    way_tags_dict['value'] = child.attrib['v']
                
                m = PROBLEMCHARS.search(child.attrib['k'])
                if m:
                    continue
                else:
                    if ':' in child.attrib['k']:
                        key_split = child.attrib['k'].split(":", 1)
                        way_tags_dict['type'] = key_split[0]
                        way_tags_dict['key'] = key_split[1]
                        
                    else:
                        way_tags_dict['type'] = "regular"
                        way_tags_dict['key'] = child.attrib['k']
                tags.append(way_tags_dict)
                      
            elif child.tag == 'nd':
                way_nodes_dict = {}
                
                
                way_nodes_dict['id'] = element.attrib['id']
                
                way_nodes_dict['node_id'] = child.attrib['ref']
                
                
                way_nodes_dict['position'] = position
                    
                position += 1
                   
                way_nodes.append(way_nodes_dict)    
            
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)
                    
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)


# In[26]:

import csv, sqlite3
from pprint import pprint
aq_file = 'sample.db'
db = sqlite3.connect(aq_file)
c = db.cursor()

c.execute('DROP TABLE IF EXISTS ways_tags')
db.commit()
c.execute("create table ways_tags (id INTERGER, key TEXT, value TEXT, type TEXT);")
db.commit()
with open('sample_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'),i['type'].decode('utf-8')) for i in dr]

c.executemany("insert into ways_tags (id, key,value,type) values (?,?,?,?);",  to_db)

db.commit()

c.execute('DROP TABLE IF EXISTS nodes_tags')
db.commit()
c.execute("create table nodes_tags (id INTERGER, key TEXT, value TEXT, type TEXT);")
db.commit()
with open('sample_nodes_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'),i['type'].decode('utf-8')) for i in dr]

c.executemany("insert into nodes_tags (id, key,value,type) values (?,?,?,?);",  to_db)

db.commit()

db.close()


# In[ ]:



