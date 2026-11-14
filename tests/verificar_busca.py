import sys
sys.path.insert(0, "src")
from busca import normalizar, tokenizar, jaccard, buscar, expandir, carregar_sinonimos

"""Assert serve para verificar se uma suposição é verdadeira, caso seja falsa ele encerra o programa com um erro. No caso abaixo ele verifica se a normalização está funcionando."""

assert normalizar("Perdi meu RG na enchente!") == "perdi meu rg na enchente"
assert normalizar("SÃO PAULO ") == "sao paulo"
assert normalizar("são-paulo") == "sao paulo"
assert normalizar("ção") == "cao"
assert normalizar("rg,identidade") == "rg identidade"
assert normalizar("") == ""
assert normalizar("   ") == ""
assert normalizar("RG    rg") == "rg rg"

print("2ª via ->", repr(normalizar("2ª via")))   # só observar

"""Verifica as tokenizações."""

assert tokenizar("Como tirar a segunda via do meu RG?") == {"tirar", "segunda", "via", "rg"}
assert tokenizar("o de a?") == set()
assert type(tokenizar("o de a?")) is set
assert tokenizar("RG rg Rg") == {"rg"}
assert tokenizar("Você precisa") == {"precisa"}
assert tokenizar("não consigo sair") == {"nao", "consigo", "sair"}

A = {"perdi", "rg"}
B = {"rg", "identidade", "segunda", "via"}

"""Verifica a similaridade de Jaccard."""

assert jaccard(A, B) == 0.2
assert jaccard(A, B) == jaccard(B, A)
assert jaccard({"a","b"}, {"a","b"}) == 1.0
assert jaccard({"a"}, {"b"}) == 0.0
assert jaccard(set(), set()) == 0.0
assert jaccard(set(), {"a"}) == 0.0
assert round (jaccard({"fgts", "saque"}, {"fgts", "saque", "calamidade"}), 2) == 0.67   
assert isinstance(jaccard(A, B), float)


import json

with open("data/base_conhecimento.json", encoding="utf-8") as f:
    BASE = json.load(f)

r = buscar("perdi meu RG na enchente", BASE, {})
assert r["status"] == "ok"
assert r["resultados"][0][0]["id"] == "DOC-03"

r = buscar("como tirar segunda via do CPF?", BASE, {})
assert r["resultados"][0][0]["id"] == "DOC-02"

r = buscar("quero sacar o FGTS", BASE, {})
assert r["resultados"][0][0]["id"] == "BEN-01"

# no máximo 3 resultados, em ordem decrescente de nota
r = buscar("segunda via", BASE, {})
notas = [nota for _, nota in r["resultados"]]
assert len(notas) <= 3
assert notas == sorted(notas, reverse=True)

# nada em comum com a base, ou pergunta vazia
assert buscar("pizza de calabresa", BASE, {}) == {"status": "sem_base", "resultados": []}
assert buscar("", BASE, {}) == {"status": "sem_base", "resultados": []}

SIN = {
    "grana": ["dinheiro", "ajuda financeira"],
    "rg": ["carteira de identidade", "cin"],
}

# sem o dicionário, "grana" não existe na base
assert buscar("preciso de grana", BASE, {})["status"] == "sem_base"
# com o dicionário, chega ao FGTS
r = buscar("preciso de grana", BASE, SIN)
assert r["status"] == "ok"
assert r["resultados"][0][0]["id"] == "BEN-01"

# via expressão com várias palavras
assert {"rg", "cin"} <= expandir("perdi minha carteira de identidade", SIN)
# o caminho inverso também funciona
assert "carteira" in expandir("perdi meu RG!", SIN)
# palavra dentro de outra palavra NÃO dispara
assert "cin" not in expandir("argentina", SIN)

r = buscar("segunda via", BASE, {})
assert r["status"] == "ambigua"
assert len(r["resultados"]) >= 2

assert buscar("perdi meu RG na enchente", BASE, {})["status"] == "ok"

SIN_REAL = carregar_sinonimos("data/sinonimos.json")
assert buscar("perdi meus documentos", BASE, SIN_REAL)["status"] == "sem_base"

# regressão: "água" genérica não pode puxar a limpeza pós-enchente
r = buscar("a água está subindo, o que eu faço?", BASE, SIN_REAL)
assert r["resultados"][0][0]["id"] == "SEG-03"

r = buscar("posso beber a água da torneira depois da enchente?", BASE, SIN_REAL)
assert r["resultados"][0][0]["id"] == "MOR-02"

print("tudo certo")

