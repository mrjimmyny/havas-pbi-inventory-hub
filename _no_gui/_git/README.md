# HAVAS PBI Inventory Framework — (Console) — Release v1.0.3 (no GUI - DEV)

> **Escopo deste README:** rodar o inventário **via Console (CMD/PowerShell)** usando **Python** e o script `framework_full.py`.  
> **Fora de escopo:** qualquer instrução de **GUI** (`inventory_gui.exe`). O manual oficial da GUI continua sendo o caminho padrão.  
> Este documento existe como **Plano B** caso seu Windows corporativo bloqueie executáveis.

> **Windows apenas.** Usuários **Mac** não são elegíveis para esta release.

---

<a id="indice"></a>
## Índice (clique para ir direto)

1. [O que você precisa (check rápido)](#check-rapido)  
2. [Estrutura do ZIP (como deve ficar)](#estrutura-zip)  
3. [Preparar o Notion (obrigatório)](#notion)  
4. [Google AI Studio (opcional)](#ai)  
5. [Instalar Python (Windows) + validar](#python)  
6. [Preparar o projeto Power BI (PBIX → PBIP)](#pbip)  
7. [Configurar os JSONs (mesma lógica da GUI)](#configs)  
8. [Preparar o ambiente Python (venv) + instalar dependências](#venv)  
9. [Rodar o inventário via Console (CMD e PowerShell)](#rodar)  
10. [Onde ficam os outputs (o que você deve procurar)](#outputs)  
11. [Segurança e boas práticas (sem dor de cabeça)](#seguranca)  
12. [Suporte (última linha)](#suporte)  
13. [Troubleshooting rápido (atalho)](#troubleshooting)

---

<a id="check-rapido"></a>
## 1) O que você precisa (check rápido)

### Acessos
- **Power BI Service**: acesso ao workspace/dataset do projeto que deseja inventariar (para conexão via XMLA).
- **Notion (obrigatório, agindo como Front-End)**: acesso ao workspace onde o template do HUB foi duplicado e compartilhado com a Integration.

### Na sua máquina (Windows)
- **Python 3.14.x (ou superior estável)** instalado **com pip** e **no PATH**.
- **Pasta do Framework** extraída localmente (não em rede/OneDrive).
- **Projeto Power BI no formato PBIP** (não funciona com PBIX direto).

> **IMPORTANTE (V3 / XMLA):** a etapa **V3** usa o conector **PbiInventoryXmla.exe**.  
> Se você **não tiver o .NET SDK x64 (idealmente 8.x / net8)** instalado, a V3 **não roda** e o inventário fica **incompleto**.


> **Por que PBIP?** porque o inventário lê a estrutura do projeto em pastas e gera outputs no diretório do projeto.  
> **PBIP garante acesso aos metadados** de forma estruturada.

---

<a id="estrutura-zip"></a>
## 2) Estrutura do ZIP (como deve ficar)

Depois de extrair o ZIP, você deve ter algo assim:

- `HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\`
  - `app\`
    - `framework_full.py`  ✅ (script que você vai rodar)
    - `minerador_pbi.py`
    - `constructor_notion.py`
    - `notion_post_links_ids.py`
    - `PbiInventoryXmla.exe` ✅ (módulo .NET da etapa V3)
    - `notion_config.json` ✅ (config do Notion)
    - `ai_config.json` ✅ (config de IA)
    - `pbi_config.json` ✅ (template para copiar para o seu projeto PBIP)
  - `docs\` (checksums e release notes)
  - `VERSION.txt`

**Regra de ouro:** não mova arquivos soltos. Se precisar mudar de lugar, mova a pasta inteira do release.

---

<a id="notion"></a>
## 3) Preparar o Notion (obrigatório)

> Você vai fazer **3 coisas**:  
> (1) criar uma **Integration** e copiar o **token**  
> (2) duplicar o **template do HUB** e dar **permissão** para a Integration (Share)  
> (3) pegar o **Database ID** do HUB

### 3.1 Acessar o portal de Integrations
Abra no navegador:
- `https://www.notion.so/profile/integrations`

### 3.2 Criar a Integration (token)
1. Clique em **New integration**.
2. Dê um nome simples, exemplo: **HAVAS PBI Inventory**.
3. Em **Capabilities**, mantenha o padrão (você só precisa de acesso às páginas/bases que vai usar).
4. Copie o **Internal Integration Token**.

**Como é esse token?**  
Ele costuma começar com `ntn_` (exemplo fake):
- `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`

> **Atenção:** token do Notion é segredo. Não compartilhe em chat e não suba para GitHub.

### 3.3 Conectar a Integration ao Template (HUB)
Você vai duplicar o template e depois “compartilhar” com a integration.

1. Abra o template do HUB (Banco de Dados já pronto para você usar):  
   `https://jspalmeida1983.notion.site/2c97048c8e2980ef8fd1d932faaf4041?v=2c97048c8e2981059d4c000cde4ab68e&source=copy_link`
2. Clique em **Duplicate** (duplicar) e escolha **seu workspace no Notion**.
3. No seu workspace Notion, abra a página duplicada do **PBI Inventory HUB**.
4. Clique em **Share** (compartilhar) e procure por **Invite** / **Connections**.
5. Selecione a sua integration **HAVAS PBI Inventory** e confirme o acesso.

> **Sem esse “Share”, o Framework não consegue escrever no seu Notion.** Vai falhar por permissão.

### 3.4 Pegar o ID da base do HUB (Database ID)
O Framework do Inventário precisa do **ID** da base principal do HUB.

1. Abra a base “PBI Inventory HUB” (a tabela dentro do Notion).
2. Copie o link da página (URL do browser).
3. O **Database ID** é a sequência longa de caracteres no link (sem `?v=` etc.).
   - Dica: normalmente aparece como um bloco tipo `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Exemplo fake: `3f06049c8e2980b0bf10cbb1f16fa580`

Esse ID vai entrar em `notion_config.json` (você faz isso no passo de configs).

> Se você não conseguir identificar com segurança, peça ajuda ao time do GD / **Jimmy** (é rápido e evita erro bobo).

---

<a id="ai"></a>
## 4) Google AI Studio (opcional)

> A IA é usada para **enriquecimento opcional** de medidas (descrições, classificações, etc.).  
> Se você não quiser usar, **pule esta parte** e desative no `pbi_config.json`.

### 4.1 Criar sua API Key (Google AI Studio)
1. Abra: `https://aistudio.google.com/api-keys`
2. Faça login com a conta autorizada.
3. Clique em **Create API key**.
4. Copie a chave.

### 4.2 Onde você cola essa chave
Você vai colar em `ai_config.json` no campo `api_key` (passo 7).

**Atenção:** chave de IA é segredo (não compartilhe em chat, não suba para GitHub).

---

<a id="python"></a>
## 5) Instalar Python (Windows) + validar

### 5.1 Baixar e instalar
1) Baixe o **Python 3.14.x (ou superior estável)** para Windows (64-bit).  
2) Rode o instalador e marque:
   - ✅ **Add python.exe to PATH**
   - ✅ **pip**
   - (Opcional) ✅ **Disable path length limit**
3) Instale **“para o seu usuário”** (não precisa admin na maioria dos casos).

> Se sua máquina corporativa bloquear o instalador, acione o time de IT ou peça uma máquina com **Python atual estável** já liberado.

### 5.2 Validar a instalação (obrigatório)
Abra um terminal e rode:

**CMD**
```bat
python --version
pip --version
```

**PowerShell**
```powershell
python --version
pip --version
```

Você deve ver algo como `Python 3.14.x`.

> Se aparecer “python não é reconhecido”, vá no troubleshooting (seção no final deste README + checklist separado).

---

### 5.3 Instalar .NET SDK x64 (obrigatório para V3 / XMLA) + validar

> A etapa **V3** (conector XMLA `PbiInventoryXmla.exe`) depende do **.NET SDK x64**, idealmente **8.x** (alinhado com `net8`).  
> Sem isso, a execução **não quebra** o Framework inteiro, mas o inventário fica **incompleto** (a V3 falha ou é pulada).

#### 5.3.1 Baixar e instalar
1) Abra o link oficial de download do .NET:  
   `https://aka.ms/dotnet/download`
2) Baixe e instale:
   - **.NET 8 SDK (x64)** (recomendado)
3) Finalize a instalação e **feche e reabra** o terminal.

> Se sua máquina corporativa bloquear a instalação, acione o time de IT.

#### 5.3.2 Validar a instalação (obrigatório)
Abra um terminal e rode:

**CMD**
```bat
dotnet --version
dotnet --info
```

**PowerShell**
```powershell
dotnet --version
dotnet --info
```

Se o comando `dotnet` não existir, o SDK não está instalado ou não entrou no PATH.

#### 5.3.3 Se você NÃO conseguir instalar o .NET SDK
Você ainda consegue rodar o Framework, mas com inventário **incompleto** (sem V3).  
Para evitar erro/ruído, desligue a V3 no `pbi_config.json`:
- `"run_v3_dotnet": false`


<a id="pbip"></a>
## 6) Preparar o projeto Power BI (PBIX → PBIP)

### 6.1 Converter PBIX para PBIP
No Power BI Desktop:
1) Abra o seu `.pbix`  
2) **File → Save As**  
3) Selecione **Power BI Project (.pbip)** e salve numa pasta de trabalho sua, por exemplo:
   - `C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\Projetos\MeuProjeto\`

**Dica de padrão (recomendado):**  
mantenha o nome da pasta igual ao nome do seu Projeto publicado no Power BI Service (nome do Modelo Semântico).

Exemplo prático:
- Seu Modelo Semântico se chama **Projeto_1**
- Crie uma pasta: `C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\Projetos\_project_pbip_Projeto_1\`
- É dentro desta pasta que você vai **salvar como** `.pbip`

### 6.2 Validar a pasta do PBIP (não pule)
Dentro da pasta do projeto, você normalmente vê:
- `MeuProjeto.pbip` (este substitui o .pbix **apenas** para desenvolvimento)
- `MeuProjeto.Report\...`
- `MeuProjeto.SemanticModel\...`

---

<a id="configs"></a>
## 7) Configurar os JSONs (mesma lógica da GUI)

> **Ponto crítico:** o Framework lê configs em **dois lugares diferentes**:
- `pbi_config.json` fica **na pasta do seu projeto PBIP**
- `notion_config.json` e `ai_config.json` ficam **na pasta `app\` do release** (junto dos scripts `.py`)

### 7.1 pbi_config.json (obrigatório)
1) Copie o arquivo:
   - De: `...\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\app\pbi_config.json`
   - Para: **a pasta raiz do seu projeto PBIP** (onde está o `.pbip`)
2) Edite os campos principais (exemplo com placeholders):

```json
{
  "project_name": "<NOME_DO_PROJETO>",
  "project_link": "<LINK_DO_RELATORIO_OU_WORKSPACE>",
  "xmla_connection_string": "Data Source=powerbi://api.powerbi.com/v1.0/myorg/<NOME_WORKSPACE>;Initial Catalog=<NOME_DATASET>;",

  "use_ai_enrichment": true,
  "measures_enrichment_enabled": true,

  "run_v2_miner": true,
  "run_v3_dotnet": true,
  "run_v4_constructor": true,
  "run_v5_links": true
}
```

**Notas diretas (sem rodeio):**
- Se você não tem **XMLA connection string**, a etapa V3 vai falhar. Peça para o dono do workspace/dataset.
- Se você quer rodar **sem IA**, coloque:
  - `"use_ai_enrichment": false`
  - `"measures_enrichment_enabled": false`
- Se você quer rodar **sem Notion**, coloque:
  - `"run_v4_constructor": false`
  - `"run_v5_links": false`  
  (ou simplesmente deixe `notion_config.json` ausente — o wrapper pula V4/V5 automaticamente.)

### 7.2 notion_config.json (obrigatório se `"run_v4_constructor": true`)
Arquivo: `...\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\app\notion_config.json`

Use os dados que você pegou no passo **3) Preparar o Notion**:

```json
{
  "notion_api_key": "<NOTION_INTERNAL_INTEGRATION_TOKEN>",
  "databases": {
    "pbi_inventory_hub": "<NOTION_DATABASE_ID_DO_HUB>"
  },
  "options": {
    "enable_measure_links": true
  }
}
```

Checklist Notion (se algo falhar, é aqui):
- Você criou uma Integration no Notion
- Você duplicou o template do HUB para o seu workspace
- Você clicou em **Share** e deu acesso do HUB para a Integration
- Você pegou o **Database ID** correto

### 7.3 ai_config.json (opcional)
Arquivo: `...\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\app\ai_config.json`

Se não for usar IA, pode deixar `api_key` vazio e desligar no `pbi_config.json`.

```json
{
  "provider": "google-gemini",
  "api_key": "<GEMINI_API_KEY>",
  "default_model": "gemini-2.5-flash"
}
```

---

<a id="venv"></a>
## 8) Preparar o ambiente Python (venv) + instalar dependências

> **Objetivo:** isolar o ambiente e garantir que “na sua máquina roda” sem quebrar o Windows.

### 8.1 Entrar na pasta `app\`
**CMD**
```bat
cd /d C:\Scripts\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\app
```

**PowerShell**
```powershell
cd 'C:\Scripts\HAVAS_PBI_Inventory_Framework_v1.0.3_no_gui\app'
```

> Ajuste o caminho acima para onde você extraiu o ZIP.

### 8.2 Criar e ativar um ambiente virtual
**CMD**
```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Se o PowerShell bloquear a ativação, rode (somente nesta sessão) e tente de novo:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 8.3 Instalar dependências mínimas
**CMD / PowerShell (igual)**
```bat
python -m pip install --upgrade pip
pip install requests
```

### 8.4 Dependências opcionais (somente se usar IA)
Se você vai usar enriquecimento de IA, instale também:
```bat
pip install google-genai
```

> **Sem requirements.txt:** este release não traz `requirements.txt`.  
> Se aparecer erro de “módulo não encontrado”, o próprio erro vai dizer o nome. Instale com `pip install <nome_do_pacote>` e rode de novo.

---

<a id="rodar"></a>
## 9) Rodar o inventário via Console (CMD e PowerShell)

> **Antes de rodar:** confirme que você está com o venv ativo (deve aparecer `(.venv)` no começo da linha do terminal).

### 9.1 Rodar o fluxo completo (recomendado)
Você vai passar o caminho da pasta do projeto PBIP usando `--project-dir` (ou `-p`).

**CMD**
```bat
python framework_full.py --project-dir "C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\Projetos\MeuProjeto\_project_pbip_MeuProjeto"
```

**PowerShell**
```powershell
python .\framework_full.py --project-dir "C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\Projetos\MeuProjeto\_project_pbip_MeuProjeto"
```

### 9.2 Gerar um log para suporte (muito recomendado)
**CMD (gera run.log na pasta app)**
```bat
python framework_full.py -p "C:\CAMINHO\DO\PROJETO_PBIP" > run.log 2>&1
```

**PowerShell (gera run.log na pasta app)**
```powershell
python .\framework_full.py -p "C:\CAMINHO\DO\PROJETO_PBIP" 2>&1 | Tee-Object -FilePath run.log
```

> **Sempre** envie o `run.log` quando pedir ajuda (sem tokens).

### 9.3 AVANÇADO (não mexa nisso se não está acostumado): forçar ou pular etapas
Você pode controlar etapas com:
- `--run-v2` / `--run-v3` / `--run-v4` / `--run-v5`
- Valores: `auto` (padrão), `yes`, `no`

Exemplo (rodar só V2 e V3):
**CMD**
```bat
python framework_full.py -p "C:\CAMINHO\DO\PROJETO_PBIP" --run-v4 no --run-v5 no
```

**PowerShell**
```powershell
python .\framework_full.py -p "C:\CAMINHO\DO\PROJETO_PBIP" --run-v4 no --run-v5 no
```

---

<a id="outputs"></a>
## 10) Onde ficam os outputs (o que você deve procurar)

**Regra simples:** os outputs são gerados **dentro da pasta do projeto PBIP** (a que você passou no `--project-dir`).

Exemplos comuns de arquivos criados (podem variar por versão do módulo):
- `model_structure.json`
- `measures_for_ai.csv`
- arquivos `.json` / `.csv` gerados pelo `PbiInventoryXmla.exe` (etapa V3)
- arquivos de apoio do Notion/links (V4/V5), quando habilitados

Se você configurou Notion corretamente, o HUB também é atualizado ao final da execução.

---

<a id="seguranca"></a>
## 11) Segurança e boas práticas (sem dor de cabeça)

- **NUNCA** suba tokens (`notion_api_key`, `api_key`) para GitHub.
- Rode sempre em pasta **local**, de preferência: `C:\Users\<seu_usuario>\Documents\...`
- Evite executar dentro de pasta sincronizada (OneDrive/rede) durante a rodada.
- Se o terminal mostrar erro, **não rode de novo no impulso**: gere o `run.log`, leia a mensagem e siga o checklist.

---

<a id="suporte"></a>
## 12) Suporte (última linha)

Se você travar mesmo após o troubleshooting:
- Fale com **Jimmy** no Teams, ou envie e-mail para **jaderson.almeida@br.havasvillage.com**
- Anexe:
  - `run.log`
  - o `pbi_config.json` **sem tokens**
  - o trecho do erro (copiado do terminal)

---

<a id="troubleshooting"></a>
## 13) Troubleshooting rápido (atalho)

➡️ Use também o arquivo separado: `TROUBLESHOOTING_CONSOLE_CHECKLIST.md` (feito para triagem rápida).
