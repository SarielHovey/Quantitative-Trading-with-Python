from lxml import etree as et
parser = et.parse('sample.xml')
root = parser.getroot()
# In case of namespaces
nsList = root.path('./class1/class2/*')[0].nsname
'''
nsList = {'ns0':'subClass:a','ns1':'subClass:b'}
'''
root.xpath('./class1/class2/ns0:class1/ns1:class2/*', namespaces=nsList).tag
root.xpath('./class1/class2/ns0:class1/ns1:class2/*', namespaces=nsList).text
root.xpath('./class1/class2/ns0:class1/ns1:class2/*', namespaces=nsList).attrib




