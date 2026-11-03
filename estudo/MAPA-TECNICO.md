# Mapa técnico de investigação

As linhas abaixo são perguntas e hipóteses de trabalho, não recursos já implementados nem recomendações finais de stack.

| Área | O que precisamos entender | Evidência ou experimento desejado |
| --- | --- | --- |
| Entrada de mídia | Metadados, codecs, containers, orientação, resolução, taxa de quadros constante/variável e cor | Inspecionar arquivos de características diferentes e acompanhar sua interpretação pelo projeto |
| Modelo de projeto | Assets, clipes, faixas, efeitos, referências, serialização e migrações | Abrir, salvar e reabrir uma edição preservando seu significado |
| Tempo e timeline | Timebase, precisão, arredondamento, trim, gaps, sobreposições e retiming | Comparar cortes e duração em limites de quadro e em material de taxa variável |
| Áudio | Sample rate, sincronização, mixagem, ganho, fades, loudness, clipping e resampling | Medir alinhamento e comportamento de uma mixagem com fontes distintas |
| Motion graphics | Keyframes, curvas de interpolação, transformações, texto, fontes e hierarquia | Avaliar os valores de uma animação em tempos conhecidos e comparar com o render |
| Composição | Ordem de camadas, máscaras, alpha, blend, efeitos e gerenciamento de cor | Compor uma cena conhecida e verificar transparência, ordem e aparência |
| Preview | Busca temporal, proxies, cache, render incremental e reprodução | Medir tempo até o primeiro quadro, resposta ao seek e fluidez no ambiente declarado |
| Exportação | Render offline, codecs de saída, resolução, áudio, cancelamento e retomada | Exportar e inspecionar duração, conteúdo, streams e eventuais desvios do preview |
| Interpretação por IA | Transcrição, análise de cena, intenção e uso das ferramentas | Converter pedidos representativos em ações com parâmetros e referências explícitos |
| Execução de ações | Esquema de comandos, pré-condições, validação, erros e dependências | Rejeitar uma operação inválida sem corromper o projeto |
| Histórico | Undo/redo, snapshots, mudanças atômicas e repetição de comandos | Desfazer e refazer uma edição recuperando o estado esperado |
| Integração com Codex | Contexto de projeto, skills, ferramentas e automação | Verificar na interface escolhida como disponibilizar ações e validar resultados |
| Avaliação | Correção temporal, aparência, inteligibilidade, desempenho e adesão ao pedido | Construir tarefas de referência com critérios verificáveis |
| Operação | CPU/GPU, memória, disco, filas, arquivos temporários e isolamento de jobs | Registrar consumo e recuperação após uma falha durante o render |

## Hipótese inicial a testar

Um possível desenho separa **entendimento do pedido**, **operações de edição**, **estado do projeto** e **renderização**. Essa separação pode permitir revisar ações, desfazer mudanças e testar o motor sem depender do modelo de IA.

Não é uma arquitetura escolhida. Cada repositório deverá fornecer evidência a favor, contra ou de alternativas melhores.

## Cenário de referência candidato

Importar dois clipes e uma narração; cortar e ordenar trechos; adicionar música com fade; inserir um título animado; produzir preview; exportar; desfazer uma alteração e renderizar novamente.

Antes de executá-lo, definir assets autorizados, resolução, duração, taxa de quadros, fontes, ambiente e comportamento esperado. Comparações entre motores devem usar os mesmos dados e condições compatíveis.
