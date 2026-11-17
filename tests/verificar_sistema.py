"""Verifica o fluxo do menu de ponta a ponta, simulando o que o usuário digita.

Execução (na raiz do repositório): python tests/verificar_sistema.py

O monitoramento é substituído por um monitor de teste, para o fluxo poder ser
verificado nas três fases mesmo antes de src/monitor.py estar pronto.
"""

import builtins
import contextlib
import io
import sys
import types

sys.path.insert(0, "src")
import sistema  # noqa: E402

AVISO = "Dado de referência para demonstração."
ESTADOS = {
    "Rio Antes": {"fase": "antes", "nivel": "normal", "nivel_cm": 200,
                  "tendencia_cm_h": 0.0, "horas_ate_inundacao": None, "aviso": AVISO},
    "Rio Durante": {"fase": "durante", "nivel": "alerta", "nivel_cm": 512,
                    "tendencia_cm_h": 18.5, "horas_ate_inundacao": 4.9, "aviso": AVISO},
    "Rio Depois": {"fase": "depois", "nivel": "alerta", "nivel_cm": 480,
                   "tendencia_cm_h": -6.0, "horas_ate_inundacao": None, "aviso": AVISO},
}


def estado_teste(municipio):
    if municipio not in ESTADOS:
        raise KeyError(municipio)
    return ESTADOS[municipio]


def rodar(entradas, monitor=True):
    """Roda o menu com as entradas dadas e devolve tudo o que foi impresso."""
    fila = list(entradas)

    def falso_input(prompt=""):
        if not fila:
            raise EOFError
        return fila.pop(0)

    original_input = builtins.input
    original_monitor = sys.modules.get("monitor")
    if isinstance(monitor, types.SimpleNamespace):
        sys.modules["monitor"] = monitor
    elif monitor:
        sys.modules["monitor"] = types.SimpleNamespace(estado=estado_teste)
    else:
        sys.modules["monitor"] = types.SimpleNamespace()
    builtins.input = falso_input
    saida = io.StringIO()
    try:
        with contextlib.redirect_stdout(saida):
            sistema.main([])
    finally:
        builtins.input = original_input
        if original_monitor is None:
            sys.modules.pop("monitor", None)
        else:
            sys.modules["monitor"] = original_monitor
    return saida.getvalue()


# Entrada vazia e opção inexistente no menu principal
s = rodar(["", "9", "abc", "0"])
assert "Entrada vazia" in s
assert "Opção inexistente: '9'" in s
assert "Opção inexistente: 'abc'" in s
assert "Até logo" in s

# Pergunta vazia
s = rodar(["2", "", "0"])
assert "Pergunta vazia" in s

# Pergunta com resposta direta (status ok), Modelo B por padrão
s = rodar(["2", "perdi meu rg", "0", "0"])
assert "[DOC-03]" in s
assert "Passo a passo:" in s
assert "Fonte:" in s and "verificado em" in s
assert "Assuntos relacionados:" in s

# Pergunta fora do tema (sem_base): não inventa e sugere alternativas
s = rodar(["2", "receita de bolo", "0"])
assert "Não vou inventar instruções" in s
assert "opção 1 do menu" in s

# Pergunta ambígua: o sistema mostra os candidatos e o usuário escolhe
s = rodar(["2", "segunda via", "2", "0", "0"])
assert "combina com mais de um assunto" in s
assert "1. DOC-01" in s and "2. DOC-02" in s
assert "=== [DOC-02]" in s
s = rodar(["2", "segunda via", "0", "0"])
assert "=== [" not in s  # voltar sem escolher não mostra resposta

# Pré-requisitos completos vindos do grafo (BEN-01 depende de DOC-03 e BEN-03)
s = rodar(["2", "como sacar fgts", "0", "0"])
assert "[BEN-01]" in s
for id_pre in ("DOC-01", "DOC-02", "DOC-03", "BEN-03"):
    assert id_pre in s, id_pre
assert s.index("DOC-01") < s.index("DOC-03")

# Navegação por tema e por relacionado
s = rodar(["1", "2", "3", "1", "0", "0"])
assert "Orientações em 'documentacao':" in s
assert "[DOC-03]" in s
assert s.count("=== [") == 2  # a orientação e o relacionado escolhido

# Troca para o Modelo A
s = rodar(["5", "1", "2", "perdi meu rg", "0", "0"])
assert "Modelo de resposta: A" in s
assert "[DOC-03]" in s and "Passo a passo:" not in s

# Opção inexistente dentro de um submenu
s = rodar(["1", "7", "0", "0"])
assert "Escolha entre 0 e 4" in s

# Fase DURANTE: bloco de segurança antes da resposta
s = rodar(["3", "Rio Durante", "2", "perdi meu rg", "0", "0"])
assert "SEGURANÇA EM PRIMEIRO LUGAR" in s
assert s.index("SEGURANÇA EM PRIMEIRO LUGAR") < s.index("[DOC-03]")
assert "fase DURANTE" in s
assert "Monitoramento: " + AVISO in s

# Fase DURANTE também em pergunta sem base
s = rodar(["3", "Rio Durante", "2", "receita de bolo", "0"])
assert "SEGURANÇA EM PRIMEIRO LUGAR" in s

# Fase ANTES: sem bloco de segurança
s = rodar(["3", "Rio Antes", "2", "perdi meu rg", "0", "0"])
assert "SEGURANÇA EM PRIMEIRO LUGAR" not in s

# "O que fazer agora": prioridades de cada fase
s = rodar(["3", "Rio Depois", "4", "0", "0"])
assert "Orientações prioritárias para a fase 'depois'" in s
assert "DOC-01" in s and "SEG-01" not in s
s = rodar(["3", "Rio Antes", "4", "0", "0"])
assert "fase 'antes'" in s and "SEG-04" in s
s = rodar(["4", "0"])
assert "Informe primeiro o seu município" in s

# Município sem leituras e monitor ausente não derrubam o fluxo
s = rodar(["3", "Cidade X", "2", "perdi meu rg", "0", "0"])
assert "Sem leituras de monitoramento para 'Cidade X'" in s
assert "[DOC-03]" in s
s = rodar(["3", "Rio Durante", "2", "perdi meu rg", "0", "0"], monitor=False)
assert "Monitoramento ainda não disponível" in s
assert "[DOC-03]" in s

# Pergunta sem base: telefones de emergência antes de tudo
s = rodar(["2", "receita de bolo", "0"])
assert s.index("Bombeiros 193 | Defesa Civil 199") < s.index("Não encontrei")

# Menu: uma opção por linha, município e modelo atuais, requisito da opção 4
s = rodar(["3", "Rio Antes", "0"])
assert "  4) O que fazer agora (precisa do município, opção 3)" in s
assert "(atual: não informado)" in s and "(atual: Rio Antes)" in s
assert "Modelo de resposta (atual: B)" in s


# Simulação do tempo (opção 6): o rio sobe e a fase muda
def monitor_simulado():
    relogio = types.SimpleNamespace(horas_simuladas=0)

    def estado(municipio):
        fase = "durante" if relogio.horas_simuladas >= 24 else "antes"
        return dict(ESTADOS["Rio " + fase.capitalize()])

    def avancar(horas):
        relogio.horas_simuladas += horas

    def reiniciar():
        relogio.horas_simuladas = 0

    relogio.estado = estado
    relogio.avancar_simulacao = avancar
    relogio.reiniciar_simulacao = reiniciar
    return relogio


s = rodar(["3", "Rio Antes", "6", "1", "6", "3", "18", "0"], monitor=monitor_simulado())
assert "Hora simulada: 6" in s and "Hora simulada: 24" in s
assert "SEGURANÇA EM PRIMEIRO LUGAR" in s and "fase DURANTE" in s
s = rodar(["6", "2", "6", "4", "0"], monitor=monitor_simulado())
assert "Hora simulada: 24" in s and "Hora simulada: 0" in s
assert "Informe o município (opção 3)" in s
s = rodar(["6", "0"])
assert "simulação do monitoramento não está disponível" in s

# Fim de entrada (Ctrl+D) encerra sem erro
s = rodar([])
assert "Até logo" in s

print("sistema: tudo certo")
