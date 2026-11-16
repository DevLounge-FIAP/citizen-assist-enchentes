# Uso de inteligência artificial

Este documento registra onde a equipe usou ferramentas de IA, para quê, e
como o resultado foi conferido antes de entrar no projeto, conforme pedido
na seção "Uso de inteligência artificial" do enunciado.

## 1. O protótipo não usa modelo de IA em tempo de execução

O Citizen Assist AI não chama nenhuma API, modelo de linguagem ou serviço
externo. Toda resposta mostrada ao usuário é montada a partir de um registro
de `data/base_conhecimento.json`, que foi escrito e verificado pela equipe
com fonte e data de verificação.

Os "modelos de prompt" pedidos no enunciado foram implementados como
**instruções de resposta determinísticas** em `src/respostas.py`
(`INSTRUCAO_MODELO_A` e `INSTRUCAO_MODELO_B`): elas definem o papel do
assistente, o formato da resposta e a obrigação de citar a fonte, e o código
segue essas regras ao montar o texto. Por isso:

- o assistente não inventa orientação: se a busca não encontra um registro
  com pontuação suficiente, a resposta é "não encontrei base suficiente" e
  uma lista de temas;
- a mesma pergunta produz sempre a mesma resposta, o que permite medir a
  taxa de acerto de forma reprodutível;
- não há risco de vazamento de dados: o único dado pedido é o município, e
  ele não sai da máquina do usuário.

Verificação: nenhum arquivo em `src/` importa bibliotecas além da biblioteca
padrão do Python e dos módulos do próprio projeto.

## 2. Onde a IA foi usada no desenvolvimento

<!-- markdownlint-disable MD013 -->

| Integrante | Ferramenta | Uso | Validação |
| --- | --- | --- | --- |
| Aelton | Claude Code (Anthropic) | Organização do plano e do cronograma; README a partir do modelo da coordenação; `src/base.py`; `src/sistema.py`; `docs/contratos.md`; `src/respostas.py`; testes do fluxo e comparação dos modelos; seções do README | Ver seção 3 |
| Bruno | Claude (Anthropic), com busca na web | Pesquisa das fontes oficiais e rascunho dos registros novos da `data/base_conhecimento.json` (de 12 para 21, incluindo o `DOC-07`); `data/sinonimos.json`; validação da base e do grafo; campo `titulo`; ajustes pedidos pela bateria de testes; seção do README sobre a origem das fontes | Ver seção 3 |
| Victor | _a preencher_ | _a preencher_ | _a preencher_ |
| Michelly | _a preencher_ | _a preencher_ | _a preencher_ |

<!-- markdownlint-enable MD013 -->

> Cada integrante completa a sua linha e, se usou IA, acrescenta uma
> subseção na seção 3 no mesmo formato. Quem não usou escreve "não usou".

## 3. Validação crítica

### Aelton — arquitetura, fluxo principal e respostas

**Como a IA foi usada.** O Claude Code trabalhou no repositório a partir de
pedidos específicos: ler o enunciado e o plano, propor a divisão das tarefas,
escrever o carregamento da base, o menu, os dois modelos de resposta, a
integração com a busca e o grafo, os scripts de verificação do fluxo e de
comparação dos modelos, e as seções do README dessa frente. As
decisões de escopo (divisão do grupo, redistribuição das tarefas da quinta
pessoa entre Aelton e Victor, prazos) foram tomadas pela equipe; a IA
registrou essas decisões no plano.

**O que foi conferido e o que mudou por causa disso:**

- **Contra o enunciado.** Cada entrega foi confrontada com os requisitos de
  `docs/requisitos-faculdade.md`: tratamento de arquivo ausente, vazio,
  JSON inválido e registro incompleto em `base.py`; entrada vazia e opção
  inexistente em `sistema.py`; fonte e aviso de confirmação em toda
  resposta.
- **Contra a base real.** Os dois modelos de resposta foram executados sobre
  os 20 registros do Bruno, não só sobre exemplos inventados. Esse teste
  mostrou dois problemas na primeira versão gerada:
  1. a quebra de linha partia os links das fontes ao meio, deixando-os
     inutilizáveis; corrigido desativando a quebra de palavras longas;
  2. o título da resposta usava a primeira palavra-chave, o que gerava
     títulos como "Rg" e "Fgts"; corrigido com o campo opcional `titulo` e,
     na falta dele, o `subtema`.
- **Contra o contrato.** A assinatura de `respostas.formatar` foi comparada
  com a seção 2 do plano. A IA propôs um parâmetro extra (`base`) para
  mostrar os pré-requisitos pelo nome; a mudança foi mantida por ser
  opcional e foi registrada em `docs/contratos.md` para o grupo.
- **Contra a execução, na integração (15/11).** Rodar o menu com a busca
  real do Victor mostrou que a opção "Fazer pergunta" quebrava (`TypeError`),
  porque o fluxo ainda chamava a busca no formato antigo; corrigido e coberto
  por `tests/verificar_sistema.py`, que simula o usuário em 20 situações
  (entradas inválidas, pergunta ambígua, fora do tema, as três fases e
  monitoramento ausente). Na mesma rodada:
  1. uma renomeação de função feita pela IA no `respostas.py` criou uma
     variável com o mesmo nome da função, o que quebraria o Modelo B;
     percebido na revisão do código e corrigido antes de rodar;
  2. a primeira versão de `tests/comparar_modelos.py` mostrava 0% de aviso
     de confirmação nos dois modelos. A conferência manual das respostas
     mostrou que o aviso estava lá: o erro era do script, que procurava o
     texto sem considerar a quebra de linha. O número foi corrigido antes de
     ir para o README;
  3. o aviso "monitoramento indisponível" se repetia a cada resposta;
     passou a aparecer uma vez por sessão.
- **Limites assumidos.** O `monitor.py` ainda não existe; o fluxo foi
  verificado com um monitor simulado no teste, e o README não afirma nada
  sobre o monitoramento real.

**O que não foi delegado à IA:** o conteúdo da base de conhecimento (as
orientações, fontes e datas de verificação são responsabilidade do Bruno,
que descreve o seu processo de verificação na subseção dele) e a escolha
final entre os modelos A e B: o Modelo B foi adotado como padrão com base
na comparação objetiva, e a decisão será confirmada com a bateria de testes
e o teste de usabilidade do Victor.

### Bruno — base de conhecimento e curadoria das fontes

**Como a IA foi usada.** O Claude trabalhou a partir de pedidos específicos:
pesquisar na web a página oficial de cada assunto (Caixa, gov.br, TSE, Receita,
Defesa Civil, ONR), redigir os registros no formato do contrato, montar o
dicionário de sinônimos, validar a base com o `src/base.py` do grupo e com uma
verificação de ciclos e de ordem de pré-requisitos no grafo, e redigir a seção
do README sobre a origem das informações. As decisões de conteúdo (quais temas
cobrir, a distribuição entre os quatro temas e quais registros dependem de
quais) foram tomadas por mim. Os 12 primeiros registros 
(SEG-01 a SEG-06, DOC-01 a DOC-03, BEN-01, MOR-01 e MOR-02) foram escritos por 
mim a partir de páginas oficiais; a IA foi usada nos registros seguintes.

**O que foi conferido e o que mudou por causa disso:**

- **Contra o arquivo real.** Os arquivos `data/base_conhecimento.json` e
  `data/sinonimos.json` chegaram a ser enviados ao repositório vazios: o
  conteúdo tinha sido colado no editor sem salvar. O `git log --stat`
  mostrou `0 insertions` e a validação com `base.py` respondeu "a base não
  contém nenhum registro". Os arquivos foram preenchidos, salvos e só então
  enviados, e o commit passou a mostrar as linhas inseridas.
- **Contra a fonte.** A IA propôs fontes que depois se mostraram fracas, e elas
  foram trocadas ou sinalizadas: o `BEN-02` (Auxílio Reconstrução) usava um blog
  e passou a citar a Agência Gov e a página do programa, com o aviso de que foi
  um benefício de 2024 exclusivo do Rio Grande do Sul; o `MOR-01` e o `SEG-05`
  tinham fonte genérica e passaram a citar a Defesa Civil de Santo André; o
  `SEG-04` usa uma página da Defesa Civil do Paraná, e isso está dito no
  campo `fonte`.
- **Limites assumidos.** Não foi possível abrir a página oficial da Prefeitura
  de Santo André: as informações locais vêm de reportagens sobre a Defesa
  Civil municipal e estão marcadas para confirmação. Não foi encontrada uma
  lista pública de abrigos, e por isso a base não inventa locais. Para o
  `BEN-03` não há página única de consulta, e o registro cita a Caixa. Os
  materiais da Caixa usados no `DOC-07` eram cópias hospedadas em sites de
  prefeituras. Conferi o DOC-07 e o BEN-01 na página oficial da Caixa e a 
  CNH no site do Detran-SP; os valores e as regras batiam com a base.
- **Contra a bateria de testes (15/11).** Os testes do Victor mostraram que
  perguntas genéricas como "meu documento sumiu" não encontravam nada. Foi
  criado o `DOC-07` (visão geral de documentos). Os testes também mostraram
  sinônimos que puxavam o registro errado (`casa` levava ao `MOR-03`;
  `agua subindo` e `alagou` levavam "depois da enchente" ao `SEG-03`): esses
  termos foram retirados, e o `MOR-01` ganhou palavras de rachadura. Duas
  verificações do `tests/verificar_busca.py` que exigiam "sem base" para essas
  perguntas foram atualizadas, e a suíte passou a verificar o `DOC-07`.
- **Contra o grafo.** A base foi verificada para garantir que todo
  `depende_de` aponta para um `id` existente e que não há ciclos; o `BEN-01`
  devolve a ordem `DOC-01 → DOC-02 → DOC-03 → BEN-03 → BEN-01`.

**O que não foi delegado à IA:** a decisão de quais assuntos entram na base e a
responsabilidade pelo que a base afirma. Os registros com
`requer_confirmacao: true` (13 de 21) existem porque valores, prazos e regras
mudam e variam por estado ou município, e a resposta avisa o usuário para
confirmar no órgão.

## 4. Comparação dos modelos de resposta

A comparação objetiva (regras cumpridas, tamanho e tempo de cada resposta)
está no README, seção "Regras de resposta, prompts e tratamento das
limitações", e pode ser refeita com `python tests/comparar_modelos.py`.
Nenhuma ferramenta de IA participa das respostas comparadas: as duas são
geradas pelo código a partir da mesma base.

_A completar em 18/11 com a bateria de testes e o teste de usabilidade
(clareza percebida por quem é de fora da equipe)._