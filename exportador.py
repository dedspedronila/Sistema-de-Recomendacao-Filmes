import json
from fpdf import FPDF

def exportar_para_txt(usuario, usuarios, caminho="relatorio.txt"):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"Relatório do usuário: {usuario}\n")
        f.write("Filmes marcados:\n")
        for id_filme, status in usuarios[usuario]["status_filmes"].items():
            f.write(f"- ID {id_filme}: {status}\n")
    print(f"✅ Relatório TXT exportado para: {caminho}")

def exportar_para_pdf(usuario, usuarios, caminho="relatorio.pdf"):
    pdf = FPDF()
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Relatório de {usuario}", ln=True, align="L")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Filmes marcados:", ln=True)

    for id_filme, status in usuarios[usuario]["status_filmes"].items():
        pdf.cell(200, 10, txt=f"ID {id_filme}: {status}", ln=True)

    pdf.output(caminho)
    print(f"✅ Relatório PDF exportado para: {caminho}")
