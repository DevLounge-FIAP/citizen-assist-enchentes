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
| Victor | Claude (Anthropic), como mentor de estudo e apoio ao desenvolvimento | Explicação dos conceitos (normalização, similaridade de Jaccard, sinônimos, grafo, ordenação topológica e detecção de ciclos); código de `src/busca.py` e `src/grafo.py` proposto passo a passo; rascunho das perguntas de `tests/perguntas_teste.json`; scripts `tests/verificar_busca.py`, `tests/verificar_grafo.py` e `tests/avaliar_busca.py`; roteiro do teste de usabilidade; seções do README sobre busca e resultados | Ver seção 3 |
| Michelly | Claude (Anthropic) | Orientação na busca dos dados reais e das cotas (ANA/HidroWeb/SGB), validação dos códigos do monitoramento, seções do README | Ver seção 3 |

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
- **Limites assumidos.** O fluxo foi verificado com um monitor simulado no
  teste e, depois da entrada do `monitor.py` real, com o roteiro da
  demonstração (município Estrela, opção 6 do menu).

**O que não foi delegado à IA:** o conteúdo da base de conhecimento (as
orientações, fontes e datas de verificação são responsabilidade do Bruno,
que descreve o seu processo de verificação na subseção dele) e a escolha
final entre os modelos A e B: o Modelo B foi adotado como padrão com base
na comparação objetiva e mantido depois da bateria de testes e do teste de
usabilidade (ver a seção 4).

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

### Michelly — monitoramento e cenário de cheia

**Como a IA foi usada.** O Claude foi usado para auxiliar a encontrar as cotas de alerta/inundação e os dados reais de nível dos rios. 
O portal da HidroWeb não disponibilizava os dados hora a hora, então o Claude apresentou a solução de obter os dados pela telemetria 
da ANA no formato XML. Os níveis e as cotas são dados oficiais dos períodos de cada cheia e não tiveram influência da IA, justamente 
por serem dados concretos e não fictícios. Além disso, o Claude foi usado para validar os códigos e em seções do README. 

**O que foi conferido e o que mudou por causa disso:**

- **Contra o contrato.** Comparei o monitor.py com o docs/contratos.md e ajustei: a data não deveria ter os segundos, nível e cotas deveriam
  ser número inteiro e deveria dar KeyError quando a cidade não tem leitura.
- **Fonte dos dados.** A opção de Séries Históricas da HidroWeb só tinha dados até 2008. Com o objetivo de pegar dados mais recentes, a telemetria
  da ANA surgiu como alternativa. Então, para garantir que os dados batiam com os oficiais, comparei os níveis do XML com os boletins do SGB.
- **Dados repetidos.** Inicialmente não havia checagem para dados repetidos, então foi identificada uma brecha que permitiria dados
  duplicados no CSV. A partir disso, uma validação de cidade/hora foi inserida. Agora é possível adicionar dados de outras cidades que
  sigam o mesmo padrão da ANA sem repetição.
- **Sugestões.** A IA sugeriu salvar as respostas de cada estação pra não perguntar de novo. Não aceitei porque acho que faz
  mais sentido inserir os dados manualmente, o que simplifica o preparar_dados.py.
- **Aviso.** Eu tinha mudado o texto do aviso e ele ficou repetindo o aviso que já existe no sistema.py. Voltei pro aviso padrão do plano.
- **Limitação.** Perto do pico de Uruguaiana o rio fica quase parado, e a fase troca entre "durante" e "depois". Decidi manter a regra do plano e registrar como limitação.

**O que não foi delegado à IA:** a escolha de usar dados reais em vez de dados criados, a definição das etapas de tratamento dos dados 
(uma leitura por hora, preenchimento das horas faltantes e junção sem repetição), o workflow de obtenção dos dados (transformar os XMLs em CSV, 
depois unir os CSVs e trabalhar em cima deles), a estrutura dos CSVs e os níveis de alerta, definidos em contrato com o grupo, e o limite da cota de atenção.

### Victor — busca, grafo e avaliação
 
**Como a IA foi usada.** O Claude atuou como mentor de estudo: cada trecho de código vinha com a explicação do raciocínio antes, e eu digitava, rodava e só avançava depois de entender. Ele propôs a estrutura de `src/busca.py` (normalização, tokenização, Jaccard, sinônimos, limiar e ambiguidade) e de `src/grafo.py` (montagem do grafo, ordem de pré-requisitos, ciclos e `relacionados`), os scripts de verificação e de avaliação e o roteiro do teste de usabilidade. As perguntas T01 a T15 foram rascunhadas pela IA e revisadas por mim; as T16 a T20 eu escrevi do meu jeito, antes de rodar. As decisões de regra (por exemplo, `relacionados` por tema e fase) e o que entra como limitação foram minhas.
 
**O que foi conferido e o que mudou por causa disso:**
 
- **Contra a execução.** Cada função foi conferida com `assert` antes de avançar (`tests/verificar_busca.py` e `tests/verificar_grafo.py`), incluindo casos de borda: texto vazio, acentos, palavra dentro de outra palavra (`cin` em `argentina`), ciclo, auto-dependência e diamante de dependências. Um erro meu (passar os sinônimos para `tokenizar`, que só normaliza) foi corrigido separando as responsabilidades: `expandir` aplica os sinônimos.
- **Contra a base real.** As perguntas que escrevi do meu jeito mostraram que o grupo `agua` do dicionário puxava qualquer pergunta sobre água para o registro de água potável. Pedi ao Bruno a troca da chave para `agua potavel` e acrescentei um teste de regressão; ao desfazer a correção de propósito, o teste falhou, o que confirmou que ele protege contra o problema.
- **Contra o uso.** O limiar da busca começou em 0,10 e foi para 0,11 depois que duas perguntas vagas tiraram exatamente 0,10 e receberam resposta com confiança. A pergunta "carteira" mostrou que empates abaixo do limiar deviam virar `ambigua`, e criamos a zona cinza.
- **Contra a base de testes.** A IA sugeriu um campo de risco em `perguntas_teste.json`; descartei, porque a classificação de risco é testada pela Michelly. O esperado de cada pergunta foi definido a partir da base, e não da saída do sistema, para o teste não ser circular.
- **Contra os números.** A primeira rodada deu 16 de 20 (80%). Para a T20, o diagnóstico mostrou nota 0,045 (uma palavra em comum, 1/22). Decidi **não** baixar o limiar só para ela, porque isso deixaria as perguntas fora do tema passarem; ela ficou como limitação.
- **Contra o usuário real.** O teste de usabilidade foi feito com uma participante de verdade; nenhum resultado foi gerado por IA. A IA ajudou a montar o roteiro e a organizar as anotações depois.
**O que não foi delegado à IA:** as decisões sobre limiares e regras, a escolha do que registrar como limitação, a aplicação do teste de usabilidade e a coleta dos resultados, e os pedidos de mudança nos dados do Bruno, que cuida da base.

## 4. Comparação dos modelos de resposta

A comparação objetiva (regras cumpridas, tamanho e tempo de cada resposta)
está no README, seção "Regras de resposta, prompts e tratamento das
limitações", e pode ser refeita com `python tests/comparar_modelos.py`.
Nenhuma ferramenta de IA participa das respostas comparadas: as duas são
geradas pelo código a partir da mesma base.

**Decisão final: Modelo B como padrão.** Os dois modelos cumprem as regras
de confiabilidade em 100% das 63 respostas; só o B mostra a situação do
município (42 de 42) e os pré-requisitos em ordem (33 de 33). A bateria de
perguntas avalia a busca, que é a mesma para os dois modelos, então não
favorece nenhum deles. No teste de usabilidade, a participante leu apenas
respostas no Modelo B e as achou claras e acionáveis. Ela não viu respostas
no Modelo A, então a preferência do usuário entre os dois não foi medida;
isso está registrado como limitação e melhoria no README.