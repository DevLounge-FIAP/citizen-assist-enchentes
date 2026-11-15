import sys
sys.path.insert(0, "src")
from grafo import montar_grafo, pre_requisitos, relacionados


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

def reg2(id_, depende_de=None, tema=None, fase=None):
    r = reg(id_, depende_de)
    if tema:
        r["tema"] = tema
    if fase:
        r["fase"] = fase
    return r


# quem depende do registro vem primeiro; o próprio id nunca entra
REL = [reg2("B", []), reg2("A", ["B"]), reg2("C", ["B"])]
assert relacionados("B", REL) == ["A", "C"]

# depois dos dependentes, entram os do mesmo tema e fase (sem repetir)
REL2 = [
    reg2("X1", [], "t", "antes"),
    reg2("X2", ["X1"], "t", "antes"),
    reg2("X3", [], "t", "antes"),
    reg2("X4", [], "t", "depois"),
]
assert relacionados("X1", REL2) == ["X2", "X3"]

# pré-requisitos não são sugeridos de novo
REL3 = [reg2("P", [], "t", "antes"), reg2("Q", ["P"], "t", "antes")]
assert relacionados("Q", REL3) == []

# sem tema e fase, só valem os dependentes
assert relacionados("Z", [reg("Z", [])]) == []

# no máximo 3
MUITOS = [reg2(f"M{i}", [], "t", "antes") for i in range(6)]
assert len(relacionados("M0", MUITOS)) == 3

# id inexistente
try:
    relacionados("nao-existe", REL)
    assert False, "deveria levantar ValueError"
except ValueError:
    pass

# base real
assert relacionados("DOC-03", BASE_REAL) == ["BEN-01", "BEN-02", "BEN-04"]
assert relacionados("SEG-01", BASE_REAL) == ["SEG-04", "SEG-05", "SEG-06"]
assert "SEG-03" in relacionados("SEG-02", BASE_REAL)

print("grafo: tudo certo")