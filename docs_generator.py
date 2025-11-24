import os
import markdown
from xhtml2pdf import pisa

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
# Acha a pasta onde o script está
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o destino final
OUTPUT_DIR = r"C:\Scripts\_glb_projects\pbi_inventory_pipeline"
if not os.path.exists(OUTPUT_DIR):
    try: os.makedirs(OUTPUT_DIR)
    except: pass

# Diagrama Visual para o PDF (Inserido via código)
DIAGRAM_HTML = """
<div style="text-align: center; font-family: Helvetica; margin: 30px 0;">
    <div style="display:inline-block; padding:10px; border:1px solid #333; border-radius:5px; width:120px;"><b>1. Setup</b><br><span style="font-size:9px">Python + VS Code</span></div>
    <span style="font-size:20px; color:#FF5722"> ➡ </span>
    <div style="display:inline-block; padding:10px; border:1px solid #333; border-radius:5px; width:120px;"><b>2. Config</b><br><span style="font-size:9px">Notion Token</span></div>
    <span style="font-size:20px; color:#FF5722"> ➡ </span>
    <div style="display:inline-block; padding:10px; background:#FFF3E0; border:1px solid #FF9800; border-radius:5px; width:120px;"><b>3. Minerador</b><br><span style="font-size:9px">Lê PBIP</span></div>
    <span style="font-size:20px; color:#FF5722"> ➡ </span>
    <div style="display:inline-block; padding:10px; background:#E1F5FE; border:1px solid #039BE5; border-radius:5px; width:120px;"><b>4. Construtor</b><br><span style="font-size:9px">Cria Notion</span></div>
</div>
<hr>
"""

def generate_all():
    print("--- Iniciando Fábrica de Documentação (Modular) ---")

    # 1. Ler Arquivos Fonte
    file_md = os.path.join(SCRIPT_DIR, "conteudo_manual.md")
    file_html = os.path.join(SCRIPT_DIR, "template_apresentacao.html")
    
    if not os.path.exists(file_md) or not os.path.exists(file_html):
        print("❌ ERRO: Arquivos 'conteudo_manual.md' ou 'template_apresentacao.html' não encontrados em C:\\Scripts")
        return

    with open(file_md, "r", encoding="utf-8") as f: md_content = f.read()
    with open(file_html, "r", encoding="utf-8") as f: html_pres_content = f.read()

    # 2. Gerar Markdown Final (Cópia Simples)
    out_md = os.path.join(OUTPUT_DIR, "MANUAL_INSTRUCOES.md")
    with open(out_md, "w", encoding="utf-8") as f: f.write(md_content)
    print(f"✅ MD Gerado: {out_md}")

    # 3. Gerar HTML Apresentação (Cópia Simples)
    out_html = os.path.join(OUTPUT_DIR, "APRESENTACAO_GENESIS.html")
    with open(out_html, "w", encoding="utf-8") as f: f.write(html_pres_content)
    print(f"✅ HTML Gerado: {out_html}")

    # 4. Gerar PDF (Com CSS e Rodapé)
    print("⏳ Gerando PDF...")
    
    # Injeta Diagrama após o título
    md_for_pdf = md_content.replace("---", DIAGRAM_HTML, 1)
    
    html_body = markdown.markdown(md_for_pdf)
    
    # Rodapé
    footer = '<div id="footerContent">Developed by Data Management Team HAVAS Brazil 🇧🇷</div>'
    
    css = """
    <style>
        @page {
            size: A4; margin: 2cm;
            @frame footer_frame {
                -pdf-frame-content: footerContent;
                bottom: 1cm; margin-left: 1cm; margin-right: 1cm; height: 1cm;
            }
        }
        body { font-family: Helvetica, sans-serif; color: #333; line-height: 1.5; }
        h1 { color: #FF5722; border-bottom: 2px solid #FF5722; font-size: 24pt; }
        h2 { color: #039BE5; margin-top: 25px; font-size: 18pt; }
        h3 { color: #555; font-size: 14pt; margin-top: 20px; }
        code { background: #f4f4f4; font-family: Courier; color: #C62828; padding: 2px; border-radius: 3px; border: 1px solid #ddd; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; font-size: 9pt; white-space: pre-wrap; }
        blockquote { background: #FFF3E0; padding: 10px; border-left: 5px solid #FF9800; font-style: italic; }
        #footerContent { text-align: center; color: #888; font-size: 9pt; }
    </style>
    """
    
    full_html = f"<html><head>{css}</head><body>{html_body}{footer}</body></html>"
    
    out_pdf = os.path.join(OUTPUT_DIR, "MANUAL_INSTRUCOES.pdf")
    with open(out_pdf, "wb") as f:
        pisa_status = pisa.CreatePDF(full_html, dest=f)

    if not pisa_status.err: print(f"✅ PDF Gerado: {out_pdf}")
    else: print("❌ Erro no PDF")

if __name__ == "__main__":
    generate_all()