'''
# Use VBA to download XML file first, due to log-in issue in typical business environment.
Option Explicit
Private Declare PtrSafe Function URLDownloadToFile Lib "urlmon" _
    Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, _
    ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long
# --------------------------------------------------------------------------------------------
Sub DownloadFilefromWeb()
    
    Call URLDownloadToFile(0, "http://sample", "C:\Users\Guest\Downloads\downloadName.xml", 0, 0)
End Sub
'''



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



