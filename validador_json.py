import json
import os

def validar_json(caminho):
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        return False
    try:
        with open(caminho, encoding="utf-8") as f:
            json.load(f)
        print(f"✅ JSON válido: {caminho}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {caminho} — erro: {e}")
        return False
