"""
Preparação dos dados da ANA para o monitoramento.

Uso: python src/preparar_dados.py (lê os XMLs de data/ana/ e gera data/monitoramento.csv)
"""

import os
from datetime import datetime, timedelta

PASTA_ENTRADA = "data/ana/"
PASTA_PROCESSADOS = "data/ana/processados/"
CAMINHO_MONITORAMENTO = "data/monitoramento.csv"
CABECALHO = "estacao,rio,municipio,data_hora,nivel_cm,cota_alerta_cm,cota_inundacao_cm\n"
FORMATO_DATA = "%Y-%m-%d %H:%M:%S"  # Formato da data que vem no XML da ANA

def processar_xml(caminho_xml):
    """
        Lê o XML da ANA, deixa uma leitura por hora, preenche as horas que faltam e salva no CSV com nome da respectiva cidade.
    """
    arquivo = open(caminho_xml, "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    leituras = []
    codigo = ""
    data = ""

    for linha in linhas:
        if "<CodEstacao>" in linha:
            codigo = linha.split("<CodEstacao>")[1].split("</CodEstacao>")[0]
        if "<DataHora>" in linha:
            data = linha.split("<DataHora>")[1].split("</DataHora>")[0].strip()
        if "<Nivel>" in linha:
            nivel = linha.split("<Nivel>")[1].split("</Nivel>")[0]
            leituras.append([data, float(nivel)])

    print("Estação", codigo, "encontrada, com", len(leituras), "leituras.")
    nome = input("Nome da estação: ")
    rio = input("Rio: ")
    municipio = input("Município: ")
    cota_alerta = int(input("Cota de alerta (cm): "))
    cota_inundacao = int(input("Cota de inundação (cm): "))

    leituras.sort()
    nivel_por_hora = []
    horas_analisadas = []

    for leitura in leituras:
        data = leitura[0]
        hora = data.split(" ")[1]
        minuto = hora.split(":")[1]
        if minuto == "00" and data not in horas_analisadas:
            nivel_por_hora.append(leitura)
            horas_analisadas.append(data)

    leituras_completas = []

    for i in range(len(nivel_por_hora) - 1):
        data_atual = datetime.strptime(nivel_por_hora[i][0], FORMATO_DATA)
        data_proxima = datetime.strptime(nivel_por_hora[i + 1][0], FORMATO_DATA)
        nivel_atual = nivel_por_hora[i][1]
        nivel_proximo = nivel_por_hora[i + 1][1]

        leituras_completas.append([nivel_por_hora[i][0], nivel_atual])

        dif_segundos = (data_proxima - data_atual).total_seconds()
        horas = int(dif_segundos / 3600)
        if horas > 1:
            passo = (nivel_proximo - nivel_atual) / horas
            nova_data = data_atual
            novo_nivel = nivel_atual

            for h in range(1, horas):
                nova_data = nova_data + timedelta(hours=1)
                novo_nivel = novo_nivel + passo
                leituras_completas.append([str(nova_data), round(novo_nivel)])

    leituras_completas.append(nivel_por_hora[-1])

    ano = leituras_completas[0][0].split("-")[0]
    nome_csv = PASTA_ENTRADA + municipio + " - " + ano + ".csv"
    saida = open(nome_csv, "w", encoding="utf-8")
    saida.write(CABECALHO)

    for leitura in leituras_completas:
        data_hora = leitura[0][0:16]
        nivel = str(int(leitura[1]))
        cotas = str(cota_alerta) + "," + str(cota_inundacao)
        linha = nome + "," + rio + "," + municipio + "," + data_hora + "," + nivel + "," + cotas + "\n"
        saida.write(linha)
    saida.close()

    print("Arquivo salvo:", nome_csv, "com", len(leituras_completas), "horas.")

def juntar_csvs():
    """
        Junta os CSVs das cidades em monitoramento.csv sem repetir leituras.
    """
    linhas_existentes = []

    if os.path.exists(CAMINHO_MONITORAMENTO):
        arquivo = open(CAMINHO_MONITORAMENTO, "r", encoding="utf-8")
        linhas = arquivo.readlines()
        arquivo.close()

        for linha in linhas[1:]:
            colunas = linha.split(",")
            cidade_e_hora = colunas[2] + " " + colunas[3]
            linhas_existentes.append(cidade_e_hora)
        monitoramento = open(CAMINHO_MONITORAMENTO, "a", encoding="utf-8")
    else:
        monitoramento = open(CAMINHO_MONITORAMENTO, "w", encoding="utf-8")
        monitoramento.write(CABECALHO)

    arquivos = os.listdir(PASTA_ENTRADA)

    for nome_arquivo in arquivos:
        extensao = nome_arquivo.split(".")[-1]
        if extensao == "csv":
            arquivo = open(PASTA_ENTRADA + nome_arquivo, "r", encoding="utf-8")
            linhas = arquivo.readlines()
            arquivo.close()

            for linha in linhas[1:]:
                colunas = linha.split(",")
                cidade_e_hora = colunas[2] + " " + colunas[3]
                if cidade_e_hora not in linhas_existentes:
                    monitoramento.write(linha)
                    linhas_existentes.append(cidade_e_hora)

    monitoramento.close()


if __name__ == "__main__":
    arquivos = os.listdir(PASTA_ENTRADA)

    for nome_arquivo in arquivos:
        extensao = nome_arquivo.split(".")[-1]
        if extensao == "xml":
            print("Processando", nome_arquivo)
            processar_xml(PASTA_ENTRADA + nome_arquivo)
            os.rename(PASTA_ENTRADA + nome_arquivo, PASTA_PROCESSADOS + nome_arquivo)
            print(nome_arquivo, "movido para", PASTA_PROCESSADOS)
            juntar_csvs()
