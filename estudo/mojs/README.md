# mo.js — SRC-005, primeiro item da fila

Fonte: [mojs/mojs](https://github.com/mojs/mojs), commit `0a9cf9a87dd5637e6fa770755e79048489bcf817`, manifest 1.7.1, licença MIT. Consulta em 3 de novembro de 2026. O pacote usado no demo é `@mojs/core@1.7.1`, fixado no lockfile.

## O que foi reconstruído

- `src/mojs.babel.js` agrega e exporta Shape, Burst, Html, Tween, Timeline e helpers; também publica uma referência no navegador.
- `Module` aplica defaults, interpreta deltas, unidades e expressões e calcula propriedades. Isso distingue o formato `{origem: destino}` do formato de keyframes do Anime.js.
- `Tweenable` cria Tween/Timeline e oferece métodos como pause e setProgress aos módulos. `Tween` converte progresso normalizado em tempo, trata direção, atraso, repetição e callbacks.
- `Timeline.add` combina filhos em paralelo; `append` acrescenta etapas, e arrays podem formar grupos paralelos. Sua duração é calculada a partir dos filhos.
- `Shape` cria um elemento e um shape SVG, calcula propriedades e escreve atributos/transformações. O polígono calcula pontos radiais e recompõe seu path.
- `Burst` compõe um mestre e swirls filhos; calcula posições radiais e duração efetiva dos filhos. Opções dos filhos precisam ser entendidas separadamente das do mestre.
- `Tweener` é o relógio autônomo com requestAnimationFrame. O nosso export não chama play nem o utiliza como relógio.
- Expressões `rand()` usam Math.random. Elas foram evitadas no preset validado; não existe garantia de determinismo para presets arbitrários que as utilizem.
- Callbacks de atualização fazem parte do próprio desenho. A estratégia de silenciar callbacks usada no Anime.js não deve ser aplicada indiscriminadamente ao mo.js.

Os caminhos e hashes consultados estão em [evidencias.json](evidencias.json). Foram inspecionados os mecanismos relevantes e executada a suíte disponível; isso não é auditoria de todo o ecossistema, issues ou exemplos externos.

## Integração implementada

Composição `MojsStudy`: polígono com raio/rotação animados e burst de doze partículas. Remotion fornece o tempo; a ponte converte para progresso de uma timeline de 2.400 ms. Cada avaliação usa instâncias e um host DOM próprios, sem autoplay. React controla o contêiner e o mo.js controla apenas sua subárvore.

O primeiro export revelou uma inicialização incorreta: a avaliação direta no progresso pedido manteve os valores iniciais. O verificador de pixels recusou o resultado. A correção inicializa a timeline em zero e depois aplica o progresso desejado pela API pública. O export corrigido demonstrou movimento e repetição do frame após visitar o final.

O helper de montagem isola também carregamentos assíncronos: o cleanup de um frame antigo só pode remover seu próprio contêiner. Isso evita que uma importação atrasada apague a cena mais recente durante preview.

## Validação

- Fonte: instalação pelo lockfile e build de teste; **1.699 testes de navegador aprovados** em Chromium, saída 0.
- A configuração upstream exclui `spec/motion-path.coffee`; não se atribui cobertura a esse arquivo. A instrumentação configurada incide sobre specs CoffeeScript, portanto seus percentuais não são uma auditoria de cobertura do motor.
- O projeto inclui testes do relógio e os testes anteriores. TypeScript e suíte local devem permanecer aprovados antes do checkpoint.
- Export corrigido: 90 frames a 30 fps, H.264/AAC, container 3,008 s; mudança média na região visual de aproximadamente 11,23/255.
- Frame 30 repetido após o fim: hash idêntico.
- Frames de referência de CodexStudy e AnimeMotionStudy: ambos preservados.
- Resultados: [render](resultados/render-report.json), [suíte upstream](resultados/upstream-summary.json) e log normalizado.

## Compatibilidade e limites

O manifest do commit estudado exige Node 24/npm 11, mas o pacote npm 1.7.1 declara Node 20/npm 10. São artefatos distintos com o mesmo número declarado; houve aviso de engine na instalação. A integração foi efetivamente testada em Node 24.22.1, sem mudar metadados nem verificações do pacote.

O runtime é dependente de DOM/SVG e não é um sampler numérico puro para Node. Não foram incorporados Html, MotionPath, Spriter, expressões aleatórias ou todos os modos de repetição. A licença MIT do mo.js não altera a licença do Remotion.

## Uso

No diretório `demos/remotion-codex`:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- mojs
```

Saídas em `out/studies/mojs/`, ignoradas pelo Git. Código, lockfile, verificações, receita e relatórios são publicados. O cenário comprova este preset e seu ciclo de avaliação; não certifica todos os presets possíveis nem uma IA de edição completa.
