"""
Monitoramento do nível dos rios durante a cheia.

Contrato: estado(municipio) -> dict
"""

import os

# Caminho a partir deste arquivo, para funcionar de qualquer pasta (IDE, terminal fora da raiz)
CAMINHO_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "monitoramento.csv")

PORCENTAGEM_ATENCAO = 0.9  # Usada para calcular a cota de atenção com base na cota de alerta

HORAS_TENDENCIA = 3  # Usada para comparar o nível de água com o de x horas antes -> identifica o estado atual (antes, durante, depois)

AVISO = "Dado de referência para demonstração. Siga sempre os alertas oficiais da Defesa Civil (199) e, em perigo imediato, ligue 193."

horas_simuladas = 0  # Relógio da simulação em horas - se baseia nos dados que foram inseridos


def carregar_simulacao(municipio):
    """
        Obtém os dados de monitoramento.csv e armazena em leituras.
    """
    arquivo = open(CAMINHO_CSV, "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    leituras = []

    for linha in linhas[1:]:
        colunas = linha.strip().split(",")
        if colunas[2].lower() == municipio.lower():
            data_hora = colunas[3]
            nivel = int(colunas[4])
            cota_alerta = int(colunas[5])
            cota_inundacao = int(colunas[6])
            leituras.append([data_hora, nivel, cota_alerta, cota_inundacao])

    leituras.sort()
    return leituras

def avancar_simulacao(horas):
    """
        Avança a simulação na quantidade de horas desejada. 
    """
    global horas_simuladas
    horas_simuladas = horas_simuladas + horas

def reiniciar_simulacao():
    """
        Reinicia o horário da simulação.
    """
    global horas_simuladas
    horas_simuladas = 0

def estado(municipio):
    """
        Calcula a situação do rio no horário atual da simulação.
    """
    leituras = carregar_simulacao(municipio)

    if len(leituras) == 0:
        raise KeyError("Sem leituras de monitoramento para o município: " + municipio)

    agora = horas_simuladas
    if agora > len(leituras) - 1:  # Se passar do fim dos dados na simulação, usa a última leitura como leitura atual
        agora = len(leituras) - 1

    nivel_cm = leituras[agora][1]
    cota_alerta = leituras[agora][2]
    cota_inundacao = leituras[agora][3]

    if agora >= HORAS_TENDENCIA:
        nivel_antes = leituras[agora - HORAS_TENDENCIA][1]
        tendencia = round((nivel_cm - nivel_antes) / HORAS_TENDENCIA, 1)
    else:
        tendencia = 0.0

    if nivel_cm >= cota_inundacao:
        nivel = "inundação"
    elif nivel_cm >= cota_alerta:
        nivel = "alerta"
    elif nivel_cm >= cota_alerta * PORCENTAGEM_ATENCAO:
        nivel = "atenção"
    else:
        nivel = "normal"

    rio_cheia = False

    for i in range(agora + 1):
        if leituras[i][1] >= cota_alerta:
            rio_cheia = True

    if rio_cheia and tendencia < 0:
        fase = "depois"
    elif nivel == "alerta" or nivel == "inundação":
        fase = "durante"
    else:
        fase = "antes"

    if tendencia > 0 and nivel_cm < cota_inundacao:
        horas_ate_inundacao = round((cota_inundacao - nivel_cm) / tendencia, 1)
    else:
        horas_ate_inundacao = None

    return {
        "fase": fase,
        "nivel": nivel,
        "nivel_cm": nivel_cm,
        "tendencia_cm_h": tendencia,
        "horas_ate_inundacao": horas_ate_inundacao,
        "aviso": AVISO,
    }


if __name__ == "__main__":
    print("Simulação com intervalos de 12h")
    for cidade in ["Estrela", "Uruguaiana"]:
        print("=== " + cidade + " ===")
        reiniciar_simulacao()
        total_horas = len(carregar_simulacao(cidade))

        for h in range(0, total_horas, 12):
            resultado = estado(cidade)
            print(
                "Hora",
                horas_simuladas,
                "|",
                resultado["nivel_cm"],
                "Cm |",
                resultado["tendencia_cm_h"],
                "Cm/h",
            )
            print(
                "   Nível:",
                resultado["nivel"],
                "| Fase:",
                resultado["fase"],
                "| Horas até inundação:",
                resultado["horas_ate_inundacao"],
            )
            avancar_simulacao(12)

        print(AVISO)
        print()
