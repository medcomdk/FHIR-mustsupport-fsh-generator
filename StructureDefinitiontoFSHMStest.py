#!/usr/bin/env python3
import lxml.etree as ET
import sys
import os

if len(sys.argv) < 2:
    print("Usage: StructureDefinitiontoFSHMStest.py <StructureDefinition.xml> [output.html]")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "TestScripts.html")
xslt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testscriptcreater.xslt")

try:
    parser = ET.XMLParser(resolve_entities=False, no_network=True)
    dom = ET.parse(input_path, parser)
except ET.XMLSyntaxError as e:
    print(f"Error parsing XML input: {e}")
    sys.exit(1)
except FileNotFoundError:
    print(f"Error: input file not found: {input_path}")
    sys.exit(1)
except Exception as e:
    print(f"Error reading input: {e}")
    sys.exit(1)

# Validate that the input is a FHIR StructureDefinition
root = dom.getroot()
if root.tag != "{http://hl7.org/fhir}StructureDefinition":
    print("Error: input is not a FHIR StructureDefinition (root element mismatch).")
    sys.exit(1)

try:
    xslt = ET.parse(xslt_path)
except ET.XMLSyntaxError as e:
    print(f"Error parsing XSLT: {e}")
    sys.exit(1)
except FileNotFoundError:
    print(f"Error: XSLT file not found: {xslt_path}")
    sys.exit(1)
except Exception as e:
    print(f"Error reading XSLT: {e}")
    sys.exit(1)

try:
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
except Exception as e:
    print(f"Error during XSLT transformation: {e}")
    sys.exit(1)

try:
    with open(output_path, "wb") as f:
        add_text = ET.tostring(newdom, pretty_print=True)
        f.write(add_text)
    print(f"Test script written to {output_path}")
except Exception as e:
    print(f"Error writing output: {e}")
    sys.exit(1)
