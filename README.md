# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="assets/logo-fiap.png"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

<br>

# Citizen Assist AI — Assistente para o ciclo de enchentes

## Global Solution 2026.2 — CitizenTech

## 👨‍🎓 Integrantes DevLounge

| Integrante | RM | Frente |
| --- | --- | --- |
| [Aelton](https://github.com/Aelton0) | 573694 | Arquitetura, integração, fluxo principal, respostas e prompts |
| [Bruno](https://github.com/Bruno-S-Martins) | 572073 | Base de conhecimento e curadoria das fontes |
| [Victor](https://github.com/VMantovaniKT) | 570608 | Busca, grafo e avaliação |
| [Michelly](https://github.com/ChellySantos) | 573625 | Monitoramento e cenário de cheia |


## 👩‍🏫 Professores

### Tutor(a)

- <a href="https://www.linkedin.com/in/andretritiack/">Andre Tritiack de Farias</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

### Problema e público beneficiado

Antes, durante e depois de uma enchente, a pessoa precisa de informações
espalhadas por vários órgãos: como se preparar, como se proteger, como
recuperar documentos perdidos, sacar o FGTS por calamidade, pedir auxílios e
regularizar o imóvel. Muitas etapas dependem umas das outras, e a pessoa não
sabe por onde começar. O público beneficiado são moradores de áreas sujeitas a
enchentes.

### Solução

Assistente de texto em Python que orienta o cidadão nas três fases do desastre.
Um módulo de monitoramento (dados simulados e referenciados) informa a fase do
município, e o assistente muda suas prioridades conforme ela:

| Fase | O que o assistente prioriza |
| --- | --- |
| **Antes** | Preparação: kit de emergência, documentos em local seguro, alertas da Defesa Civil, rotas para abrigos |
| **Durante** | Segurança primeiro: bloco com contatos de emergência antes de qualquer resposta |
| **Depois** | Recuperação: pré-requisitos de documentos (grafo), FGTS calamidade, auxílios, vistoria do imóvel |

**Temas abordados:** documentação, benefícios e financeiro, segurança e
alertas, moradia.

### Organização da base de conhecimento, estruturas e estratégia de busca

#### Base de conhecimento: estrutura, origem das informações e verificação

A base fica em `data/base_conhecimento.json` e tem **21 registros** nos quatro
temas do projeto e nas três fases do desastre. O formato completo está em
[`docs/contratos.md`](docs/contratos.md).

| Tema | Registros | Conteúdo |
| --- | --- | --- |
| Segurança e alertas | 6 | Alertas da Defesa Civil, telefones de emergência, o que fazer durante a inundação, kit de emergência, local seguro, preparação da casa |
| Documentação | 7 | Certidões, CPF, identidade (CIN), carteira de trabalho, título de eleitor, CNH e uma visão geral dos documentos necessários (`DOC-07`) |
| Benefícios e financeiro | 4 | Saque-calamidade do FGTS, município habilitado, auxílios federais, Cadastro Único e assistência social |
| Moradia | 4 | Vistoria e interdição, limpeza depois da enchente, documentos do imóvel, registro de danos e seguro |

Por fase: **4** registros de *antes*, **2** de *durante* e **15** de *depois*.
A maior parte está na recuperação porque é nela que as etapas dependem umas das
outras.

**Campos de cada registro**

| Campo | Função |
| --- | --- |
| `id` | Identificador único (ex.: `DOC-03`), usado pelo grafo |
| `titulo` (opcional) | Nome legível para o menu e as respostas (ex.: "CPF (comprovante e regularização)") |
| `tema`, `subtema` | Organização por assunto |
| `fase` | `antes`, `durante` ou `depois` |
| `palavras_chave` | Termos usados pela busca, com e sem acento |
| `orientacao` | Texto da orientação ao cidadão |
| `fonte` | Órgão e link de onde a informação foi tirada |
| `data_verificacao` | Dia em que a informação foi conferida |
| `requer_confirmacao` | `true` quando valores, prazos ou regras variam e o usuário deve confirmar no órgão |
| `depende_de` | `id` dos registros que devem ser feitos antes; forma o grafo |

O `src/base.py` valida os campos obrigatórios, ignora registros inválidos com
aviso e remove referências de `depende_de` a ids inexistentes.

**Origem das informações**

As orientações foram redigidas a partir de fontes públicas, priorizando páginas
oficiais, e reescritas em linguagem simples (sem copiar o texto):

- **Governo Federal (gov.br):** alertas da Defesa Civil, CPF (Receita Federal),
  Carteira de Identidade Nacional, Carteira de Trabalho Digital (Ministério do
  Trabalho e Emprego), Cadastro Único (Ministério do Desenvolvimento e
  Assistência Social) e Auxílio Reconstrução (Ministério da Integração e do
  Desenvolvimento Regional, via Agência Gov).
- **Caixa Econômica Federal:** saque-calamidade do FGTS, habilitação dos
  municípios e documentos do trabalhador. Em `DOC-07`, parte da lista foi
  conferida em materiais da Caixa publicados por prefeituras.
- **Tribunal Superior Eleitoral:** segunda via do título de eleitor.
- **Defesa Civil:** orientações da Defesa Civil de São Paulo e do Paraná (kit de
  emergência) e atendimento da Defesa Civil de Santo André.
- **Registro Civil e de imóveis:** Portal do Registro Civil e RI Digital (ONR).
- **Ministério da Saúde:** cuidados de saúde depois da enchente.
- **Fontes de apoio:** Idec e Procon-SP (seguro residencial), Detran e Senatran
  (CNH) e reportagens locais sobre a Defesa Civil de Santo André. Quando não foi
  possível abrir a página oficial, isso aparece no campo `fonte` do registro.

**Processo de verificação**

1. Cada registro foi escrito a partir da página do órgão responsável.
2. Todo registro traz órgão, link e `data_verificacao` (11/11/2026; o `DOC-07`
   é de 15/11/2026, e o `DOC-04` foi reverificado em 18/11/2026, quando a
   fonte antiga saiu do ar).
3. **13 dos 21 registros** têm `requer_confirmacao: true` (`BEN-01` a `BEN-04`,
   `DOC-01`, `DOC-03`, `DOC-06`, `DOC-07`, `MOR-01`, `MOR-03`, `MOR-04`,
   `SEG-04` e `SEG-05`): valor, prazo ou procedimento varia por estado,
   município ou momento, e o assistente avisa o usuário para confirmar no órgão.
4. A pesquisa e o rascunho dos registros tiveram apoio de IA; o que foi feito e
   o que foi conferido pela equipe está em [`docs/uso_ia.md`](docs/uso_ia.md).
5. Depois da bateria de testes da busca, a base foi ajustada: criação do
   `DOC-07` (perguntas genéricas sobre documentos não achavam nada), novas
   palavras-chave no `MOR-01` (rachadura, trinca) e retirada de sinônimos que
   puxavam o registro errado.

**Grafo de pré-requisitos (`depende_de`)**

**11** dos 21 registros dependem de outros, em **16 ligações**. O grafo é
dirigido e não tem ciclos. Exemplos:

- **FGTS** (`BEN-01`): depende da identidade (`DOC-03`) e do município habilitado
  (`BEN-03`). A identidade depende da certidão (`DOC-01`) e do CPF (`DOC-02`).
  Ordem: `DOC-01 → DOC-02 → DOC-03 → BEN-03 → BEN-01`.
- **Limpeza da casa** (`MOR-02`): depende da vistoria (`MOR-01`).
- **Durante a inundação** (`SEG-03`): depende dos contatos de emergência
  (`SEG-02`).

O `DOC-07` é uma visão geral e não depende de nenhum registro.

**Dicionário de sinônimos**

O arquivo `data/sinonimos.json` tem **30 grupos** e **137 sinônimos**, em
minúsculas e sem acentos, cobrindo a linguagem de quem está em situação de
estresse (*perdi*, *roubaram*, *levou a água*), os números de emergência
(*199*, *193*, *192*, *190*) e os termos de cada órgão (*CIN*, *CadÚnico*,
*CNH*, *matrícula*). Termos amplos demais foram retirados quando faziam a busca
errar (por exemplo, *casa* puxava os documentos do imóvel).

**Limitações da base**

- Valores, prazos e taxas mudam e variam por estado e município (taxa da segunda
  via de identidade e CNH, prazo do saque-calamidade).
- O Auxílio Reconstrução (`BEN-02`) foi um benefício de 2024 exclusivo do Rio
  Grande do Sul e está na base como exemplo.
- Não há lista de abrigos: os locais são definidos pela Defesa Civil de cada
  município durante o desastre (`SEG-05`).
- Algumas informações de Santo André vêm de reportagens sobre a Defesa Civil
  municipal, por não ter sido possível abrir a página oficial da prefeitura.
- A base não substitui os canais oficiais: em risco, ligue para a Defesa Civil
  (**199**) ou os Bombeiros (**193**).

#### Estratégia de busca e grafo de pré-requisitos

**Por que sobreposição de termos.** A base tem 21 registros curados e o assistente não pode inventar orientação. Por isso a busca foi feita com um método que é **explicável** (dá para mostrar por que um registro foi escolhido), **determinístico** (a mesma pergunta dá sempre a mesma resposta, o que torna a taxa de acerto reprodutível) e **sem dependências** (só a biblioteca padrão do Python). Um modelo de linguagem ou embeddings exigiriam bibliotecas externas e poderiam gerar texto não verificado, o que contraria a regra de nunca inventar orientação. O custo é que a busca compara **palavras**, não sentido (ver limitações).

**Como a busca funciona** (`buscar(pergunta, base, sinonimos)` em `src/busca.py`):

| Etapa | O que faz | Exemplo |
| --- | --- | --- |
| 1. Normalizar | Minúsculas, sem acentos, pontuação vira espaço, espaços repetidos removidos | `"Perdi meu RG na enchente!"` → `"perdi meu rg na enchente"` |
| 2. Tokenizar | Divide em palavras e remove as *stopwords* (`como`, `a`, `o`, `do`, `meu`, `de`, `você`) | `"como tirar a segunda via do meu RG"` → `{tirar, segunda, via, rg}` |
| 3. Expandir por sinônimos | Se um termo de um grupo de `data/sinonimos.json` aparece na pergunta (palavra ou expressão inteira), todos os termos do grupo entram | Um grupo com `rg` e `carteira de identidade` é ativado pelos dois lados; `cin` não dispara dentro de `argentina` |
| 4. Pontuar | Similaridade de Jaccard entre as palavras da pergunta e todas as palavras-chave de cada registro: `\|A ∩ B\| / \|A ∪ B\|` | `{perdi, rg}` e `{rg, identidade, segunda, via}`: 1 em comum, 5 no total → 0,20 |
| 5. Decidir | Ordena por nota e aplica as regras abaixo | |

A lista de *stopwords* é curta de propósito: "não" e "sem" ficam, porque mudam o sentido. Uma lista maior foi testada e descartada.

**Regras de decisão** (a busca devolve até 3 resultados, em ordem decrescente de nota):

| Situação | Regra | `status` | O que o sistema faz |
| --- | --- | --- | --- |
| Nenhuma palavra em comum, ou melhor nota abaixo de **0,11** (`LIMIAR`) | Sem base confiável | `sem_base` | Diz que não encontrou, não inventa, sugere palavras e repete os telefones de emergência |
| Nota do 2º colocado ≥ **85%** da nota do 1º (`MARGEM = 0,85`) | Dois assuntos colados | `ambigua` | Mostra os candidatos e pergunta qual o usuário quer |
| Nota entre **0,09** e 0,11 com empate (zona cinza, `LIMIAR_AMBIGUA`) | Tema entendido, assunto não | `ambigua` | Igual à anterior |
| Demais casos | Um vencedor claro | `ok` | Usa o primeiro resultado |

Os três valores foram calibrados com perguntas reais, não escolhidos de antemão:

- O limiar começou em 0,10, mas duas perguntas vagas tiraram exatamente 0,10 e recebiam resposta com confiança. Subiu para 0,11.
- A zona cinza surgiu porque "carteira" (uma palavra, três documentos empatados abaixo do limiar) saía como `sem_base`. Quando há empate, perguntar qual assunto é melhor do que dizer "não sei".
- O Jaccard **penaliza perguntas longas**: cada palavra sem correspondência aumenta o denominador. No caso T20, a pergunta tem 13 palavras, o registro tem 10 e só 1 é comum: 1 / 22 = 0,045, abaixo do limiar.

**Grafo de pré-requisitos** (`src/grafo.py`):

- `montar_grafo` lê o campo `depende_de` e monta um dicionário `{id: [ids dos quais depende]}`, ignorando ids que não existem. A seta vai do registro dependente para o pré-requisito.
- `pre_requisitos(id, base)` faz uma busca em profundidade e só coloca um registro na lista **depois** de todos os seus pré-requisitos. Isso devolve a ordem pronta (é uma ordenação topológica) e cada id aparece uma vez só, mesmo quando dois caminhos chegam ao mesmo pré-requisito. Exemplo real: `BEN-01` → `DOC-01 → DOC-02 → DOC-03 → BEN-03`.
- **Ciclos:** o algoritmo guarda o caminho em andamento e os registros já concluídos. Se um registro reaparece no caminho em andamento, levanta `ValueError("ciclo de dependências: A -> B -> C -> A")`. Um registro que depende de si mesmo também é ciclo. O `respostas.py` trata esse erro e usa as dependências diretas, então um dado errado não derruba o assistente. A base atual não tem ciclos.
- `relacionados(id, base)` sugere até 3 assuntos para continuar: primeiro quem depende do registro, depois registros do **mesmo tema e fase**, sem repetir o próprio registro nem seus pré-requisitos. O contrato original previa "mesmo subtema", mas na base real esse critério não agrupava nenhum registro; usar tema e fase considera o momento em que a pessoa está. Exemplo: `DOC-03` → `BEN-01`, `BEN-02`, `BEN-04`.

#### Conselhos para quem for evoluir a busca

1. **Cuidado com palavras comuns como chave de um grupo de sinônimos.** Um grupo é ativado por qualquer um dos seus termos; "água" e "casa" puxavam registros errados e foram retirados ou trocados (`agua` virou `agua potavel`). Cada ajuste de sinônimo deve ter um teste de regressão.
2. **Perguntas longas e informais perdem nota.** O Jaccard divide pelo total de palavras; vale testar com frases como as das pessoas, e não só com palavras-chave.
3. **Sem stemming, cada forma de uma palavra é uma palavra diferente** ("perdi" ≠ "perdidos", "bombeiro" ≠ "bombeiros"). Os sinônimos cobrem parte disso; a solução geral é reduzir ao radical.
4. **A busca entende palavras, não intenção.** "Alerta de tempestade" casa com o cadastro nos alertas, e não com a preparação da casa.
5. **Registros de visão geral resolvem perguntas genéricas.** O `DOC-07` foi criado depois que "meu documento sumiu" não achava nada.
6. **Em dúvida, perguntar.** Empate vira `ambigua`; sem base, o assistente recusa e mostra os telefones de emergência (193, 199).
7. **Os limiares (0,11, 0,85 e 0,09) foram calibrados com cerca de 44 perguntas.** Qualquer mudança deve rodar `tests/avaliar_busca.py` e `tests/verificar_busca.py` antes de ser aceita.

### Regras de resposta, prompts e tratamento das limitações

O assistente não gera texto livre: toda resposta é montada a partir de um
registro verificado da base, seguindo uma de duas **instruções de resposta**
(os "modelos de prompt" do projeto), definidas em `src/respostas.py`
(`INSTRUCAO_MODELO_A` e `INSTRUCAO_MODELO_B`). As duas têm as mesmas regras e
diferem no formato:

| | Modelo A — direto | Modelo B — estruturado |
| --- | --- | --- |
| **Papel** | Assistente de orientação ao cidadão sobre enchentes; não é canal oficial | Igual |
| **Formato** | A orientação em um parágrafo, como está na base | Blocos: situação do município, pré-requisitos em ordem (grafo), passo a passo numerado (uma frase por passo) |
| **Fonte** | Obrigatória: órgão, link e data de verificação | Igual |
| **Avisos** | Confirmação quando `requer_confirmacao`; aviso do monitoramento; "não é canal oficial" | Igual |

**Comparação.** O script `tests/comparar_modelos.py` formata os 21 registros
nos dois modelos em três situações (sem município, fase "durante" e fase
"depois"), o que dá 63 respostas por modelo, e confere se cada regra foi
cumprida:

| Critério | Modelo A | Modelo B |
| --- | --- | --- |
| Cita a fonte e a data de verificação | 63/63 (100%) | 63/63 (100%) |
| Aviso de confirmação quando o registro exige | 39/39 (100%) | 39/39 (100%) |
| Aviso do monitoramento quando há município | 42/42 (100%) | 42/42 (100%) |
| Situação do município quando há município | 0/42 (0%) | 42/42 (100%) |
| Pré-requisitos quando o registro tem dependências | 0/33 (0%) | 33/33 (100%) |
| Aviso de que não é canal oficial | 63/63 (100%) | 63/63 (100%) |
| Linhas por resposta (média) | 19,8 | 27,1 |
| Caracteres por resposta (média) | 1.215 | 1.448 |
| Tempo de formatação (média) | 0,11 ms | 0,19 ms |

**Escolha: Modelo B como padrão.** Os dois cumprem igualmente as regras de
confiabilidade (fonte e avisos em 100% das respostas), mas só o Modelo B
entrega os dois diferenciais do projeto: a ordem dos pré-requisitos (33
respostas em que o cidadão precisaria descobrir sozinho que deve tirar outro
documento antes) e a situação do município. O custo é uma resposta com
cerca de 37% mais linhas e 19% mais caracteres, compensado pela divisão em
passos numerados, que são mais fáceis de seguir do que um parágrafo corrido.
A diferença de tempo (0,08 ms) é imperceptível. O Modelo A continua disponível
na opção 5 do menu para quem prefere a resposta curta.

**Confirmação com os testes (17/11).** A escolha foi mantida:

- A bateria de perguntas mede a busca, que é a mesma para os dois modelos:
  os dois formatam o mesmo registro encontrado. Por isso ela não favorece
  nenhum dos dois, e a decisão se apoia na tabela acima.
- No teste de usabilidade, todas as respostas que a participante leu
  estavam no Modelo B (o padrão). Ela as achou claras e disse que dava para
  agir com elas, e concluiu sem ajuda a tarefa que dependia de seguir uma
  resposta até o fim (o kit de emergência).
- Limite da confirmação: a participante não viu respostas no Modelo A; ela
  opinou pelas descrições do menu. Não houve um teste A×B com respostas
  reais, o que fica como melhoria (seção de conclusões).

**Tratamento das limitações:**

- **Sem orientação confiável** (pontuação abaixo do limiar ou pergunta fora
  do tema): o assistente diz que não encontrou base, **não inventa
  instruções**, sugere palavras que existem na base e o menu de temas, e
  repete os contatos de emergência.
- **Pergunta ambígua:** mostra os candidatos e pergunta qual o usuário quer.
- **Entrada vazia ou opção inexistente:** mensagem explicando o que digitar,
  sem sair do menu.
- **Fase "durante":** o bloco "segurança em primeiro lugar" (199/193) aparece
  antes de qualquer resposta, inclusive quando não há resposta.
- **Monitoramento indisponível ou município sem leituras:** o assistente
  avisa uma vez e continua respondendo sem a situação do município.
- **Nunca se apresenta como canal oficial:** o aviso aparece na abertura, em
  cada resposta e na saída.

### Monitoramento do nível dos rios

#### Introdução geral

Os dados de monitoramento são provenientes de cheias reais das cidades escolhidas (Estrela e Uruguaiana). Portanto, eles não são dados em tempo real. 
Essa escolha foi feita para que fosse possível trabalhar com dados reais, mesmo que não em tempo real. Dessa maneira, as cotas de alerta e inundação 
também seriam reais e fariam maior sentido físico, já que foram definidas por órgãos competentes especializados no assunto.

No entanto, como só foi possível encontrar dados oficiais para as cotas de alerta e de inundação, foi usado como base um cálculo para estimar a cota de atenção:

`cota de atenção = cota de alerta × 0,9`

Assim, o valor não é baixo demais para gerar alertas excessivos e ainda é menor que a cota de alerta. Além disso, também foi decidido que, para estimar a 
tendência, são usados os dados das últimas três horas do nível do rio:

`tendência (cm/h) = (nível atual - nível 3h antes) / 3`

#### Fontes

Foi feita a escolha de usar dados de enchentes reais para as simulações. Inicialmente, foi usado o portal HidroWeb, uma ferramenta do Sistema Nacional de 
Informações sobre Recursos Hídricos (SNIRH) que contém os dados da Rede Hidrometeorológica Nacional (RHN), coordenada pela Agência Nacional de Águas e 
Saneamento Básico (ANA). Como as séries históricas do HidroWeb só tinham dados até 2008, os dados das cheias foram obtidos pela telemetria da ANA, em formato XML. 
Dessa maneira, foi possível escolher duas cidades para popular um único CSV com todos os dados de monitoramento, além de uma terceira (Itaqui), deixada como XML extra para teste.

Além disso, os boletins do Serviço Geológico do Brasil (SGB), da Superintendência Regional de Porto Alegre, registram as cotas oficiais de cidades do Rio Grande 
do Sul. Então, foram escolhidas cidades dessa região, de modo que tanto os dados da simulação quanto as cotas são dados oficiais e concretos, definidos por órgãos competentes.


| Cidade | Estação (ANA) | Rio | Cota de alerta | Cota de inundação | Período |
| --- | --- | --- | --- | --- | --- |
| Estrela | 86879300 | Rio Taquari | 1700 cm | 1900 cm | 29/04 a 10/05/2024 |
| Uruguaiana | 77150000 | Rio Uruguai | 750 cm | 850 cm | 15/06 a 15/07/2025 |
| Itaqui (extra) | 75900000 | Rio Uruguai | 730 cm | 830 cm | 15/06 a 30/06/2025 |


- HidroWeb: https://www.snirh.gov.br/hidroweb
- Telemetria da ANA: https://telemetriaws1.ana.gov.br/ServiceANA.asmx
- Boletins do SGB (SACE): https://www.sgb.gov.br/sace/


#### O que cada script faz

**preparar_dados.py** -> processa os dados da ANA no formato XML. Durante esse processo, pede algumas informações sobre a cidade (nome da estação de monitoramento, nome do rio, 
município, cota de alerta e cota de inundação) e gera um CSV que segue o padrão de colunas definido no contrato e de nome (Nome da cidade - ano.csv) no diretório ana. Depois, 
move os XMLs processados para a subpasta processados, dentro de ana. Além disso, junta os dados dos CSVs de diferentes cidades no CSV principal, chamado monitoramento.csv.
Essa junção faz uma verificação que se baseia no nome da cidade e no horário dos dados, para impedir que uma mesma leitura seja inserida duas vezes.

**monitor.py** -> permite avançar ou zerar o horário da simulação. A partir dos dados do monitoramento.csv e do momento da simulação, devolve a situação do rio no horário simulado, 
indicando se está normal ou se atingiu a cota de atenção, alerta ou inundação. Além disso, devolve a fase (antes, durante ou depois), a tendência em cm/h (positiva quando o rio 
está subindo e negativa quando está baixando) e quantas horas faltam até a inundação.

**verificar_monitor.py** -> contém os testes do monitor.py. Faz sete verificações: simulação em nível normal, de atenção, alerta e inundação; baixa do rio, também chamada de 
"fase depois"; fim dos dados, caso a pessoa avance a simulação para um número de horas maior que o total de horas armazenadas; e cidade sem dados, situação que deve retornar KeyError.

#### Limitações

- O preparar_dados.py só consegue trabalhar com XMLs que venham da ANA, ou seja, se um XML com padrão diferente for adicionado, o script não vai conseguir tratar os dados.
- Os dados não são de fato em tempo real. Eles são dados reais de cheias passadas.
- Os XMLs da ANA usados no trabalho vieram com algumas horas faltando. Então, foi feita uma estimativa ligando a leitura anterior à próxima para preencher os períodos vazios.
  Portanto, algumas partes dos dados não são leituras reais.
- Caso o rio fique quase parado depois de passar da cota de alerta (como perto do pico de Uruguaiana), a tendência oscila entre subir e baixar um pouco, e a fase pode alternar com
  frequência entre "durante" e "depois". O nível (alerta ou inundação) continua certo, mas a troca de fase pode acabar causando confusão nos alertas.

### Plano de testes, indicadores e resultados

**O que foi medido.** Três frentes: a **busca** (20 perguntas, `tests/perguntas_teste.json`), a **classificação de risco do monitoramento** (`tests/verificar_monitor.py`) e a **facilidade de uso** (teste de usabilidade, [`docs/teste_usabilidade.md`](docs/teste_usabilidade.md)).

**Bateria de perguntas.** São 20 perguntas em seis categorias. Cada uma traz o status esperado (`ok`, `sem_base` ou `ambigua`) e, quando há resposta certa, o `id` esperado. O esperado foi definido a partir da base, antes de rodar o sistema, e não a partir da saída dele. Uma pergunta **acerta** quando o status obtido é o esperado e, nos casos `ok`, o primeiro resultado é o registro esperado. O tempo é a média de 200 repetições por pergunta, medida com `time.perf_counter()`. Para rodar: `python tests/avaliar_busca.py`. A saída completa, pergunta por pergunta (esperado, obtido, acerto e tempo), está em [`docs/resultados_busca.txt`](docs/resultados_busca.txt).

| Categoria | Perguntas | Acertos | Taxa |
| --- | --- | --- | --- |
| Direta | 4 | 4 | 100% |
| Reformulação | 9 | 7 | 78% |
| Fora do tema | 2 | 2 | 100% |
| Vazia | 1 | 1 | 100% |
| Ambígua | 2 | 2 | 100% |
| Sem resposta confiável | 2 | 1 | 50% |
| **Total** | **20** | **17** | **85%** |

| Indicador | Resultado |
| --- | --- |
| Acerto da busca | 17 de 20 (85%) |
| Tempo médio por busca | cerca de 1 a 2 ms (2,0 ms na execução registrada em `docs/resultados_busca.txt`; varia conforme o computador) |
| Classificação de risco (`tests/verificar_monitor.py`) | 7 de 7 verificações (100%); os 4 níveis (normal, atenção, alerta e inundação) classificados corretamente |
| Tarefas do teste de usabilidade concluídas sem ajuda | 4 de 5 |
| Facilidade de uso (1 a 5) | 4 |

**Evolução.** A primeira rodada deu 16 de 20 (80%). A pergunta "carteira" respondia `sem_base` e, com a zona cinza, passou a `ambigua`, chegando a 17 de 20. Antes disso, a bateria já tinha apontado o `DOC-07` (visão geral de documentos) e os sinônimos que puxavam o registro errado, corrigidos junto com o Bruno.

**O que ainda falha:**

| Pergunta | Esperado → obtido | Causa |
| --- | --- | --- |
| T15: "como pedir indenização da prefeitura pelos móveis que perdi" | `sem_base` → `ok` (MOR-04, seguro) | A pergunta tem palavras em comum com o registro de seguro, mas indenização da prefeitura não está na base. É o erro mais sério: responder com confiança algo parecido é pior do que recusar. |
| T17: "Minha cidade está com alerta de tempestade, e eu estou em choque, como posso prosseguir?" | SEG-06 → SEG-01 | A busca compara palavras, não intenção: "alerta" leva ao cadastro nos alertas. |
| T20: "Meus documentos foram perdidos na tempestade e não faço a minima ideia de onde tirar" | DOC-07 → `sem_base` | Só "documentos" é comum ao DOC-07 (nota 1/22 = 0,045), porque "perdidos" não é reconhecido como "perdi" (sem stemming) e a pergunta longa dilui o Jaccard. |

**Interpretação.** O tempo não é um problema: poucos milissegundos por busca. A precisão é boa nas perguntas diretas, vazias, fora do tema e ambíguas, e cai nas reformulações longas e informais, que é como as pessoas escrevem de verdade. Das três falhas, a T15 é a que mais importa para um assistente que não pode induzir ao erro. Um teste com uma pessoa de fora ainda achou uma falha que a bateria não tinha: "qual o número do bombeiro" não encontra o registro de telefones de emergência (a bateria só tinha "telefone dos bombeiros").

**Teste de usabilidade** (uma participante de 20 anos, 13 minutos, 5 tarefas; detalhes em [`docs/teste_usabilidade.md`](docs/teste_usabilidade.md)):

| Resultado | Valor |
| --- | --- |
| Tarefas concluídas sem ajuda | 4 de 5 |
| Facilidade geral | 4 de 5 |
| Confiaria na orientação numa emergência? | Sim ("porque é prático") |
| Maior dificuldade | O menu |

Achados e o que foi feito:

| Achado | Situação |
| --- | --- |
| O telefone de emergência só aparecia no fim da mensagem "não encontrei" | Corrigido (PR #17): os telefones passaram para o topo |
| O menu confundiu (tentou a opção 4 antes de informar o município) | Menu reformulado na PR #17 |
| "Qual o número do bombeiro" não encontra o SEG-02 | Pendente: depende de sinônimos e palavras-chave na base (Bruno) |
| O município digitado com erro é aceito sem aviso | Pendente (melhoria 3 da seção de conclusões) |

**Limitações da avaliação.**

- As 20 perguntas foram escritas pela equipe, e os limiares (0,11, 0,85 e 0,09) foram ajustados com perguntas do mesmo tipo. Por isso, os 85% provavelmente são **otimistas**; perguntas de pessoas de fora tendem a render menos.
- As 7 verificações do monitoramento são casos escritos pela autora do módulo (os quatro níveis, a fase "depois", o fim dos dados e uma cidade sem leituras): a taxa de 100% mostra que as regras funcionam nesses casos, mas a amostra é pequena e não cobre a oscilação de fase perto do pico, já registrada como limitação.
- O teste de usabilidade teve **uma participante**, de 20 anos, que já usa assistentes de chat e é próxima do desenvolvedor da busca. Tempos por tarefa e número de erros não foram coletados.
- A preferência entre os modelos A e B não foi medida com respostas reais (ver a seção de regras de resposta).

**Melhorias.**

1. **Reduzir palavras ao radical (stemming) e ponderar termos raros (TF-IDF)**, para acertar plurais e flexões ("perdidos", "bombeiro") e reduzir o peso de palavras comuns.
2. **Medir a cobertura da pergunta**, e não só o Jaccard, para não punir frases longas; qualquer mudança de limiar só deve valer depois de testar com mais perguntas, porque subir o limiar pode piorar outras categorias.
3. **Alimentar os sinônimos com perguntas reais** de usuários (como "número do bombeiro") e manter um teste de regressão para cada correção.
4. **Avaliar com uma amostra maior**: mais perguntas escritas por pessoas de fora da equipe e mais participantes no teste de usabilidade, com tempo por tarefa cronometrado.


### Exemplos de perguntas, respostas com fontes e entradas inválidas

Saídas reais do `python src/sistema.py` com a base atual.

**Pergunta direta** — "cpf", no Modelo A:

```text
[DOC-02] CPF (comprovante e regularização)
O CPF não tem mais cartão físico: a chamada segunda via é o comprovante de
inscrição, que é gratuito. Consulte e emita o comprovante no site da Receita
Federal (informando CPF e data de nascimento), no aplicativo da Receita
Federal ou pelo gov.br. [...] Qualquer site que cobre para emitir o CPF não
é oficial.

Fonte: Receita Federal — Consultar Cadastro de Pessoa Física (CPF) —
https://www.gov.br/pt-br/servicos/consultar-cadastro-de-pessoas-fisicas
(verificado em 2026-11-11)
Orientação de um protótipo educacional, não de um canal oficial.
```

**Pergunta ambígua** — "segunda via":

```text
Sua pergunta combina com mais de um assunto. Qual deles você quer?
  1. DOC-01 - Certidões de nascimento, casamento e óbito (segunda via)
  2. DOC-02 - CPF (comprovante e regularização)
  3. DOC-03 - Identidade (RG/CIN): segunda via
  0. Voltar
```

**Pré-requisitos (grafo)** — escolhendo a identidade (DOC-03), no Modelo B:

```text
=== [DOC-03] Identidade (RG/CIN): segunda via ===
Antes, você precisa ter feito (nesta ordem):
  1. DOC-01 - Certidões de nascimento, casamento e óbito (segunda via)
  2. DOC-02 - CPF (comprovante e regularização)

Passo a passo:
  1. Para refazer a identidade, solicite a segunda via da Carteira de
     Identidade Nacional (CIN) no órgão de identificação do seu estado; [...]
  2. Leve a certidão de nascimento (solteiros) ou de casamento (casados) e o
     CPF.
  3. Em caso de perda ou roubo, registre antes um boletim de ocorrência.
  [...]
Fonte: Governo Federal — Carteira de Identidade Nacional —
https://www.gov.br/governodigital/pt-br/identidade (...) (verificado em
2026-11-11)
Atenção: requisitos e prazos podem mudar; confirme no órgão responsável antes
de ir.
Orientação de um protótipo educacional, não de um canal oficial.

Assuntos relacionados:
  1. BEN-01 - Saque-calamidade do FGTS
  2. BEN-02 - Auxílios federais (Auxílio Reconstrução)
  3. BEN-04 - Cadastro Único e assistência social
  0. Voltar ao menu
```

**Pergunta fora do tema** — "receita de bolo":

```text
Em risco imediato: Bombeiros 193 | Defesa Civil 199.
Não encontrei na base uma orientação confiável para essa pergunta.
Não vou inventar instruções.
Tente outras palavras, como "fgts", "certidão", "vistoria", "alerta".
Ou use a opção 1 do menu para navegar pelos temas.
```

**Entradas inválidas:**

```text
Digite sua pergunta: (Enter)
Pergunta vazia. Escreva sua dúvida ou use o menu de temas.
Opção: 9
Opção inexistente: '9'. Escolha entre 0 e 6.
```

### Cuidados: clareza, acessibilidade, privacidade e informação não oficial

- O assistente **não é um canal oficial** e não se integra a órgãos públicos.
- O único dado solicitado é o município; nenhum dado pessoal é coletado.
- Em risco imediato: Bombeiros **193**; alertas e orientações: Defesa Civil
  **199**.
- Os dados de monitoramento são de referência para demonstração.

### ODS relacionados

- **ODS 11 — Cidades e comunidades sustentáveis.** Meta 11.5: "Até 2030,
  reduzir significativamente o número de mortes e o número de pessoas
  afetadas por catástrofes [...], incluindo os desastres relacionados à
  água, com o foco em proteger os pobres e as pessoas em situação de
  vulnerabilidade." O assistente atua nas três fases da enchente: prepara
  antes, coloca a segurança em primeiro lugar durante e orienta a
  recuperação depois.
- **ODS 13 — Ação contra a mudança global do clima.** Meta 13.1: "Reforçar a
  resiliência e a capacidade de adaptação a riscos relacionados ao clima e
  às catástrofes naturais em todos os países." O monitoramento do nível dos
  rios avisa a mudança de fase e indica o que fazer em cada uma, o que
  ajuda a população a se adaptar a um risco que tende a ser mais frequente.
- **ODS 10 — Redução das desigualdades.** Meta 10.2: "Até 2030, empoderar e
  promover a inclusão social, econômica e política de todos [...]." Quem
  mais sofre com enchentes costuma ter menos acesso a informação e à
  burocracia. O assistente explica, em linguagem simples e sem custo, como
  recuperar documentos e acessar benefícios como o saque-calamidade do FGTS
  e o Cadastro Único.

Texto das metas: versão das Nações Unidas, conforme as páginas do Ipea sobre
os ODS ([11](https://www.ipea.gov.br/ods/ods11.html),
[13](https://www.ipea.gov.br/ods/ods13.html) e
[10](https://www.ipea.gov.br/ods/ods10.html)).

## 📁 Estrutura de pastas

- **`data/`** Base de conhecimento (`base_conhecimento.json`), dicionário de
  sinônimos (`sinonimos.json`) e leituras do monitoramento
  (`monitoramento.csv`). Em `data/ana/`, os dados originais da ANA usados
  para gerar o CSV.
- **`docs/`** Documentação: contratos entre módulos (`contratos.md`), uso de
  IA (`uso_ia.md`), teste de usabilidade (`teste_usabilidade.md`), saída da
  bateria de perguntas (`resultados_busca.txt`), plano do projeto e
  requisitos.
- **`src/`** Código-fonte Python: `sistema.py` (menu e fluxo), `base.py`,
  `busca.py`, `grafo.py`, `monitor.py`, `respostas.py` e `preparar_dados.py`
  (converte os XMLs da ANA no CSV do monitoramento).
- **`tests/`** Perguntas de teste (`perguntas_teste.json`) e scripts:
  verificação da busca, do grafo, do monitor e do fluxo do menu
  (`verificar_*.py`), avaliação da busca com taxa de acerto e tempo
  (`avaliar_busca.py`) e comparação dos modelos de resposta
  (`comparar_modelos.py`).
- **`assets/`** Logo da FIAP.
- **`README.md`** Este arquivo.

## 📎 Links e Observações

### 🔗 Links do Projeto

- **Vídeo de apresentação no YouTube (Não Listado):** _(link a preencher)_ - _(preencher quando
  publicado)_.

### 🧠 Decisões Técnicas

- **Sem APIs nem modelos externos.** Só a biblioteca padrão do Python. As
  respostas vêm sempre da base verificada, o que impede o assistente de
  inventar orientação e torna os testes reproduzíveis.
- **Base em JSON.** Legível e editável por quem cuida do conteúdo, sem banco
  de dados. `src/base.py` valida os campos obrigatórios e descarta registros
  problemáticos com aviso, em vez de parar o programa.
- **Grafo de pré-requisitos.** O campo `depende_de` liga as orientações; a
  ordenação topológica (`src/grafo.py`) diz o que fazer primeiro, e a
  detecção de ciclos evita laço infinito com dado errado.
- **Busca por sobreposição de termos** (Jaccard com sinônimos, em
  `src/busca.py`), com limiar mínimo e detecção de empate.
- **Contratos fixos entre módulos** ([`docs/contratos.md`](docs/contratos.md)),
  para que cada integrante trabalhasse em paralelo e a integração não
  exigisse retrabalho.
- **Módulos opcionais no fluxo.** `src/sistema.py` segue funcionando se a
  busca, o grafo ou o monitoramento faltarem ou falharem: o recurso afetado
  avisa e o restante continua.

### 📢 Observações Gerais

- **Participação na Competição:** [x] Sim, aceitamos participar / [ ] Não
  vamos participar.
- Uso de IA documentado em [`docs/uso_ia.md`](docs/uso_ia.md).

## 🔧 Como executar o código

Pré-requisito: Python 3.10 ou superior. Não há dependências externas.

```bash
git clone https://github.com/DevLounge-FIAP/citizen-assist-enchentes.git
cd citizen-assist-enchentes
python src/sistema.py
```

Menu principal:

| Opção | O que faz |
| --- | --- |
| 1 | Navegar pelos temas e escolher uma orientação |
| 2 | Fazer uma pergunta em texto livre |
| 3 | Informar o município (único dado pedido) para ativar o monitoramento |
| 4 | Ver as orientações prioritárias da fase atual do município |
| 5 | Trocar o modelo de resposta (A direto ou B estruturado) |
| 6 | Simular a passagem do tempo no monitoramento (demonstração) |
| 0 | Sair |

A série de `data/monitoramento.csv` é real (ANA), mas é reproduzida em horas
simuladas, a partir da primeira leitura. A opção 6 avança esse relógio para
mostrar o rio subindo e baixando. Roteiro usado na demonstração, com o
município **Estrela**:

| Passo | Entrada | O que aparece |
| --- | --- | --- |
| 1 | Opção 3, `Estrela` | Fase ANTES, nível normal (1303 cm) |
| 2 | Opção 6, avançar 30 horas; depois opção 4 | Fase DURANTE, nível alerta, bloco de segurança e cerca de 3 h até a cota de inundação |
| 3 | Opção 6, avançar mais 170 horas; depois opção 4 | Fase DEPOIS, nível atenção, orientações de documentos e benefícios |
| 4 | Opção 2, pergunta fora do tema | Telefones de emergência e recusa sem inventar resposta |

Verificações (na raiz do repositório):

```bash
python tests/verificar_sistema.py   # fluxo do menu, entradas inválidas e fases
python tests/verificar_busca.py
python tests/verificar_grafo.py
python tests/verificar_monitor.py
python tests/comparar_modelos.py    # tabela de comparação dos modelos A e B
python tests/avaliar_busca.py       # taxa de acerto e tempo da busca (20 perguntas)
```

---

## 🏁 Conclusões, limitações e melhorias

### Conclusões

O protótipo cumpre o fluxo completo pedido pelo desafio: recebe a pergunta
(texto livre ou menu), localiza a orientação na base, responde com a fonte e
a data de verificação, avisa quando o usuário deve confirmar no órgão e
recusa o que não sabe, sem inventar resposta.

- **Base verificada:** 21 orientações em 4 temas, todas com órgão, link e
  data de verificação, ligadas por pré-requisitos (`depende_de`).
- **Busca:** 17 de 20 perguntas de teste corretas (85%), com 100% nas
  perguntas diretas, fora do tema, vazias e ambíguas, e cerca de 1 a 2 ms
  por busca.
  O tempo não é um problema; a precisão nas reformulações é.
- **Respostas:** fonte, aviso de confirmação e aviso de "não é canal
  oficial" em 100% das respostas dos dois modelos. O Modelo B, padrão,
  acrescenta a ordem dos pré-requisitos e a situação do município.
- **Monitoramento:** com dados reais de cheias (ANA), o assistente muda o
  que mostra conforme a fase do rio (antes, durante e depois) e coloca o
  bloco de segurança na frente de qualquer resposta na fase "durante".
- **Uso:** no teste de usabilidade, a participante concluiu 4 de 5 tarefas
  sem ajuda, deu nota 4 de 5 à facilidade e disse que confiaria na
  orientação numa emergência.

O diferencial que mais pesou foi tratar a enchente como um ciclo: o mesmo
assistente prepara o cidadão antes, protege durante e o guia na papelada
depois, na ordem certa.

### Limitações

- **A busca compara palavras, não sentido.** Sem stemming, "número do
  bombeiro" não encontra o registro de "telefone dos bombeiros", e reformulações longas
  falharam (T17 e T20).
- **Um erro é do tipo mais sério:** em T15 (indenização da prefeitura), a
  busca respondeu com o MOR-04 (seguro), quando o certo era dizer que não há
  orientação confiável. Responder com confiança uma pergunta parecida é pior
  do que recusar.
- **Avaliação pequena:** 20 perguntas escritas pela própria equipe e um
  teste de usabilidade com uma participante, conduzido pelo desenvolvedor
  da busca. Os números indicam tendência, não são estatisticamente
  representativos.
- **Monitoramento de demonstração:** os dados são de cheias passadas,
  reproduzidos em horas simuladas, com algumas horas estimadas. Perto do
  pico, a fase pode alternar entre "durante" e "depois" (ver a seção do
  monitoramento).
- **Base estática:** as orientações foram verificadas em novembro de 2026;
  prazos e valores mudam, e não há rotina de atualização. Por isso 13 dos 21
  registros pedem confirmação no órgão.
- **Modelos A e B** não foram comparados por usuários com respostas reais.

### Melhorias

1. **Busca mais robusta:** reduzir as palavras ao radical (stemming) e
   pesar os termos raros (TF-IDF), para acertar reformulações e plurais.
   Subir o limiar de confiança também diminuiria casos como o T15.
2. **Fase do rio mais estável:** calcular a tendência com média móvel e só
   trocar de fase depois de algumas horas seguidas na mesma direção.
3. **Validar o município** contra uma lista oficial e perguntar "Você quis
   dizer...?" quando o nome vier com erro de digitação.
4. **Priorizar a fase "depois":** hoje a opção 4 lista 15 orientações;
   mostrar primeiro as 3 ou 4 mais urgentes (documentos de identidade,
   vistoria e saque do FGTS).
5. **Avaliação maior:** mais perguntas escritas por pessoas de fora da
   equipe, mais participantes e um teste A×B com respostas reais nos dois
   modelos.
6. **Atualização da base:** revisar as datas de verificação periodicamente
   e, numa versão futura, ler os níveis dos rios direto da ANA.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
