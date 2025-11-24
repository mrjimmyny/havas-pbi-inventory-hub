import os
import json
import csv
import requests
from datetime import datetime
import sys
import time

# ==============================================================================
# CONFIGURAÇÕES (V28 - Page Unifier)
# ==============================================================================
NOTION_TOKEN = "COLE_SEU_TOKEN_AQUI"
DATABASE_ID = "COLE_SEU_ID_AQUI"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ==============================================================================
# 1. CARREGAMENTO E UNIFICAÇÃO
# ==============================================================================
def load_data():
    print("--- 1. Carregando Dados (V28) ---")
    if not os.path.exists("pbi_config.json"): sys.exit("[ERRO] pbi_config.json ausente.")
    if not os.path.exists("model_structure.json"): sys.exit("[ERRO] model_structure.json ausente.")

    with open("pbi_config.json", "r", encoding="utf-8") as f: config = json.load(f)
    with open("model_structure.json", "r", encoding="utf-8") as f: structure = json.load(f)
    
    descriptions = {}
    if os.path.exists("measures_enriched.csv"):
        with open("measures_enriched.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean = {k.strip(): v.strip() for k, v in row.items() if k and v}
                if "global_id" in clean: descriptions[clean["global_id"]] = clean.get("description", "")

    # --- UNIFICAÇÃO INTELIGENTE DE PÁGINAS ---
    # Cria um dicionário mestre de páginas para garantir unicidade
    # Chave: Nome da Página -> Valor: Lista de Visuais únicos
    unified_pages = {}

    # 1. Carrega do Report Structure (Vindo do Minerador)
    raw_pages = structure.get("report_structure", [])
    for p in raw_pages:
        p_name = p.get("name", "Geral")
        if p_name not in unified_pages: unified_pages[p_name] = []
        
        # Adiciona visuais evitando duplicatas de ID
        current_ids = {v["id"] for v in unified_pages[p_name]}
        for v in p.get("visuals", []):
            if v["id"] not in current_ids:
                unified_pages[p_name].append(v)
                current_ids.add(v["id"])

    # 2. Carrega das Medidas (Fallback para garantir que nada foi perdido)
    # Se uma medida diz que está na página "X" e "X" não existe, cria ela.
    for m in structure["measures"]:
        vis_details = m.get("visual_details", [])
        for v in vis_details:
            p_name = v["page"]
            if p_name not in unified_pages: unified_pages[p_name] = []
            
            # Reconstrói o objeto visual a partir do detalhe da medida
            # (É uma aproximação, pois o detalhe da medida é simplificado)
            v_obj = {
                "id": v["id"],
                "type": v["type"],
                "measures": [m["name"]] # Começa só com essa medida
            }
            
            # Verifica se esse visual já existe na página
            # Se existir, adiciona a medida a ele. Se não, cria.
            found = False
            for existing_v in unified_pages[p_name]:
                if existing_v["id"] == v["id"]:
                    if m["name"] not in existing_v["measures"]:
                        existing_v["measures"].append(m["name"])
                    found = True
                    break
            
            if not found:
                unified_pages[p_name].append(v_obj)

    # Injeta de volta na estrutura para uso nos builders
    structure["unified_pages"] = unified_pages
    
    # Enriquece medidas (descrições)
    for m in structure["measures"]:
        m["desc"] = descriptions.get(m["global_id"], "Descrição pendente.")
        m["visual_text"] = "Sim" if m.get("in_visual") else "Não"

    print(f"> Páginas unificadas para processamento: {len(unified_pages)}")
    return config, structure

# ==============================================================================
# 2. API HELPERS
# ==============================================================================
def create_sub_page(parent_id, title, blocks=[]):
    url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"page_id": parent_id}, "properties": {"title": [{"text": {"content": title}}]}, "children": blocks}
    try: return requests.post(url, headers=HEADERS, json=payload).json()["id"]
    except: return None

def create_inline_db(parent_id, title, properties):
    url = "https://api.notion.com/v1/databases"
    payload = {"parent": {"page_id": parent_id}, "title": [{"type": "text", "text": {"content": title}}], "properties": properties, "is_inline": True}
    try: return requests.post(url, headers=HEADERS, json=payload).json()["id"]
    except: return None

def add_row_heavy(db_id, props, children_blocks, name="Row"):
    url_create = "https://api.notion.com/v1/pages"
    payload_create = {"parent": {"database_id": db_id}, "properties": props}
    
    page_id = None
    for _ in range(3):
        try:
            r = requests.post(url_create, headers=HEADERS, json=payload_create)
            if r.status_code == 200: 
                page_id = r.json()["id"]; break
            elif r.status_code == 429: time.sleep(5)
            else: time.sleep(1)
        except: time.sleep(1)
    
    if not page_id: return print(f"❌ Erro criar: {name}")

    if children_blocks:
        url_app = f"https://api.notion.com/v1/blocks/{page_id}/children"
        batch = 30
        for i in range(0, len(children_blocks), batch):
            req_batch = children_blocks[i:i+batch]
            for _ in range(3):
                try:
                    r = requests.patch(url_app, headers=HEADERS, json={"children": req_batch})
                    if r.status_code == 200: break
                    elif r.status_code == 429: time.sleep(5)
                    else: time.sleep(1)
                except: time.sleep(1)

# Builders
def mk_p(t): return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": t[:1900]}}]}}
def mk_code(t): return {"object": "block", "type": "code", "code": {"language": "markdown", "rich_text": [{"type": "text", "text": {"content": t[:1900]}}]}}
def mk_head(t, lvl=3): 
    if lvl > 3: lvl = 3
    return {"object": "block", "type": f"heading_{lvl}", f"heading_{lvl}": {"rich_text": [{"type": "text", "text": {"content": t[:1900]}}]}}
def mk_li(t): return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": t[:1900]}}]}}
def mk_div(): return {"object": "block", "type": "divider", "divider": {}}

def create_table_block(headers, rows):
    tb = {"object": "block", "type": "table", "table": {"table_width": len(headers), "has_column_header": True, "children": []}}
    tb["table"]["children"].append({"type": "table_row", "table_row": {"cells": [[{"type": "text", "text": {"content": h}}] for h in headers]}})
    for r in rows:
        cells = [[{"type": "text", "text": {"content": str(c)[:1900]}}] for c in r]
        tb["table"]["children"].append({"type": "table_row", "table_row": {"cells": cells}})
    return tb

def archive_old_entries(project_name):
    print("--- 2. Limpando Notion ---")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"filter": {"property": "Project Name", "title": {"equals": project_name}}}
    try:
        resp = requests.post(url, headers=HEADERS, json=payload)
        for p in resp.json().get("results", []):
            requests.patch(f"https://api.notion.com/v1/pages/{p['id']}", headers=HEADERS, json={"archived": True})
    except: pass

# ==============================================================================
# 3. BUILDER
# ==============================================================================
def build_structure(config, structure):
    print("--- 3. Construindo V28 (Final Corrected) ---")
    
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Project Name": {"title": [{"text": {"content": config['project_name']}}]},
            "Project Link": {"url": config['project_link']},
            "Last Update": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
        }
    }
    main_id = requests.post(url, headers=HEADERS, json=payload).json()["id"]
    print(f"> Capa criada.")

    # 1. RELACIONAMENTOS
    print("> DB 1: Relacionamentos")
    db_rel = create_inline_db(main_id, "1. Relacionamentos", {
        "ID": {"title": {}}, "De": {"rich_text": {}}, "Para": {"rich_text": {}}, 
        "Cardinalidade": {"select": {}}, "Direção": {"select": {}}
    })
    if db_rel:
        for i, r in enumerate(structure.get("relationships", [])):
            add_row_heavy(db_rel, {
                "ID": {"title": [{"text": {"content": f"R{i+1}"}}]},
                "De": {"rich_text": [{"text": {"content": r.get('from','?')}}]},
                "Para": {"rich_text": [{"text": {"content": r.get('to','?')}}]},
                "Cardinalidade": {"select": {"name": r.get('cardinality', '-')}},
                "Direção": {"select": {"name": r.get('filter', '-')}}
            }, [])

    # 2. TABELAS
    print("> DB 2: Tabelas")
    db_tbl = create_inline_db(main_id, "2. Tabelas", {"Nome": {"title": {}}})
    IGNORE = ["_DAX", "_DAX_AUDIT", "DAX", "_TEST"]
    if db_tbl:
        for t_name, t_data in sorted(structure.get("tables", {}).items()):
            if any(ign in t_name for ign in IGNORE): continue
            body = []
            cols = t_data.get("columns", [])
            if cols:
                body.append(mk_p(f"Colunas ({len(cols)}):"))
                h = ["Coluna", "Origem", "Tipo"]
                rs = [[c['name'], c.get('origin','Física'), c['type']] for c in cols]
                if len(rs)>90: rs = rs[:90]
                body.append(create_table_block(h, rs))
            add_row_heavy(db_tbl, {"Nome": {"title": [{"text": {"content": t_name}}]}}, body, t_name)

    # 3. PÁGINAS (CORRIGIDO COM UNIFICAÇÃO)
    print("> DB 3: Páginas (Unified)")
    db_pg = create_inline_db(main_id, "3. Páginas do Relatório", {
        "Página": {"title": {}}, "Qtd Visuais": {"number": {}}
    })
    
    unified_pages = structure.get("unified_pages", {})
    
    if db_pg:
        for p_name, vis_list in sorted(unified_pages.items()):
            # Corpo: Tabela de Visuais
            body = [mk_head(f"Visuais nesta página ({len(vis_list)}):", 3)]
            
            if vis_list:
                # Agrupa por Tipo para ficar bonito
                # Tipo | Qtd | Medidas
                h = ["Tipo Visual", "Qtd", "Medidas"]
                rs = []
                for v in vis_list:
                    m_len = len(v["measures"])
                    m_str = ", ".join(v["measures"])
                    # Corta string se for absurda
                    if len(m_str) > 100: m_str = m_str[:100] + "..."
                    rs.append([v["type"], str(m_len), m_str])
                
                if len(rs) > 90: rs = rs[:90]
                body.append(create_table_block(h, rs))
            else:
                body.append(mk_p("Nenhum visual com medidas detectado."))

            add_row_heavy(db_pg, {
                "Página": {"title": [{"text": {"content": p_name}}]},
                "Qtd Visuais": {"number": len(vis_list)}
            }, body, p_name)

    # 4. VISUAIS (Agregado por Tipo)
    print("> DB 4: Tipos de Visuais")
    db_vis = create_inline_db(main_id, "4. Visuais Detalhados", {
        "Tipo": {"title": {}}, "Qtd Páginas": {"number": {}}
    })
    
    # Agrega por Tipo a partir do Unified
    type_map = {}
    for p_name, v_list in unified_pages.items():
        for v in v_list:
            vt = v["type"]
            if vt not in type_map: type_map[vt] = set()
            type_map[vt].add(p_name)
            
    if db_vis:
        for v_type, pages in type_map.items():
            body = [mk_head("Presente nas Páginas:", 3)]
            for pg in sorted(list(pages)): body.append(mk_li(pg))
            
            add_row_heavy(db_vis, {
                "Tipo": {"title": [{"text": {"content": v_type}}]},
                "Qtd Páginas": {"number": len(pages)}
            }, body, v_type)

    # 5. DAX
    print("> DB 5: Medidas DAX")
    db_dax = create_inline_db(main_id, "5. Medidas DAX", {
        "Nome": {"title": {}}, "ID": {"rich_text": {}}, "Status": {"select": {}}, "Visual?": {"select": {}}
    })
    
    if db_dax:
        total = len(structure["measures"])
        for i, m in enumerate(structure["measures"]):
            status = m.get('status', 'Analise')
            
            body = [
                mk_head("📖 Descrição", 3), mk_p(m['desc']), mk_div(),
                mk_head("💻 Código DAX", 3), mk_code(m['dax']), mk_div(),
                mk_head("📄 Uso em Visuais", 3)
            ]
            
            # Busca na estrutura unificada onde essa medida aparece
            found_in_pages = []
            for p_name, v_list in unified_pages.items():
                for v in v_list:
                    if m["name"] in v["measures"]:
                        found_in_pages.append(f"Pág: {p_name} | {v['type']}")
            
            if found_in_pages:
                for fp in sorted(list(set(found_in_pages))): body.append(mk_li(fp))
            else:
                body.append(mk_p("Sem uso direto."))

            body.append(mk_div())
            body.append(mk_head("🔗 Pais", 3))
            if m.get('parent_names'): 
                for x in m.get('parent_names'): body.append(mk_li(x))
            else: body.append(mk_p("-"))
            
            body.append(mk_head("🌲 Filhos", 3))
            if m.get('child_names'):
                for x in m.get('child_names'): body.append(mk_li(x))
            else: body.append(mk_p("-"))

            time.sleep(0.1)
            add_row_heavy(db_dax, {
                "Nome": {"title": [{"text": {"content": m['name']}}]},
                "ID": {"rich_text": [{"text": {"content": m['global_id']}}]},
                "Status": {"select": {"name": status}},
                "Visual?": {"select": {"name": m['visual_text']}}
            }, body, m['name'])
            
            if (i+1) % 50 == 0: print(f"  - {i+1}/{total}...")

    print("\n✨ SUCESSO TOTAL! ✨")

if __name__ == "__main__":
    conf, struct = load_data()
    archive_old_entries(conf['project_name'])
    build_structure(conf, struct)