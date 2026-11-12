# Contratos entre módulos

Este documento fixa o que cada módulo recebe e devolve. Quem implementa um
módulo pode mudar o código interno à vontade, mas não pode mudar o que está
aqui sem avisar o grupo, porque a integração (16/11) depende disso.

| Módulo | Responsável | Arquivo |
| --- | --- | --- |
| Base de conhecimento | Bruno | `data/base_conhecimento.json`, `data/sinonimos.json` |
| Carregamento da base | Aelton | `src/base.py` |
| Busca | Victor | `src/busca.py` |
| Grafo de pré-requisitos | Victor | `src/grafo.py` |
| Monitoramento | Michelly | `src/monitor.py`, `data/monitoramento.csv` |
| Respostas (modelos A e B) | Aelton | `src/respostas.py` |
| Menu e fluxo principal | Aelton | `src/sistema.py` |

---

## 1. Registro da base (`data/base_conhecimento.json`)

O arquivo é uma lista de registros:

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

| Campo | Tipo | Obrigatório | Observação |
| --- | --- | --- | --- |
| `id` | texto | sim | Único. Prefixo do tema: `DOC`, `BEN`, `SEG`, `MOR` |
| `tema` | texto | sim | `documentacao`, `beneficios`, `seguranca` ou `moradia` |
| `titulo` | texto | não | Nome curto exibido nas respostas e no menu (ex.: "Segunda via do RG"). Sem ele, usa o `subtema` |
| `subtema` | texto | não | Livre |
| `fase` | texto | não | `antes`, `durante` ou `depois` |
| `palavras_chave` | lista de textos | sim | Não pode ser vazia |
| `orientacao` | texto | sim | Frases completas; cada frase vira um passo no Modelo B |
| `fonte` | texto | sim | Órgão + link |
| `data_verificacao` | texto | sim | `AAAA-MM-DD` |
| `requer_confirmacao` | booleano | não | `true` faz a resposta mostrar aviso de confirmação |
| `depende_de` | lista de ids | não | Forma o grafo. Ids inexistentes são removidos com aviso |

`base.carregar_base` descarta (com aviso) registros sem campo obrigatório,
com campo vazio ou com `id` repetido. Arquivo ausente, vazio, JSON inválido
ou base sem nenhum registro válido levantam `base.ErroBase`.

## 2. Sinônimos (`data/sinonimos.json`)

```json
{"termo": ["sinônimo1", "sinônimo2"]}
```

Mantido pelo Bruno, lido pela busca do Victor.

## 3. Leitura do monitoramento (`data/monitoramento.csv`)

```text
estacao,rio,municipio,data_hora,nivel_cm,cota_alerta_cm,cota_inundacao_cm
```

- `data_hora` no formato `AAAA-MM-DD HH:MM`.
- Níveis e cotas em centímetros, números inteiros.
- Uma linha por leitura; várias leituras do mesmo município formam a série
  usada para calcular a tendência.

---

## 4. Funções

<!-- markdownlint-disable MD013 -->

```python
base.carregar_base(caminho) -> list[dict]
busca.buscar(pergunta, base, sinonimos) -> dict
grafo.pre_requisitos(id_registro, base) -> list[str]
grafo.relacionados(id_registro, base) -> list[str]
monitor.estado(municipio) -> dict
respostas.formatar(registro, modelo, contexto, base=None) -> str
```

<!-- markdownlint-enable MD013 -->

### `busca.buscar(pergunta, base, sinonimos)`

Devolve sempre um dicionário:

```python
{"status": "ok", "resultados": [(registro, 0.62), (registro, 0.31)]}
{"status": "ambigua", "resultados": [(registro_a, 0.40), (registro_b, 0.38)]}
{"status": "sem_base", "resultados": []}
```

- `resultados` em ordem decrescente de pontuação (0 a 1).
- `sem_base`: a melhor pontuação ficou abaixo do limiar.
- `ambigua`: os dois melhores ficaram muito próximos; o sistema mostra os
  candidatos e pergunta ao usuário qual deles quer.
- Pergunta vazia não chega à busca (o `sistema.py` trata antes), mas, se
  chegar, a busca devolve `sem_base`.

### `grafo.pre_requisitos(id_registro, base)`

- Devolve os ids que precisam ser feitos **antes** de `id_registro`, em ordem
  de execução (ordenação topológica), incluindo dependências indiretas.
- Não inclui o próprio `id_registro`.
- Lista vazia quando não há pré-requisitos.
- Se houver ciclo, levanta `ValueError` com os ids envolvidos na mensagem.

Exemplo com a base atual: `pre_requisitos("BEN-01", base)` deve conter
`DOC-01`, `DOC-02`, `DOC-03` e `BEN-03`, com `DOC-01` e `DOC-02` antes de
`DOC-03`.

### `grafo.relacionados(id_registro, base)`

- Ids sugeridos para continuar a navegação (por exemplo: quem depende deste
  registro e registros do mesmo subtema).
- Não inclui o próprio `id_registro`. Lista vazia se não houver.

### `monitor.estado(municipio)`

```python
{
    "fase": "durante",            # "antes" | "durante" | "depois"
    "nivel": "alerta",            # "normal" | "atenção" | "alerta" | "inundação"
    "nivel_cm": 512,
    "tendencia_cm_h": 18.5,
    "horas_ate_inundacao": 4.9,   # None se o nível não está subindo
    "aviso": "Dado de referência para demonstração. ...",  # aviso padrão
}
```

- `fase`: `antes` para normal/atenção; `durante` para alerta/inundação;
  `depois` quando o nível está baixando depois de ter atingido alerta ou
  inundação.
- Município sem leituras: levanta `KeyError` com mensagem clara. O
  `sistema.py` captura o erro e segue sem monitoramento.

### `respostas.formatar(registro, modelo, contexto, base=None)`

- `modelo`: `"A"` (direto) ou `"B"` (estruturado). Outro valor levanta
  `ValueError`.
- `contexto`: o dicionário devolvido por `monitor.estado`, ou `None`/`{}`
  quando não há município ou monitoramento.
- `base`: opcional. O Modelo B usa para mostrar os pré-requisitos pelo nome;
  sem ela, mostra só os ids.
- Devolve o texto pronto para `print`. Sempre inclui a fonte e a data de
  verificação; inclui o aviso de confirmação quando `requer_confirmacao` é
  `true` e o aviso do monitoramento quando o contexto tiver um.
