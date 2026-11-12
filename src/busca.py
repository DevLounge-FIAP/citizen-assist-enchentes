"""
Busca: normalização, sinônimos e pontuação por sobreposição de termos.

Contrato (versão de 11/11):

   buscar(pergunta, base, sinonimos)  -> dict
      {"status": "ok" | "sem_base" | "ambigua",
      "resultados": [(registro, pontuacao), ...]}
"""

#Todo 12/11 normalizar, tokenizar e jaccard

#Todo 13/11 sinônimos, limiar (sem_base) e ambiguade (ambigua)

def buscar (pergunta: str, base: list[dict], sinonimos: dict) -> dict:
    """Esqueleto: ainda não busca nada, sempre responde 'sem_base'."""

    return {"status": "sem_base", "resultados": []}
    

