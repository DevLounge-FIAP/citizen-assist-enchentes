# Citizen Assist AI — Assistente para o ciclo de enchentes

## Global Solution 2026.2 — CitizenTech (FIAP)

| Integrante | RM | Frente |
| --- | --- | --- |
| Aelton Soares de Menezes | 573694 | Pessoa 1 — Arquitetura, integração, fluxo principal, respostas e prompts |
| Bruno Santos Martins | 572073 | Pessoa 2 — Base de conhecimento e curadoria das fontes |
| Victor Gonçalves Mantovani | 570608 | Pessoa 3 — Busca, grafo e avaliação |
| Michelly Nunes dos Santos | 573625 | Pessoa 4 — Monitoramento e cenário de cheia |

## Prazo final de entrega

Data: 19/11/2026 (data oficial FIAP ON)

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
busca.buscar(pergunta, base, sinonimos) -> dict            # {"status": "ok" | "sem_base" | "ambigua", "resultados": [(registro, pontuação), ...]}
grafo.pre_requisitos(id_registro, base) -> list[str]       # ids na ordem em que devem ser feitos; erro claro se houver ciclo
grafo.relacionados(id_registro, base) -> list[str]         # ids sugeridos para continuar a navegação
monitor.estado(municipio) -> dict                          # {"fase", "nivel", "nivel_cm", "tendencia_cm_h", "horas_ate_inundacao", "aviso"}
respostas.formatar(registro, modelo, contexto) -> str      # modelo "A" ou "B"; contexto = dict devolvido por monitor.estado
```

Regras do contrato:

- `status` = `sem_base` quando a melhor pontuação fica abaixo do limiar
  (`resultados` vazio); `ambigua` quando os dois melhores ficam muito próximos
  (`resultados` traz os candidatos para o sistema perguntar ao usuário).
- `monitor.estado` já devolve a fase calculada: `nivel` é normal, atenção,
  alerta ou inundação; `fase` é antes (normal/atenção), durante
  (alerta/inundação) ou depois (nível baixando após ter atingido alerta ou
  inundação, ou seja, tendência negativa). `horas_ate_inundacao` é `None` se o
  nível não está subindo.
- Dicionário de sinônimos em `data/sinonimos.json`:
  `{"termo": ["sinônimo1", "sinônimo2"]}`, mantido pelo Bruno e lido pelo
  Victor.

<!-- markdownlint-enable MD013 -->

---

## 3. Estrutura do repositório

```text
data/base_conhecimento.json    # orientações + campo depende_de (grafo)
data/monitoramento.csv         # leituras simuladas/referenciadas
data/sinonimos.json            # dicionário de sinônimos para a busca
src/sistema.py                 # menu e fluxo principal
src/base.py                    # carregar e validar a base
src/busca.py                   # normalização, sinônimos, pontuação
src/grafo.py                   # pré-requisitos (ordenação topológica)
src/monitor.py                 # classificação de risco e tendência
src/respostas.py               # os dois modelos de resposta
tests/perguntas_teste.json     # 12+ perguntas e resultados esperados
tests/test_monitor.py          # testes de classificação do monitoramento
docs/uso_ia.md                 # uso de IA e validação crítica
README.md
```

> Ajustar para seguir o repositório modelo da coordenação:
> <https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master>

Execução: `python src/sistema.py`

---

## 4. Divisão das frentes

### Pessoa 1 — Arquitetura, integração, fluxo principal, respostas e prompts

- [x] Criar o repositório público seguindo o modelo da coordenação; definir
  regras de branch e revisão
- [x] `src/base.py`: carregar o JSON e validar os campos obrigatórios
- [x] Tratar arquivo ausente, arquivo vazio, JSON inválido e registros com
  campos faltando
- [x] `src/sistema.py`: menu de temas, pergunta livre, pedido do município
- [x] Tratar entrada vazia e opção inexistente com mensagens compreensíveis
- [ ] Integrar os módulos e conduzir as revisões
- [ ] Consolidar o README a partir das seções de cada frente
- [ ] `src/respostas.py` — Modelo A: template direto (orientação + fonte)
- [ ] `src/respostas.py` — Modelo B: estruturado (passos, pré-requisitos do
  grafo, fonte e aviso)
- [ ] Documentar os dois modelos: papel do assistente, formato e obrigação de
  citar a fonte
- [ ] Comparar os modelos A e B e justificar a escolha (com os resultados da
  bateria de testes da Pessoa 3)
- [ ] `docs/uso_ia.md`

### Pessoa 2 — Base de conhecimento e curadoria das fontes

- [ ] **Entregar 3 a 5 registros reais nos primeiros dias** (as Pessoas 1 e 3
  dependem disso) — **prazo: 12/11**
- [ ] Redigir no mínimo 15 registros (meta: 20) distribuídos nos 4 temas
- [ ] Para cada registro: fonte identificável e data de verificação
- [ ] Preencher o campo `depende_de` de forma consistente (forma o grafo)
- [ ] Montar o dicionário de sinônimos para a busca em `data/sinonimos.json`
- [ ] README: origem das informações e processo de verificação

### Pessoa 3 — Busca, grafo e avaliação

- [ ] `src/busca.py`: normalização (minúsculas, acentos, stopwords)
- [ ] Expansão por sinônimos
- [ ] Pontuação por sobreposição de termos (Jaccard; TF-IDF se der tempo)
- [ ] Limiar mínimo → `status: sem_base`
- [ ] Dois melhores resultados muito próximos → `status: ambigua` (perguntar ao
  usuário)
- [ ] `src/grafo.py`: montar o grafo a partir de `depende_de`
- [ ] Ordenação topológica dos pré-requisitos e detecção de ciclos
- [ ] `grafo.relacionados`: sugestão de assuntos para continuar a navegação
- [ ] README: estratégia de busca e comportamento com várias correspondências
- [ ] `tests/perguntas_teste.json` com no mínimo 12 perguntas (meta: 15):
  diretas, reformulações, fora do tema, entrada vazia, consulta ambígua, sem
  resposta confiável
- [ ] Rodar os testes e registrar: resposta esperada, resposta obtida,
  acerto/erro e tempo
- [ ] Calcular taxa de acerto (busca e classificação de risco, separadas) e
  tempo médio
- [ ] Teste de usabilidade com pelo menos um usuário de fora da equipe
- [ ] README: resultados, interpretação, limitações e pelo menos duas melhorias

### Pessoa 4 — Monitoramento e cenário de cheia

- [ ] Pesquisar as fontes de referência para justificar níveis e cotas
- [ ] `data/monitoramento.csv` com pelo menos 2 municípios
- [ ] Série simulando a subida de um rio (roteiro da demonstração no vídeo)
- [ ] `src/monitor.py`: classificação por cotas (normal, atenção, alerta,
  inundação)
- [ ] Cálculo de tendência (cm/h) e estimativa de horas até a cota de inundação
- [ ] Aviso de limitação em toda saída do monitoramento
- [ ] Testes de classificação com entradas e saídas esperadas
  (`tests/test_monitor.py`)
- [ ] README: monitoramento e avisos de limitação

**Aviso padrão do monitoramento:**
> Dado de referência para demonstração. Siga sempre os alertas oficiais da
> Defesa Civil (199) e, em perigo imediato, ligue 193.

---

## 5. Sequência de trabalho

<!-- markdownlint-disable MD013 -->

| Etapa | Datas | O que acontece |
| --- | --- | --- |
| Alinhamento | 11/11 (qua) | Contratos de interface fechados, primeiros registros da base iniciados |
| Construção paralela | 12/11 a 14/11 (qui–sáb) | Cada um no seu módulo, testando com dados de exemplo |
| Fechamento dos módulos | 15/11 (dom) | Bruno fecha a base completa; demais ajustam contra a base real |
| Integração | 16/11 (seg) | Aelton junta os módulos; correção dos problemas de encaixe |
| Testes e ajustes | 17/11 (ter) | Victor roda a bateria de testes; todos corrigem o que falhar |
| Documentação e vídeo | 18/11 (qua) | README final, roteiro e gravação do vídeo |
| Entrega | 19/11 (qui) | Revisão final pela manhã e envio (margem de segurança) |

### Escala de entregas

| Data | Aelton | Bruno | Victor | Michelly |
| --- | --- | --- | --- | --- |
| 11/11 | Contrato das funções (busca, grafo, monitor, respostas) publicado no repo | Começa os 3–5 primeiros registros reais | Lê o contrato; esqueleto de `busca.py` | Pesquisa das fontes de cotas |
| 12/11 | Modelo A de `respostas.py` (com registro de exemplo) | **Entrega 3–5 registros reais** (marco 1) | `busca.py`: normalização e Jaccard | `monitoramento.csv` com 2 municípios |
| 13/11 | Modelo B de `respostas.py` | 10 registros + `depende_de` | `busca.py` completo: limiar, ambiguidade, sinônimos básicos | `monitor.py`: classificação por cotas |
| 14/11 | `docs/uso_ia.md` (rascunho) e documentação dos modelos | **15+ registros e dicionário de sinônimos** (marco 2) | `grafo.py` (topológica e ciclos) e `perguntas_teste.json` (rascunho) | **`monitor.py` completo**: tendência, horas até inundação, aviso e testes (marco 3) |
| 15/11 (feriado) | Ajusta `sistema.py` à base real | Revisão de fontes e datas | Ajusta busca com a base real; fecha `perguntas_teste.json` (12+) | Série da subida do rio para o vídeo; README do monitor |
| 16/11 | **Integração**: junta tudo no `sistema.py` (marco 4) | README: origem e verificação das fontes | Apoia a integração; testa busca integrada | README do monitor; revisa a integração do monitor |
| 17/11 | Corrige falhas de integração e respostas | Corrige registros com problema | **Roda a bateria**, taxas de acerto e tempo; teste de usabilidade (marco 5) | Corrige falhas do monitor; roteiro do vídeo |
| 18/11 | README consolidado; comparação A×B com os números do Victor | Revisão final da base | README de busca e de resultados/avaliação (taxas, interpretação, limitações, melhorias) | Grava a demonstração do monitor |
| 19/11 | Revisão final e entrega até o meio-dia (conferir checklist da seção 6) | Revisão | Revisão | Revisão |

### Dependências críticas

- Bruno (12/11) → Victor e Aelton: sem registros reais, a busca e as respostas
  só rodam com dados de exemplo.
- Victor `busca.py` e `grafo.py` (13–14/11) → Aelton: o Modelo B usa os
  pré-requisitos do grafo e a integração depende da busca.
- Michelly `monitor.py` (14/11) → Aelton: o fluxo principal chama o monitor.
- Contrato de `buscar` e `monitor.estado` (11/11) → todos: é o que evita
  retrabalho na integração.
- Bruno base completa (14/11) → Victor: as perguntas de teste só fecham com a
  base final.
- Bateria do Victor (17/11) → comparação A×B do Aelton e README de resultados
  do Victor (18/11).
- Integração (16/11) → bateria de testes (17/11) → resultados no README (18/11):
  é a cadeia que não tem folga; qualquer atraso antes de 16/11 consome o
  buffer do dia 19.

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

- [x] Repositório GitHub público e acessível
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
- [x] ODS identificados e explicados no README
