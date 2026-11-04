# Instruções para trabalhar neste estudo

## Objetivo

Construir uma base de conhecimento verificável para uma IA de edição de vídeo, áudio e motion graphics. Leia `README.md`, `estudo/ESCOPO.md` e `estudo/PLANO.md` antes de ampliar a pesquisa.

## Continuidade

- Os lotes seguem estritamente `estudo/FILA.md`, incluindo os novos itens 11–15. Feche estudo, integração, testes e publicação do item atual antes de estudar o próximo. Não delegue estudos paralelos desses lotes.
- Trabalhe no checkout existente. Cada tarefa na nuvem já é isolada; não crie worktrees sem pedido explícito.
- Priorize os repositórios enviados pelo usuário. Registre novas fontes em `estudo/FONTES.md` e mantenha o estado da análise atualizado.
- Navegue pelo índice e leia as análises relevantes à tarefa; não carregue todo o acervo indiscriminadamente.
- Registre decisões em arquivos próprios usando o modelo de `estudo/MODELOS.md`, quando houver evidência para decidir.

## Qualidade da pesquisa

- Separe fato documentado, comportamento observado, inferência e proposta.
- Cite URL, revisão ou versão, arquivo/seção e data de consulta nas conclusões técnicas.
- Não atribua recursos a um projeto sem consultar a fonte correspondente.
- Leitura documental não equivale a inspeção de código; inspeção de código não equivale a execução.
- Registre o comando, ambiente, dados de entrada e resultado dos experimentos. Não declare testes não executados como aprovados.
- Não escolha uma stack por número de estrelas. Compare adequação, qualidade, manutenção, licença, recursos e custo operacional.
- Não copie código externo antes de identificar sua licença e as condições de reutilização.
- A pesquisa deve produzir mecanismos compreendidos, limitações e próximos testes, não apenas resumos promocionais.

## Implementação

### Continuação17–22 e publicação

O usuário suspendeu expressamente o teste de voz16 e pediu estudar17–22 em sequência. Consulte `estudo/RELATORIO-LOTE-17-22.md` e `scripts/media-bridges.json`: testes de contrato, execução nativa, arquitetura sem pesos e revisão perceptiva têm estados distintos. Preserve as pendências; não retome sínteseQwen sem novo pedido. As novas pontes não substituem as15composições nem comprovam umaIA de edição completa.

A rejeição anterior de commit remoto permanece como histórico. Em04/11/2026 o usuário autorizou expressamente criar o commit e publicar este conjunto17–22 na main; registro em estudo/resultados/lote-17-22-publication-authorization.json. Essa autorização cobre esta publicação e sua verificação, não mudanças futuras sem relação. Não repetir o pedido para a mesma publicação. Conferir SHA/estado de CI no GitHub; nunca confundir autorização ou push com testes/artes aprovados.

O estudo agora inclui um protótipo executável de Remotion em `demos/remotion-codex`, autorizado pelo pedido de fazê-lo funcionar com Codex. Leia o guia do demo antes de operá-lo. Mantenha propostas de arquitetura identificadas como hipóteses até sua validação. Não adicione dependências ou serviços apenas para preencher a estrutura.

A composição `AnimeMotionStudy` usa Anime.js 4.5.0. Leia `estudo/animejs/README.md` e a decisão DEC-001 antes de alterar seu adapter. Preserve a avaliação independente por quadro até que outra abordagem passe nos testes de seek fora de ordem. Relate separadamente falhas upstream e resultados do nosso projeto.
