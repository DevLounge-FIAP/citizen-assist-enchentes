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

_(a preencher: campos dos registros, origem e verificação das fontes,
normalização/sinônimos/pontuação, limiar, tratamento de ambiguidade, grafo de
pré-requisitos.)_

### Regras de resposta, prompts e tratamento das limitações

_(a preencher: Modelo A e Modelo B, comparação e justificativa, avisos de
limitação.)_

### Plano de testes, indicadores e resultados

_(a preencher: perguntas de teste, taxa de acerto, tempo médio, teste de
usabilidade, interpretação, melhorias e limitações da avaliação.)_

### Exemplos de perguntas, respostas com fontes e entradas inválidas

_(a preencher.)_

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

- **`data/`** Base de conhecimento (`base_conhecimento.json`) e leituras do
  monitoramento (`monitoramento.csv`).
- **`docs/`** Documentação: contratos entre módulos, uso de IA (`uso_ia.md`) e
  requisitos.
- **`src/`** Código-fonte Python: `sistema.py` (menu e fluxo), `base.py`,
  `busca.py`, `grafo.py`, `monitor.py` e `respostas.py`.
- **`tests/`** Perguntas de teste e arquivos de apoio.
- **`assets/`** Logo da FIAP.
- **`README.md`** Este arquivo.

## 📎 Links e Observações

### 🔗 Links do Projeto

- **Vídeo de apresentação no YouTube (Não Listado):** _(link a preencher)_ - _(preencher quando
  publicado)_.

### 🧠 Decisões Técnicas

> _(a preencher: JSON como formato da base, grafo de pré-requisitos com
> ordenação topológica, busca por sobreposição de termos, sem APIs externas.)_

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

---

## 🏁 Conclusões, limitações e melhorias

_(a preencher ao final do projeto.)_

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
