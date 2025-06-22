# Sistema de Recomendacao de Filmes

Este projeto é um **Sistema de Recomendação de Filmes** desenvolvido em Python com Flask, utilizando técnicas de recomendação baseadas em preferências explícitas e Inteligência Artificial (IA semântica com Sentence Transformers).

---

## 🎯 Funcionalidades Principais

* Cadastro e login simples por nome de usuário (sem senha)
* Recomendação de filmes baseada em:

  * Gêneros e temas favoritos informados
  * Descrição em linguagem natural interpretada por IA
* Marcação de status dos filmes:

  * ✅ "Já assisti"
  * ⏲ "Quero assistir"
  * ❌ "Não gostei"
* Visualização das listas por status
* Exportação das listas em PDF
* Tradução automática de gêneros/temas do português para inglês

---

## 🧪 Tecnologias Utilizadas

* **Python 3.12**
* **Flask** (backend e rotas)
* **Bootstrap 5** (estilização)
* **FPDF** (geração de PDF)
* **SentenceTransformers** (IA semântica)
* **HTML5** (páginas frontend)

---

## 🗂️ Estrutura do Projeto

```
Projeto_Filmes/
├── web/
│   ├── templates/
│   │   ├── home.html
│   │   ├── preferencias.html
│   │   ├── recomendacoes.html
│   │   ├── recomendacoes_ia.html
│   │   ├── meus_filmes.html
│   │   ├── login.html
│   │   └── cadastro.html
│   └── app.py
├── data/
│   ├── filmes_db.json
│   └── usuarios_db.json
├── utils.py
├── recomendador.py
├── exportador.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/Sistema-de-Recomendacao-Filmes.git
cd Sistema-de-Recomendacao-Filmes
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate    # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python web/app.py
```

5. Acesse em seu navegador:

```
http://127.0.0.1:5000/
```

---

## 📚 Créditos e Observações

* Os dados de filmes utilizados estão em `filmes_db.json`
* O sistema funciona offline (sem dependência de banco de dados SQL)
* Projeto com fins **educacionais** e acadêmicos

---

## 👤 Autor

Desenvolvido por **André Pedronila** — Projeto educacional com fins de aprendizado e apresentação acadêmica.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para reutilizar com os devidos créditos.
