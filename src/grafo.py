"""Grafo de pré-requisitos a partir do campo depende_de.

Contrato (versão 11/11):
     pre_requisitos(id_registro, base) -> list[str]
     relacionados (id_registro, base) -> list[str]
"""

# Todo 14/11: montar grafo, ordenação topológica, ciclos e relacionados


def pre_requisitos(id_registro: str, base: list[dict]) -> list [str]:
    """Esqueleto: devolve lista vazia (nenhum pré requisito)."""
    return[]

def relacionados(id_registro: str, base: list[dict]) -> list [str]:
    """Esqueleto: devolve lista vazia (sem recomendação)."""
    return[]