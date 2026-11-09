# Citizen Assist AI — Assistente para o ciclo de enchentes 🌊

Global Solution 2026.2 — CitizenTech (FIAP)

## 1. 👥 Equipe

**Nome da equipe:** _DevLounge_

| Nome | RM | Frente |
|---|---|---|
| _Aleton_ | _RM 573694_ | Pessoa 1 — Arquitetura, integração e fluxo principal |
| _Bruno_ | _RM 572073_ | Pessoa 2 — Base de conhecimento e curadoria das fontes |
| _Victor_ | _RM 570608_ | Pessoa 3 — Busca e grafo |
| _Michelly_ | _RM 573625_ | Pessoa 4 — Monitoramento e cenário de cheia |

## 2. 🎯 Problema, público beneficiado e temas

### O problema
Antes, durante e depois de uma enchente, a pessoa precisa de informações que estão espalhadas por vários órgãos: como se preparar, como se proteger, como recuperar documentos perdidos, como sacar o FGTS por calamidade, como pedir auxílios e como regularizar o imóvel. O que torna a situação ainda mais difícil é que muitas dessas etapas dependem umas das outras. Por exemplo, para pedir certos benefícios é preciso ter antes um documento, que por sua vez exige outro. Em um momento de estresse, a pessoa não sabe por onde começar nem em que ordem agir.

### A solução
O Citizen Assist AI é um assistente em Python, executado no terminal, que orienta o cidadão ao longo das três fases do desastre. Um módulo de monitoramento lê dados de nível de rio (simulados e referenciados) e informa em que fase o município está. A partir dessa fase, o assistente muda o que mostra primeiro:

| Fase | Situação do rio/alerta | O que o assistente prioriza |
|---|---|---|
| **Antes** | Normal ou atenção | Preparação: kit de emergência, documentos em local seguro, cadastro em alertas da Defesa Civil, rotas para abrigos |
| **Durante** | Alerta ou inundação | Segurança primeiro: toda resposta é precedida por um bloco com contatos de emergência e orientação para sair de área de risco |
| **Depois** | Nível baixando | Recuperação: pré-requisitos de documentos, FGTS calamidade, auxílios, vistoria do imóvel |

O diferencial do projeto é o **grafo de pré-requisitos**. Cada orientação da base indica de quais outras depende, e o assistente usa isso para responder perguntas como "para fazer X, você precisa antes de A e B, nesta ordem". Assim, o usuário recebe um caminho a seguir, e não apenas uma lista de informações soltas.

### Público beneficiado
Moradores de áreas sujeitas a enchentes. O projeto é especialmente útil para quem tem menos acesso a informação organizada sobre onde e como pedir ajuda, que costuma ser quem mais sofre com esses eventos.

### Temas abordados
1. **Documentação:** segundas vias de documentos pessoais e do imóvel.
2. **Benefícios e financeiro:** saque do FGTS por calamidade e auxílios.
3. **Segurança e alertas:** Defesa Civil, abrigos e contatos de emergência.
4. **Moradia:** vistoria e laudos do imóvel.

### Escopo
O projeto cobre **somente enchentes**. Ampliar para outros desastres, como deslizamentos ou secas, exigiria outra base de conhecimento, outras fontes e outras regras de monitoramento, e por isso ficou como melhoria futura.

### ODS relacionados
- **ODS 11 — Cidades e comunidades sustentáveis:** o assistente contribui para reduzir o número de pessoas afetadas por desastres, ao orientar a preparação, a proteção e a recuperação.
- **ODS 13 — Ação contra a mudança global do clima:** enchentes são um risco ligado ao clima, e o projeto reforça a capacidade da população de se adaptar e reagir a ele.
- **ODS 10 — Redução das desigualdades:** reunir as orientações em um só lugar, em linguagem simples, reduz a barreira de informação enfrentada por quem tem menos recursos.

<!-- TODO: conferir o texto oficial das metas 11.5 e 13.1 antes de citá-las e ajustar a redação acima. -->

## 3. 📚 Base de conhecimento, estruturas e estratégia de busca

### Organização da base
A base fica em `data/base_conhecimento.json` e é uma lista de registros. Cada registro representa uma orientação e tem os campos abaixo:

```json
{
  "id": "DOC-01",
  "tema": "documentacao",
  "subtema": "segunda_via",
  "fase": "depois",
  "palavras_chave": ["rg", "identidade", "perdi documento"],
  "orientacao": "...",
  "fonte": "nome do órgão + link",
  "data_verificacao": "2026-11-10",
  "requer_confirmacao": true,
  "depende_de": ["DOC-02"]
}
```

| Campo | Para que serve |
|---|---|
| `id` | Identificador único, usado pelo grafo |
| `tema` / `subtema` | Organização por assunto (documentação, benefícios, segurança, moradia) |
| `fase` | Indica em qual fase (antes, durante, depois) a orientação é mais útil |
| `palavras_chave` | Termos que ajudam a busca a encontrar o registro |
| `orientacao` | O texto que é mostrado ao usuário |
| `fonte` | Órgão responsável e link, para o usuário conferir a informação |
| `data_verificacao` | Quando a informação foi conferida pela última vez |
| `requer_confirmacao` | Marca orientações que podem mudar e que o usuário deve confirmar no órgão |
| `depende_de` | Lista de `id` de orientações que precisam ser feitas antes (forma o grafo) |

Toda orientação tem fonte identificável e data de verificação. Essa regra existe porque o assistente lida com informação que o usuário vai usar para tomar decisões reais, e a informação pode mudar.

O formato completo dos registros e das funções entre módulos está em [`docs/contratos.md`](docs/contratos.md).

### Estruturas utilizadas
- **Lista de dicionários:** guarda os registros da base em memória e é simples de percorrer na busca.
- **Grafo dirigido:** montado a partir do campo `depende_de`. Cada orientação é um vértice, e cada dependência é uma aresta apontando do pré-requisito para a orientação.
- **CSV:** guarda as leituras do monitoramento (`estacao, rio, municipio, data_hora, nivel_cm, cota_alerta_cm, cota_inundacao_cm`).

### Estratégia de busca
A busca recebe a pergunta do usuário e devolve os registros mais parecidos, com uma pontuação. Ela funciona em quatro etapas:

1. **Normalização:** a pergunta é convertida para minúsculas, os acentos são removidos e as palavras sem valor para a busca (stopwords, como "o", "de", "para") são descartadas. Assim, "Perdi minha identidade" e "perdi minha identidade" são tratadas igual.
2. **Expansão por sinônimos:** um dicionário de sinônimos aproxima as palavras do usuário das palavras da base. Por exemplo, "carteira de identidade", "RG" e "identidade" apontam para o mesmo assunto.
3. **Pontuação por sobreposição de termos:** compara-se o conjunto de termos da pergunta com o conjunto de termos de cada registro (palavras-chave, subtema e orientação) usando o índice de Jaccard, que é a quantidade de termos em comum dividida pelo total de termos distintos. Quanto maior, mais parecido.
4. **Decisão:** os registros são ordenados pela pontuação, e o resultado passa por duas verificações descritas abaixo.

### Comportamento com várias correspondências
- **Pontuação abaixo do limiar mínimo:** o assistente não inventa uma resposta. Informa que não tem base suficiente para responder e direciona o usuário à Defesa Civil.
- **Dois melhores resultados com pontuação muito próxima:** a consulta é considerada ambígua, e o assistente pergunta ao usuário qual dos assuntos ele quer, em vez de escolher um sozinho.
- **Um resultado claramente melhor:** esse registro é usado na resposta. Os demais podem ser sugeridos como assuntos relacionados.

O limiar mínimo e a margem de ambiguidade são constantes ajustáveis, definidas a partir dos testes da seção 5.

### Grafo de pré-requisitos
Quando o usuário pergunta sobre uma orientação, o assistente consulta o grafo para descobrir tudo que precisa ser feito antes. Ele percorre as dependências do registro, direta e indiretamente, e aplica **ordenação topológica**, que organiza os vértices de modo que cada pré-requisito apareça antes de quem depende dele. O resultado é uma lista de passos na ordem correta de execução.

Exemplo: se o saque do FGTS depende do documento A, e o documento A depende do documento B, o assistente responde "primeiro B, depois A, depois o saque".

O grafo também detecta **ciclos**. Se duas orientações dependerem uma da outra, não existe ordem possível, e o sistema avisa sobre a inconsistência em vez de entrar em repetição infinita. Isso ajuda a manter a base correta.

## 4. 💬 Regras de resposta, modelos de instrução e limitações

### Regras gerais de resposta
- Toda resposta cita a **fonte** e a **data de verificação** da informação.
- Orientações marcadas com `requer_confirmacao` trazem o lembrete de confirmar no órgão responsável.
- O assistente **nunca se apresenta como canal oficial**.
- Na fase **durante**, toda resposta, qualquer que seja a pergunta, começa com o bloco de segurança: contatos de emergência (Defesa Civil 199, Bombeiros 193) e orientação para sair de área de risco.
- O assistente só responde com base nos registros da base. Se não encontrar informação confiável, ele diz isso.

### Modelos de resposta
O projeto implementa dois modelos de resposta para o mesmo registro, que são comparados na avaliação:

- **Modelo A (direto):** mostra a orientação e a fonte. É curto e rápido de ler.
- **Modelo B (estruturado):** divide a resposta em passos, mostra os pré-requisitos vindos do grafo na ordem correta, a fonte e o aviso de limitação. É mais completo e indicado quando existem dependências.

Nos dois modelos, o papel do assistente é o de um guia informativo que explica o caminho, e a citação da fonte é obrigatória. A escolha entre os modelos é justificada na seção 5, com base nos resultados dos testes.

### Monitoramento e fases
O módulo de monitoramento lê as leituras de nível do rio e calcula, para o município informado:

- **Nível de risco**, comparando o nível atual com as cotas da estação:

| Condição | Nível |
|---|---|
| Abaixo da cota de atenção | normal |
| Entre a atenção e a cota de alerta | atenção |
| Entre a cota de alerta e a cota de inundação | alerta |
| Igual ou acima da cota de inundação | inundação |

- **Tendência**, em cm por hora, calculada pela diferença entre as leituras mais recentes dividida pelo tempo entre elas. Valor positivo indica rio subindo, e negativo indica rio baixando.
- **Horas até a cota de inundação**, estimadas dividindo a distância até a cota pela tendência, quando o rio está subindo.
- **Fase do assistente**, definida pela regra abaixo:

| Situação | Fase |
|---|---|
| Nível normal ou atenção | antes |
| Nível alerta ou inundação | durante |
| Abaixo do pico e caindo (tendência negativa) | depois |

As leituras usadas no protótipo são **simuladas ou de referência**, e isso é informado ao usuário. As fontes consideradas como referência para níveis e cotas são o SACE (Serviço Geológico do Brasil), o INMET e o Cemaden. Os dados incluem pelo menos dois municípios e uma série que simula a subida de um rio, usada na demonstração.

**Aviso exibido em toda saída do monitoramento:**

> Dado de referência para demonstração. Siga sempre os alertas oficiais da Defesa Civil (199) e, em perigo imediato, ligue 193.

### Tratamento das limitações
| Situação | Como o assistente reage |
|---|---|
| Pergunta sem informação confiável na base | Informa que não tem base suficiente e indica a Defesa Civil |
| Consulta ambígua | Pergunta ao usuário qual assunto ele quer |
| Pergunta fora do tema | Explica o escopo e sugere os temas disponíveis |
| Município sem dados de monitoramento | Avisa e continua só com as orientações gerais |
| Arquivo da base ausente, vazio ou inválido | Mostra mensagem de erro compreensível e não quebra o programa |
| Registro com campos obrigatórios faltando | O registro é ignorado e o problema é informado |

## 5. 📊 Plano de testes, indicadores e resultados

### Plano de testes
Os testes ficam em `tests/perguntas_teste.json`, com no mínimo 12 perguntas. Cada uma traz o resultado esperado. As perguntas cobrem seis situações:

1. **Perguntas diretas:** o texto é próximo ao da base.
2. **Reformulações:** a mesma dúvida dita de outro jeito, para testar a normalização e os sinônimos.
3. **Fora do tema:** assuntos que o assistente não cobre.
4. **Entrada vazia:** o usuário não digita nada.
5. **Consulta ambígua:** pergunta que combina com mais de um assunto.
6. **Sem resposta confiável:** pergunta dentro do tema, mas que a base não cobre.

Para o monitoramento, há testes à parte com leituras de entrada e a classificação esperada (normal, atenção, alerta, inundação), incluindo os valores exatamente sobre as cotas.

### Indicadores
Para cada pergunta são registrados: resposta esperada, resposta obtida, acerto ou erro e tempo de resposta. Com isso são calculados:

| Indicador | Como é calculado |
|---|---|
| Taxa de acerto da busca | Perguntas respondidas corretamente ÷ total de perguntas |
| Taxa de acerto da classificação de risco | Classificações corretas ÷ total de leituras testadas |
| Tempo médio de resposta | Soma dos tempos ÷ número de perguntas |
| Facilidade de uso | Teste com pelo menos uma pessoa de fora da equipe: se conseguiu completar as tarefas sem ajuda e que nota deu |

A busca e a classificação de risco têm taxas separadas, porque são partes diferentes do sistema e erram por motivos diferentes.

### Resultados

| Indicador | Resultado |
|---|---|
| Taxa de acerto da busca | _(preencher após os testes)_ |
| Taxa de acerto da classificação de risco | _(preencher após os testes)_ |
| Tempo médio de resposta | _(preencher após os testes)_ |
| Facilidade de uso | _(preencher após o teste de usabilidade)_ |

### Interpretação
_(preencher após os testes: o que os números significam, em quais perguntas o sistema errou e por quê, e qual modelo de resposta (A ou B) foi escolhido e por quê.)_

## 6. 🚀 Como executar

**Pré-requisitos:** Python 3.11+ e Git. Não há dependências externas obrigatórias. Se alguma for adicionada, estará em `requirements.txt`.

```bash
git clone https://github.com/SEU-USUARIO/citizen-assist-enchentes.git
cd citizen-assist-enchentes
python src/sistema.py
```

**Como usar:** ao iniciar, o assistente pede o município. Em seguida mostra a situação do rio e a fase atual. A partir daí, o usuário pode escolher um tema no menu ou digitar uma pergunta livre.

### Estrutura do repositório

| Arquivo | Conteúdo |
|---|---|
| `src/sistema.py` | Menu e fluxo principal |
| `src/base.py` | Carregamento e validação da base de conhecimento |
| `src/busca.py` | Normalização, sinônimos e pontuação da busca |
| `src/grafo.py` | Grafo de pré-requisitos e ordenação topológica |
| `src/monitor.py` | Classificação de risco, tendência e definição da fase |
| `src/respostas.py` | Modelos de resposta A e B |
| `data/base_conhecimento.json` | Orientações com fonte, data de verificação e dependências |
| `data/monitoramento.csv` | Leituras de rio simuladas ou de referência |
| `tests/perguntas_teste.json` | Perguntas de teste e resultados esperados |
| `docs/contratos.md` | Formatos combinados entre os módulos |
| `docs/uso_ia.md` | Uso de IA e validação crítica |

## 7. 🗣️ Exemplos de perguntas, respostas com fontes e entradas inválidas

### Exemplos de interação
Os exemplos abaixo mostram o formato esperado das respostas em cada fase. O conteúdo das orientações vem da base de conhecimento.

**Fase antes (rio em nível normal):**
```
Pergunta: como me preparar para uma enchente?
Resposta: [orientação de preparação da base]
Fonte: [órgão] — verificado em [data]
```

**Fase durante (rio em alerta ou inundação):**
```
⚠️ SEGURANÇA: se estiver em área de risco, saia imediatamente.
   Defesa Civil: 199 | Bombeiros: 193

Pergunta: onde fica o abrigo mais próximo?
Resposta: [orientação da base]
Fonte: [órgão] — verificado em [data]
```

**Fase depois (nível baixando), com grafo:**
```
Pergunta: perdi meu RG, o que faço?
Resposta: [orientação da base]
Antes de fazer isso, você precisa, nesta ordem:
  1. [pré-requisito mais básico]
  2. [pré-requisito seguinte]
Fonte: [órgão] — verificado em [data]
```

_(substituir pelos textos reais da execução do sistema.)_

### Comportamento para entradas inválidas

| Entrada | O que o assistente faz |
|---|---|
| Entrada vazia | Pede que o usuário digite uma pergunta ou escolha uma opção |
| Opção de menu inexistente | Informa as opções válidas |
| Pergunta fora do tema | Explica o escopo e sugere os temas disponíveis |
| Município digitado com acento ou maiúscula diferente | Reconhece o município normalmente |
| Município sem dados | Avisa que não há monitoramento para ele |
| Pergunta sem resposta confiável | Informa que não há base suficiente e indica a Defesa Civil (199) |

## 8. 🔒 Clareza, acessibilidade, privacidade e informação não oficial

- **Clareza:** as respostas usam linguagem simples e passos curtos. Em situação de estresse, texto direto é mais fácil de seguir. Toda resposta mostra de onde veio a informação.
- **Acessibilidade:** a interface é em texto puro, no terminal. Isso funciona com leitores de tela e não depende de cores, imagens ou mouse para transmitir informação. Os alertas de segurança são identificados por texto, não só por cor.
- **Privacidade:** o único dado pedido ao usuário é o município. Nenhum dado pessoal é coletado, armazenado ou enviado a terceiros.
- **Informação não oficial:** o assistente não é um canal oficial e não substitui a Defesa Civil (199) nem os Bombeiros (193). Os dados de monitoramento são simulados ou de referência, e isso é informado em toda saída do monitoramento. Orientações que podem mudar trazem o lembrete de confirmar no órgão responsável.

## 9. 🎬 Vídeo

- YouTube (não listado): _(preencher)_

O vídeo apresenta o funcionamento do sistema em uma sequência: rio em nível normal (fase antes), série de subida (fase durante, com o bloco de segurança), nível baixando (fase depois, com o grafo de documentos), tratamento de pergunta fora do tema e entrada vazia, e por fim os indicadores.

## 10. ✅ Conclusões, limitações e melhorias

### Conclusões
O projeto mostra que é possível reunir, em um assistente simples e sem dependências externas, informações que hoje estão espalhadas por vários órgãos. O uso do grafo de pré-requisitos transforma uma lista de informações em um caminho ordenado, e a adaptação por fase faz o assistente priorizar a segurança quando o risco é maior. _(complementar com o aprendizado do grupo após os testes.)_

### Limitações
- Os dados de monitoramento são simulados ou de referência e não substituem os alertas oficiais.
- A base de conhecimento cobre apenas os temas e órgãos listados, e as informações podem mudar com o tempo.
- A busca por sobreposição de termos não entende o sentido da frase e pode falhar com perguntas muito diferentes do vocabulário da base.
- O projeto cobre somente enchentes.

### Possibilidades de melhoria
- **Dados em tempo real:** integrar o monitoramento com fontes oficiais (SACE, INMET, Cemaden), se houver API disponível.
- **Busca mais robusta:** usar TF-IDF ou outra técnica que dê mais peso a termos raros e relevantes.
- **Outros desastres:** ampliar a base e o monitoramento para deslizamentos e outros eventos.
- **Atualização da base:** criar um processo para revisar periodicamente as fontes e as datas de verificação.

## 🤖 Uso de IA

## 🤝 Como contribuir

- A `main` é protegida: todo código entra por Pull Request com 1 aprovação.
- Cada pessoa trabalha em uma branch própria e abre Pull Request para a `main`.
- Mudanças nos contratos entre módulos devem ser avisadas ao grupo e registradas em [`docs/contratos.md`](docs/contratos.md).
