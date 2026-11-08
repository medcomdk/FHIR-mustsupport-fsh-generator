# CORRECTIONS.md

## Repositório alvo
- **Nome:** FHIR-mustsupport-fsh-generator
- **URL:** https://github.com/medcomdk/FHIR-mustsupport-fsh-generator
- **Branch padrão (upstream):** main
- **Commit-base analisado:** 770c009
- **Data da elaboração:** 2026-11-08 (horário local)
- **Autor:** admeduardovieira (Kilo, REA 6.7.0)

---

## Correções implementadas

### REA-FSH-001 — Verificação de argumento de linha de comando
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** `dom = ET.parse(str(sys.argv[1]))` — IndexError se nenhum argumento.
**Depois:** Verifica `len(sys.argv) < 2` e imprime mensagem de uso, saindo com código 1.
**Risco:** Baixo. **Teste:** executar script sem argumento → deve exibir mensagem de uso e sair com código 1 (não executado: lxml não instalado).

### REA-FSH-002 — Caminho absoluto para o XSLT
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** `ET.parse('testscriptcreater.xslt')` — relativo ao diretório de trabalho.
**Depois:** Usa `os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testscriptcreater.xslt')`.
**Risco:** Baixo. **Teste:** executar script de diretório diferente → deve encontrar o XSLT.

### REA-FSH-003 — Caminho de saída configurável
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** `open("TestScripts.html", "wb")` — hardcoded no diretório atual.
**Depois:** Aceita segundo argumento opcional para caminho de saída; padrão `TestScripts.html` no diretório do script.
**Risco:** Baixo.

### REA-FSH-004 — Shebang portável para Windows
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** `#!/usr/bin/python`
**Depois:** `#!/usr/bin/env python3`
**Risco:** Baixo.

### REA-FSH-005 — Proteção contra XXE
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** `ET.parse(...)` sem configuração de parser.
**Depois:** Usa `ET.XMLParser(resolve_entities=False, no_network=True)`.
**Risco:** Baixo. **Teste:** enviar XML com entidade externa → deve ser bloqueado.

### REA-FSH-006 — Tratamento de exceções
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** Sem try/except.
**Depois:** Embala parse, transformação e escrita em try/except com mensagens de erro descritivas e saída com código de erro.
**Risco:** Baixo.

### REA-FSH-007 — Validação de entrada StructureDefinition FHIR
**Arquivo:** `StructureDefinitiontoFSHMStest.py`
**Antes:** Nenhuma validação.
**Depois:** Verifica elemento raiz `<StructureDefinition>` com namespace FHIR após o parse.
**Risco:** Baixo.

---

## Correções não implementadas
- Adicionar requirements.txt com dependência lxml (pendente — requer decisão do mantenedor sobre nome do pacote no PyPI)
- Adicionar testes automatizados (pendente — requer framework de teste)

---

*Este documento será atualizado conforme as correções forem implementadas e validadas.*
