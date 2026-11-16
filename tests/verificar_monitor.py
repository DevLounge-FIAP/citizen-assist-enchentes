"""
Script de Testes e Validação do Arquivo monitor.py
"""

import sys
sys.path.insert(0, "src")

from monitor import estado, carregar_simulacao, avancar_simulacao, reiniciar_simulacao

print("=== Verificação do monitoramento dos rios ===")

print("\n=== TESTE 1: Verificação do nível normal ===")
reiniciar_simulacao()
resultado = estado("Estrela")
assert resultado["nivel"] == "normal", "Estrela na hora 0 deveria estar normal"
assert resultado["fase"] == "antes", "Estrela na hora 0 deveria estar na fase antes"
print("Estrela hora 0 |", resultado["nivel_cm"], "cm |", resultado["nivel"], "|", resultado["fase"])
print("✓ Nível normal válido")

print("\n=== TESTE 2: Verificação do nível de atenção ===")
reiniciar_simulacao()
avancar_simulacao(108)
resultado = estado("Uruguaiana")
assert resultado["nivel"] == "atenção", "Uruguaiana na hora 108 deveria estar em atenção"
assert resultado["fase"] == "antes", "Uruguaiana na hora 108 deveria estar na fase antes"
print("Uruguaiana hora 108 |", resultado["nivel_cm"], "cm |", resultado["nivel"], "|", resultado["fase"])
print("✓ Nível de atenção válido")

print("\n=== TESTE 3: Verificação do nível de alerta ===")
reiniciar_simulacao()
avancar_simulacao(132)
resultado = estado("Uruguaiana")
assert resultado["nivel"] == "alerta", "Uruguaiana na hora 132 deveria estar em alerta"
assert resultado["fase"] == "durante", "Uruguaiana na hora 132 deveria estar na fase durante"
print("Uruguaiana hora 132 |", resultado["nivel_cm"], "cm |", resultado["nivel"], "|", resultado["fase"])
print("✓ Nível de alerta válido")

print("\n=== TESTE 4: Verificação do nível de inundação ===")
reiniciar_simulacao()
avancar_simulacao(36)
resultado = estado("Estrela")
assert resultado["nivel"] == "inundação", "Estrela na hora 36 deveria estar em inundação"
assert resultado["fase"] == "durante", "Estrela na hora 36 deveria estar na fase durante"
print("Estrela hora 36 |", resultado["nivel_cm"], "cm |", resultado["nivel"], "|", resultado["fase"])
print("✓ Nível de inundação válido")

print("\n=== TESTE 5: Verificação da fase depois ===")
reiniciar_simulacao()
avancar_simulacao(96)
resultado = estado("Estrela")
assert resultado["tendencia_cm_h"] < 0, "Estrela na hora 96 deveria estar baixando"
assert resultado["fase"] == "depois", "Estrela na hora 96 deveria estar na fase depois"
print("Estrela hora 96 |", resultado["nivel_cm"], "cm |", resultado["tendencia_cm_h"], "cm/h |", resultado["fase"])
print("✓ Fase depois válida")

print("\n=== TESTE 6: Verificação do fim dos dados ===")
leituras = carregar_simulacao("Estrela")
ultimo_nivel = leituras[-1][1]
reiniciar_simulacao()
avancar_simulacao(9999)
resultado = estado("Estrela")
assert resultado["nivel_cm"] == ultimo_nivel, "Depois do fim dos dados deveria usar a última leitura"
print("Estrela hora 9999 |", resultado["nivel_cm"], "cm | última leitura:", ultimo_nivel, "cm")
print("✓ Fim dos dados válido")

print("\n=== TESTE 7: Verificação de cidade sem leituras ===")
deu_erro = False
try:
    estado("Cidade Teste")
except KeyError:
    deu_erro = True
assert deu_erro, "Cidade sem leituras deveria dar KeyError"
print("✓ Cidade sem leituras válida")

print("\n=== Testes concluídos com sucesso ===")
