# Fontes

Os repositórios de edição serão enviados pelo usuário. Este índice distingue fontes já consultadas de sugestões ou materiais ainda pendentes.

| ID | Fonte | Papel no estudo | Revisão consultada | Estado | Análise |
| --- | --- | --- | --- | --- | --- |
| SRC-001 | [openai/codex](https://github.com/openai/codex) | Referência de integração e organização do trabalho com Codex | `f1b0721c88002066201e7d977c449fbf14f1e499` | Documentação consultada parcialmente; código e execução não analisados | [Leitura inicial](analises/SRC-001-codex.md) |
| SRC-002 | [Post indicado pelo usuário — @chesny](https://x.com/chesny/status/2116976201080213799) | Primeiro material solicitado para estudo teórico | Post `2116976201080213799`; conteúdo não recuperado | Recebida; acesso bloqueado pela política de rede | [Registro de acesso](analises/SRC-002-material-chesny.md) |
| SRC-003 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Composição, tempo, mídia, motion, render e integração com Codex | `fe9f0c372706f2039da6b2a0a92b92aa746e69cf`, versão 4.0.540 | Inspeção de código e documentação; experimento com pacotes publicados executado | [Estudo aprofundado](remotion/README.md) |
| SRC-004 | [juliangarnier/anime](https://github.com/juliangarnier/anime) | Timeline, easing, stagger e integração de motion por quadro | `01b81be1df6843ccfe0a71c0699a746bf740dd77`, versão 4.5.0 | Código inspecionado; 10/12 testes Node upstream aprovados; ponte e render no nosso projeto validados | [Estudo e resultados](animejs/README.md) |
| SRC-005 | [mojs/mojs](https://github.com/mojs/mojs) | Shape, Burst, deltas e timeline normalizada | `0a9cf9a87dd5637e6fa770755e79048489bcf817`, manifest 1.7.1 | 1.699 testes upstream; ponte e export validados | [Estudo e resultados](mojs/README.md) |
| SRC-006 | [theatre-js/theatre](https://github.com/theatre-js/theatre) | Estado de projeto, keyframes, derivação e driver temporal | `6ea82b938ea49609489f6377ded693ccc6ee8f5b`, core no HEAD 0.7.0; runtime 0.7.2 | Estado JSON, ordem temporal e export do core validados; suíte monorepo não executada | [Estudo](theatre/README.md) |
| SRC-007 | [jonobr1/two.js](https://github.com/jonobr1/two.js) | Cena vetorial, grupos, transformações e SVG | `cc74b6ae7ab1fa210d900f2c0766a6ae2789af2e`, runtime 0.8.24 | 124/125 testes do subconjunto upstream; 21 testes locais e export aprovados | [Estudo](two/README.md) |

## Fila de entrada

Recebido `remotion-main.zip`; o usuário confirmou que é o Remotion oficial, sem alterações. O ZIP excedeu o limite de transferência; a análise usou o repositório público, sem confirmar igualdade de revisão com o anexo.

Prioridade mais recente: SRC-004 e sua integração com a base de Remotion. SRC-002 permanece pendente de conteúdo acessível e não bloqueia esses estudos.

## Regras do índice

- Atribuir IDs estáveis: `SRC-002`, `SRC-003` etc.
- Fixar commit ou versão para repositórios; registrar data e seção para documentação sem versão.
- Registrar a licença na análise, incluindo diferenças entre código, assets e modelos quando existirem.
- Links presentes em uma fonte, mas ainda não abertos, são pistas de pesquisa, não evidência consultada.
