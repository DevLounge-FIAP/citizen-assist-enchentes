import sys
sys.path.insert(0, "src")
from busca import normalizar

"""Assert serve para verificar se uma suposição é verdadeira, caso seja falsa ele encerra o programa com um erro. No caso abaixo ele verifica se a normalização está funcionando."""

assert normalizar("Perdi meu RG na enchente!") == "perdi meu rg na enchente"
assert normalizar("SÃO PAULO ") == "sao paulo"
assert normalizar("são-paulo") == "sao paulo"
assert normalizar("ção") == "cao"
assert normalizar("rg,identidade") == "rg identidade"
assert normalizar("") == ""
assert normalizar("   ") == ""
assert normalizar("RG    rg") == "rg rg"
print("2ª via ->", repr(normalizar("2ª via")))   # só observar

print("tudo certo")

