"""Menu e fluxo principal do Citizen Assist AI.

Execução: python src/sistema.py [caminho_da_base]

Fluxo de uma consulta: pergunta (ou tema) -> busca na base -> estado do
monitoramento do município -> bloco de segurança, se a fase for "durante"
-> resposta no modelo escolhido (A ou B) -> assuntos relacionados (grafo).
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import base  # noqa: E402
import respostas  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BASE = os.path.join(RAIZ, "data", "base_conhecimento.json")
CAMINHO_SINONIMOS = os.path.join(RAIZ, "data", "sinonimos.json")

# Modelo usado por padrão; o usuário pode trocar no menu (opção 5).
MODELO_PADRAO = "B"

AVISO_GERAL = (
    "Este assistente é um protótipo educacional e NÃO é um canal oficial. "
    "Em risco imediato ligue 193 (Bombeiros); para alertas, Defesa Civil 199."
)
BLOCO_SEGURANCA = (
    "!! SEGURANÇA EM PRIMEIRO LUGAR !!\n"
    "Se estiver em área de risco, saia para um local alto e seguro.\n"
    "Defesa Civil: 199 | Bombeiros: 193"
)
FASES = ("antes", "durante", "depois")


def _modulo(nome):
    """Importa um módulo opcional; None se ainda não existir ou falhar."""
    try:
        return __import__(nome)
    except ImportError:
        return None


def _funcao(modulo, nome):
    return getattr(modulo, nome, None) if modulo else None


def ler(prompt):
    """input() que devolve None em fim de entrada (Ctrl+D / Ctrl+C)."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def escolher_opcao(prompt, total):
    """Pede um número de 0 a `total`. Repete em entrada vazia/inválida."""
    while True:
        texto = ler(prompt)
        if texto is None:
            return 0
        if not texto:
            print("Entrada vazia. Digite o número de uma das opções.")
        elif not texto.isdigit() or not 0 <= int(texto) <= total:
            print(f"Opção inexistente: '{texto}'. Escolha entre 0 e {total}.")
        else:
            return int(texto)


# --- Carregamento -----------------------------------------------------------


def carregar_ou_sair(caminho):
    avisos = []
    try:
        registros = base.carregar_base(caminho, avisos)
    except base.ErroBase as erro:
        print(f"Erro ao carregar a base: {erro}")
        sys.exit(1)
    for aviso in avisos:
        print(f"Aviso: {aviso}")
    return registros


def carregar_sinonimos(caminho=CAMINHO_SINONIMOS):
    """Dicionário de sinônimos; vazio (com aviso) se o arquivo faltar ou falhar."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        print(f"Aviso: sinônimos indisponíveis ({erro}); a busca segue sem eles.")
        return {}
    if not isinstance(dados, dict):
        print("Aviso: sinonimos.json não é um objeto; a busca segue sem sinônimos.")
        return {}
    return dados


# --- Monitoramento ----------------------------------------------------------


def _avisar_uma_vez(contexto, mensagem):
    """Mostra um aviso do monitoramento só na primeira vez da sessão."""
    if mensagem not in contexto["avisos_mostrados"]:
        contexto["avisos_mostrados"].add(mensagem)
        print(mensagem)


def obter_estado(contexto):
    """Estado do monitoramento do município do contexto, ou None.

    Qualquer falha do monitoramento vira uma mensagem: ele nunca derruba o
    fluxo principal.
    """
    municipio = contexto.get("municipio")
    if not municipio:
        return None
    estado_fn = _funcao(_modulo("monitor"), "estado")
    if not estado_fn:
        _avisar_uma_vez(contexto, "(Monitoramento ainda não disponível nesta versão.)")
        return None
    try:
        estado = estado_fn(municipio)
    except KeyError:
        _avisar_uma_vez(contexto, f"(Sem leituras de monitoramento para '{municipio}'.)")
        return None
    except Exception as erro:  # noqa: BLE001 - qualquer falha vira aviso
        _avisar_uma_vez(contexto, f"(Monitoramento indisponível: {erro})")
        return None
    return estado if isinstance(estado, dict) else None


def preparar_resposta(contexto):
    """Busca o estado do município e mostra o bloco de segurança se preciso."""
    estado = obter_estado(contexto)
    if estado and estado.get("fase") == "durante":
        print("\n" + BLOCO_SEGURANCA)
    return estado


# --- Apresentação -----------------------------------------------------------


def rotulo(registro):
    return f"{registro['id']} - {respostas.titulo(registro)}"


def apresentar(registro, registros_base, contexto, estado):
    """Mostra a resposta e oferece os assuntos relacionados (grafo)."""
    while registro:
        print()
        print(respostas.formatar(registro, contexto["modelo"], estado, registros_base))
        registro = escolher_relacionado(registro, registros_base)


def escolher_relacionado(registro, registros_base):
    """Lista os relacionados do grafo; devolve o escolhido ou None."""
    relacionados_fn = _funcao(_modulo("grafo"), "relacionados")
    if not relacionados_fn:
        return None
    try:
        ids = relacionados_fn(registro["id"], registros_base)
    except ValueError:
        return None
    por_id = base.indexar_por_id(registros_base)
    itens = [por_id[i] for i in ids if i in por_id]
    if not itens:
        return None
    print("\nAssuntos relacionados:")
    for i, item in enumerate(itens, start=1):
        print(f"  {i}. {rotulo(item)}")
    print("  0. Voltar ao menu")
    escolha = escolher_opcao("Ver relacionado: ", len(itens))
    return itens[escolha - 1] if escolha else None


def sem_resposta(registros_base):
    """Ausência de orientação confiável: não inventa, sugere caminhos.

    Os telefones de emergência vêm primeiro: no teste de usabilidade, a
    participante só achou o 193 na última linha de uma mensagem longa.
    """
    print("\nEm risco imediato: Bombeiros 193 | Defesa Civil 199.")
    print("Não encontrei na base uma orientação confiável para essa pergunta.")
    print("Não vou inventar instruções.")
    exemplos = []
    for tema in base.listar_temas(registros_base):
        primeiro = base.registros_do_tema(registros_base, tema)[0]
        exemplos.append(f"\"{primeiro['palavras_chave'][0]}\"")
    print("Tente outras palavras, como " + ", ".join(exemplos) + ".")
    print("Ou use a opção 1 do menu para navegar pelos temas.")


def escolher_entre(candidatos, prompt):
    """Lista registros numerados e devolve o escolhido (ou None)."""
    for i, registro in enumerate(candidatos, start=1):
        print(f"  {i}. {rotulo(registro)}")
    print("  0. Voltar")
    escolha = escolher_opcao(prompt, len(candidatos))
    return candidatos[escolha - 1] if escolha else None


# --- Opções do menu ---------------------------------------------------------


def consultar_tema(registros_base, contexto):
    temas = base.listar_temas(registros_base)
    print("\nTemas disponíveis:")
    for i, tema in enumerate(temas, start=1):
        print(f"  {i}. {tema}")
    print("  0. Voltar")
    escolha = escolher_opcao("Tema: ", len(temas))
    if escolha == 0:
        return
    tema = temas[escolha - 1]
    itens = base.registros_do_tema(registros_base, tema)
    print(f"\nOrientações em '{tema}':")
    registro = escolher_entre(itens, "Orientação: ")
    if registro:
        estado = preparar_resposta(contexto)
        apresentar(registro, registros_base, contexto, estado)


def consultar_pergunta(registros_base, contexto):
    pergunta = ler("\nDigite sua pergunta: ")
    if pergunta is None:
        return
    if not pergunta:
        print("Pergunta vazia. Escreva sua dúvida ou use o menu de temas.")
        return
    buscar = _funcao(_modulo("busca"), "buscar")
    if not buscar:
        print("A busca por pergunta ainda não está disponível. Use o menu de temas.")
        return

    resultado = buscar(pergunta, registros_base, contexto["sinonimos"])
    status = resultado.get("status")
    candidatos = [registro for registro, _ in resultado.get("resultados", [])]

    if status == "sem_base" or not candidatos:
        preparar_resposta(contexto)
        sem_resposta(registros_base)
        return
    if status == "ambigua":
        print("\nSua pergunta combina com mais de um assunto. Qual deles você quer?")
        registro = escolher_entre(candidatos, "Assunto: ")
        if not registro:
            return
    else:
        registro = candidatos[0]
    estado = preparar_resposta(contexto)
    apresentar(registro, registros_base, contexto, estado)


def pedir_municipio(contexto):
    print("\nO único dado pedido é o município (não coletamos dados pessoais).")
    municipio = ler("Município (Enter para pular): ")
    contexto["municipio"] = municipio or None
    if not municipio:
        return
    print(f"Município definido: {municipio}")
    estado = obter_estado(contexto)
    if estado:
        print(respostas.situacao(estado) or "")
        if estado.get("aviso"):
            print(f"Monitoramento: {estado['aviso']}")


def o_que_fazer_agora(registros_base, contexto):
    """Orientações da fase atual do município (antes, durante ou depois)."""
    if not contexto.get("municipio"):
        print("\nInforme primeiro o seu município (opção 3) para saber a fase atual.")
        return
    estado = preparar_resposta(contexto)
    if not estado or estado.get("fase") not in FASES:
        print("Sem fase do monitoramento agora. Use o menu de temas (opção 1).")
        return
    fase = estado["fase"]
    itens = [r for r in registros_base if r.get("fase") == fase]
    print(f"\n{respostas.situacao(estado)}")
    if not itens:
        print("Não há orientações cadastradas para esta fase. Use o menu de temas.")
        return
    print(f"Orientações prioritárias para a fase '{fase}':")
    registro = escolher_entre(itens, "Orientação: ")
    if registro:
        apresentar(registro, registros_base, contexto, estado)


def trocar_modelo(contexto):
    print("\nModelos de resposta:")
    print("  1. Modelo A - direto: orientação em um parágrafo + fonte")
    print("  2. Modelo B - estruturado: situação, pré-requisitos, passo a passo, fonte")
    print("  0. Voltar")
    escolha = escolher_opcao("Modelo: ", 2)
    if escolha:
        contexto["modelo"] = "A" if escolha == 1 else "B"
        print(f"Modelo de resposta: {contexto['modelo']}")


def mostrar_situacao(contexto):
    """Situação do município no momento simulado, com o bloco de segurança."""
    estado = preparar_resposta(contexto)
    if estado:
        print(respostas.situacao(estado) or "")


def simular_tempo(contexto):
    """Avança o relógio da simulação do monitoramento (roteiro do vídeo).

    A série de data/monitoramento.csv é real (ANA), mas reproduzida em horas
    simuladas: assim dá para mostrar o rio subindo e baixando na demonstração.
    """
    monitor = _modulo("monitor")
    avancar = _funcao(monitor, "avancar_simulacao")
    reiniciar = _funcao(monitor, "reiniciar_simulacao")
    if not avancar or not reiniciar:
        print("\nA simulação do monitoramento não está disponível nesta versão.")
        return
    print("\nSimulação do nível do rio (demonstração, não é leitura em tempo real):")
    print("  1. Avançar 6 horas")
    print("  2. Avançar 24 horas")
    print("  3. Avançar outra quantidade de horas")
    print("  4. Voltar ao início da série")
    print("  0. Voltar")
    escolha = escolher_opcao("Simulação: ", 4)
    if escolha == 0:
        return
    if escolha == 4:
        reiniciar()
    else:
        horas = {1: 6, 2: 24}.get(escolha) or escolher_opcao("Quantas horas (1 a 500)? ", 500)
        if not horas:
            return
        avancar(horas)
    print(f"Hora simulada: {getattr(monitor, 'horas_simuladas', '?')}")
    if contexto.get("municipio"):
        mostrar_situacao(contexto)
    else:
        print("Informe o município (opção 3) para ver a situação do rio.")


def menu(contexto):
    """Uma opção por linha, com o município e o modelo atuais à vista."""
    municipio = contexto.get("municipio") or "não informado"
    return (
        "\nMenu:\n"
        "  1) Escolher tema\n"
        "  2) Fazer pergunta\n"
        f"  3) Informar município (atual: {municipio})\n"
        "  4) O que fazer agora (precisa do município, opção 3)\n"
        f"  5) Modelo de resposta (atual: {contexto['modelo']})\n"
        "  6) Simular a passagem do tempo (demonstração do monitoramento)\n"
        "  0) Sair"
    )


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    caminho = argv[0] if argv else CAMINHO_BASE
    registros = carregar_ou_sair(caminho)
    contexto = {
        "municipio": None,
        "modelo": MODELO_PADRAO,
        "sinonimos": carregar_sinonimos(),
        "avisos_mostrados": set(),
    }

    print("=== Citizen Assist AI - Assistente para enchentes ===")
    print(AVISO_GERAL)
    acoes = {
        1: lambda: consultar_tema(registros, contexto),
        2: lambda: consultar_pergunta(registros, contexto),
        3: lambda: pedir_municipio(contexto),
        4: lambda: o_que_fazer_agora(registros, contexto),
        5: lambda: trocar_modelo(contexto),
        6: lambda: simular_tempo(contexto),
    }
    while True:
        print(menu(contexto))
        opcao = escolher_opcao("Opção: ", len(acoes))
        if opcao == 0:
            print("Até logo. Em emergência: Defesa Civil 199 | Bombeiros 193.")
            return
        acoes[opcao]()


if __name__ == "__main__":
    main()
