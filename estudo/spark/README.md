# Spark: Gaussian splats e ordenação antes da captura

SRC-012: [sparkjsdev/spark](https://github.com/sparkjsdev/spark), revisão `ffe210dc0a45d0515a06c9235878108112827d61`, manifest/runtime **@sparkjsdev/spark 2.4.0**, peer Three >=0.180.0; executado com Three **0.187.0**. Consulta em 3–4/11/2026, São Paulo. [Inventário de 25 arquivos](evidencias.json), com links imutáveis e hash do módulo npm executado.

Licença **MIT**, copyright World Labs. Preservar licença e avisos ao redistribuir código substancial. Os splats do preset são criados por nós com funções matemáticas; não baixamos cenas de exemplo nem incorporamos assets com licenças desconhecidas.

## Decisão e capacidade incorporada

Spark renderiza Gaussian splats na infraestrutura Three. É uma representação útil para cenários capturados e elementos volumétricos, diferente de malhas triangulares. Não treina um modelo 3D nem transforma vídeo automaticamente em uma cena. Incorporamos `SparkStudy`: 192 splats procedurais animados por transformação absoluta do objeto, câmera fixa e export Remotion.

O principal requisito da ponte é **esperar a ordenação**, não apenas montar o objeto. Um render inicial pode iniciar trabalho assíncrono e ainda não mostrar os splats. Para este caso pequeno, desligamos autoUpdate e LoD, fazemos update explícito e aguardamos o trabalho antes de liberar a captura.

## Reconstrução do fluxo

| Etapa | Fonte | Mecanismo e consequência |
| --- | --- | --- |
| Atributos → dados compactados | `PackedSplats.ts`, `pushSplat`/`setSplat`; `utils.ts`, `setPackedSplat` | Cada splat usa quatro uint32 (16 bytes): cor/opacidade, centro em half, escala logarítmica quantizada e rotação codificada. Comparações numéricas exigem tolerância; não é armazenamento sem perda. |
| Leitura dos atributos | `PackedSplats.getSplat` → `utils.unpackSplat` | O resultado usa um objeto temporário reutilizado. Copiar seus valores antes da próxima leitura; guardar referências ou comparar duas chamadas diretamente pode mascarar divergências. Nosso teste usa snapshots numéricos. |
| Objeto → splats globais | `SplatMesh.ts`, inicialização e herança descrita em `system-design.md` | SplatMesh participa da hierarquia Object3D e alimenta o pipeline de geração/transformação. A implementação mais geral usa SplatGenerator/dyno. Usamos PackedSplats, sem graph customizado. |
| Cena → geração e distância | `SparkRenderer.update`/`updateInternal`, acumuladores/readback | Reúne os geradores visíveis, calcula atributos e prepara distâncias para ordenação. Mudanças de câmera/objeto podem invalidar o resultado anterior. |
| Distâncias → ordem | `SparkRenderer.driveSort`, `SplatWorker.ts`, `worker.ts`, `wasm.ts` | Faz readback GPU, envia dados ao worker e ordena; troca a textura de índices quando o resultado chega. O worker recebe o módulo WASM compilado. A publicação npm inclui worker/WASM no bundle. |
| Ordem → imagem | `shaders/splatFragment.glsl` e renderer | Desenha splats com falloff gaussiano e descarte abaixo do alpha mínimo. Composição transparente requer ordem; aspecto macio é parte da representação. |
| Finalização | `SparkRenderer.dispose`, `SplatMesh.dispose`, `SplatWorker.dispose` | Cancela timers, libera targets/texturas/acumuladores, termina workers e rejeita mensagens pendentes. O mesh possui seus PackedSplats. Depois liberamos renderer e contexto. |

`docs/docs/on-demand-rendering.md` explica `onDirty`/requestRender para cenas que continuam carregando ou paginando. Nossa integração tem outro contrato delimitado: cena nova por amostra, dados locais já construídos, LoD desativado e `minSortIntervalMs=0`. Nesse cenário, `await spark.update({scene, camera})` aguarda a ordenação iniciada; confirmamos `sorting=false`, `sortDirty=false` e splats ativos antes do único render final. Isso não prova que um único update basta para streaming ou para uma engine reutilizada com operações pendentes.

## Implementação

- `spark-splats.ts`: gera uma curva espacial com cores e covariâncias orientadas; reutiliza objetos temporários durante packing. Quantidade aceita de 16 a 4096; preset 192, sem aleatoriedade.
- `SparkStudy.tsx`: importa o runtime e a fábrica sob demanda, cria WebGLRenderer sem antialias (recomendação da API Spark), 640×360/DPR=1 e buffer preservado. Usa transformação em função de `timeMs`, aguarda inicialização/update, renderiza e fornece cleanup ao host.
- O runtime/WASM fica no caminho da composição Spark, evitando inicialização dessa dependência ao montar os presets anteriores.
- O relógio de Remotion, áudio sintético e encoder continuam fora do Spark. O catálogo usa `swangle` no Chromium disponível; não requer credenciais ou chamadas remotas para a cena.

## Validação

No demo:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- spark
```

**32 testes locais**: os dois novos usam packing real do pacote publicado, conferem quantidade, centro/escala/opacidade/rotação com tolerâncias, atributos finitos, reprodutibilidade e entradas inválidas. O teste de reprodução copia os valores porque `getSplat` compartilha scratch state. [Relatório do export](resultados/render.json): MP4 H.264/AAC, 90 frames a 30 fps, região central animada, frame 30 repetido depois do fim e nove regressões anteriores. No export, worker, WASM e readback são reais.

**88/88 testes oficiais selecionados passaram**: utils 64, SparkRenderer 17, SplatMesh 4, PackedSplats 2 e SplatWorker 1. [Resultado](resultados/upstream.json), [harness](resultados/upstream.config.mjs), [log](resultados/upstream.log), manifests/lockfile adjacentes. A fonte e os asserts permaneceram intactos. O setup oficial de unit tests **simula WASM**; esses casos verificam lógica TypeScript/contratos, não o Rust ou a imagem GPU. Isso é distinto da execução real no nosso browser.

No primeiro harness, aliases JS/WASM apontavam para o mesmo ID e colidiram os mocks: 64 casos passaram e quatro arquivos falharam na coleta. IDs separados corrigiram a configuração, sem relaxar assertions. Não executamos os testes Rust, toda a suíte unit, o build WASM do zero ou os snapshots Playwright do upstream.

Para reproduzir o subconjunto: checkout da revisão em `/workspace/research-cache/spark`; diretório externo `spark-runner` com os arquivos `upstream-package*.json` renomeados para `package*.json`, `upstream.config.mjs` para `vitest.config.mjs`, e ambos os stubs ao lado; instalar pelo lock. As dependências do demo precisam estar instaladas no caminho indicado pelos aliases. Executar `./node_modules/.bin/vitest run --config vitest.config.mjs`. Os stubs reproduzem somente a estratégia do setup oficial; não devem entrar na composição de produção.

## Limites e aprofundamentos úteis

Não validamos importação PLY/SPZ/SPLAT/KSPLAT/SOG, LoD/paging/RAD, cenas grandes, iluminação/cor de captura real, spherical harmonics, skinning, XR ou treino/reconstrução de splats. A lista de formatos do README é documentação, não resultado de teste nosso. Streaming demanda um protocolo de readiness por mesh/página e cancelamento, para não capturar um conjunto parcial. Sessões longas e reuso de workers/contextos precisam de medição de memória. SwiftShader comprova execução por software; não é benchmark de GPU física nem garantia de pixels idênticos entre plataformas.
