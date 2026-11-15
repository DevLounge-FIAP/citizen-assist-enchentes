"""Grafo de pré-requisitos a partir do campo depende_de.

Contrato (versão 11/11):
     pre_requisitos(id_registro, base) -> list[str]
     relacionados (id_registro, base) -> list[str]
"""

# Todo 14/11: montar grafo, ordenação topológica, ciclos e relacionados

def montar_grafo(base: list[dict]) -> dict[str, list[str]]:
    """Monta {id: [ids dos quais ele depende]}, ignorando dependências que não existem."""
    ids = {registro["id"] for registro in base}
    grafo = {}
    for registro in base:
        dependencias = registro.get("depende_de") or []
        grafo[registro["id"]] = [d for d in dependencias if d in ids]
    return grafo

def pre_requisitos(id_registro: str, base: list[dict]) -> list[str]:
    """Pré-requisitos (diretos e indiretos) na ordem em que devem ser feitos."""
    grafo = montar_grafo(base)
    if id_registro not in grafo:
        raise ValueError(f"id inexistente na base: {id_registro}")

    ordem = []
    visitados = set()   # já concluídos
    caminho = []        # em andamento: o caminho percorrido até aqui

    def visitar(no):
        if no in caminho:
            ciclo = caminho[caminho.index(no):] + [no]
            raise ValueError("ciclo de dependências: " + " -> ".join(ciclo))
        if no in visitados:
            return
        caminho.append(no)
        for dependencia in grafo[no]:
            visitar(dependencia)
        caminho.pop()
        visitados.add(no)
        ordem.append(no)

    visitar(id_registro)
    ordem.pop()
    return ordem

LIMITE_RELACIONADOS = 3


def relacionados(id_registro: str, base: list[dict]) -> list[str]:
    """Ids para continuar a navegação: quem depende deste, depois o mesmo tema e fase."""
    atual = next((r for r in base if r["id"] == id_registro), None)
    if atual is None:
        raise ValueError(f"id inexistente na base: {id_registro}")

    ja_vistos = set(pre_requisitos(id_registro, base)) | {id_registro}

    dependentes = [r["id"] for r in base if id_registro in (r.get("depende_de") or [])]

    mesma_fase = []
    tema, fase = atual.get("tema"), atual.get("fase")
    if tema and fase:
        mesma_fase = [r["id"] for r in base if r.get("tema") == tema and r.get("fase") == fase]

    resultado = []
    for candidato in dependentes + mesma_fase:
        if candidato not in ja_vistos and candidato not in resultado:
            resultado.append(candidato)
    return resultado[:LIMITE_RELACIONADOS]