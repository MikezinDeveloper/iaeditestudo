# Fila sequencial de estudo, integração e publicação

Ordem enviada pelo usuário em 3 de novembro de 2026. Esta é a fila oficial deste lote. Não iniciar o estudo do próximo repositório antes de fechar e publicar a etapa atual. Não há estudos paralelos deste lote.

| Ordem | Repositório | Estado | Objetivo inicial a confirmar no estudo |
| --- | --- | --- | --- |
| 1 | [mojs/mojs](https://github.com/mojs/mojs) | Concluída | [Estudo, integração e validação](mojs/README.md) de Shape/Burst por quadro |
| 2 | [theatre-js/theatre](https://github.com/theatre-js/theatre) | Concluída | [Estado JSON, keyframes e driver explícito](theatre/README.md) |
| 3 | [jonobr1/two.js](https://github.com/jonobr1/two.js) | Concluída | [Cena SVG, transformações e cleanup](two/README.md); limite de Two.Text registrado |
| 4 | [d3/d3](https://github.com/d3/d3) | Concluída | [Gráficos por dados, escalas e interpolação](d3/README.md) |
| 5 | [mrdoob/three.js](https://github.com/mrdoob/three.js) | Concluída | [Cena, câmera, PBR e recursos WebGL](three/README.md) |
| 6 | [BabylonJS/Babylon.js](https://github.com/BabylonJS/Babylon.js) | Na fila | Investigar o motor 3D e sua adequação frente às alternativas |
| 7 | [pmndrs/drei](https://github.com/pmndrs/drei) | Na fila | Investigar helpers de React Three Fiber aplicáveis ao editor |
| 8 | [sparkjsdev/spark](https://github.com/sparkjsdev/spark) | Na fila | Investigar render de Gaussian splats e requisitos de assets/GPU |

Os objetivos são hipóteses de triagem, não conclusões sobre os repositórios ainda não consultados.

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

## Checkpoint atual

Base publicada em `ed066313be69369e142bb69e5ba28286fb095431`; mo.js em `13c9a63e9397cb0da80897b5e4b1b230a921075a`; Theatre.js em `c87f03f448183829aa6331545d7ff28effb66862`; Two.js em `2770f086fd57216efbe1f9aa450c9720b5b2b846`. D3 passou pelo escopo de gráfico SVG, 24 testes locais, export e regressões; sua suíte upstream está não executada conforme o estudo. Este arquivo integra o checkpoint de publicação D3. Publicação D3 confirmada: `5e5af875ecba690c8f9f904c50cad5e090f2f98e`. Item atual: Three.js. Confirmar o SHA remoto depois de cada envio.

Three.js: 26 testes locais, 163 testes upstream selecionados, export de 90 frames e seis regressões aprovados. Este arquivo integra seu checkpoint; confirmar o SHA remoto após envio antes de iniciar Babylon.js.
