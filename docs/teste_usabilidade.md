# Teste de usabilidade - Citizen Assist AI

**Data:** 16/11/2026 · **Observador:** Victor · **Participante:** P1, 20 anos, já usa assistentes de chat · **Duração:** 13 min

## Resumo

| Medida | Resultado |
| --- | --- |
| Tarefas concluídas sem ajuda | 4 de 5 |
| Facilidade geral (1 a 5) | 4 |
| Confiaria na orientação numa emergência? | Sim, "porque é prático" |
| Maior dificuldade | O menu |

## Como foi feito

O sistema foi executado com `python src/sistema.py`. O observador leu cada tarefa, pediu à participante que pensasse em voz alta e não deu dicas durante o uso. Nenhum dado pessoal foi registrado. Os tempos por tarefa não foram cronometrados; só a duração total.

## Resultados por tarefa

| # | Tarefa | Resultado | O que aconteceu |
| --- | --- | --- | --- |
| 1 | Descobrir como tirar outra via do RG | Sem ajuda | Perguntou "Como eu faço a segunda via do RG" e chegou ao DOC-03 na primeira tentativa. Antes, tentou a opção 4 e viu o pedido de município. |
| 2 | Descobrir o telefone dos bombeiros | Sem ajuda, pela mensagem de erro | Perguntou "Qual o número do bombeiro" e a busca respondeu "não encontrei". Ela achou o 193 na última linha da mensagem. |
| 3 | Descobrir o que levar na mochila de emergência | Sem ajuda | Usou o menu de temas até o SEG-04. Entendeu e achou fácil. |
| 4 | Perguntar algo fora do tema | Com ajuda | Perguntou "Qual minha a cor favorita ?". Entendeu por que não foi respondida e como prosseguir. |
| 5 | Comparar os modelos de resposta A e B | Sem ajuda | Leu as descrições no menu e opinou sobre qual modelo fazia mais sentido, sem ver uma resposta no modelo A. |

## O que a participante disse

- A mensagem "Monitoramento ainda não disponível nesta versão" ficou "meio sem nexo, já que não funciona".
- Na pergunta sem resposta, preferiria ver o número do bombeiro logo, e não no fim de uma mensagem longa de erro.
- O menu foi o que mais confundiu, e ela sugeriu melhorar a visualização dele.
- A resposta do sistema foi clara e dava para agir com ela.

## Melhorias identificadas

Nada foi alterado ainda. A lista abaixo está em ordem de prioridade.

| Prioridade | Problema | O que alterar | Quem |
| --- | --- | --- | --- |
| Alta | "Qual o número do bombeiro" não encontra o SEG-02, mas "qual o telefone dos bombeiros" encontra. | Acrescentar "número" e o singular "bombeiro" aos sinônimos e às palavras-chave do SEG-02. A causa geral é a falta de stemming. | Bruno |
| Alta | O telefone de emergência só aparece na última linha da mensagem "não encontrei". | Mostrar "Bombeiros 193 · Defesa Civil 199" no início e encurtar a lista de sugestões. | Aelton |
| Média | A mensagem de monitoramento indisponível parece defeito. | Remover quando o monitor entrar (PR #14) ou trocar por um texto neutro. | Aelton e Michelly |
| Média | Ela tentou "O que fazer agora" (opção 4) antes de informar o município (opção 3). | Indicar no menu que a opção 4 precisa do município e mostrar uma opção por linha. | Aelton |
| Baixa | O município "Embu-Guaç~u" (com til no lugar do acento) foi aceito sem aviso. | Validar contra uma lista de municípios ou confirmar ("Você quis dizer...?"). | Aelton |


## Limitações


- A preferência entre os modelos A e B se baseou nas descrições do menu, não em respostas reais.
- O observador é o desenvolvedor da busca, o que pode ter influenciado o uso, mesmo seguindo a regra de não ajudar.