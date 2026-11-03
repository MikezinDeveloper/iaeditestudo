# Tempo, mídia, áudio e motion

## Dois relógios que não podem ser confundidos

O tempo da composição define **quando o clipe aparece**. O tempo da fonte define **qual trecho da mídia ele mostra**. Para um caso simples, sem loop ou grupos com velocidade, com início `from`, recorte `trimBefore` e taxa `r`:

`frameDaFonte = trimBefore + (frameGlobal - from) × r`

A unidade do recorte nessa API é o frame na taxa da composição. Isso não significa que se possa tratar o índice de um frame codificado de mídia VFR como se fosse sempre o índice da composição.

**Evidência:** `packages/docs/docs/timing.mdx`; `packages/core/src/use-current-frame.ts`; tratamento de trim em `packages/core/src/video/OffthreadVideo.tsx`.

### Exemplo do experimento

| Clipe | Faixa global | Trim | Frame da fonte no primeiro frame visível |
| --- | --- | --- | --- |
| source-01 | `[0, 90)` | 15 | 15 |
| source-02 | `[90, 180)` | 30 | 30 |

Assim, o frame global 89 deve corresponder ao frame 104 da primeira fonte; o frame 90 deve corresponder ao frame 30 da segunda. O verificador compara regiões do export com esses frames originais.

No caso simples, sem alterações de velocidade/trim na própria `Sequence`, o relógio local de uma sequência iniciada no frame 10 mostra 20 no frame global 30. No código real, contextos aninhados, trim, velocidades e loops tornam a composição de relógios mais rica; a fórmula acima não substitui essa implementação.

## Duração é contagem, último frame é índice

Uma composição de 180 frames a 30 fps dura 6 segundos; seus índices são 0 a 179. As faixas do nosso contrato usam fim exclusivo: `[from, from + durationInFrames)`.

**Aplicação:** modelar posição e duração em frames inteiros onde o contrato exigir isso, e converter segundos com uma regra explícita de arredondamento. Não acumular durações em ponto flutuante ao construir uma timeline de muitos cortes.

O protótipo só cobre 30 fps constante. Frações como 30000/1001, mídia VFR, resampling e retiming exigem experimentos próprios.

## Interpolação e springs

`interpolate()` mapeia intervalos de entrada para saída e permite configurar extrapolação e easing. `spring()` calcula valores a partir de frame, fps e parâmetros físicos, com opções de atraso, duração e inversão.

**Evidência:** `packages/core/src/interpolate.ts`; `packages/core/src/spring/index.ts`.

**Aplicação:** montar uma biblioteca de movimentos parametrizados: entrada de título, lower third, zoom, destaque e callout. O contrato de cada movimento deve definir duração, referência espacial e propriedades que podem ser alteradas.

Springs podem ultrapassar o valor final. Isso pode ser desejado para posição/escala, mas requer cuidado quando a saída representa uma propriedade limitada, como opacidade ou volume. No experimento, opacidade usa interpolação com clamp; posição usa spring.

## Aleatoriedade e repetição

O guia oficial explica que instâncias paralelas da página podem produzir valores diferentes com `Math.random()`. Recomenda `random(seed)` para valores repetíveis.

**Evidência:** `packages/docs/docs/using-randomness.mdx`.

A repetição de um mesmo PNG no mesmo ambiente é uma evidência limitada e útil. Não demonstra identidade binária de MP4 entre sistemas, versões de navegador, GPU, codecs ou fontes diferentes.

## Áudio: três verificações distintas

1. **Presença:** existe uma stream de áudio decodificável?
2. **Envelope:** o volume exportado segue o fade definido?
3. **Sincronização:** eventos acústicos coincidem com eventos visuais esperados?

O experimento desta etapa mede presença e envelope de uma senoide de referência. Não valida sincronização labial, transcrição ou mixagem de múltiplas faixas.

No caminho HTML5 inspecionado, callbacks de volume e media frames recebem ajustes de contextos de sequência/loop. Por isso, não se deve assumir sem teste que um callback de volume recebe sempre o frame global.

**Evidência:** `packages/core/src/audio/use-audio-frame.ts`; `packages/core/src/audio/AudioForRendering.tsx`; `packages/docs/docs/audio/volume.mdx`.

## Transições alteram o cálculo da timeline

Uma transição sobreposta entre cenas ocupa frames compartilhados. Para uma série simples, sem retiming nem overlays que mudem o caso, a duração total corresponde à soma das cenas menos as sobreposições. O código de `TransitionSeries` calcula offsets e valida durações; não basta somar os números das cenas.

**Evidência:** `packages/transitions/src/TransitionSeries.tsx`, cálculo de `transitionDuration` e `transitionOffsets`; `packages/docs/docs/transitions/index.mdx`.

Esse mecanismo foi inspecionado, mas não incluído no experimento, que usa corte seco. Uma prova de dissolve deve verificar, no mínimo, início, meio e fim da sobreposição e a duração final.

## Código parametrizado versus edição independente no Studio

A documentação de interatividade orienta dar um nó JSX próprio a cada item que deve ser editado independentemente. Também descreve condições para que propriedades e keyframes sejam reconhecidos pela análise estática.

**Evidência:** `packages/docs/docs/studio/interactivity-best-practices.mdx`.

O protótipo usa `.map()` sobre clipes para demonstrar edição por dados. Isso é adequado para o experimento e não comprova seleção, duplicação ou edição independente de cada instância pelo Studio. Para uma interface com esse comportamento, estudar uma representação compatível ou geração explícita de nós.

## Próximos experimentos prioritários

- Flash e beep em tempos conhecidos para medir desvio audiovisual.
- Transição com sobreposição e verificação da duração.
- Fontes locais e texto em português com captura de quebras e clipping.
- Mídias reais com orientações, taxas e sample rates diferentes.
- Paridade entre preview e export com um mesmo conjunto de assets.
- Componentes modernos de `@remotion/media`, sem presumir equivalência com o caminho legado validado aqui.
