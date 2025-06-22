import json

def recomendar_filmes(preferencias, caminho_arquivo="filmes_db.json", limite=10):
    with open(caminho_arquivo, encoding="utf-8") as f:
        filmes = json.load(f)

    recomendacoes = []

    for filme in filmes:
        score = 0

        # Pontuar gêneros
        for genero in filme.get("genero", []):
            if genero.strip().capitalize() in preferencias["generos"]:
                score += 2

        # Pontuar tags
        for tag in filme.get("tags", []):
            if tag.strip().lower() in preferencias["tags"]:
                score += 1

        if score > 0:
            recomendacoes.append((score, filme))

    # Ordena pelos filmes mais relevantes
    recomendacoes.sort(reverse=True, key=lambda x: x[0])

    # Retorna apenas os filmes (sem o score)
    return [filme for _, filme in recomendacoes[:limite]]
