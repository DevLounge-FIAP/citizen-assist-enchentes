"""Menu e fluxo principal do Citizen Assist AI.

Execução: python src/sistema.py [caminho_da_base]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import base  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BASE = os.path.join(RAIZ, "data", "base_conhecimento.json")

AVISO_GERAL = (
    "Este assistente é um protótipo educacional e NÃO é um canal oficial. "
    "Em risco imediato ligue 193 (Bombeiros); para alertas, Defesa Civil 199."
)
BLOCO_SEGURANCA = (
    "!! SEGURANÇA EM PRIMEIRO LUGAR !!\n"
    "Se estiver em área de risco, saia para um local alto e seguro.\n"
    "Defesa Civil: 199 | Bombeiros: 193"
)


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


def mostrar_bloco_seguranca(municipio):
    """Na fase 'durante' o bloco de segurança vem antes de qualquer resposta."""
    estado_fn = _funcao(_modulo("monitor"), "estado")
    if not (estado_fn and municipio):
        return
    try:
        estado = estado_fn(municipio)
    except Exception as erro:  # monitoramento não pode derrubar o fluxo
        print(f"(Monitoramento indisponível: {erro})")
        return
    if estado.get("fase") == "durante":
        print("\n" + BLOCO_SEGURANCA)


def apresentar(registro, contexto):
    formatar = _funcao(_modulo("respostas"), "formatar")
    if formatar:
        print("\n" + formatar(registro, "A", contexto))
        return
    print(f"\n[{registro['id']}] {registro['orientacao']}")
    print(f"Fonte: {registro['fonte']} (verificado em {registro['data_verificacao']})")
    if registro.get("requer_confirmacao"):
        print("Aviso: confirme os requisitos atualizados no órgão responsável.")


def sem_resposta(registros_base):
    print("\nNão encontrei base suficiente para orientar sobre isso.")
    print("Não vou inventar instruções. Tente outras palavras ou escolha um tema:")
    for tema in base.listar_temas(registros_base):
        print(f"  - {tema}")


def consultar_tema(registros_base, contexto):
    temas = base.listar_temas(registros_base)
    print("\nTemas disponíveis:")
    for i, tema in enumerate(temas, start=1):
        print(f"  {i}. {tema}")
    print("  0. Voltar")
    escolha = escolher_opcao("Tema: ", len(temas))
    if escolha == 0:
        return
    itens = base.registros_do_tema(registros_base, temas[escolha - 1])
    print(f"\nOrientações em '{temas[escolha - 1]}':")
    for i, registro in enumerate(itens, start=1):
        print(f"  {i}. {registro['id']} - {registro['palavras_chave'][0]}")
    print("  0. Voltar")
    escolha = escolher_opcao("Orientação: ", len(itens))
    if escolha:
        mostrar_bloco_seguranca(contexto.get("municipio"))
        apresentar(itens[escolha - 1], contexto)


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
    resultados = buscar(pergunta, registros_base)
    mostrar_bloco_seguranca(contexto.get("municipio"))
    if not resultados:
        sem_resposta(registros_base)
        return
    apresentar(resultados[0][0], contexto)


def pedir_municipio(contexto):
    print("\nO único dado pedido é o município (não coletamos dados pessoais).")
    municipio = ler("Município (Enter para pular): ")
    contexto["municipio"] = municipio or None
    if municipio:
        print(f"Município definido: {municipio}")


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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    caminho = argv[0] if argv else CAMINHO_BASE
    registros = carregar_ou_sair(caminho)
    contexto = {"municipio": None}

    print("=== Citizen Assist AI - Assistente para enchentes ===")
    print(AVISO_GERAL)
    while True:
        print("\nMenu: 1) Escolher tema  2) Fazer pergunta  3) Informar município  0) Sair")
        opcao = escolher_opcao("Opção: ", 3)
        if opcao == 0:
            print("Até logo. Em emergência: Defesa Civil 199 | Bombeiros 193.")
            return
        if opcao == 1:
            consultar_tema(registros, contexto)
        elif opcao == 2:
            consultar_pergunta(registros, contexto)
        else:
            pedir_municipio(contexto)


if __name__ == "__main__":
    main()
