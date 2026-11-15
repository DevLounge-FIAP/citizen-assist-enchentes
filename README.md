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
| Aelton | 573694 | Arquitetura, integração, fluxo principal, respostas e prompts |
| Bruno | 572073 | Base de conhecimento e curadoria das fontes |
| Victor | 570608 | Busca, grafo e avaliação |
| Michelly | 573625 | Monitoramento e cenário de cheia |


<!-- TODO: trocar os nomes pelos links de LinkedIn/GitHub, como no modelo:
- <a href="LINK">Nome</a> -->

## 👩‍🏫 Professores

### Tutor(a)

- _(preencher: nome e link do LinkedIn do tutor)_

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

_(a preencher — Bruno: campos dos registros, origem e verificação das fontes.
Victor: normalização, sinônimos, pontuação, limiar, ambiguidade e grafo de
pré-requisitos. O formato dos registros está em
[`docs/contratos.md`](docs/contratos.md).)_

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

**Comparação.** O script `tests/comparar_modelos.py` formata os 20 registros
nos dois modelos em três situações (sem município, fase "durante" e fase
"depois") e confere se cada regra foi cumprida:

| Critério | Modelo A | Modelo B |
| --- | --- | --- |
| Cita a fonte e a data de verificação | 60/60 (100%) | 60/60 (100%) |
| Aviso de confirmação quando o registro exige | 36/36 (100%) | 36/36 (100%) |
| Aviso do monitoramento quando há município | 40/40 (100%) | 40/40 (100%) |
| Situação do município quando há município | 0/40 (0%) | 40/40 (100%) |
| Pré-requisitos quando o registro tem dependências | 0/33 (0%) | 33/33 (100%) |
| Aviso de que não é canal oficial | 60/60 (100%) | 60/60 (100%) |
| Linhas por resposta (média) | 19,1 | 26,4 |
| Tempo de formatação (média) | 0,12 ms | 0,17 ms |

**Escolha: Modelo B como padrão.** Os dois cumprem igualmente as regras de
confiabilidade (fonte e avisos em 100% das respostas), mas só o Modelo B
entrega os dois diferenciais do projeto: a ordem dos pré-requisitos (33
respostas em que o cidadão precisaria descobrir sozinho que deve tirar outro
documento antes) e a situação do município. O custo é uma resposta cerca de
38% mais longa, compensado pela divisão em passos numerados, que são mais
fáceis de seguir do que um parágrafo corrido. O Modelo A continua disponível
na opção 5 do menu para quem prefere a resposta curta. _(A escolha será
confirmada com o teste de usabilidade e a bateria de perguntas, na seção de
resultados.)_

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

### Plano de testes, indicadores e resultados

_(a preencher — Victor, após a bateria de 17/11: perguntas de teste, taxa de
acerto, tempo médio, teste de usabilidade, interpretação, melhorias e
limitações da avaliação.)_

### Exemplos de perguntas, respostas com fontes e entradas inválidas

Saídas reais do `python src/sistema.py` com a base atual.

**Pergunta direta** — "cpf", no Modelo A:

```text
[DOC-02] Cpf
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
  1. DOC-01 - Certidao segunda via
  2. DOC-02 - Cpf
  3. DOC-03 - Identidade cin
  0. Voltar
```

**Pré-requisitos (grafo)** — escolhendo a identidade (DOC-03), no Modelo B:

```text
=== [DOC-03] Identidade cin ===
Antes, você precisa ter feito (nesta ordem):
  1. DOC-01 - Certidao segunda via
  2. DOC-02 - Cpf

Passo a passo:
  1. Para refazer a identidade, solicite a segunda via da Carteira de
     Identidade Nacional (CIN) no órgão de identificação do seu estado; [...]
  2. Leve a certidão de nascimento (solteiros) ou de casamento (casados) e o
     CPF.
  3. Em caso de perda ou roubo, registre antes um boletim de ocorrência.
  [...]
Fonte: Governo Federal — Carteira de Identidade Nacional —
https://www.gov.br/identidade (...) (verificado em 2026-11-11)
Atenção: requisitos e prazos podem mudar; confirme no órgão responsável antes
de ir.
Orientação de um protótipo educacional, não de um canal oficial.

Assuntos relacionados:
  1. BEN-01 - Fgts calamidade
  2. BEN-02 - Auxilios federais
  3. BEN-04 - Cadunico assistencia
  0. Voltar ao menu
```

**Pergunta fora do tema** — "receita de bolo":

```text
Não encontrei na base uma orientação confiável para essa pergunta.
Não vou inventar instruções. Você pode tentar outras palavras, por exemplo:
  - "fgts" (tema beneficios)
  - "certidão" (tema documentacao)
  - "vistoria" (tema moradia)
  - "alerta" (tema seguranca)
Ou use a opção 1 do menu para navegar pelos temas.
Em risco imediato: Bombeiros 193 | Defesa Civil 199.
```

**Entradas inválidas:**

```text
Digite sua pergunta: (Enter)
Pergunta vazia. Escreva sua dúvida ou use o menu de temas.
Opção: 9
Opção inexistente: '9'. Escolha entre 0 e 5.
```

### Cuidados: clareza, acessibilidade, privacidade e informação não oficial

- O assistente **não é um canal oficial** e não se integra a órgãos públicos.
- O único dado solicitado é o município; nenhum dado pessoal é coletado.
- Em risco imediato: Bombeiros **193**; alertas e orientações: Defesa Civil
  **199**.
- Os dados de monitoramento são de referência para demonstração.

### ODS relacionados

- **ODS 11** — Cidades e comunidades sustentáveis
- **ODS 13** — Ação contra a mudança global do clima
- **ODS 10** — Redução das desigualdades

<!-- TODO: conferir o texto oficial das metas antes de citar. -->

## 📁 Estrutura de pastas

- **`data/`** Base de conhecimento (`base_conhecimento.json`), dicionário de
  sinônimos (`sinonimos.json`) e leituras do monitoramento
  (`monitoramento.csv`).
- **`docs/`** Documentação: contratos entre módulos, uso de IA (`uso_ia.md`) e
  requisitos.
- **`src/`** Código-fonte Python: `sistema.py` (menu e fluxo), `base.py`,
  `busca.py`, `grafo.py`, `monitor.py` e `respostas.py`.
- **`tests/`** Perguntas de teste e scripts de verificação: busca, grafo,
  fluxo do menu (`verificar_sistema.py`) e comparação dos modelos de resposta
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

- **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos
  participar. _(decisão da equipe pendente)_
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
| 0 | Sair |

Verificações (na raiz do repositório):

```bash
python tests/verificar_sistema.py   # fluxo do menu, entradas inválidas e fases
python tests/verificar_busca.py
python tests/verificar_grafo.py
python tests/comparar_modelos.py    # tabela de comparação dos modelos A e B
```

---

## 🏁 Conclusões, limitações e melhorias

_(a preencher ao final do projeto.)_

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
