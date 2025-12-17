# HAVAS PBI Inventory Framework — Manual do Usuário Final (GUI)

> **Objetivo:** você entra na aplicação, segue as **Telas 1–5**, e sai com o **inventário do seu projeto** (arquivos locais + atualização do Notion).  
> **Regra de ouro:** **zero console**. Se algo der errado, este manual te diz exatamente onde clicar e o que ajustar.

Se a dúvida persistir, entre em contato com o **Jimmy** (jaderson.almeida@br.havasvillage.com)

---

## Sumário
1. [O que você vai precisar](#o-que-você-vai-precisar)
2. [Pré-requisitos no Notion (FREE)](#pré-requisitos-no-notion-free)
3. [Preparar seu projeto Power BI (PBIX → PBIP)](#preparar-seu-projeto-power-bi-pbix--pbip)
4. [Configurar arquivos (.json)](#configurar-arquivos-json)
5. [Google AI Studio (opcional)](#google-ai-studio-opcional)
6. [Passo a passo na GUI (Telas 1–5)](#passo-a-passo-na-gui-telas-15)
7. [Outputs esperados](#outputs-esperados)
8. [Troubleshooting (sem travar)](#troubleshooting-sem-travar)
9. [Boas práticas e segurança](#boas-práticas-e-segurança)

---

## O que você vai precisar

### Acessos
- **Notion (FREE)**: acesso ao seu workspace e permissão para duplicar um template.
- **Power BI**: permissão de acesso ao projeto (workspace/modelo).  
  - Se o seu ambiente usa **XMLA** (comum em Premium/PPU), você precisa ter permissão para ler o modelo.  
  - Se você não sabe, peça para o time responsável pelo workspace confirmar.

### Na sua máquina
- **Power BI Desktop** (para salvar o projeto como PBIP).
- **Aplicação GUI** do HAVAS PBI Inventory Framework (o pack .zip com os executáveis).
- **Uma pasta de trabalho** no seu usuário (sem admin), por exemplo:
  - `C:\Users\<seu_usuario>\Documents\HAVAS_PBI_Inventory\`

---

## Pré-requisitos no Notion (FREE)

### 1) Criar uma Integration (token)
1. Abra o Notion na página de integrações:  
   `https://www.notion.so/profile/integrations`
2. Clique em **New integration** (ou equivalente).
3. Dê um nome fácil, por exemplo: **HAVAS PBI Inventory**.
4. Em **Capabilities**, mantenha o padrão (você só precisa de acesso às páginas/bases que vai usar).
5. Copie o **Internal Integration Token** (isso é seu “token do Notion”).  
   - **Guarde com cuidado.** Quem tem esse token pode escrever no seu Notion.
   - Ex: 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
   - Você vai precisar informar essa API no arquivo de config chamado `notion_config.json` que está na pasta app do pack .zip que baixou para Aplicação (junto dos executáveis). 

### 2) Conectar a Integration ao Template (HUB)
Você vai duplicar o template e depois “compartilhar” com a integration.

1. Abra o template do HUB (Banco de Dados já pronto para você usar):  
   `https://jspalmeida1983.notion.site/2c97048c8e2980ef8fd1d932faaf4041?v=2c97048c8e2981059d4c000cde4ab68e&source=copy_link`
2. Clique em **Duplicate** (duplicar) e escolha **seu workspace no Notion**.
3. No seu workspace Notion, abra a página duplicada do **PBI Inventory HUB**.
4. Clique em **Share** (compartilhar) e procure por **Invite** / **Connections**.
5. Selecione a sua integration **HAVAS PBI Inventory** e confirme o acesso.

### 3) Pegar o ID da base do HUB (Database ID)
O Framework do Inventário precisa do **ID** da base principal do HUB.

1. Abra a base “PBI Inventory HUB” (a tabela dentro do Notion).
2. Copie o link da página (URL do browser).
3. O **Database ID** é a sequência longa de caracteres no link (sem `?v=` etc.).  
   - Dica: normalmente aparece como um bloco tipo `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.
   - Ex: 3f06049c8e2980b0bf10cbb1f16fa580
   - Você vai precisar informar essa API no arquivo de config chamado `notion_config.json` que está na pasta app do pack .zip que baixou para Aplicação (junto dos executáveis). 

> Se você não conseguir identificar com segurança, peça ajuda ao time do GD, Jimmy (é rápido e evita erro bobo).

---

## Preparar seu projeto Power BI (PBIX → PBIP)

### Por que isso importa?
O Framework trabalha com o projeto no formato **PBIP** (Project). Tudo fica organizado em pastas e facilita leitura/validação.

### Passo a passo (Power BI Desktop)
1. Abra seu `.pbix` no Power BI Desktop.
2. Vá em **File → Save As**.
3. Selecione o tipo **Power BI Project (.pbip)**.
4. Salve dentro da sua pasta de trabalho, exemplo:
   - `...\HAVAS_PBI_Inventory\Projetos\MeuProjeto\`
   - Ex. prático: Digamos que o nome do arquivo .pbix do Projeto que quer inventariar seja "pbi_operacao_a.pbix". Um nível abaixo de `...\HAVAS_PBI_Inventory\Projetos\MeuProjeto\` crie uma pasta vazia chamada '...\_project_pbip_pbi_operacao_a
   -É dentro desta pasta que você vai salvar seu Projeto PBI de .pbix para .pbip.


### Como deve ficar a pasta (check rápido)
Dentro da pasta do projeto, normalmente você verá algo como:
- `.gitignore`
- `MeuProjeto.pbip`
- `MeuProjeto.SemanticModel\...`
- `MeuProjeto.Report\...`

> **Importante:** selecione sempre a **pasta do projeto PBIP** na GUI (não selecione um arquivo solto).

**(Opcional — prints de referência)**  
Se você estiver usando a mesma estrutura do pacote de documentação, os prints podem ficar assim no repositório:

- `assets/estrutura_pastas_tela1.png`  
- `assets/estrutura_pastas_tela2.png`  
- `assets/estrutura_pastas_tela3.png`  
- `assets/estrutura_pastas_tela4.png`

---

## Configurar arquivos (.json)

> Você vai editar 3 arquivos: `notion_config.json`, `pbi_config.json`, `ai_config.json`.  
> **Sem console:** use o **Explorador de Arquivos** e um editor simples (Bloco de Notas / VS Code).

### Onde colocar os arquivos
- `pbi_config.json` fica na **pasta raiz do seu projeto PBIP** (a mesma pasta onde está o `.pbip`).
- `notion_config.json` e `ai_config.json` ficam em **HAVAS_PBI_Inventory_Framework_v1.0.3\app** (a mesma quando você baixou o pack .zip do Framework e junto de todos os executáveis).

### 1) notion_config.json (obrigatório para atualizar Notion)
Use o token da integration e o Database ID do HUB.

```json - EXEMPLO. Você deve ter a sua própria API + Database ID.

{
  "notion_api_key": "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",
  "databases": {
    "pbi_inventory_hub": "3f06049c8e2980b0bf10cbb1f16fa580"
  },
  "options": {
    "enable_measure_links": true
  }
}
```

**O que pode dar errado aqui (e como evitar):**
- Token vazio/errado → Notion não atualiza.
- Integration não foi “share” na página/base → Notion retorna erro de permissão.

### 2) pbi_config.json (obrigatório para identificar o projeto e conexão)
Este arquivo guarda o “mínimo” para o framework reconhecer o projeto e conectar no modelo.

> **Dica prática:** se você já tem um `pbi_config.json` “modelo” do time, **não inventa moda**.  
> Só preencha os campos vazios.
> Você pode preencher antes de rodar o App do Framework ou durante a execução (sugestão: se não estiver acostumado, preencha durante a execução).

Exemplo (compatível com o template mais comum do framework):
```json
{
  "project_name": "CR_Brazil_Reckitt_Bigpromo",
  "project_link": "https://app.powerbi.com/groups/<workspaceId>/reports/<reportId>",
  "project_url": "",
  "use_ai_enrichment": true,
  "measures_enrichment_enabled": true,
  "xmla_connection_string": "Data Source=powerbi://api.powerbi.com/v1.0/myorg/<NOME_WORKSPACE>;Initial Catalog=<NOME_DO_DATASET>;",
  "powerbi_connection_string": "",
  "project": "",
  "connection_string": "",
  "project_workspace_url": ""
}
```

**Notas importantes (sem enrolação):**
- `project_name`: nome amigável (vai aparecer nos outputs).
- `project_link`: link do relatório/workspace (opcional, mas ajuda).
- `xmla_connection_string`: é o que permite o inventário técnico via Power BI Service.
  - Se você não tem isso, peça para o time do projeto te passar o correto.
- Campos vazios extras (`project_url`, `project_workspace_url`, etc.): pode manter vazio se você não usa.

> Se você quer rodar **sem IA**, coloque `use_ai_enrichment` e `measures_enrichment_enabled` como `false`.
> Se você quer o enrquecimento das Medidas DAX, precisa ter uma API ativa do Google AI Studio ou outra LLM que preferir (padrão é o Gemini).


### 3) ai_config.json (opcional — só se usar IA)
Se você **não** quer IA, pode deixar `api_key` vazio e desligar no `pbi_config.json`.

```json
{
  "provider": "google-gemini",
  "api_key": "AIzaSyxxxxxxxxxxxxxxxxxxxx",
  "default_model": "gemini-2.5-flash"
}
```

---

## Google AI Studio (opcional)

> A IA é usada para **enriquecimento opcional** de medidas (descrições, classificações, etc.).  
> Se você não quiser usar, **pule esta parte** e desative no `pbi_config.json`.

1. Abra: `https://aistudio.google.com/api-keys`
2. Faça login com a conta autorizada.
3. Clique em **Create API key**.
4. Copie a chave e cole em `ai_config.json` no campo `api_key`.

**Atenção:** chave de IA é segredo (não compartilhe em chat, não suba para GitHub).

---

## Passo a passo na GUI (Telas 1–5)

> A GUI é um assistente em 5 passos. Você só precisa preencher o básico e clicar em **Avançar**.

### Tela 1 — Boas-vindas
**O que você faz:**
- Clique em **Começar**.

**O que você confere:**
- Você entende que o assistente vai ler o projeto e gerar inventário + Notion.

**(Opcional — print)**  
`docs/assets/inventory_gui__exe_screen_example_step1.png`

---

### Tela 2 — Dados do projeto
**O que você faz:**
1. Selecione a **pasta do projeto PBIP** (a pasta que contém o `.pbip`).
2. Informe (se tiver) o **link do projeto** (report/workspace).
3. Confirme o nome do projeto (se o campo existir).

**Checklist antes de avançar:**
- ✅ Você selecionou a pasta certa (PBIP).
- ✅ O arquivo `pbi_config.json` está na pasta do Projeto PBI.

**(Opcional — print)**  
`docs/assets/inventory_gui__exe_screen_example_step2.png`

---

### Tela 3 — Checagens
Aqui a aplicação valida se está tudo pronto **antes de rodar**.

**O que você faz:**
- Leia os status (OK / Atenção / Erro).
- Se existir **Erro (bloqueante)**, ajuste e clique para revalidar.

**Como interpretar:**
- ✅ **OK**: segue o jogo.
- ⚠️ **Atenção**: normalmente dá para rodar, mas pode ter perda (ex.: Notion não atualiza).
- ⛔ **Erro**: trava execução. Você precisa corrigir.

**Correções mais comuns:**
- **Não achou PBIP** → você escolheu a pasta errada. Volte e selecione a pasta correta.
- **pbi_config.json faltando** → copie o arquivo para a pasta do projeto.
- **notion_config.json com token vazio** → cole o token e salve.
- **Sem internet** → conecte e tente de novo.

**(Opcional — print)**  
`docs/assets/inventory_gui__exe_screen_example_step3.png`

---

### Tela 4 — Execução do inventário
Aqui você só acompanha o progresso. Dependendo do tamanho do Projeto, pode demorar vários minutos. Não feche o App.


**O que você faz:**
- Clique em **Iniciar** (ou equivalente).
- Aguarde as etapas concluírem.
- Se aparecer erro, **não fecha**: anote o texto do erro e vá para o troubleshooting.

**O que você espera ver:**
- Status por etapa (rodando / ok / erro).
- Mensagens curtas e claras (sem console).

**(Opcional — print)**  
`docs/assets/inventory_gui__exe_screen_example_step4.png`

---

### Tela 5 — Resumo da rodada
Aqui você sai com o resultado.

**O que você faz:**
1. Leia o **Status geral** (sucesso / avisos / erro).
2. Use os botões de 1 clique para abrir:
   - **Pasta do Projeto / Outputs**
   - **Link do Projeto** (report/workspace)
   - **Log detalhado** (para suporte)

> Se o Notion não atualizou, esta tela normalmente explica o motivo (token/permissão/instabilidade).

**(Opcional — print)**  
`docs/assets/inventory_gui__exe_screen_example_step5.png`

---

## Outputs esperados

Ao final, você deve ter:

### 1) Arquivos locais (sempre)
Dentro da pasta do projeto, o framework gera pastas/arquivos de inventário (exemplos comuns):
- `outputs\` (ou similar)
- `.json` / `.csv` técnicos (inventário do modelo)
- `logs\` com o log da rodada

> Nomes podem variar por versão, mas a **Tela 5** te leva até a pasta certa.

### 2) Notion atualizado (se configurado corretamente)
No seu Notion (template HUB duplicado), você verá:
- Uma nova rodada/versionamento (governança).
- Bases com inventário (medidas, tabelas, etc.) preenchidas/atualizadas.
- São ao todo 9 Módulos de Inventário para cada Projeto.

---

## Troubleshooting (sem travar)

### Regra de ouro de triagem
1. Volte para a **Tela 3 (Checagens)** e veja o que está marcado como **Erro**.
2. Se o erro aconteceu na execução (Tela 4), vá para a **Tela 5** e clique em **Abrir Log**.
3. Se ainda estiver confuso, envie o log para o time de suporte (sem compartilhar tokens).

---

### Problema: “Notion não atualizou”
**Causas mais comuns:**
- Token do Notion errado/vazio no `notion_config.json`.
- Você não “compartilhou” a página/base com a integration.
- Database ID errado.

**Como resolver (passo a passo):**
1. Abra `notion_config.json` e confirme se o token começa com `secret_`.
2. No Notion, abra a página do HUB e vá em **Share** → confirme a integration.
3. Rode novamente.

---

### Problema: “Não identificamos projeto PBIP”
**Causa:** pasta errada.

**Como resolver:**
1. Volte à Tela 2.
2. Selecione a pasta que contém o arquivo `.pbip` e as pastas `.Report`/`.SemanticModel`.
3. Avance.

---

### Problema: “Falha de conexão com Power BI / XMLA”
**Causas mais comuns:**
- Connection string errada.
- Você não tem permissão de leitura do modelo.
- Workspace sem capacidade (Premium/PPU) para o tipo de conexão.

**Como resolver (objetivo):**
1. Confirme o `xmla_connection_string` no `pbi_config.json`.
2. Peça ao dono do workspace para confirmar suas permissões.
3. Tente novamente.

---

### Problema: “IA não enriqueceu as medidas”
**Causas mais comuns:**
- `use_ai_enrichment` está `false` no `pbi_config.json`.
- API key vazia/errada no `ai_config.json`.
- Limite/bloqueio de rede.

**Como resolver:**
1. Se você quer IA, confirme `use_ai_enrichment: true`.
2. Cole uma chave válida do Google AI Studio em `ai_config.json`.
3. Rode novamente.

---

### Problema: “A aplicação fechou” / “Travou”
**Checklist rápido:**
- Você está rodando a GUI a partir de uma pasta local do seu usuário? (não rede)
- Você tem internet estável?
- Você tem permissão no projeto Power BI?

**Como agir sem perder tempo:**
1. Abra a GUI de novo.
2. Faça a Tela 2 com calma (pasta PBIP correta).
3. Na Tela 5 (se chegar), clique em **Abrir Log** e envie para suporte.

---

## Boas práticas e segurança

- **NUNCA** publique tokens (`notion_api_key` / `api_key`) em GitHub.
- Se você compartilhar a pasta do projeto com alguém, **remova** as chaves dos `.json` antes.
- Evite pastas com sincronização agressiva (OneDrive/rede) durante a execução, para não corromper arquivos.
- Se você for rodar em vários projetos, crie uma pasta por projeto (organização evita erro humano).

---

### Versão do documento
- Atualizado em: **2025-12-15**
- Público-alvo: **usuário final (100% GUI)**
- Developer: **Jimmy**
- Área: **Data Management HAVAS Brazil**

