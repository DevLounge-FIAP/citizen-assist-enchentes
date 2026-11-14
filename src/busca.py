import unicodedata
import json

LIMIAR = 0.11   # nota mínima do 1º colocado; abaixo disso, não há base confiável
MARGEM = 0.85   # se nota do 2º / nota do 1º >= MARGEM, os dois estão "colados" -> ambígua

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

STOPWORDS = {normalizar(p) for p in ["como", "a", "o", "do", "meu", "de", "você"]}

def tokenizar(texto: str) -> set[str]:
    """Normalize o texto, remova as STOPWORDS e divida por palavras."""
    palavras = normalizar(texto).split()
    return {p for p in palavras if p not in STOPWORDS}

def jaccard(a: set[str], b: set[str]) -> float:
    """Similaridade de Jaccard: tamanho da interseção dividido pelo da união (de 0 a 1)."""
    uniao = a | b
    if not uniao:
        return 0.0
    return len(a & b) / len(uniao)


def tokens_do_registro(registro: dict) -> set[str]:
    """Junta todas as palavras_chave do registro em um único conjunto de tokens."""
    tokens = set()
    for frase in registro.get("palavras_chave", []):
        tokens |= tokenizar(frase)
    return tokens


def carregar_sinonimos(caminho: str) -> dict:
    """Lê o data/sinonimos.json e devolve o dicionário {termo: [sinônimos]}."""
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def expandir(pergunta: str, sinonimos: dict) -> set[str]:
    """Tokeniza a pergunta e acrescenta os tokens dos sinônimos que ela menciona."""
    texto = f" {normalizar(pergunta)} "
    tokens = tokenizar(pergunta)

    for termo, lista in sinonimos.items():
        grupo = [normalizar(termo)] + [normalizar(s) for s in lista]
        if any(frase and f" {frase} " in texto for frase in grupo):
            for frase in grupo:
                tokens |= tokenizar(frase)

    return tokens

def buscar(pergunta: str, base: list[dict], sinonimos: dict) -> dict:
    """Compara a pergunta com cada registro da base e devolve os melhores."""
    tokens_pergunta = expandir(pergunta, sinonimos)

    pontuados = []
    for registro in base:
        nota = jaccard(tokens_pergunta, tokens_do_registro(registro))
        if nota > 0:
            pontuados.append((registro, nota))

    if not pontuados:
        return {"status": "sem_base", "resultados": []}

    pontuados.sort(key=lambda par: par[1], reverse=True)
    melhor = pontuados[0][1]

    if melhor < LIMIAR:
        return {"status": "sem_base", "resultados": []}

    if len(pontuados) > 1 and pontuados[1][1] / melhor >= MARGEM:
        return {"status": "ambigua", "resultados": pontuados[:3]}

    return {"status": "ok", "resultados": pontuados[:3]}
    

