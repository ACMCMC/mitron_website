import xmltodict

with open('/Users/agustinsuarez/Documents/swe-spa.tei') as fd:
    doc = xmltodict.parse(fd.read())

print(doc['TEI']['text']['body']['entry'][1])
