# Citizen Assist AI — Assistente para o ciclo de enchentes

## Global Solution 2026.2 — CitizenTech (FIAP)

| Integrante | RM | Frente |
| --- | --- | --- |
| _Aelton_ | _(573694)_ | Pessoa 1 — Arquitetura, integração e fluxo principal |
| _Bruno_ | _(572073)_ | Pessoa 2 — Base de conhecimento e curadoria das fontes |
| _Victor_ | _(570608)_ | Pessoa 3 — Busca e grafo |
| _Michelly_ | _(573625)_ | Pessoa 4 — Monitoramento e cenário de cheia |
| _nome_ | _(RM)_ | Pessoa 5 — Respostas, prompts e avaliação |

## Prazo final de entrega

Data: _(19/11/2026)_

---

## 1. A ideia

### Problema

Antes, durante e depois de uma enchente, a pessoa precisa de informações que
estão espalhadas por vários órgãos: como se preparar, como se proteger, como
recuperar documentos perdidos, como sacar o FGTS por calamidade, como pedir
auxílios e como regularizar o imóvel. Muitas dessas etapas dependem umas das
outras, e a pessoa não sabe por onde começar.

### Solução

Um assistente em Python que orienta o cidadão ao longo das três fases do
desastre. Um módulo de monitoramento (com dados simulados e referenciados)
informa em que fase o município está, e o assistente muda suas prioridades
conforme essa fase.

<!-- markdownlint-disable MD013 -->

| Fase | Situação do rio/alerta | O que o assistente prioriza |
| --- | --- | --- |
| **Antes** | Normal ou atenção | Preparação: kit de emergência, documentos em local seguro, cadastro em alertas da Defesa Civil, rotas para abrigos |
| **Durante** | Alerta ou inundação | Segurança primeiro: qualquer pergunta recebe antes um bloco com contatos de emergência e orientação para sair de área de risco |
| **Depois** | Nível baixando | Recuperação: pré-requisitos de documentos (grafo), FGTS calamidade, auxílios, vistoria do imóvel |

<!-- markdownlint-enable MD013 -->

### Diferenciais

- **Grafo de pré-requisitos:** cada orientação indica de quais outras depende. O
  assistente responde "para fazer X, você precisa antes de A e B, nesta ordem"
  usando ordenação topológica.
- **Respostas sensíveis ao contexto:** o estado do monitoramento muda o que é
  mostrado primeiro.
- **Limites claros:** o assistente nunca se apresenta como canal oficial e
  sempre direciona para a Defesa Civil (199) e os Bombeiros (193) em situações
  de risco.
- **Privacidade:** o único dado pedido ao usuário é o município. Nenhum dado
  pessoal é coletado.

### Temas da base de conhecimento

1. Documentação (segundas vias)
2. Benefícios e financeiro (FGTS, auxílios)
3. Segurança e alertas (Defesa Civil, abrigos, contatos)
4. Moradia (vistoria, laudos)

### ODS relacionados

- **ODS 11** — Cidades e comunidades sustentáveis (meta 11.5: reduzir mortes e
  pessoas afetadas por desastres)
- **ODS 13** — Ação contra a mudança global do clima (meta 13.1: reforçar a
  resiliência a riscos climáticos)
- **ODS 10** — Redução das desigualdades (quem mais sofre com enchentes costuma
  ter menos acesso à informação)

> Conferir o texto oficial das metas antes de citar no README.

### Fontes candidatas para o monitoramento (verificar)

- SACE — Serviço Geológico do Brasil (níveis de rios e cotas)
- INMET (avisos meteorológicos)
- Cemaden (monitoramento de áreas de risco)

As leituras usadas no protótipo podem ser simuladas, desde que isso esteja
claramente informado na documentação.

---

## 2. Contratos entre módulos (fechar no dia 1)

### Formato de um registro da base

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

### Formato de uma leitura do monitoramento (`data/monitoramento.csv`)

```text
estacao,rio,municipio,data_hora,nivel_cm,cota_alerta_cm,cota_inundacao_cm
```

### Assinaturas das funções

<!-- markdownlint-disable MD013 -->

```python
base.carregar_base(caminho) -> list[dict]
busca.buscar(pergunta, base) -> list[tuple[dict, float]]   # registros + pontuação, ordenados
grafo.pre_requisitos(id_registro, base) -> list[str]       # ids na ordem em que devem ser feitos
monitor.estado(municipio) -> dict                          # fase, nível, tendência, horas até a cota
respostas.formatar(registro, modelo, contexto) -> str      # modelo "A" ou "B"
```

<!-- markdownlint-enable MD013 -->

---

## 3. Estrutura do repositório

```text
data/base_conhecimento.json    # orientações + campo depende_de (grafo)
data/monitoramento.csv         # leituras simuladas/referenciadas
src/sistema.py                 # menu e fluxo principal
src/base.py                    # carregar e validar a base
src/busca.py                   # normalização, sinônimos, pontuação
src/grafo.py                   # pré-requisitos (ordenação topológica)
src/monitor.py                 # classificação de risco e tendência
src/respostas.py               # os dois modelos de resposta
tests/perguntas_teste.json     # 12+ perguntas e resultados esperados
docs/uso_ia.md                 # uso de IA e validação crítica
README.md
```

> Ajustar para seguir o repositório modelo da coordenação:
> <https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master>

Execução: `python src/sistema.py`

---

## 4. Divisão das frentes

### Pessoa 1 — Arquitetura, integração e fluxo principal

- [ ] Criar o repositório público seguindo o modelo da coordenação; definir
  regras de branch e revisão
- [ ] `src/base.py`: carregar o JSON e validar os campos obrigatórios
- [ ] Tratar arquivo ausente, arquivo vazio, JSON inválido e registros com
  campos faltando
- [ ] `src/sistema.py`: menu de temas, pergunta livre, pedido do município
- [ ] Tratar entrada vazia e opção inexistente com mensagens compreensíveis
- [ ] Integrar os módulos e conduzir as revisões
- [ ] Consolidar o README a partir das seções de cada frente

### Pessoa 2 — Base de conhecimento e curadoria das fontes

- [ ] **Entregar 3 a 5 registros reais nos primeiros dias** (as Pessoas 3 e 5
  dependem disso)
- [ ] Redigir no mínimo 15 registros (meta: 20) distribuídos nos 4 temas
- [ ] Para cada registro: fonte identificável e data de verificação
- [ ] Preencher o campo `depende_de` de forma consistente (forma o grafo)
- [ ] Montar o dicionário de sinônimos para a busca
- [ ] README: origem das informações e processo de verificação

### Pessoa 3 — Busca e grafo

- [ ] `src/busca.py`: normalização (minúsculas, acentos, stopwords)
- [ ] Expansão por sinônimos
- [ ] Pontuação por sobreposição de termos (Jaccard; TF-IDF se der tempo)
- [ ] Limiar mínimo → "sem base suficiente"
- [ ] Dois melhores resultados muito próximos → "consulta ambígua" (perguntar ao
  usuário)
- [ ] `src/grafo.py`: montar o grafo a partir de `depende_de`
- [ ] Ordenação topológica dos pré-requisitos e detecção de ciclos
- [ ] Sugestão de assuntos relacionados para continuar a navegação
- [ ] README: estratégia de busca e comportamento com várias correspondências

### Pessoa 4 — Monitoramento e cenário de cheia

- [ ] Pesquisar as fontes de referência para justificar níveis e cotas
- [ ] `data/monitoramento.csv` com pelo menos 2 municípios
- [ ] Série simulando a subida de um rio (roteiro da demonstração no vídeo)
- [ ] `src/monitor.py`: classificação por cotas (normal, atenção, alerta,
  inundação)
- [ ] Cálculo de tendência (cm/h) e estimativa de horas até a cota de inundação
- [ ] Aviso de limitação em toda saída do monitoramento
- [ ] Testes de classificação com entradas e saídas esperadas
- [ ] README: monitoramento e avisos de limitação

**Aviso padrão do monitoramento:**
> Dado de referência para demonstração. Siga sempre os alertas oficiais da
> Defesa Civil (199) e, em perigo imediato, ligue 193.

### Pessoa 5 — Respostas, prompts e avaliação

- [ ] `src/respostas.py` — Modelo A: template direto (orientação + fonte)
- [ ] `src/respostas.py` — Modelo B: estruturado (passos, pré-requisitos do
  grafo, fonte e aviso)
- [ ] Documentar os dois modelos: papel do assistente, formato e obrigação de
  citar a fonte
- [ ] `tests/perguntas_teste.json` com no mínimo 12 perguntas (meta: 15):
  diretas, reformulações, fora do tema, entrada vazia, consulta ambígua, sem
  resposta confiável
- [ ] Rodar os testes e registrar: resposta esperada, resposta obtida,
  acerto/erro e tempo
- [ ] Calcular taxa de acerto (busca e classificação de risco, separadas) e
  tempo médio
- [ ] Comparar os modelos A e B e justificar a escolha
- [ ] Teste de usabilidade com pelo menos um usuário de fora da equipe
- [ ] `docs/uso_ia.md`
- [ ] README: resultados, interpretação, limitações e pelo menos duas melhorias

---

## 5. Sequência de trabalho

<!-- markdownlint-disable MD013 -->

| Etapa | % do prazo | Datas | O que acontece |
| --- | --- | --- | --- |
| Alinhamento | ~10% | _(preencher)_ | Reunião inicial, contratos fechados, repositório criado, primeiros registros da base |
| Construção paralela | ~40% | _(preencher)_ | Cada um no seu módulo, testando com dados de exemplo |
| Integração | ~20% | _(preencher)_ | Pessoa 1 junta os módulos; correção dos problemas de encaixe |
| Testes e ajustes | ~15% | _(preencher)_ | Pessoa 5 roda a bateria de testes; todos corrigem o que falhar |
| Documentação e vídeo | ~15% | _(preencher)_ | README final, roteiro e gravação do vídeo |

<!-- markdownlint-enable MD013 -->

### Ponto de controle

Conversa rápida duas vezes por semana. Cada um diz o que
fez, o que vai fazer e se está travado.

### Vídeo

Cada pessoa apresenta a parte que construiu. Roteiro sugerido para a
demonstração: rio em nível normal (fase Antes) → série de subida (fase Durante,
bloco de segurança) → nível baixando (fase Depois, grafo de documentos) →
pergunta fora do tema e entrada vazia (tratamento de limitações) → indicadores.

---

## 6. Checklist de entrega

- [ ] Repositório GitHub público e acessível
- [ ] Arquivo .TXT na plataforma com os dois links corretos (GitHub e YouTube)
- [ ] Vídeo no YouTube como "Não Listado"
- [ ] Código funciona sem erros nas operações demonstradas
- [ ] Perguntas, respostas com fontes e consultas não previstas documentadas
- [ ] Estratégia de busca e organização dos temas justificadas
- [ ] Indicadores de acerto, tempo e facilidade de uso calculados e
  interpretados
- [ ] Entradas inválidas e ausência de informação confiável tratadas
- [ ] Avisos de limitação claros (nunca se apresentar como canal oficial)
- [ ] Uso de IA documentado em `docs/uso_ia.md`
- [ ] ODS identificados e explicados no README
