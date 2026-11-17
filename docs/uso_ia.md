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
| Bruno | _a preencher_ | _a preencher_ | _a preencher_ |
| Victor | _a preencher_ | _a preencher_ | _a preencher_ |
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
- **Limites assumidos.** O `monitor.py` ainda não existe; o fluxo foi
  verificado com um monitor simulado no teste, e o README não afirma nada
  sobre o monitoramento real.

**O que não foi delegado à IA:** o conteúdo da base de conhecimento (as
orientações, fontes e datas de verificação são responsabilidade do Bruno,
que descreve o seu processo de verificação na subseção dele) e a escolha
final entre os modelos A e B: o Modelo B foi adotado como padrão com base
na comparação objetiva, e a decisão será confirmada com a bateria de testes
e o teste de usabilidade do Victor.

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

## 4. Comparação dos modelos de resposta

A comparação objetiva (regras cumpridas, tamanho e tempo de cada resposta)
está no README, seção "Regras de resposta, prompts e tratamento das
limitações", e pode ser refeita com `python tests/comparar_modelos.py`.
Nenhuma ferramenta de IA participa das respostas comparadas: as duas são
geradas pelo código a partir da mesma base.

_A completar em 18/11 com a bateria de testes e o teste de usabilidade
(clareza percebida por quem é de fora da equipe)._
