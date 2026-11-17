"""Avalia a busca com tests/perguntas_teste.json.

Mede, para cada pergunta: status obtido, registro em 1o lugar, acerto/erro e
tempo. No final mostra a taxa de acerto (geral e por categoria) e o tempo medio.

Execucao (na raiz do repositorio): python tests/avaliar_busca.py
"""

import json
import sys
import time
from collections import defaultdict

sys.path.insert(0, "src")
from busca import buscar, carregar_sinonimos

REPETICOES = 200  # a busca é muito rápida; repetir dá um tempo médio estável

with open("data/base_conhecimento.json", encoding="utf-8") as f:
    BASE = json.load(f)
with open("tests/perguntas_teste.json", encoding="utf-8") as f:
    PERGUNTAS = json.load(f)
SIN = carregar_sinonimos("data/sinonimos.json")


def avaliar(item: dict) -> dict:
    """Roda uma pergunta e compara com o esperado."""
    inicio = time.perf_counter()
    for _ in range(REPETICOES):
        resposta = buscar(item["pergunta"], BASE, SIN)
    tempo_ms = (time.perf_counter() - inicio) / REPETICOES * 1000

    status = resposta["status"]
    topo = resposta["resultados"][0][0]["id"] if resposta["resultados"] else None

    acertou = status == item["esperado_status"]
    if acertou and item["esperado_id"] is not None:
        acertou = topo == item["esperado_id"]

    return {
        "id": item["id"],
        "categoria": item["categoria"],
        "pergunta": item["pergunta"],
        "esperado": f"{item['esperado_status']} {item['esperado_id'] or ''}".strip(),
        "obtido": f"{status} {topo or ''}".strip(),
        "acertou": acertou,
        "tempo_ms": tempo_ms,
    }


resultados = [avaliar(item) for item in PERGUNTAS]

print(f"{'ID':<5}{'categoria':<24}{'esperado':<18}{'obtido':<18}{'ok?':<5}{'ms':>8}")
for r in resultados:
    marca = "OK" if r["acertou"] else "ERRO"
    print(f"{r['id']:<5}{r['categoria']:<24}{r['esperado']:<18}{r['obtido']:<18}{marca:<5}{r['tempo_ms']:>8.3f}")

total = len(resultados)
acertos = sum(r["acertou"] for r in resultados)
print(f"\nAcerto geral: {acertos}/{total} = {acertos / total:.0%}")

por_categoria = defaultdict(list)
for r in resultados:
    por_categoria[r["categoria"]].append(r["acertou"])
for categoria, lista in por_categoria.items():
    print(f"  {categoria:<24}{sum(lista)}/{len(lista)} = {sum(lista) / len(lista):.0%}")

tempo_medio = sum(r["tempo_ms"] for r in resultados) / total
print(f"\nTempo médio por busca: {tempo_medio:.3f} ms (média de {REPETICOES} execuções por pergunta)")

erros = [r for r in resultados if not r["acertou"]]
if erros:
    print("\nPerguntas que falharam (material para a seção de limitações do README):")
    for r in erros:
        print(f"  {r['id']}: \"{r['pergunta']}\" -> esperado [{r['esperado']}], obtido [{r['obtido']}]")