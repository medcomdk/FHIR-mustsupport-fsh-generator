#!/usr/bin/python
import lxml.etree as ET
import sys

dom = ET.parse(str(sys.argv[1]))
xslt = ET.parse('testscriptcreater.xslt')
transform = ET.XSLT(xslt)
newdom = transform(dom)

f = open("TestScripts.html", "wb")
add_text = ET.tostring(newdom, pretty_print=True)
f.write(add_text)
f.close()

#with open("randomfile.html", "w") as external_file:
#    add_text = ET.tostring(newdom, pretty_print=True)
#    print(add_text, file=external_file)
#    external_file.close()