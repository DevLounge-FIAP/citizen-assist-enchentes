import sys
sys.path.insert(0, "src")
from busca import normalizar, tokenizar, jaccard

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

"""Verifica as tokenizações."""

assert tokenizar("Como tirar a segunda via do meu RG?") == {"tirar", "segunda", "via", "rg"}
assert tokenizar("o de a?") == set()
assert type(tokenizar("o de a?")) is set
assert tokenizar("RG rg Rg") == {"rg"}
assert tokenizar("Você precisa") == {"precisa"}
assert tokenizar("não consigo sair") == {"nao", "consigo", "sair"}

A = {"perdi", "rg"}
B = {"rg", "identidade", "segunda", "via"}

"""Verifica a similaridade de Jaccard."""

assert jaccard(A, B) == 0.2
assert jaccard(A, B) == jaccard(B, A)
assert jaccard({"a","b"}, {"a","b"}) == 1.0
assert jaccard({"a"}, {"b"}) == 0.0
assert jaccard(set(), set()) == 0.0
assert jaccard(set(), {"a"}) == 0.0
assert round (jaccard({"fgts", "saque"}, {"fgts", "saque", "calamidade"}), 2) == 0.67   
assert isinstance(jaccard(A, B), float)


print("tudo certo")

