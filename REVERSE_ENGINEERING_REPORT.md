# REVERSE_ENGINEERING_REPORT.md

## Repositório alvo
- **Nome:** FHIR-mustsupport-fsh-generator
- **URL:** https://github.com/medcomdk/FHIR-mustsupport-fsh-generator
- **Branch padrão (upstream):** main
- **Commit-base analisado:** 770c009 (added testdata)
- **Versão do projeto:** não versionada (sem pom.xml/setup.py)
- **Pasta de trabalho local:** C:\Users\User\audit-repos\fsh-generator
- **Pasta de auditoria:** C:\Users\User\audit-repos\audit-work
- **Data/horário da auditoria:** 2026-11-08 (horário local)
- **Ambiente:** Windows, PowerShell 5.1, Git 2.49.0, Python 3.12.14 (sem lxml)

---

## A. Diagnóstico geral

### Arquitetura identificada
Projeto Python mínimo (4 arquivos, 18 linhas no script principal) que gera regras de teste Mustsupport FHIR (formato SUSHI) a partir de StructureDefinitions openEHR/FHIR em XML.

Fluxo:
1. `StructureDefinitiontoFSHMStest.py` recebe um arquivo XML de StructureDefinition como argumento de linha de comando (`sys.argv[1]`).
2. Faz parse do XML com `lxml.etree`.
3. Aplica transformação XSLT (`testscriptcreater.xslt`).
4. Escreve o resultado em `TestScripts.html` no diretório de trabalho atual.
5. O usuário abre o HTML no navegador e copia os scripts de teste.

### Tecnologias e dependências
- Python 3 (shebang `#!/usr/bin/python`)
- lxml.etree (XML parsing + XSLT transformação)
- testscriptcreater.xslt (folha de estilo XSLT 1.0)
- 7 arquivos de testdata (StructureDefinitions FHIR de exemplo)

### Estado de manutenção
- Baixa atividade: 4 commits, último em 770c009 (added testdata)
- Sem arquivo de dependências (requirements.txt, setup.py, pyproject.toml ausentes)
- Sem testes automatizados
- Sem CI/CD configurado
- Sem arquivo de licença visível (LICENSE não encontrado no root)

### Mecanismos de testes existentes
- Nenhum teste automatizado
- 7 arquivos de testdata XML para execução manual
- Não há pytest, unittest, etc.

### Limitações da investigação
- lxml não instalado → impossível executar o script para validar comportamento
- Análise baseada exclusivamente em inspeção estática do código-fonte (18 linhas) e XSLT (32 linhas)

---

## B. Problemas encontrados

| ID | Localização | Problema | Status | Severidade | Evidência |
|----|-------------|----------|--------|------------|-----------|
| REA-FSH-001 | `StructureDefinitiontoFSHMStest.py:5` | `sys.argv[1]` acessado sem verificação de presença de argumento → IndexError se executado sem parâmetro | CONFIRMADO (estática) | P2 | Linha 5: `dom = ET.parse(str(sys.argv[1]))` |
| REA-FSH-002 | `StructureDefinitiontoFSHMStest.py:6` | Caminho hardcoded `'testscriptcreater.xslt'` relativo ao diretório de trabalho atual | CONFIRMADO (estática) | P2 | Linha 6: `xslt = ET.parse('testscriptcreater.xslt')` |
| REA-FSH-003 | `StructureDefinitiontoFSHMStest.py:10` | Saída hardcoded `"TestScripts.html"` no diretório de trabalho atual | CONFIRMADO (estática) | P2 | Linha 10: `open("TestScripts.html", "wb")` |
| REA-FSH-004 | `StructureDefinitiontoFSHMStest.py:1` | Shebang `#!/usr/bin/python` não portável para Windows | CONFIRMADO (estática) | P3 | Linha 1: `#!/usr/bin/python` |
| REA-FSH-005 | `StructureDefinitiontoFSHMStest.py:5` | `ET.parse()` sem parser com resolvendo de entidades externas desabilitado → potencial XXE | HIPÓTESE | P2 | Linha 5: `ET.parse(str(sys.argv[1]))` sem `XMLParser(resolve_entities=False)` |
| REA-FSH-006 | `StructureDefinitiontoFSHMStest.py` | Nenhum tratamento de exceções (try/except) para parse, transformação ou escrita de arquivo | CONFIRMADO (estática) | P3 | Nenhum bloco try/except no arquivo |
| REA-FSH-007 | `StructureDefinitiontoFSHMStest.py` | Nenhuma validação de que o arquivo de entrada é um StructureDefinition FHIR válido | HIPÓTESE | P3 | Nenhuma validação de entrada |

### Sem problemas P0 ou P1
Nenhum problema crítico confirmado.

---

## C. Problemas recorrentes
Não há histórico de issues/PRs público disponível para este repositório (projeto pequeno, 4 commits). Não foram encontrados problemas recorrentes documentados.

---

## D. Erros não documentados
Todos os problemas listados acima (REA-FSH-001 a REA-FSH-007) não estavam documentados em issues ou PRs.

---

## E. Performance
Não há oportunidades de performance relevantes em um script de 18 linhas que executa uma única transformação XSLT.

---

## F. Melhorias técnicas
1. Adicionar verificação de argumento de linha de comando (REA-FSH-001)
2. Usar caminho absoluto ou relativo ao script para o XSLT (REA-FSH-002)
3. Permitir caminho de saída configurável (REA-FSH-003)
4. Ajustar shebang para portabilidade Windows (REA-FSH-004)
5. Configurar parser XML sem resolvendo de entidades externas (REA-FSH-005)
6. Adicionar tratamento de exceções (REA-FSH-006)
7. Adicionar validação de entrada StructureDefinition FHIR (REA-FSH-007)
8. Adicionar requirements.txt com dependência lxml
9. Adicionar testes automatizados

---

## G. Plano de execução
Todas as correções são independentes e de baixo risco:
1. REA-FSH-001 (verificação de argumento) — imediata
2. REA-FSH-002 (caminho do XSLT) — imediata
3. REA-FSH-003 (caminho de saída) — imediata
4. REA-FSH-004 (shebang Windows) — baixa
5. REA-FSH-005 (XXE) — baixa
6. REA-FSH-006 (try/except) — baixa
7. REA-FSH-007 (validação de entrada) — baixa

---

## H. Resultado esperado
Script mais robusto, portável para Windows, seguro contra XXE, com tratamento de erros e saída configurável.

---

## Análise de malware e ameaças (estática)
**Resultado:** Nenhum indicador identificado pela análise estática realizada.
- Não foram encontradas credenciais, chaves, tokens ou senhas embutidas.
- Não foram encontradas URLs/domínios/IPs suspeitos (apenas namespaces FHIR normais nos dados de teste).
- Não foram encontrados comandos de shell, subprocess, exec, eval, persistência, ofuscação ou exfiltração de dados.
- Limitação: análise exclusivamente estática; lxml não instalado para validação dinâmica.
- Não se afirma que o projeto está livre de malware.

---

## Perguntas finais obrigatórias
1. **Bugs críticos comprovados?** Nenhum P0/P1.
2. **Problemas repetitivos não resolvidos?** Não há histórico de issues/PRs para avaliar.
3. **Erros não documentados?** Todos os 7 problemas (REA-FSH-001 a REA-FSH-007).
4. **Oportunidades de performance?** Nenhuma relevante (script de 18 linhas).
5. **Melhorias de segurança/confiabilidade?** Tratamento de argumento, caminho absoluto do XSLT, proteção XXE, try/except, validação de entrada.
6. **Correções rápidas?** Verificação de argumento, caminho absoluto do XSLT, try/except, shebang.
7. **Três contribuições de maior valor?** (a) Proteção XXE, (b) tratamento de argumento + try/except, (c) caminhos absolutos para portabilidade.
8. **Correções a evitar por falta de evidência?** Nenhuma — todas são de baixo risco e bem fundamentadas.
9. **Modificações recomendadas primeiro?** REA-FSH-001, REA-FSH-002, REA-FSH-006 (baixo risco, alto impacto em robustez).
