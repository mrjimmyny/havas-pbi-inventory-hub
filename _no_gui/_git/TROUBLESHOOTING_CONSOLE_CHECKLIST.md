# Troubleshooting — Console Safe (Checklist rápido)

> Objetivo: você **não travar**. Faça na ordem.  
> Regra: **não rode “de novo” sem entender**. Primeiro gere `run.log`.
> Não está acostumado. Mesmo assim não conseguiu. **NO PANIC! SOS Jimmy no Teams** ou E-mail para **jaderson.almeida@br.havasvillage.com**.


---

## 0) Evidência mínima para suporte (sempre)
Antes de pedir ajuda, tenha:
- ✅ `run.log` (log completo)
- ✅ print do erro (se possível)
- ✅ `pbi_config.json` **sem tokens**
- ✅ versão do Python: `python --version`
- ✅ versão do .NET: `dotnet --version` (obrigatório para V3)

---

## 1) “python não é reconhecido” / “pip não é reconhecido”
**Causa provável:** Python não está no PATH.

### Como validar
- CMD/PowerShell:
  - `where python`
  - `python --version`

### Como resolver (sem drama)
1) Reinstale Python marcando **Add python.exe to PATH**  
2) Feche e reabra o terminal  
3) Teste novamente

---

## 2) PowerShell bloqueia o Activate.ps1
Erro típico: “running scripts is disabled…”

### Resolver (somente nesta sessão)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Depois:
```powershell
.\.venv\Scripts\Activate.ps1 (exemplo. Altere de acordo com o seu caso)
```

---

## 3) “ModuleNotFoundError: No module named 'requests'”
**Causa:** dependências não instaladas no venv.

### Resolver (com venv ativo)
```bat
pip install requests
```

---

## 4) Erro relacionado a IA / “No module named 'google'” / “genai”
**Causa:** você ligou IA no `pbi_config.json`, mas não instalou o SDK.

### Opção A (instalar IA)
```bat
pip install google-genai
```

### Opção B (desligar IA)
No `pbi_config.json`:
- `"use_ai_enrichment": false`
- `"measures_enrichment_enabled": false`

---

## 5) “Não foi possível localizar um pbi_config.json”
**Causa:** você apontou a pasta errada no `--project-dir`.

### Check de pasta correta
A pasta do projeto deve conter:
- `*.pbip`
- `*.Report\`
- `*.SemanticModel\`
- `pbi_config.json`

**Resolva**:
- ajuste o caminho no `-p / --project-dir`

---

---

## 5B) V3 não roda / PbiInventoryXmla.exe falha — falta .NET SDK x64
**Causa provável:** sua máquina não tem **.NET SDK x64** (idealmente **8.x / net8**) instalado.

### Como validar
- CMD/PowerShell:
  - `dotnet --version`
  - `dotnet --info`

Se `dotnet` não for reconhecido, o SDK não está instalado (ou não entrou no PATH).

### Como resolver
1) Baixe e instale o **.NET 8 SDK (x64)**:  
   `https://aka.ms/dotnet/download`
2) Feche e reabra o terminal
3) Rode novamente o Framework

### Plano B (se não conseguir instalar)
Você consegue rodar o Framework, mas o inventário fica **incompleto** (sem V3).  
No `pbi_config.json`, desative:
- `"run_v3_dotnet": false`


## 6) Falha de conexão XMLA / Power BI
Sintomas: erro no V3 (.NET) ou mensagens de conexão.

**Causas mais comuns**
- Connection string errada
- Sem permissão no dataset/workspace
- Workspace sem XMLA habilitado (ou sua conta sem acesso)

**Ações objetivas**
1) Valide o campo `xmla_connection_string` no `pbi_config.json`
2) Teste com o dono do workspace: “meu usuário tem permissão de Build/Read no dataset?”
3) Se necessário, peça a string completa já validada:
   - `Data Source=powerbi://api.powerbi.com/v1.0/myorg/<WORKSPACE>;Initial Catalog=<DATASET>;`

---

## 7) Notion não atualiza (401 / 403 / 404)
**Causas mais comuns**
- Token errado/vazio
- HUB não foi “Share” com a Integration
- Database ID errado

**Checklist**
- token está preenchido em `app\notion_config.json`?
- HUB foi compartilhado com a Integration?
- Database ID é o da base (não da página)?

---

## 8) “Access is denied” / “PermissionError”
**Causas mais comuns**
- pasta em rede / OneDrive com lock
- você tentou rodar dentro de `C:\Program Files\...`

**Resolver**
- mova o release e o projeto para uma pasta sua, ex.:
  - `C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\...`

---

## 9) Log “vira bagunça” / caracteres quebrados
**Causa:** encoding do terminal.

**Resolver rápido**
- Prefira PowerShell moderno
- Gere `run.log` e leia pelo VS Code/Notepad++

---

## 10) Quando chamar o Jimmy (última tentativa)
Se você passou por este checklist e ainda falha:
- envie para **Jimmy** no Teams ou **jaderson.almeida@br.havasvillage.com**
- anexe:
  - `run.log`
  - print do erro
  - `pbi_config.json` (sem tokens)
  - sua versão do Python
  - explicação clara do que está acontecendo
