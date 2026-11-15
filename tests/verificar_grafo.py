import sys
sys.path.insert(0, "src")
from grafo import montar_grafo, pre_requisitos


def reg(id_, depende_de=None):
    r = {"id": id_}
    if depende_de is not None:
        r["depende_de"] = depende_de
    return r


# cadeia: DOC-01 depende de DOC-02, que depende de DOC-03
CADEIA = [reg("DOC-01", ["DOC-02"]), reg("DOC-02", ["DOC-03"]), reg("DOC-03", [])]
assert montar_grafo(CADEIA) == {"DOC-01": ["DOC-02"], "DOC-02": ["DOC-03"], "DOC-03": []}

# campo ausente ou null -> lista vazia, sem erro
assert montar_grafo([reg("A"), {"id": "B", "depende_de": None}]) == {"A": [], "B": []}

# depende_de aponta para um id que não existe -> ignora
assert montar_grafo([reg("A", ["Z"])]) == {"A": []}

# base vazia
assert montar_grafo([]) == {}

# cadeia: o mais fundo vem primeiro, sem o próprio id
assert pre_requisitos("DOC-01", CADEIA) == ["DOC-03", "DOC-02"]
assert pre_requisitos("DOC-02", CADEIA) == ["DOC-03"]
assert pre_requisitos("DOC-03", CADEIA) == []

# diamante: A depende de B e C; B e C dependem de D
DIAMANTE = [reg("A", ["B", "C"]), reg("B", ["D"]), reg("C", ["D"]), reg("D", [])]
ordem = pre_requisitos("A", DIAMANTE)
assert sorted(ordem) == ["B", "C", "D"]      # cada um aparece uma vez só
assert ordem.index("D") < ordem.index("B")   # D antes de B
assert ordem.index("D") < ordem.index("C")   # D antes de C

# id inexistente deve levantar ValueError
try:
    pre_requisitos("Z", CADEIA)
    assert False, "deveria levantar ValueError"
except ValueError:
    pass

CICLO = [reg("A", ["B"]), reg("B", ["C"]), reg("C", ["A"])]
try:
    pre_requisitos("A", CICLO)
    assert False, "deveria levantar ValueError"
except ValueError as erro:
    assert "A -> B -> C -> A" in str(erro)

# um registro que depende de si mesmo também é ciclo
try:
    pre_requisitos("X", [reg("X", ["X"])])
    assert False, "deveria levantar ValueError"
except ValueError as erro:
    assert "X -> X" in str(erro)

# ciclo que não está no caminho do registro consultado não atrapalha
FORA = [reg("A", []), reg("B", ["C"]), reg("C", ["B"])]
assert pre_requisitos("A", FORA) == []

# o diamante continua funcionando (D repetido não é ciclo)
assert sorted(pre_requisitos("A", DIAMANTE)) == ["B", "C", "D"]

import json
with open("data/base_conhecimento.json", encoding="utf-8") as f:
    BASE_REAL = json.load(f)

# nenhum registro da base real pode ter ciclo
for registro in BASE_REAL:
    pre_requisitos(registro["id"], BASE_REAL)

# FGTS: documentos primeiro, depois o município habilitado
assert pre_requisitos("BEN-01", BASE_REAL) == ["DOC-01", "DOC-02", "DOC-03", "BEN-03"]

print("grafo: tudo certo")