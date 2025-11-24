# 📘 Protocolo Management Data: Operation Setup
### 🚀 Automação de Inventário - Projetos Power BI Versão 2.0 Elite (Nov/2025)

---

## 0. 🎯 O Briefing: Bem-vindo à Elite

> *"Eu escolho uma pessoa preguiçosa para fazer um trabalho difícil. Porque ela encontrará uma maneira fácil de fazê-lo."* — **Bill Gates** 🧠

Se você está lendo isso, parabéns. Você cansou de fazer trabalho repetitivo e decidiu se tornar o **Comandante dos Dados**.

O que vamos fazer aqui não é apenas "rodar um script". Nós vamos instalar uma **Pipeline de Engenharia de Dados** que vai entrar no cérebro do seu Power BI, mapear cada veia, cada artéria, e cuspir um Raio-X completo no seu Notion.

**O Resultado?** Uma documentação viva, que se atualiza sozinha, com Tabelas, Relacionamentos, DAX e Visuais mapeados.

Respire fundo, pegue seu café ☕. A jornada começa agora.

---

## 1. ⚠️ Checklist de Decolagem (Pré-Requisitos)

> *"Dê-me seis horas para derrubar uma árvore e passarei as quatro primeiras afiando o machado."* — **Abraham Lincoln** 🪓

Antes de pilotar, verifique os instrumentos. Sem isso, o sistema não roda:

* ✅ **Acesso de Administrador:** Você precisará criar pastas.
* ✅ **Conta no Notion:** Pode ser a gratuita. [Crie aqui](https://www.notion.so/).
* ✅ **Conta no GitHub:** Para baixar atualizações. [Acesse aqui](https://github.com/).
* ✅ **Projeto Power BI (.PBIP):** Seu arquivo PBIX deve estar salvo no formato moderno "Projeto do Power BI".

---

## 2. 🧰 O Arsenal (Setup do Ambiente)

Vamos instalar o motor (Python) e o painel de controle (VS Code).

### A. 🐍 Python (O Motor)

O Python é o cérebro que vai ler os arquivos.

1.  Baixe a versão mais recente: [python.org/downloads](https://www.python.org/downloads/)
2.  Rode o instalador.
3.  🛑 **PARE TUDO AGORA!** Na primeira tela, marque a caixinha:
    **[x] Add Python to PATH**
    *(Se não marcar isso, nada funciona).*
4.  Clique em "Install Now".

> 📺 **Reforço Tático:** [Vídeo Sugerido: Instalação Python 2025](https://www.youtube.com/results?search_query=como+instalar+python+windows+2025)


### B. 💻 O Editor (O Painel)

Recomendamos o **VS Code**. Se você já é um Jedi do Python, use o que preferir.

1.  Baixe e instale: [code.visualstudio.com](https://code.visualstudio.com/)
2.  Abra o VS Code.
3.  No menu lateral esquerdo (ícone de quadrados), instale a extensão **"Python"** da Microsoft.

> 📺 **Reforço Tático:** [Vídeo Sugerido: VS Code para Iniciantes](https://www.youtube.com/results?search_query=vscode+para+iniciantes)


---

## 3. 🔑 A Chave Mestra (Configurando o Notion)

> *"Com grandes poderes vêm grandes responsabilidades."* — **Tio Ben** 🕷️

O script precisa de um crachá para entrar no seu Notion.

1.  **Crie o Robô:** Vá em [notion.so/my-integrations](https://www.notion.so/my-integrations).
    * Clique em **New integration**.
    * Nome: `Robo_Inventario_BI`.
    * Clique em **Submit**.
    * 🔐 **COPIE O TOKEN** (Começa com `ntn_...`). Guarde essa senha!

2.  **Destrave a Porta (O Pulo do Gato):**
    * Crie uma página nova no seu Notion chamada **"HUB Inventários BI"**.
    * No canto superior direito, clique nos **3 pontinhos (...)**.
    * Vá em **Connections** (ou "Connect to").
    * Procure por `Robo_Inventario_BI` e confirme.
    * *Sem isso, o robô bate na porta e ninguém abre.*

3.  **Pegue o Endereço (ID):**
    * Com a página aberta, copie o Link do navegador.
    * O ID é a sequência de 32 caracteres no final.
    * Exemplo: `notion.so/HUB...1a2b3c4d5e6f78901234567890abcdef` -> O ID é **`1a2b3c4d5e6f78901234567890abcdef`**.

---

## 4. 📂 O QG (Organização é Vida)

> *"Para cada minuto gasto organizando, ganha-se uma hora."* — **Benjamin Franklin** ⏳

O TI da sua empresa bloqueia o disco `C:\`? Não tem problema.

**Escolha seu Caminho:**

* 🛡️ **Rota Segura (Recomendada):** Vá em **Meus Documentos** e crie uma pasta chamada `Automacao_BI`.
* ⚔️ **Rota Hardcore (Raiz):** Crie `C:\Scripts` (Se tiver permissão).

**Ação:** Mova os arquivos `minerador_pbi.py` e `constructor_notion.py` (que você baixou do GitHub) para dentro dessa pasta.

---

## 5. ⚙️ O Combustível (Configuração)

1.  Vá até a pasta do seu **PROJETO POWER BI** (`.pbip`).
2.  Crie um arquivo de texto chamado `pbi_config.json`.
3.  Cole isso dentro dele (use o Bloco de Notas):

```json
{
    "project_name": "Nome do Projeto",
    "project_link": ""
}
Edite o Script: Abra o constructor_notion.py e cole seu Token e ID nas linhas indicadas no topo. Salve.

6. 🚀 O Lançamento (Hora da Verdade)
Abra o VS Code.

Vá em File > Open Folder e abra a pasta do seu Projeto Power BI.

Abra o Terminal (Ctrl + ').

Primeira vez? Digite pip install requests e dê Enter.

Missão 1: Minerar os Dados ⛏️

Digite o caminho do script e dê Enter:

PowerShell

python "C:\Users\SeuUsuario\Documents\Automacao_BI\minerador_pbi.py"
(Espere aparecer: "MINERADOR CONCLUÍDO")

Missão 2: Construir o Império 🏗️

Digite:

PowerShell

python "C:\Users\SeuUsuario\Documents\Automacao_BI\constructor_notion.py"
(Espere aparecer: "SUCESSO FINAL")

🏁 7. Debriefing
Corra para o Notion. 🏃‍♂️💨 Você verá todas as informações do Inventário, contendo toda a inteligência do seu projeto.

Você venceu. Agora vá tomar um café, você mereceu. ☕😎

Developed by Data Management Team HAVAS Brazil 🇧🇷