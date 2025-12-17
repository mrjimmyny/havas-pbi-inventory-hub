# HAVAS PBI Inventory Framework — Release v1.0.3 (no GUI / Console Safe)

## O que é isso
Pacote **portátil (ZIP)** para rodar o inventário do Power BI via **Console (CMD/PowerShell)**, usando **Python** (Modo DEV SEM GUI).

> Manual completo: **README_CONSOLE_SAFE.md**

---

## Como rodar (5 minutos)
1) Extraia o ZIP em uma pasta local (ex.: `C:\Scripts\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui`).
2) Instale **Python 3.14.x (ou superior estável)** + **pip** (com Python no PATH).
3) Converta seu `.pbix` para **PBIP (.pbip)**.
4) Copie `app\pbi_config.json` para a pasta raiz do seu projeto PBIP e preencha:
   - `project_name`
   - `xmla_connection_string`
   - (opcional) flags `run_v2_miner` / `run_v3_dotnet` / `run_v4_constructor` / `run_v5_links`
5) Preencha na pasta `app\`:
   - `notion_config.json` (Notion. Obrigatório)
   - `ai_config.json` (IA. Opcional)
6) Abra um terminal na pasta `app\`, crie venv e instale dependências:
   - `pip install requests`
   - `pip install google-genai` (somente se usar IA)
7) Rode o inventário:
   - `python framework_full.py -p "C:\CAMINHO\DO\PROJETO_PBIP"`

---

---

## Pré-requisito extra (V3 / XMLA): .NET SDK x64 (obrigatório)

A etapa **V3** usa o conector **PbiInventoryXmla.exe** (XMLA).  
Se você **não tiver o .NET SDK x64 (idealmente 8.x / net8)** instalado, a V3 **não roda** e o inventário fica **incompleto**.

**Download oficial (.NET):**
- `https://aka.ms/dotnet/download`

**O que instalar (Windows):**
- **.NET 8 SDK (x64)** (recomendado)

**Como validar:**
- `dotnet --version`

## Arquivos importantes
- `app\framework_full.py` → orquestrador principal (Console)
- `app\PbiInventoryXmla.exe` → etapa V3 (.NET XMLA que substitui o DAX Studio)
  - Requer **.NET SDK x64** (idealmente **8.x / net8**)
- `app\notion_config.json` → config do Notion (obrigatório)
- `app\ai_config.json` → config de IA (opcional)
- `app\pbi_config.json` → template (copiar para a pasta do seu PBIP)

---

## Suporte
Se der erro, gere um log e envie para o Jimmy:
- CMD: `python framework_full.py -p "C:\PROJETO" > run.log 2>&1`
- PowerShell: `python .\framework_full.py -p "C:\PROJETO" 2>&1 | Tee-Object -FilePath run.log`

Contato: **Jimmy** (Teams) ou **jaderson.almeida@br.havasvillage.com**
