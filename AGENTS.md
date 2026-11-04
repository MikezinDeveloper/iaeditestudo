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

O estudo agora inclui um protótipo executável de Remotion em `demos/remotion-codex`, autorizado pelo pedido de fazê-lo funcionar com Codex. Leia o guia do demo antes de operá-lo. Mantenha propostas de arquitetura identificadas como hipóteses até sua validação. Não adicione dependências ou serviços apenas para preencher a estrutura.

A composição `AnimeMotionStudy` usa Anime.js 4.5.0. Leia `estudo/animejs/README.md` e a decisão DEC-001 antes de alterar seu adapter. Preserve a avaliação independente por quadro até que outra abordagem passe nos testes de seek fora de ordem. Relate separadamente falhas upstream e resultados do nosso projeto.
