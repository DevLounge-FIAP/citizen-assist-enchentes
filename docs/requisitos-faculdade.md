# Requisitos do Projeto — Citizen Assist AI

## Introdução

A Global Solution – 2º Semestre de 2026 propõe o desafio CitizenTech: desenvolver tecnologias orientadas às necessidades reais das pessoas. O case Citizen Assist AI convida as equipes a construir um assistente digital introdutório que facilite o acesso a informações úteis sobre serviços, documentos, direitos e orientações comunitárias.

É comum que cidadãos encontrem informações dispersas, termos difíceis ou instruções incompletas ao procurar orientações sobre serviços do cotidiano. Um assistente pode organizar conteúdos verificados, sugerir caminhos de consulta e explicar os limites de suas respostas, tornando a busca mais clara e acessível.

Neste contexto, as equipes deverão desenvolver um protótipo funcional capaz de receber perguntas, consultar uma base de informações organizada, apresentar respostas acompanhadas de referências e tratar dúvidas não previstas. A solução deverá mobilizar principalmente conhecimentos das fases 4, 5 e 6, apoiando-se nos fundamentos de programação, lógica e estruturas de dados das fases anteriores.

O projeto também deverá considerar clareza de linguagem, acessibilidade, privacidade e responsabilidade no uso de inteligência artificial. A prioridade estará na qualidade das orientações, na comprovação das fontes e na avaliação objetiva do funcionamento do assistente.

---

## Período e formato de participação

- **Período de realização:** conforme as datas informadas oficialmente na plataforma FIAP ON para a Global Solution 2026.2.

- **Formato:** o projeto pode ser desenvolvido individualmente ou em grupo de até 5 pessoas, conforme as orientações oficiais da turma. Recomenda-se a organização de responsabilidades e o registro das decisões da equipe.

- **Aviso sobre as orientações de abertura:** As informações sobre abertura, esclarecimento de dúvidas e acompanhamento serão comunicadas pelos canais oficiais da FIAP.

Os prazos e links oficiais divulgados pela instituição prevalecem sobre qualquer planejamento interno da equipe.

## Contexto do desafio

Cidadãos precisam encontrar orientações confiáveis sobre documentos, serviços e situações comuns. Quando fontes e instruções não estão bem organizadas, a busca pode se tornar lenta, confusa e sujeita a interpretações incorretas.

Neste desafio, sua equipe deverá criar o Citizen Assist AI, um assistente que organiza informações verificadas e responde consultas simples do cotidiano. Ele deverá permitir escolher um tema ou inserir uma pergunta, localizar uma orientação na base de conhecimento, citar a fonte associada e avisar quando não houver resposta suficiente.

O desafio está em estruturar uma navegação fácil, tratar entradas inválidas, construir respostas consistentes e verificar seu desempenho com perguntas de teste. A aplicação não deverá solicitar dados pessoais desnecessários nem se apresentar como canal oficial de órgãos públicos.

## Objetivo geral

Desenvolver um protótipo funcional de assistente digital para orientação cidadã, aplicando principalmente conteúdos que foram passados até a fase 6, Python, manipulação de dados e arquivos, estratégias de prompts, lógica computacional, algoritmos de busca e avaliação de resultados, com atenção às fontes, aos limites das respostas e à facilidade de uso.

## Conteúdos integrados

Este projeto articula conhecimentos das fases 1 a 6, com ênfase nos conteúdos trabalhados nas fases 4, 5 e 6. Os fundamentos das fases anteriores devem apoiar o desenvolvimento, sem constituir o foco principal da atividade.

> **Tabela 1 — Fundamentos das fases anteriores**
>
> Fonte: elaborada pelo autor (2026).

---

## Missão da equipe

A equipe deverá desenvolver um assistente digital de orientação cidadã capaz de executar as seguintes tarefas:

- Organizar uma base de informações verificadas sobre serviços, documentos, direitos ou orientações comunitárias, contendo resposta e referência para cada tema.

- Receber consultas por pergunta ou menu, localizar orientações relacionadas e apresentar respostas claras com a fonte consultada.

- Aplicar estratégias introdutórias de construção de prompts ou modelos de resposta, com instruções e limites documentados.

- Tratar perguntas sem correspondência, entradas inválidas e ambiguidades, informando quando não houver base suficiente para orientar.

- Registrar testes e calcular indicadores de acerto das respostas, tempo de consulta e facilidade de utilização.

- Organizar o código e os dados para permitir consulta, revisão das informações e demonstração funcional do protótipo.

## Dados simulados obrigatórios

A equipe poderá criar perguntas e cenários fictícios, mas deverá construir a base de orientações com informações conferidas em fontes identificáveis. O conjunto mínimo deverá conter:

1. Pelo menos 15 registros de orientações, distribuídos por ao menos 3 temas de interesse cidadão, como documentação, serviços e orientações comunitárias.
2. Para cada registro: identificador, tema, pergunta ou palavras-chave, orientação resumida, referência consultada e data de verificação.
3. No mínimo 12 perguntas de teste, incluindo dúvidas diretas, reformulações e consultas fora dos temas contemplados.
4. Pelo menos 3 situações que testem limitações, como entrada vazia, consulta ambígua e ausência de resposta confiável.
5. Um registro de resultados dos testes, indicando resposta esperada, resposta obtida, acerto ou erro e tempo de consulta quando aplicável.

## Requisitos técnicos do sistema

### Base de conhecimento e leitura de arquivos

O assistente deverá carregar e consultar informações estruturadas em arquivo JSON ou TXT/CSV simples. A organização dos registros e a origem das orientações deverão ser explicadas na documentação.

#### Requisitos específicos

- Definir campos obrigatórios para cada orientação, incluindo conteúdo e referência verificável.
- Ler a base de conhecimento por meio de código Python e apresentar os temas disponíveis.
- Permitir acrescentar ou corrigir registros na base sem reescrever as regras centrais do programa.
- Validar a existência dos campos essenciais e tratar arquivo ausente, vazio ou com dados inconsistentes.

### Consulta, navegação e algoritmos

A interação deverá ser organizada com estruturas de dados e algoritmos compatíveis com os conteúdos estudados, permitindo localizar orientações e navegar entre assuntos.

#### Requisitos específicos

- Utilizar listas e dicionários para organizar os registros e recuperar informações por identificador, tema ou palavras-chave.
- Implementar uma busca de orientações que aceite uma pergunta ou a seleção de um assunto.
- Representar temas e subtemas em uma organização hierárquica ou em grafo simples, explicando as relações utilizadas.
- Criar navegação entre pelo menos três assuntos relacionados, indicando ao usuário opções de continuidade da consulta.
- Explicar a estratégia de busca ou comparação adotada e indicar como ela se comporta quando existem várias correspondências.
- Organizar funções e estruturas de forma a facilitar a manutenção da base e o acréscimo de novas orientações.

### Lógica de resposta e estratégias de prompts

O assistente deverá selecionar orientações e apresentá-las em linguagem clara, utilizando regras computacionais e estratégias introdutórias de instrução e formatação das respostas.

#### Requisitos específicos

- Utilizar condicionais e operações lógicas para tratar perguntas válidas, correspondências e ausência de orientação.
- Elaborar e documentar pelo menos dois modelos de prompt ou de instrução de resposta, por exemplo: papel do assistente, formato da resposta e obrigação de citar a fonte.
- Comparar os dois modelos em perguntas de teste, justificando qual oferece respostas mais claras e consistentes.
- Apresentar aviso de limitação quando a informação não estiver na base, sem inventar instruções ou alegar atendimento oficial.

### Interação, tratamento de erros e confiabilidade

A aplicação deverá oferecer navegação simples e um fluxo de consulta completo, do recebimento da pergunta à apresentação da orientação e de sua referência.

#### Requisitos específicos

- Permitir escolher temas em um menu ou formular perguntas em texto.
- Exibir resposta, fonte e aviso quando a orientação exigir confirmação adicional.
- Tratar entrada vazia, opção inexistente e perguntas sem correspondência com mensagens compreensíveis.
- Exibir alternativas de consulta ou assuntos relacionados quando não encontrar uma resposta adequada.

### Testes e indicadores de desempenho

A equipe deverá avaliar o comportamento do assistente a partir de um conjunto de perguntas de teste, empregando métricas e operações compatíveis com os conteúdos de análise e avaliação de modelos.

#### Requisitos específicos

- Executar ao menos 12 perguntas de teste e registrar a orientação esperada, a resposta obtida e a classificação de acerto.
- Calcular uma taxa de acerto das respostas e uma medida simples de tempo de consulta (por exemplo, média dos tempos medidos).
- Realizar um teste de facilidade de uso com pelo menos um usuário de teste ou roteiro de tarefas, registrando dificuldades e resultados.
- Interpretar os indicadores, apresentar ao menos duas melhorias possíveis e explicar as limitações da avaliação.

## Exemplo de funcionamento

O exemplo abaixo é ilustrativo. A equipe poderá definir outros assuntos e formas de interação, desde que atenda aos requisitos técnicos.

1. **Entrada simulada:** tema = documentos; pergunta = “Quais documentos consultar antes de solicitar um serviço?”
2. **Consulta:** localizar o registro correspondente na base e apresentar uma orientação resumida com a referência utilizada.
3. **Indicadores:** 12 perguntas testadas; 10 respostas classificadas como corretas; taxa de acerto = 83,3%.
4. **Ação 1:** validar a pergunta e buscar uma correspondência na base de conhecimento.
5. **Ação 2:** apresentar a orientação, a fonte consultada e um aviso para confirmar requisitos atualizados.
6. **Ação 3:** se não houver informação suficiente, informar o limite e sugerir outro tema ou consulta.

## Entregáveis obrigatórios

Envie um arquivo `.TXT` pela plataforma FIAP ON contendo apenas os dois links abaixo:

- Link direto do repositório GitHub público da equipe.
- Link do vídeo de apresentação publicado no YouTube como **“Não Listado”**.

Todos os arquivos desenvolvidos nesta etapa deverão estar organizados no repositório GitHub do grupo, seguindo o modelo oficial disponibilizado pela coordenação.

**Repositório modelo da coordenação:**
<https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master>

Seu repositório GitHub deverá conter os arquivos e pastas indicados na tabela, organizados para permitir a execução e a correção:

> **Tabela 2 — Estrutura e conteúdo dos arquivos do repositório**
>
> Fonte: elaborada pelo autor (2026).

## Estrutura do README

- Nome da equipe e RMs dos integrantes.
- Descrição do problema, público beneficiado e temas abordados.
- Organização da base de conhecimento, estruturas utilizadas e estratégia de busca.
- Regras de resposta, estratégias de prompts ou modelos de instrução e tratamento das limitações.
- Plano de testes, indicadores, resultados obtidos e interpretação.
- Como executar: `python src/sistema.py`.
- Exemplo de perguntas, respostas com fontes e comportamento para entradas inválidas.
- Cuidados com clareza, acessibilidade, privacidade e informação não oficial.
- Link do vídeo no YouTube.
- Conclusões, limitações e possibilidades de melhoria.

## Regras técnicas

- Priorize os conhecimentos das fases 4, 5 e 6, considerando os fundamentos das fases anteriores.

- Uma interface textual funcional é suficiente; interface gráfica, chatbot online ou aplicativo web são opcionais.

- Não é obrigatório utilizar APIs pagas, serviços externos, LangChain, n8n ou treinar um modelo de inteligência artificial.

- Utilize Python, leitura de arquivos, listas, dicionários, validações, algoritmos de consulta e procedimentos de teste compatíveis com os conteúdos estudados.

- Não colete dados pessoais desnecessários, não prometa integração com órgãos públicos e identifique as fontes e as limitações das orientações.

## Uso de inteligência artificial

Ferramentas de IA podem apoiar a elaboração e a comparação de prompts, a revisão de textos e o planejamento de testes. Caso um modelo externo seja utilizado no protótipo, suas respostas deverão ser confrontadas com a base de informações verificada. A equipe deve compreender, testar e justificar o funcionamento da solução e registrar no arquivo docs/uso_ia.md o uso de IA e a validação crítica realizada.

## Checklist de entrega

- [ ] Repositório GitHub público e acessível?
- [ ] Arquivo `.TXT` enviado na plataforma contém os links corretos?
- [ ] Vídeo disponível no YouTube como **“Não Listado”**?
- [ ] Código Python funciona sem erros nas operações demonstradas?
- [ ] Perguntas, respostas com fontes e tratamento de consultas não previstas documentados?
- [ ] Estratégia de busca e organização dos temas justificadas?
- [ ] Indicadores de acerto, tempo e facilidade de uso calculados e interpretados?
- [ ] Entradas inválidas e ausência de informações confiáveis tratadas corretamente?
- [ ] Fluxo de consulta e avisos de limitação apresentados com clareza?
- [ ] Uso de IA documentado, quando aplicável?

## Objetivo final

Ao final da Global Solution, espera-se que cada equipe demonstre a capacidade de organizar informações verificadas e transformá-las em orientações digitais úteis. O assistente deverá permitir consultas, recuperar conteúdos relevantes, apresentar referências e informar seus limites de maneira transparente.

Mais do que demonstrar respostas isoladas, a equipe deverá justificar a organização da base, os algoritmos de busca, as estratégias de resposta e os testes utilizados. Os resultados devem evidenciar acertos, dificuldades observadas e propostas de melhoria.

O Citizen Assist AI deverá mostrar como fundamentos de programação e conteúdos recentes de algoritmos, manipulação de dados, prompts e avaliação de desempenho podem contribuir para o acesso responsável e acessível à informação cidadã.
