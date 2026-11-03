# Arquitetura reconstruída do Anime.js 4.5.0

Os caminhos abaixo pertencem ao commit fixado no [índice](README.md); as URLs e hashes estão no inventário de evidências.

## Camadas e responsabilidades

| Camada | Papel identificado | Evidência principal |
| --- | --- | --- |
| Clock | Cadência, velocidade e cálculo de delta | `src/core/clock.js` |
| Engine | Dirigir instâncias ativas e solicitar ticks | `src/engine/engine.js` |
| Timer | Estado temporal, loops, direção, callbacks, seek e descarte | `src/timer/timer.js` |
| JSAnimation | Normalizar parâmetros, targets, keyframes e tweens | `src/animation/animation.js` |
| Composição | Coordenar tweens que disputam a mesma propriedade | `src/animation/composition.js` |
| Render | Resolver tempo e valores, aplicar easing e escrever o resultado | `src/core/render.js` |
| Timeline | Agregar filhos, labels e posições relativas | `src/timeline/timeline.js`, `position.js` |
| Utilitários | Stagger, aleatoriedade, manipulação de valores | `src/utils/stagger.js`, `random.js` |
| Integrações | DOM/SVG, WAAPI, texto, scope e adapters | Entradas públicas em `src/index.js` e exports do manifest |

## 1. O relógio padrão é de execução, não de vídeo

O engine escolhe `requestAnimationFrame` no navegador e `setImmediate` fora dele. Ele mantém uma lista de instâncias ativas e, ao atualizar, calcula o tempo a partir do relógio de execução. `defaults.autoplay` é verdadeiro. O engine também tem unidade de tempo e velocidade globais.

**Consequência para nós:** iniciar uma animação comum em um efeito React criaria outro relógio competindo com o frame escolhido pelo Remotion. Um export pode avaliar páginas em paralelo e visitar tempos diferentes de uma reprodução contínua.

**Adaptação implementada:** `autoplay: false` por instância e `tempoMs = frame × 1000 / fps`. Não alteramos `engine.useDefaultMainLoop` ou pausamos o engine global, pois isso afetaria outros consumidores da biblioteca.

## 2. Timer é uma máquina com estado

O timer guarda tempo anterior, posição, direção, iteração, estado de pausa e conclusão. `seek()` reavalia a instância e aceita silenciar callbacks, mas preserva a condição anterior de reprodução: uma instância que estava tocando pode voltar a tocar depois do seek. `cancel()` descarta a participação dos tweens; `revert()` também tenta recuperar o estado inicial.

**Evidência:** `src/timer/timer.js`, `init`, `resume`, `seek`, `cancel` e `revert`.

Logo, disponibilidade de `seek()` não equivale a uma garantia universal de função pura em qualquer desenho de timeline. Foi justamente isso que nosso teste de ida e volta investigou.

## 3. Target e tipo de valor definem como o resultado é escrito

`registerTargets()` normaliza alvos e registra características de DOM/SVG. O código de valores distingue propriedade de objeto, atributo, transform, CSS e variável CSS. Valores podem ser funções, números, strings com unidades ou cores. Alguns caminhos leem estilos e variáveis CSS do documento.

**Evidência:** `src/core/targets.js`; `src/core/values.js`, `getFunctionValue`, `getTweenType` e leitura de CSS.

**Adaptação implementada:** nossos targets são objetos numéricos privados, criados durante a amostragem. Não passamos seletores ou elementos React ao engine; tampouco fornecemos CSS variables como valores dos targets numéricos. React continua sendo o responsável pelo DOM final.

Isso reduz dependências de layout e conflitos de propriedade entre render declarativo e mutação externa. Não prova que o uso direto com DOM seja inadequado para interfaces interativas; é uma escolha para este export.

## 4. Parâmetros são convertidos em tweens

`JSAnimation` transforma keyframes e propriedades em estruturas de tween. O teste oficial de keyframes documenta diferenças importantes: um array de dois valores simples representa origem/destino; sequências de objetos representam keyframes com suas próprias opções. O código de composição mantém relações entre tweens da mesma propriedade.

Durante o render, o progresso é calculado a partir do tempo local, passa por easing e modifier e produz um valor. A implementação escreve números em objetos ou recompõe strings/unidades conforme o tipo.

**Evidência:** `src/animation/animation.js`, `generateKeyframes`; `src/core/render.js`; `tests/suites/keyframes.test.js`.

**Aplicação:** expor operações claras na futura linguagem de motion: propriedade, origem, destino, início, duração e easing. Não confundir um vetor numérico que é dado do domínio com o array de origem/destino da API.

## 5. Timeline resolve posições antes de renderizar

Uma timeline agrega animações e timers, calcula duração e organiza posições. O parser aceita posições numéricas, labels e expressões relativas. Nesta versão, `<` referencia o final do filho anterior e `<<` seu início; operadores relativos podem ser combinados com labels.

**Evidência:** `src/timeline/position.js`; `src/timeline/timeline.js`, `addTlChild` e `add`; exemplos em `tests/suites/timelines.test.js`.

**Aplicação:** labels são úteis para fases como entrada, destaque e saída. Para integrar com uma timeline audiovisual, devemos resolver esses tempos para uma unidade explícita e verificar a duração efetiva. Duração de uma timeline de motion não define automaticamente duração da composição de vídeo.

## 6. Stagger é uma função de distribuição

`stagger()` calcula valores por target e índice. A implementação cobre origem central, início/fim, grids, distribuição aleatória e jitter, entre outras opções. Grids automáticos podem depender da geometria dos targets; opções aleatórias exigem atenção à seed.

**Evidência:** `src/utils/stagger.js`.

**Adaptação implementada:** sete barras numéricas, com atrasos de 80 ms a partir do centro. Não há leitura de dimensões do DOM, jitter ou aleatoriedade no cenário validado.

## 7. Easings e springs exigem contratos diferentes

O parser de easing resolve funções ou nomes. Nomes desconhecidos podem cair no easing neutro, e certas sintaxes antigas produzem aviso e fallback. Uma IA que gere um nome incorreto pode, portanto, obter uma animação aparentemente válida com curva diferente da pretendida.

**Evidência:** `src/easings/eases/parser.js`.

**Aplicação proposta:** aceitar um catálogo explícito de curvas no contrato de edição. A implementação atual usa nomes fixos conhecidos; ainda não recebe nomes arbitrários do usuário.

O solver de spring tem parâmetros físicos e opções de duração percebida/bounce. A função de easing do spring também possui lógica de conclusão e callback. Não se deve pressupor que toda função com formato de easing seja desprovida de estado nem copiar parâmetros do spring do Remotion esperando igualdade visual.

**Evidência:** `src/easings/spring/index.js`, `Spring` e `this.ease`. O demo atual usa curvas cúbicas, não springs do Anime.js.

## 8. Recursos de navegador precisam de testes próprios

- **SVG motion path:** consulta `getTotalLength`, `getPointAtLength` e matriz de transformação. A geometria depende do elemento e de seu contexto.
- **SVG drawable:** usa proxies para atualizar atributos de stroke. Nosso demo usa apenas progresso numérico convertido por React em `strokeDashoffset`; não utiliza esse helper.
- **Scope:** agrupa instâncias e restauração de efeitos, incluindo listeners e estilos; oferece um caminho para integração de interface com ciclo de vida React.
- **WAAPI:** transforma parâmetros para animação nativa do navegador. Isso acrescenta outra implementação e contratos de reprodução que não foram validados no nosso export.
- **Texto:** o código de split consulta DOM e segmentação; tipografia e medidas precisam ser reproduzíveis no ambiente de render.

**Evidência:** `src/svg/motionpath.js`, `drawable.js`; `src/scope/scope.js`; `src/waapi/waapi.js`; `src/text/split.js`.

## 9. Aleatoriedade com seed ainda tem sequência

`createSeededRandom()` retorna um gerador cujo estado avança a cada chamada. A mesma seed não garante o mesmo resultado por frame se a ordem ou o número de chamadas mudar. Para vídeo, seria necessário derivar valores por identidade estável ou reconstruir uma sequência definida. Nosso adaptador não usa aleatoriedade.

**Evidência:** `src/utils/random.js`.

## Limite da reconstrução

A descrição explica o caminho investigado e as consequências para nosso projeto. Ela não certifica todos os modos de composição, adapters, cores, unidades, curvas, browsers e formas de target. Os próximos experimentos devem acompanhar um recurso concreto que quisermos incorporar.
