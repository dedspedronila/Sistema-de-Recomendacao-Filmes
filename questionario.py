def coletar_preferencias():
    print("🎯 QUESTIONÁRIO DE PREFERÊNCIAS")
    generos = input("Quais gêneros você gosta? (ex: Ação, Drama, Romance): ").split(",")
    tags = input("Cite temas/assuntos que você curte em filmes (ex: vingança, hacker, alienígenas): ").split(",")

    return {
        "generos": [g.strip().capitalize() for g in generos if g.strip()],
        "tags": [t.strip().lower() for t in tags if t.strip()]
    }
    