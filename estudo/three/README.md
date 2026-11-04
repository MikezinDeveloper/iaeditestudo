# Three.js: cena 3D avaliada pelo tempo da edição

Fonte SRC-009: [mrdoob/three.js](https://github.com/mrdoob/three.js), commit `c6a4b78be1a3d7839399410cc157950c5fd6e58b`, manifest e runtime npm **0.187.0**, tipos **0.187.0**. Consulta em 3/11/2026, horário de São Paulo. [Inventário de trechos consultados](evidencias.json). Licença **MIT**: preservar aviso de copyright e licença ao redistribuir código substancial. Não importamos modelos, texturas ou exemplos de terceiros.

## Papel no editor e decisão

Adicionar uma camada 3D procedural: câmera em perspectiva, objeto, material e iluminação, sobre uma composição audiovisual. Remotion continua responsável por duração, áudio e export; Three resolve a imagem 3D. Isso permite vinhetas e elementos espaciais sem transformar o editor inteiro em uma engine de jogos.

Decisão desta etapa: incorporar `three` em uma composição delimitada, `ThreeStudy`. Não substituir os mecanismos vetoriais anteriores. A avaliação é por tempo absoluto e o renderer não possui relógio autônomo. Esta é uma capacidade executável do protótipo, ainda sem interface de autoria, importação GLTF ou planejamento por IA.

## Reconstrução do mecanismo

| Entrada → saída | Código da fonte | Consequência para a integração |
| --- | --- | --- |
| Hierarquia → matrizes de mundo | `src/core/Object3D.js`, `add`, `updateMatrixWorld` | A transformação local é composta com a matriz do pai e propagada aos filhos. Rotação usa radianos; alterar propriedades não implica possuir um relógio. |
| Câmera → projeção | `src/cameras/PerspectiveCamera.js`, construtor e `updateProjectionMatrix` | FOV, aspect, near/far determinam o frustum. Fixamos 640/360, FOV 40, limites 0.1–100; câmera em z=7. Alterar resolução exigirá recalcular aspect. |
| Parâmetros → buffers | `src/geometries/TorusKnotGeometry.js` | Amostra uma curva, constrói uma base ortonormal e extruda o tubo; produz positions, normals, UVs e índices. Segmentar mais aumenta o custo de CPU e GPU. Nossa malha usa 72×12 segmentos. |
| Superfície + luz → shader | `src/materials/MeshStandardMaterial.js` | Modelo PBR com roughness/metalness. Usamos luz hemisférica e direcional; sem environment map, não prometemos aparência fotográfica. |
| Cena + câmera → pixels | `src/renderers/WebGLRenderer.js`, `render` | Atualiza matrizes, calcula projeção/frustum, organiza objetos e executa chamadas de desenho. A chamada única é suficiente para a cena escolhida. |
| Recursos → descarte | `WebGLRenderer.dispose`, `forceContextLoss`; `webgl/WebGLGeometries.js` | Remover o canvas não libera automaticamente buffers, materiais e contexto. Eventos de dispose removem atributos/estados; o contexto é encerrado quando disponível. |

Essas conclusões vêm dos símbolos acima, vinculados à revisão fixa no inventário. A documentação `docs/llms-full.txt`, seções iniciais, apresenta WebGL e WebGPU. Seus exemplos com loop, controles e CDN são referências, não instruções para nosso projeto: usamos npm travado, câmera fixa e render explícito. WebGPU/TSL não foram incorporados nesta etapa.

## Ponte implementada

- `src/studies/three-scene.ts`: fábrica de cena sem DOM, valida tempo finito não negativo, calcula rotação e posição diretamente a partir de milissegundos; devolve câmera, malha e descarte.
- `src/studies/ThreeStudy.tsx`: cria renderer WebGL, DPR=1, antialias e `preserveDrawingBuffer`, renderiza uma vez e libera geometria/material/renderer/contexto no cleanup, inclusive após erro de render.
- `BrowserStudy`: espera a inicialização antes de liberar a captura; host próprio por frame evita que a limpeza assíncrona de um frame apague outro.
- `scripts/studies.json`: preset de 90 frames, 30 fps e backend Chromium `swangle`. Esse backend usa SwiftShader neste ambiente sem GPU física. Os estudos SVG anteriores mantêm sua configuração.

Construir uma cena e um contexto por frame simplifica isolamento e seek, mas tem custo alto. É uma decisão de corretude deste experimento, não a arquitetura final de um preview em tempo real. Reutilização de contexto requer provar reset completo, descarte e seek antes de substituir esta ponte.

## Validação e reprodução

No diretório `demos/remotion-codex`:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- three
```

Os dois testes novos verificam buffers finitos/contagem, enquadramento, eventos de descarte, rejeição de tempo inválido e matrizes dos 90 frames em ordem reversa. A suíte completa local tem 26 casos. O export verifica mídia real, movimento fora dos contadores, repetição do frame 30 após visitar o fim e regressões dos estudos anteriores com baselines locais. Consulte o [relatório de render](resultados/render.json).

Separadamente, **163/163 testes oficiais do subconjunto** Vector3, Matrix4, Object3D, BufferGeometry, PerspectiveCamera, TorusKnotGeometry e MeshStandardMaterial passaram. Importamos os testes da fonte sem alterar asserts, em Chromium e QUnit 2.25.0. [Resultado](resultados/upstream.json), [harness](resultados/upstream-harness.html) e [versão/hash dos assets](resultados/upstream-assets.json). Não equivale a executar `npm test`, lint, addons, loaders, exemplos ou e2e de todo o upstream.

Para reproduzir o subconjunto: clonar a revisão para `research-cache/three`; salvar o harness como `research-cache/three-runner/index.html`; baixar o QUnit da URL registrada como `qunit.js` ao lado, conferir hash; servir `research-cache` por HTTP. Executar `node scripts/run-browser-suite.mjs http://127.0.0.1:3210/three-runner/index.html ../../estudo/three/resultados/upstream.json` a partir do demo. O harness só expõe o resultado ao runner, sem modificar o checkout da fonte.

## Falha encontrada e correção

O primeiro export completou mídia e repetição, mas a regressão de `CodexStudy` falhou: ela foi capturada com `swangle`, enquanto seu baseline usava `angle`. O runner passou a manter instâncias por backend e comparar cada composição com sua configuração original. Os hashes continuam exatos; nenhum baseline foi substituído para acomodar a falha.

## Limites e próximos aprofundamentos

Renderização por software não mede desempenho em GPU física. Hash de PNG prova repetição neste ambiente, não equivalência entre drivers/plataformas. Não validamos WebGPU, XR, pós-processamento, transparência complexa, sombras, assets externos ou materiais texturizados. Cor utiliza defaults da versão fixada; gerenciamento de cor/HDR e correspondência com vídeo precisam de ensaio próprio. A próxima capacidade útil seria descrever câmera/material/geometria em dados validados e medir reuso seguro de contexto; esta etapa fornece a implementação e as evidências iniciais, sem declarar esses itens prontos.
