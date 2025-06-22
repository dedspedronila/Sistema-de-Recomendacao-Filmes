import json
import os
from questionario import coletar_preferencias
from recomendador import recomendar_filmes
from exportador import exportar_para_txt, exportar_para_pdf
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

CAMINHO_USUARIOS = "usuarios_db.json"
CAMINHO_FILMES = "filmes_db.json"

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
        console.rule(f"[bold blue]🎯 Filmes com status '{status_desejado}'")
        for f in encontrados:
            console.print(f"- {f['titulo']}", style="green")
    else:
        console.print(f"\n⚠️ Nenhum filme com status '{status_desejado}'.", style="yellow")

# Início
console.rule("[bold magenta]🔐 Bem-vindo ao Sistema de Recomendação de Filmes")

usuario = Prompt.ask("Digite seu nome de usuário").strip().lower()
usuarios = carregar_usuarios()

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

console.rule("[bold green]🎬 Filmes recomendados para você")

table = Table(title="🎯 Recomendações", header_style="bold magenta")
table.add_column("ID", justify="center", style="cyan")
table.add_column("Título", style="yellow")
table.add_column("Gêneros", style="green")

for filme in recomendacoes:
    table.add_row(str(filme['id']), filme['titulo'], ", ".join(filme.get("genero", [])))

console.print(table)

# Marcar status
opc = Prompt.ask("\nDeseja marcar algum filme?", choices=["s", "n"], default="n")
if opc == "s":
    try:
        filme_id = int(Prompt.ask("Digite o ID do filme"))
        status = Prompt.ask("Status", choices=["ja_assisti", "vou_assistir", "nao_gostei"])
        atualizar_status(usuario, usuarios, filme_id, status)
        console.print("✔️ Status atualizado com sucesso!", style="bold green")
    except Exception as e:
        console.print(f"❌ Erro ao atualizar status: {e}", style="bold red")

# Ver lista por status
opc = Prompt.ask("\nDeseja ver sua lista de filmes?", choices=["s", "n"], default="n")
if opc == "s":
    console.print("1 - Filmes já assistidos", style="cyan")
    console.print("2 - Quero assistir", style="cyan")
    console.print("3 - Não gostei", style="cyan")
    escolha = Prompt.ask("Escolha a opção", choices=["1", "2", "3"])
    if escolha == "1":
        listar_filmes_por_status(usuario, usuarios, "ja_assisti")
    elif escolha == "2":
        listar_filmes_por_status(usuario, usuarios, "vou_assistir")
    elif escolha == "3":
        listar_filmes_por_status(usuario, usuarios, "nao_gostei")

# Exportar dados
opc = Prompt.ask("\nDeseja exportar sua lista?", choices=["s", "n"], default="n")
if opc == "s":
    console.print("1 - Exportar para .txt", style="cyan")
    console.print("2 - Exportar para .pdf", style="cyan")
    escolha = Prompt.ask("Escolha o formato", choices=["1", "2"])
    if escolha == "1":
        exportar_para_txt(usuario, usuarios)
    elif escolha == "2":
        exportar_para_pdf(usuario, usuarios)

console.rule("[bold cyan]✅ Programa finalizado.")
