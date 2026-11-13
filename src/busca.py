import unicodedata

"""
Busca: normalização, sinônimos e pontuação por sobreposição de termos.

Contrato (versão de 11/11):

   buscar(pergunta, base, sinonimos)  -> dict
      {"status": "ok" | "sem_base" | "ambigua",
      "resultados": [(registro, pontuacao), ...]}
"""

#Todo 12/11 normalizar, tokenizar e jaccard

#Todo 13/11 sinônimos, limiar (sem_base) e ambiguade (ambigua)


def normalizar(texto: str) -> str:
    """Padroniza o texto: minúsculas, sem acento, sem pontuação, espaços limpos."""
    # 1) minúsculas
    texto = texto.lower()
    # 2) separar a letra do acento (NFD)
    texto = unicodedata.normalize("NFD", texto)
    # 3) descartas as marcas de acento (categoria "Mn")
    texto = "".join(c for c in texto if unicodedata.category(c) !="Mn")
    # 4) trocar o que não é letra, número ou espaço por um espaço
    texto = "".join(c if c.isalnum() or c.isspace() else " " for c in texto)
    # 5) juntar espaços repetidos e tirar os das pontas
    texto = " ".join(texto.split())
    return texto


def buscar (pergunta: str, base: list[dict], sinonimos: dict) -> dict:
    """Esqueleto: ainda não busca nada, sempre responde 'sem_base'."""

    return {"status": "sem_base", "resultados": []}
    

