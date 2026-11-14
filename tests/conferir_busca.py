import json
import sys

sys.path.insert(0, "src")
from busca import buscar, carregar_sinonimos

with open("data/base_conhecimento.json", encoding="utf-8") as f:
    BASE = json.load(f)
SIN = carregar_sinonimos("data/sinonimos.json")

while True:
    pergunta = input("\nPergunta (digite 'sair' para encerrar): ")
    if pergunta.strip().lower() == "sair":
        break
    r = buscar(pergunta, BASE, SIN)
    print("status:", r["status"])
    for registro, nota in r["resultados"]:
        print(f"  {nota:.2f}  {registro['id']}  {registro.get('subtema')}")