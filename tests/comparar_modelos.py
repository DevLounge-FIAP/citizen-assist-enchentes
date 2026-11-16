"""Compara os modelos de resposta A e B com critérios objetivos.

Execução (na raiz do repositório): python tests/comparar_modelos.py

Cada modelo formata todos os registros da base em três situações de
monitoramento (sem município, fase "durante" e fase "depois"). Para cada
resposta, verifica se as regras das instruções foram cumpridas e mede o
tamanho e o tempo de formatação. Imprime uma tabela em Markdown, pronta para
o README.

A clareza percebida não é medida aqui: ela vem do teste de usabilidade.
"""

import sys
import time

sys.path.insert(0, "src")
import base  # noqa: E402
import respostas  # noqa: E402

AVISO = "Dado de referência para demonstração."
CONTEXTOS = {
    "sem município": None,
    "durante": {"fase": "durante", "nivel": "alerta", "nivel_cm": 512,
                "horas_ate_inundacao": 4.9, "aviso": AVISO},
    "depois": {"fase": "depois", "nivel": "alerta", "nivel_cm": 480,
               "horas_ate_inundacao": None, "aviso": AVISO},
}
MODELOS = ("A", "B")


def avaliar(modelo, registros):
    """Conta, para um modelo, quantas respostas cumprem cada critério."""
    criterios = {
        "Cita a fonte e a data de verificação": [0, 0],
        "Aviso de confirmação quando o registro exige": [0, 0],
        "Aviso do monitoramento quando há município": [0, 0],
        "Situação do município quando há município": [0, 0],
        "Pré-requisitos quando o registro tem dependências": [0, 0],
        "Aviso de que não é canal oficial": [0, 0],
    }

    def conta(nome, ok):
        criterios[nome][0] += bool(ok)
        criterios[nome][1] += 1

    linhas, caracteres, segundos, total = 0, 0, 0.0, 0
    for contexto in CONTEXTOS.values():
        for registro in registros:
            inicio = time.perf_counter()
            texto = respostas.formatar(registro, modelo, contexto, registros)
            segundos += time.perf_counter() - inicio
            total += 1
            linhas += texto.count("\n") + 1
            caracteres += len(texto)
            # Os avisos podem ser quebrados em várias linhas; compara sem quebras.
            texto = " ".join(texto.split())

            conta("Cita a fonte e a data de verificação",
                  "Fonte:" in texto and registro["data_verificacao"] in texto)
            conta("Aviso de que não é canal oficial", respostas.AVISO_NAO_OFICIAL in texto)
            if registro.get("requer_confirmacao"):
                conta("Aviso de confirmação quando o registro exige",
                      respostas.AVISO_CONFIRMACAO in texto)
            if contexto:
                conta("Aviso do monitoramento quando há município", AVISO in texto)
                conta("Situação do município quando há município",
                      "Situação no seu município" in texto)
            if registro.get("depende_de"):
                conta("Pré-requisitos quando o registro tem dependências",
                      all(d in texto for d in registro["depende_de"]))

    medidas = {
        "Linhas por resposta (média)": f"{linhas / total:.1f}",
        "Caracteres por resposta (média)": f"{caracteres / total:.0f}",
        "Tempo de formatação (média)": f"{segundos / total * 1000:.2f} ms",
    }
    return criterios, medidas, total


def main():
    registros = base.carregar_base("data/base_conhecimento.json")
    resultados = {m: avaliar(m, registros) for m in MODELOS}
    total = resultados["A"][2]

    print(f"Respostas avaliadas por modelo: {total} "
          f"({len(registros)} registros x {len(CONTEXTOS)} situações)\n")
    print("| Critério | Modelo A | Modelo B |")
    print("| --- | --- | --- |")
    for nome in resultados["A"][0]:
        celulas = []
        for m in MODELOS:
            ok, n = resultados[m][0][nome]
            celulas.append(f"{ok}/{n} ({ok / n:.0%})" if n else "-")
        print(f"| {nome} | {celulas[0]} | {celulas[1]} |")
    for nome in resultados["A"][1]:
        print(f"| {nome} | {resultados['A'][1][nome]} | {resultados['B'][1][nome]} |")


if __name__ == "__main__":
    main()
