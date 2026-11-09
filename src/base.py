"""Carregamento e validação da base de conhecimento (JSON).

Contrato: carregar_base(caminho) -> list[dict]
"""

import json
import os

CAMPOS_OBRIGATORIOS = (
    "id",
    "tema",
    "palavras_chave",
    "orientacao",
    "fonte",
    "data_verificacao",
)
CAMPOS_TEXTO = ("id", "tema", "orientacao", "fonte", "data_verificacao")


class ErroBase(Exception):
    """Falha que impede o uso da base (arquivo ausente, vazio ou inválido)."""


def validar_registro(registro):
    """Retorna a lista de problemas do registro (vazia se estiver válido)."""
    if not isinstance(registro, dict):
        return ["registro não é um objeto JSON"]

    problemas = []
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in registro:
            problemas.append(f"campo ausente: {campo}")
    for campo in CAMPOS_TEXTO:
        if campo in registro and not (
            isinstance(registro[campo], str) and registro[campo].strip()
        ):
            problemas.append(f"campo vazio ou inválido: {campo}")

    palavras = registro.get("palavras_chave")
    if "palavras_chave" in registro and not (
        isinstance(palavras, list)
        and palavras
        and all(isinstance(p, str) and p.strip() for p in palavras)
    ):
        problemas.append("palavras_chave deve ser uma lista não vazia de textos")

    dep = registro.get("depende_de", [])
    if not (isinstance(dep, list) and all(isinstance(d, str) for d in dep)):
        problemas.append("depende_de deve ser uma lista de ids")
    return problemas


def carregar_base(caminho, avisos=None):
    """Lê o JSON, valida e devolve apenas os registros utilizáveis.

    Levanta ErroBase se o arquivo não existir, estiver vazio, não for um JSON
    válido ou não tiver nenhum registro válido. Registros com problemas são
    descartados e descritos em `avisos` (lista opcional, preenchida in-place).
    """
    if avisos is None:
        avisos = []

    if not os.path.isfile(caminho):
        raise ErroBase(f"Arquivo da base não encontrado: {caminho}")
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            texto = arquivo.read()
    except (OSError, UnicodeDecodeError) as erro:
        raise ErroBase(f"Não foi possível ler a base: {erro}") from erro

    if not texto.strip():
        raise ErroBase("O arquivo da base está vazio.")
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise ErroBase(f"JSON inválido na base (linha {erro.lineno}): {erro.msg}") from erro
    if not isinstance(dados, list):
        raise ErroBase("A base deve ser uma lista de registros.")
    if not dados:
        raise ErroBase("A base não contém nenhum registro.")

    validos = []
    ids_vistos = set()
    for posicao, registro in enumerate(dados, start=1):
        problemas = validar_registro(registro)
        rotulo = registro.get("id", f"#{posicao}") if isinstance(registro, dict) else f"#{posicao}"
        if not problemas and registro["id"] in ids_vistos:
            problemas = ["id duplicado"]
        if problemas:
            avisos.append(f"Registro {rotulo} ignorado: " + "; ".join(problemas))
            continue
        ids_vistos.add(registro["id"])
        validos.append(registro)

    ids_validos = {r["id"] for r in validos}
    for registro in validos:
        desconhecidos = [d for d in registro.get("depende_de", []) if d not in ids_validos]
        if desconhecidos:
            avisos.append(
                f"Registro {registro['id']}: depende_de referencia ids inexistentes "
                f"({', '.join(desconhecidos)}); removidos."
            )
            registro["depende_de"] = [
                d for d in registro["depende_de"] if d in ids_validos
            ]

    if not validos:
        raise ErroBase("Nenhum registro válido encontrado na base.")
    return validos


def listar_temas(base):
    """Temas disponíveis, em ordem alfabética, sem repetição."""
    return sorted({registro["tema"] for registro in base})


def indexar_por_id(base):
    """Dicionário id -> registro, para recuperação direta."""
    return {registro["id"]: registro for registro in base}


def registros_do_tema(base, tema):
    return [registro for registro in base if registro["tema"] == tema]
