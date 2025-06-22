from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from sentence_transformers import SentenceTransformer, util
import torch
from flask import make_response
from fpdf import FPDF
from flask import flash, render_template


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Caminhos dos dados
CAMINHO_FILMES = "../filmes_db.json"
CAMINHO_USUARIOS = "../usuarios_db.json"

# Dicionários de tradução
MAPA_GENEROS = {
    "ação": "Action",
    "drama": "Drama",
    "comédia": "Comedy",
    "romance": "Romance",
    "aventura": "Adventure",
    "ficção científica": "Sci-Fi",
    "terror": "Horror",
    "animação": "Animation",
    "documentário": "Documentary",
    "mistério": "Mystery",
    "crime": "Crime",
    "fantasia": "Fantasy",
    "thriller": "Thriller"
}

MAPA_TAGS = {
    "vingança": "revenge",
    "futurista": "futuristic",
    "distopia": "dystopia",
    "hacker": "hacker",
    "alienígena": "alien",
    "guerra": "war",
    "amor proibido": "forbidden love",
    "ação rápida": "fast-paced",
    "zumbis": "zombies",
    "inteligência artificial": "artificial intelligence",
    "universo paralelo": "parallel universe"
}

# Utilitários
def carregar_filmes():
    with open(CAMINHO_FILMES, encoding='utf-8') as f:
        return json.load(f)

def carregar_usuarios():
    if os.path.exists(CAMINHO_USUARIOS):
        with open(CAMINHO_USUARIOS, encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open(CAMINHO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def recomendar_filmes(preferencias, filmes):
    recomendados = []
    for filme in filmes:
        score = 0
        for genero in filme.get("genero", []):
            if genero.strip().capitalize() in preferencias["generos"]:
                score += 2
        for tag in filme.get("tags", []):
            if tag.strip().lower() in preferencias["tags"]:
                score += 1
        if score > 0:
            recomendados.append((score, filme))
    recomendados.sort(reverse=True, key=lambda x: x[0])
    return [f for _, f in recomendados[:10]]

# Funções de tradução
def traduzir_generos_pt_en(lista_pt):
    return [MAPA_GENEROS.get(g.lower().strip(), g.strip().capitalize()) for g in lista_pt]

def traduzir_tags_pt_en(lista_pt):
    return [MAPA_TAGS.get(t.lower().strip(), t.strip().lower()) for t in lista_pt]

# Rotas
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/preferencias')
def preferencias_form():
    return render_template("preferencias.html")

@app.route('/preferencias/enviar', methods=["POST"])
def preferencias():
    nome = request.form["nome"].strip().lower()
    generos_originais = request.form["generos"].split(",")
    tags_originais = request.form["tags"].split(",")

    generos_traduzidos = traduzir_generos_pt_en(generos_originais)
    tags_traduzidas = traduzir_tags_pt_en(tags_originais)

    preferencias = {
        "generos": generos_traduzidos,
        "tags": tags_traduzidas
    }

    usuarios = carregar_usuarios()

    # Verifica se o usuário quer excluir preferências anteriores
    excluir = request.form.get("excluir_preferencias") == "1"
    if nome not in usuarios or excluir:
        usuarios[nome] = {
            "preferencias": preferencias,
            "status_filmes": {}  # zera status caso exclua
        }
    else:
        usuarios[nome]["preferencias"] = preferencias  # mantém status antigos

    salvar_usuarios(usuarios)
    session["usuario"] = nome
    return redirect(url_for("recomendacoes"))

@app.route('/recomendacoes')
def recomendacoes():
    nome = session.get("usuario")
    if not nome:
        return redirect(url_for("login"))

    usuarios = carregar_usuarios()
    preferencias = usuarios[nome]["preferencias"]
    filmes = carregar_filmes()
    recomendados = recomendar_filmes(preferencias, filmes)

    return render_template("recomendacoes.html", nome=nome, filmes=recomendados)

@app.route('/marcar_status', methods=["POST"])
def marcar_status():
    nome = session.get("usuario")
    if not nome:
        return redirect(url_for("login"))

    filme_id = request.form["filme_id"]
    status = request.form["status"]

    usuarios = carregar_usuarios()
    if nome in usuarios:
        usuarios[nome]["status_filmes"][filme_id] = status
        salvar_usuarios(usuarios)

    return redirect(url_for("recomendacoes"))

# === Integração com IA semântica ===
modelo_ia = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@app.route("/ia")
def ia_interface():
    return render_template("ia.html")

@app.route("/ia/recomendar", methods=["POST"])
def ia_recomendar():
    descricao_usuario = request.form["preferencias"]
    filmes = carregar_filmes()

    vetor_usuario = modelo_ia.encode(descricao_usuario, convert_to_tensor=True)

    textos_filmes = []
    for filme in filmes:
        texto = f"{filme['titulo']} {' '.join(filme.get('genero', []))} {' '.join(filme.get('tags', []))}"
        textos_filmes.append(texto)

    vetores_filmes = modelo_ia.encode(textos_filmes, convert_to_tensor=True)

    similaridades = util.cos_sim(vetor_usuario, vetores_filmes)[0]
    indices_ordenados = torch.topk(similaridades, k=10).indices
    recomendados = [filmes[i] for i in indices_ordenados]

    return render_template("recomendacoes_ia.html", filmes=recomendados, descricao=descricao_usuario)

@app.route('/meus-filmes')
def meus_filmes():
    nome = session.get("usuario")
    if not nome:
        return redirect(url_for("login"))

    usuarios = carregar_usuarios()
    filmes = carregar_filmes()
    status_filmes = usuarios[nome].get("status_filmes", {})

    categorias = {
        "ja_assisti": [],
        "vou_assistir": [],
        "nao_gostei": []
    }

    for filme in filmes:
        filme_id = str(filme["id"])
        status = status_filmes.get(filme_id)
        if status in categorias:
            categorias[status].append(filme)

    return render_template("meus_filmes.html", nome=nome, categorias=categorias)

@app.route('/meus-filmes/pdf')

def gerar_pdf():

    nome = session.get("usuario")
    if not nome:
        return redirect(url_for("login"))


    usuarios = carregar_usuarios()
    filmes = carregar_filmes()
    status_filmes = usuarios[nome].get("status_filmes", {})

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Listas de Filmes - {nome}", ln=True, align="C")

    def adicionar_secao(titulo, status):
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=titulo, ln=True)
        pdf.set_font("Arial", size=11)
        for filme in filmes:
            if status_filmes.get(str(filme["id"])) == status:
                # Remove emojis e substitui bullet por hífen
                titulo_limpo = filme["titulo"].encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(200, 8, txt=f"- {titulo_limpo}", ln=True)

    adicionar_secao("Ja assisti", "ja_assisti")
    adicionar_secao("Quero assistir", "vou_assistir")
    adicionar_secao("Nao gostei", "nao_gostei")

    response = make_response(pdf.output(dest='S').encode('latin-1', 'ignore'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=meus_filmes.pdf'
    return response

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['username'].strip().lower()
        senha = request.form['senha'].strip()

        usuarios = carregar_usuarios()
        if nome in usuarios and usuarios[nome].get("senha") == senha:
            session["usuario"] = nome
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
            return render_template("login.html")

    return render_template("login.html")

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['username'].strip().lower()
        senha = request.form['senha'].strip()

        usuarios = carregar_usuarios()
        if nome in usuarios:
            flash("Nome de usuário já cadastrado.", "warning")
            return redirect(url_for("cadastro"))

        usuarios[nome] = {
            "senha": senha,
            "preferencias": {},
            "status_filmes": {}
        }
        salvar_usuarios(usuarios)
        session["usuario"] = nome
        return redirect(url_for("index"))

    return render_template("cadastro.html")

# Rota de logout
@app.route('/logout')
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
