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
| Aelton | Claude Code (Anthropic) | Organização do plano e do cronograma; README a partir do modelo da coordenação; `src/base.py`; `src/sistema.py`; `docs/contratos.md`; `src/respostas.py` | Ver seção 3 |
| Bruno | _a preencher_ | _a preencher_ | _a preencher_ |
| Victor | _a preencher_ | _a preencher_ | _a preencher_ |
| Michelly | _a preencher_ | _a preencher_ | _a preencher_ |

<!-- markdownlint-enable MD013 -->

> Cada integrante completa a sua linha e, se usou IA, acrescenta uma
> subseção na seção 3 no mesmo formato. Quem não usou escreve "não usou".

## 3. Validação crítica

### Aelton — arquitetura, fluxo principal e respostas

**Como a IA foi usada.** O Claude Code trabalhou no repositório a partir de
pedidos específicos: ler o enunciado e o plano, propor a divisão das tarefas,
escrever o carregamento da base, o menu e os dois modelos de resposta. As
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
- **Limites assumidos.** Enquanto `grafo.py` não está pronto, o Modelo B
  mostra só as dependências diretas de cada registro. Isso está documentado
  no código e no contrato, em vez de ser escondido.

**O que não foi delegado à IA:** o conteúdo da base de conhecimento (as
orientações, fontes e datas de verificação são responsabilidade do Bruno,
que descreve o seu processo de verificação na subseção dele) e a escolha
final entre os modelos A e
B, que será feita com os números da bateria de testes do Victor.

## 4. Comparação dos modelos de resposta

_A preencher em 18/11 com os resultados da bateria de testes: taxa de
acerto, clareza percebida no teste de usabilidade e justificativa do modelo
escolhido._
