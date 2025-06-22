import json
import os
from questionario import coletar_preferencias
from recomendador import recomendar_filmes
from exportador import exportar_para_txt, exportar_para_pdf

CAMINHO_USUARIOS = "usuarios_db.json"
CAMINHO_FILMES = "filmes_db.json"

# Funções auxiliares
def carregar_usuarios():
    if os.path.exists(CAMINHO_USUARIOS) and os.path.getsize(CAMINHO_USUARIOS) > 0:
        with open(CAMINHO_USUARIOS, encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open(CAMINHO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def atualizar_status(usuario, usuarios, filme_id, status):
    usuarios[usuario]["status_filmes"][str(filme_id)] = status
    salvar_usuarios(usuarios)

def listar_filmes_por_status(usuario, usuarios, status_desejado, filmes_path=CAMINHO_FILMES):
    with open(filmes_path, encoding="utf-8") as f:
        filmes = json.load(f)

    status_filmes = usuarios[usuario]["status_filmes"]
    encontrados = []

    for filme in filmes:
        if str(filme["id"]) in status_filmes and status_filmes[str(filme["id"])] == status_desejado:
            encontrados.append(filme)

    if encontrados:
        print(f"\n🎯 Filmes com status '{status_desejado}':")
        for f in encontrados:
            print(f"- {f['titulo']}")
    else:
        print(f"\n⚠️ Nenhum filme com status '{status_desejado}'.")

# Execução principal
print("🔐 Bem-vindo ao Sistema de Recomendação de Filmes!")
usuario = input("Digite seu nome de usuário: ").strip().lower()
usuarios = carregar_usuarios()

# Cria novo perfil se necessário
if usuario not in usuarios:
    preferencias = coletar_preferencias()
    usuarios[usuario] = {
        "preferencias": preferencias,
        "status_filmes": {}
    }
    salvar_usuarios(usuarios)

# Recomendação
preferencias = usuarios[usuario]["preferencias"]
recomendacoes = recomendar_filmes(preferencias)

print("\n🎬 Filmes recomendados para você:")
for filme in recomendacoes:
    id_f = filme['id']
    titulo = filme['titulo']
    generos = ", ".join(filme.get("genero", []))
    print(f"[{id_f}] {titulo} ({generos})")

# Marcar status de filme
try:
    opc = input("\nDeseja marcar algum filme? (s/n): ").strip().lower()
    if opc == "s":
        filme_id = int(input("Digite o ID do filme: "))
        status = input("Status (ja_assisti, vou_assistir, nao_gostei): ").strip().lower()
        if status in ["ja_assisti", "vou_assistir", "nao_gostei"]:
            atualizar_status(usuario, usuarios, filme_id, status)
            print("✔️ Status atualizado com sucesso!")
        else:
            print("❌ Status inválido.")
except Exception as e:
    print(f"❌ Erro ao atualizar status: {e}")

# Ver lista por status
opc = input("\nDeseja ver sua lista de filmes? (s/n): ").strip().lower()
if opc == "s":
    print("1 - Filmes já assistidos")
    print("2 - Quero assistir")
    print("3 - Não gostei")
    escolha = input("Escolha a opção: ").strip()
    if escolha == "1":
        listar_filmes_por_status(usuario, usuarios, "ja_assisti")
    elif escolha == "2":
        listar_filmes_por_status(usuario, usuarios, "vou_assistir")
    elif escolha == "3":
        listar_filmes_por_status(usuario, usuarios, "nao_gostei")

# Exportar dados
opc = input("\nDeseja exportar sua lista? (s/n): ").strip().lower()
if opc == "s":
    print("1 - Exportar para .txt")
    print("2 - Exportar para .pdf")
    escolha = input("Escolha o formato: ").strip()
    if escolha == "1":
        exportar_para_txt(usuario, usuarios)
    elif escolha == "2":
        exportar_para_pdf(usuario, usuarios)

print("\n✅ Programa finalizado.")
