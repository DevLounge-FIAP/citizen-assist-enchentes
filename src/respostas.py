"""Modelos de resposta do Citizen Assist AI.

Contrato: formatar(registro, modelo, contexto, base=None) -> str

O assistente não gera texto livre: ele monta a resposta a partir de um
registro verificado da base, seguindo uma das duas instruções abaixo.
Os dois modelos têm as mesmas regras fixas (nunca inventar orientação,
sempre citar a fonte, nunca se apresentar como canal oficial) e diferem
no formato.
"""

import re
import textwrap

LARGURA = 78

INSTRUCAO_MODELO_A = """\
Papel: assistente de orientação ao cidadão sobre enchentes. Não é canal
oficial.
Formato: resposta direta, em um parágrafo, com o texto da orientação como
está na base, seguido da fonte e da data de verificação.
Regras: usar apenas o registro encontrado; citar a fonte sempre; mostrar
aviso de confirmação quando o registro exigir; mostrar o aviso do
monitoramento quando houver."""

INSTRUCAO_MODELO_B = """\
Papel: assistente de orientação ao cidadão sobre enchentes. Não é canal
oficial.
Formato: resposta estruturada em blocos: (1) situação atual do município,
(2) o que precisa estar pronto antes (pré-requisitos do grafo, em ordem),
(3) passo a passo numerado, uma frase da orientação por passo, (4) fonte e
data de verificação, (5) avisos.
Regras: usar apenas o registro encontrado e os registros de que ele
depende; citar a fonte sempre; mostrar aviso de confirmação quando o
registro exigir; mostrar o aviso do monitoramento quando houver."""

INSTRUCOES = {"A": INSTRUCAO_MODELO_A, "B": INSTRUCAO_MODELO_B}

AVISO_CONFIRMACAO = (
    "requisitos e prazos podem mudar; confirme no órgão responsável antes de ir."
)
AVISO_NAO_OFICIAL = "Orientação de um protótipo educacional, não de um canal oficial."

DESCRICAO_FASE = {
    "antes": "fase ANTES (preparação)",
    "durante": "fase DURANTE (segurança primeiro)",
    "depois": "fase DEPOIS (recuperação)",
}

# Fim de frase: pontuação seguida de espaço e letra maiúscula, número ou aspas.
_FIM_DE_FRASE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9\"“])")


def _quebrar(texto, recuo=""):
    # Sem quebrar palavras longas nem hifens, para não partir URLs ao meio.
    return textwrap.fill(
        texto,
        width=LARGURA,
        initial_indent=recuo,
        subsequent_indent=recuo,
        break_long_words=False,
        break_on_hyphens=False,
    )


def _passos(orientacao):
    """Divide a orientação em frases; cada frase vira um passo."""
    return [frase.strip() for frase in _FIM_DE_FRASE.split(orientacao) if frase.strip()]


def _titulo(registro):
    """Rótulo curto do registro.

    Ordem: campo opcional `titulo`; senão o `subtema` legível; senão a
    primeira palavra-chave.
    """
    rotulo = registro.get("titulo")
    if not rotulo and registro.get("subtema"):
        rotulo = registro["subtema"].replace("_", " ")
    if not rotulo:
        rotulo = (registro.get("palavras_chave") or [registro["id"]])[0]
    return rotulo[:1].upper() + rotulo[1:]


def _rodape(registro, contexto):
    linhas = [
        _quebrar(
            f"Fonte: {registro['fonte']} (verificado em {registro['data_verificacao']})"
        )
    ]
    if registro.get("requer_confirmacao"):
        linhas.append(_quebrar(f"Atenção: {AVISO_CONFIRMACAO}"))
    if contexto and contexto.get("aviso"):
        linhas.append(_quebrar(f"Monitoramento: {contexto['aviso']}"))
    linhas.append(AVISO_NAO_OFICIAL)
    return linhas


def _situacao(contexto):
    """Linha com a fase e o nível do rio; None se não houver monitoramento."""
    if not contexto or not contexto.get("fase"):
        return None
    partes = [DESCRICAO_FASE.get(contexto["fase"], contexto["fase"])]
    if contexto.get("nivel"):
        nivel = f"nível {contexto['nivel']}"
        if contexto.get("nivel_cm") is not None:
            nivel += f" ({contexto['nivel_cm']} cm)"
        partes.append(nivel)
    horas = contexto.get("horas_ate_inundacao")
    if horas is not None:
        partes.append(f"cerca de {horas:.0f} h até a cota de inundação")
    return "Situação no seu município: " + ", ".join(partes) + "."


def _pre_requisitos(registro, base):
    """Ids que devem ser feitos antes, em ordem.

    Usa grafo.pre_requisitos quando o módulo existir; senão, cai para as
    dependências diretas do registro (depende_de). Um ciclo no grafo
    (ValueError) também cai para as dependências diretas, para não
    derrubar a resposta.
    """
    try:
        import grafo

        return grafo.pre_requisitos(registro["id"], base or [])
    except (ImportError, AttributeError, ValueError):
        return list(registro.get("depende_de", []))


def modelo_a(registro, contexto=None):
    """Modelo A: resposta direta (orientação + fonte)."""
    linhas = [
        f"[{registro['id']}] {_titulo(registro)}",
        _quebrar(registro["orientacao"]),
        "",
    ]
    linhas.extend(_rodape(registro, contexto))
    return "\n".join(linhas)


def modelo_b(registro, contexto=None, base=None):
    """Modelo B: resposta estruturada (situação, pré-requisitos, passos, fonte)."""
    linhas = [f"=== [{registro['id']}] {_titulo(registro)} ==="]

    situacao = _situacao(contexto)
    if situacao:
        linhas.extend([_quebrar(situacao), ""])

    pre = _pre_requisitos(registro, base)
    if pre:
        por_id = {r["id"]: r for r in base} if base else {}
        linhas.append("Antes, você precisa ter feito (nesta ordem):")
        for i, id_pre in enumerate(pre, start=1):
            nome = _titulo(por_id[id_pre]) if id_pre in por_id else ""
            linhas.append(f"  {i}. {id_pre}" + (f" - {nome}" if nome else ""))
        linhas.append("")

    linhas.append("Passo a passo:")
    for i, passo in enumerate(_passos(registro["orientacao"]), start=1):
        recuo = " " * (len(str(i)) + 4)
        texto = _quebrar(passo, recuo)
        linhas.append(f"  {i}. " + texto[len(recuo):])
    linhas.append("")

    linhas.extend(_rodape(registro, contexto))
    return "\n".join(linhas)


def formatar(registro, modelo, contexto=None, base=None):
    """Monta a resposta final para o registro no modelo pedido ("A" ou "B")."""
    modelo = str(modelo).upper()
    if modelo == "A":
        return modelo_a(registro, contexto)
    if modelo == "B":
        return modelo_b(registro, contexto, base)
    raise ValueError(f"Modelo de resposta desconhecido: {modelo!r} (use 'A' ou 'B').")
