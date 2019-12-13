from lxml import etree as et
parser = et.parse('sample.xml')
root = parser.getroot()
# In case of namespaces
nsList = root.path('./class1/class2/*')[0].nsmap
'''
nsList = {'ns0':'subClass:a','ns1':'subClass:b'}
'''
root.xpath('./class1/class2/ns0:class1/ns1:class2/tag1', namespaces=nsList)[0].tag
root.xpath('./class1/class2/ns0:class1/ns1:class2/tag1', namespaces=nsList)[0].text
root.xpath('./class1/class2/ns0:class1/ns1:class2/tag1', namespaces=nsList)[0].attrib
root.xpath('./class1/class2/ns0:class1/ns1:class2/tag1[@attrib="Attrib1"]', namespaces=nsList)[0].text



