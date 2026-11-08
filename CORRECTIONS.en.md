# CORRECTIONS.en.md

## Target repository
- **Name:** FHIR-mustsupport-fsh-generator
- **URL:** https://github.com/medcomdk/FHIR-mustsupport-fsh-generator
- **Default branch (upstream):** main
- **Base commit analyzed:** 770c009
- **Date of preparation:** 2026-11-08 (local time)
- **Author:** admeduardovieira (Kilo, REA 6.7.0)

---

## Corrections implemented

### REA-FSH-001 — Command-line argument check
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** `dom = ET.parse(str(sys.argv[1]))` — IndexError if no argument.
**After:** Checks `len(sys.argv) < 2` and prints usage message, exits with code 1.
**Risk:** Low. **Test:** run script without argument → should show usage and exit code 1 (not executed: lxml not installed).

### REA-FSH-002 — Absolute path for XSLT
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** `ET.parse('testscriptcreater.xslt')` — relative to current working directory.
**After:** Uses `os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testscriptcreater.xslt')`.
**Risk:** Low. **Test:** run script from different directory → should find the XSLT.

### REA-FSH-003 — Configurable output path
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** `open("TestScripts.html", "wb")` — hardcoded in current directory.
**After:** Accepts optional second argument for output path; defaults to `TestScripts.html` in script directory.
**Risk:** Low.

### REA-FSH-004 — Windows-portable shebang
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** `#!/usr/bin/python`
**After:** `#!/usr/bin/env python3`
**Risk:** Low.

### REA-FSH-005 — XXE protection
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** `ET.parse(...)` without parser configuration.
**After:** Uses `ET.XMLParser(resolve_entities=False, no_network=True)`.
**Risk:** Low. **Test:** submit XML with external entity → should be blocked.

### REA-FSH-006 — Exception handling
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** No try/except.
**After:** Wraps parse, transformation and writing in try/except with descriptive error messages and error exit codes.
**Risk:** Low.

### REA-FSH-007 — FHIR StructureDefinition input validation
**File:** `StructureDefinitiontoFSHMStest.py`
**Before:** No validation.
**After:** Checks root element `<StructureDefinition>` with FHIR namespace after parse.
**Risk:** Low.

---

## Corrections not implemented
- Add requirements.txt with lxml dependency (pending — requires maintainer decision on PyPI package name)
- Add automated tests (pending — requires test framework)

---

*This document will be updated as corrections are implemented and validated.*
