# EXP-002 — Anime.js avaliado por quadro no Remotion

## Hipótese

É possível aproveitar timeline, easing e stagger do Anime.js para gerar motion controlado pelo relógio do Remotion e operado por comandos do Codex, sem deixar a animação avançar sozinha.

## Ambiente

- Node.js 24.22.1 e npm 11.9.0.
- Anime.js 4.5.0; Remotion, bundler, renderer e CLI 4.0.540.
- Chromium 155.0.8059.79 e FFmpeg/FFprobe 7.1.5.
- Composição `AnimeMotionStudy`: 640×360, 30 fps, 120 quadros.
- Código de integração próprio; pacote publicado do Anime.js, não recompilação do checkout.

## Critérios e resultados

| Critério | Resultado observado |
| --- | --- |
| TypeScript | Aprovado |
| Testes do projeto | 14 aprovados: 6 do contrato original e 8 do adapter |
| Ordem temporal | Todos os 120 frames visitados em permutação; valores iguais aos de uma avaliação nova |
| Amostra conhecida | Em 300 ms, título com opacidade 0,875 e deslocamento 6,25 |
| Stagger | Centro inicia antes dos extremos |
| Engine autônomo | Nenhuma requisição adicional do engine observada no teste numérico Node |
| Callbacks | `seek(..., true)` atualiza o target sem chamar `onUpdate` no caso testado |
| Exportação | 120 quadros, 30 fps, 640×360, H.264 e AAC, container com 4,011 s |
| Retorno ao frame 30 | PNG com hash idêntico antes e depois de visitar o final |
| Movimento no MP4 | Região do título muda entre os frames 0 e 30, excluindo o contador |
| Regressão da composição original | Frame 30 continua idêntico à referência local anterior |

A média da diferença absoluta por canal na região do título exportado foi aproximadamente **20,19**, em uma escala de 0 a 255. Esse teste comprova alteração da região visual; não avalia preferência estética ou toda a trajetória do movimento.

O comando registrado levou aproximadamente **44,7 segundos**, incluindo bundle, capturas, exportação, inspeção e regressão. Esse tempo não é um benchmark isolado do Anime.js nem comparação de desempenho com outras bibliotecas.

## Comandos reproduzíveis

Diretório: `/workspace/iaeditestudo/demos/remotion-codex`.

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:anime
```

O script grava `out/anime/report.json`. Se existir `out/frame-30.png` do experimento anterior, também verifica essa referência; em um checkout sem baseline, registra a comparação como não executada. Não considera ausência de referência como aprovação de regressão.

## Problema encontrado: timeline reutilizada

A primeira implementação manteve o teste de igualdade entre uma instância reutilizada e uma nova. A sequência `0, 37, 74, 111, 28` falhou no último frame: a instância reutilizada devolveu o estado de saída do título.

A reprodução foi reduzida para dois tweens no mesmo objeto. Os valores e tempos estão em [seek-reuse-reproduction.json](resultados/seek-reuse-reproduction.json). Isso caracteriza o caso observado; não estabelece que todo seek ou toda timeline da biblioteca falhe.

A correção foi feita no nosso adapter: ele cria timeline e targets novos em cada amostra, copia os números e cancela a instância. O teste original não foi desabilitado nem afrouxado. Essa escolha foi registrada em [DEC-001](../decisoes/DEC-001-animejs-por-quadro.md).

## Verificações do repositório de origem

### Instalação congelada

`npm ci` no checkout upstream falhou porque manifest e lockfile discordam: o manifest requer `three` e `@types/three` na série 0.184, enquanto o lockfile não contém uma resolução consistente. O arquivo de origem não foi corrigido para fazer o setup passar.

Foi preparado um runner externo com **Mocha 10.2.0 e Chai 4.3.10**, ligado a caminhos ignorados em `node_modules`. A suíte oficial continuou usando o comando e as asserções do upstream. O working tree de origem permaneceu sem alterações rastreadas.

### Suíte Node oficial

`npm run test:node` executou **12 testes: 10 aprovados e 2 falhos**, com saída 2. As falhas foram:

- `test if the render() function can be optimized`.
- `test if the engine.update() function can be optimized`.

Ambas esperavam exatamente `49` de `%GetOptimizationStatus` e observaram `81` neste Node/V8. O resultado demonstra uma diferença em relação à expectativa de implementação interna do runtime; não demonstra, por si só, uma falha visual. Não foi provado que a causa exclusiva seja a versão do Node e não foi alterada a expectativa dos testes.

Os resultados são preservados em [upstream-node.log](resultados/upstream-node.log) e [upstream-summary.json](resultados/upstream-summary.json). As suítes de navegador oficiais, typecheck e build completos do upstream não foram executados.

## Artefatos

- [Relatório de render e inspeção](resultados/render-report.json).
- [Inventário de arquivos e revisão](evidencias.json).
- MP4: `demos/remotion-codex/out/anime/anime-motion.mp4`.
- PNGs: `demos/remotion-codex/out/anime/frame-*.png`.

Os binários ficam ignorados pelo Git e podem ser regenerados. O estudo, código, lockfile e relatórios são versionáveis.

## Limites

O experimento cobre um desenho numérico pequeno com curvas cúbicas. Não valida estabilidade/performance de grandes timelines, uso direto com DOM, WAAPI, todos os easings, SVG morphing, tipografia complexa ou sincronização labial. A existência da composição no projeto não comprova controle via plugin oficial ou WebMCP.
