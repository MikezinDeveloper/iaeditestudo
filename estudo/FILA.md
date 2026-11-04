# Fila sequencial de estudo, integração e publicação

Ordem enviada pelo usuário em 3 de novembro de 2026. Esta é a fila oficial deste lote. Não iniciar o estudo do próximo repositório antes de fechar e publicar a etapa atual. Não há estudos paralelos deste lote.

| Ordem | Repositório | Estado | Objetivo inicial a confirmar no estudo |
| --- | --- | --- | --- |
| 1 | [mojs/mojs](https://github.com/mojs/mojs) | Concluída | [Estudo, integração e validação](mojs/README.md) de Shape/Burst por quadro |
| 2 | [theatre-js/theatre](https://github.com/theatre-js/theatre) | Concluída | [Estado JSON, keyframes e driver explícito](theatre/README.md) |
| 3 | [jonobr1/two.js](https://github.com/jonobr1/two.js) | Concluída | [Cena SVG, transformações e cleanup](two/README.md); limite de Two.Text registrado |
| 4 | [d3/d3](https://github.com/d3/d3) | Concluída | [Gráficos por dados, escalas e interpolação](d3/README.md) |
| 5 | [mrdoob/three.js](https://github.com/mrdoob/three.js) | Concluída | [Cena, câmera, PBR e recursos WebGL](three/README.md) |
| 6 | [BabylonJS/Babylon.js](https://github.com/BabylonJS/Babylon.js) | Concluída | [Engine, cena e keyframes por seek](babylon/README.md) |
| 7 | [pmndrs/drei](https://github.com/pmndrs/drei) | Concluída | [RoundedBox, Center e render R3F manual](drei/README.md) |
| 8 | [sparkjsdev/spark](https://github.com/sparkjsdev/spark) | Concluída | [Packing, worker/WASM e ordenação antes da captura](spark/README.md) |

Os oito objetivos foram delimitados e verificados nos estudos vinculados. O critério de conclusão abaixo continua valendo para novos lotes.

## Plano aplicado a cada repositório

1. **Identificação:** fixar commit/versão, licença, manutenção consultável, estrutura, requisitos e documentação disponível.
2. **Reconstrução:** seguir uma capacidade concreta do ponto de entrada aos dados, relógio, avaliação e saída; registrar caminhos e símbolos.
3. **Adequação:** comparar com a base existente; decidir entre usar a biblioteca, criar uma ponte, aproveitar um mecanismo ou não incorporá-la em runtime. Justificar sobreposições e condições de licença.
4. **Implementação:** incorporar uma capacidade útil e delimitada ao nosso projeto, com configuração explícita e sem depender de autoplay ou histórico de frames quando o destino for Remotion.
5. **Validação:** testar os contratos relevantes, ordens temporais quando aplicável, export/preview significativo e regressões. Separar falhas do upstream, do ambiente e do nosso código.
6. **Acervo:** salvar análise, proveniência, decisão, comandos, resultados, limitações e próximos aprofundamentos. Preservar o material anterior.
7. **Publicação:** revisar o diff, criar commit, enviar ao GitHub autorizado e confirmar o SHA remoto. Registrar um checkpoint antes de abrir o próximo item.

## Critério de conclusão

A etapa só recebe “Concluída” quando o escopo de integração definido durante a análise estiver implementado, suas verificações obrigatórias passarem, os limites forem documentados e o commit estiver confirmado no GitHub. Um obstáculo externo deve ser registrado como bloqueio, sem simular conclusão ou avançar silenciosamente.

“Completo” refere-se ao escopo e aos critérios comprovados da etapa. Não significa conhecer todas as linhas, issues e versões da biblioteca ou certificar todos os seus recursos. A IA de edição inteira terá requisitos próprios além da integração dessas referências.

## Publicação e continuidade

- Destino confirmado pela origem existente: `MikezinDeveloper/iaeditestudo`.
- Preservar o checkout existente; sem worktrees e sem sobrescrever histórico remoto.
- Publicar primeiro a base já construída e esta fila; depois publicar checkpoints por repositório.
- Não incluir dependências instaladas, caches ou mídia de teste volumosa nos commits. Incluir receitas, lockfiles, código, verificações e relatórios que permitam reproduzi-los.
- Uma retomada deve ler esta fila, o checkpoint atual e o estado do Git antes de continuar.

## Checkpoints de publicação

Cada checkpoint anterior foi confirmado no remoto antes de começar o item seguinte.

| Etapa | SHA confirmado em `main` |
| --- | --- |
| Base e fila | `ed066313be69369e142bb69e5ba28286fb095431` |
| mo.js | `13c9a63e9397cb0da80897b5e4b1b230a921075a` |
| Theatre | `c87f03f448183829aa6331545d7ff28effb66862` |
| Two.js | `2770f086fd57216efbe1f9aa450c9720b5b2b846` |
| D3 | `5e5af875ecba690c8f9f904c50cad5e090f2f98e` |
| Three.js | `3d45a40e23f7765ca9bc3f422b77cbc4dd68ef2e` |
| Babylon.js | `7632a6f8822f87810982fd6543ce836561bc2998` |
| Drei | `7953a648f25d878c39b31165350022345fb54d48` |
| Spark | `53dc155f033d33b490d63e05512f92a7207ce5b3` |

## Fechamento do lote

Os oito escopos de integração estão implementados, com exports aprovados e limites registrados. A instalação final pelo lockfile aprovou tipos e 32 testes. O último export aprovou 90 frames H.264/AAC, repetição após o fim e nove regressões anteriores. Há [síntese das capacidades](INTEGRACOES.md), [instruções operacionais](AMBIENTE.md) e [relatórios finais](resultados/lote-final.json).

Não há próximo repositório neste lote. Os aprofundamentos e o contrato de edição proposto estão na síntese. As suites upstream não executadas/falhas observadas continuam registradas; a conclusão não certifica todo o código externo ou o produto de IA inteiro. GitHub Actions não foi observado remotamente. O rascunho de instruções do ambiente foi salvo, mas depende de salvar/publicar nas configurações para ativação.
