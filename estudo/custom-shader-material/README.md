# Custom Shader Material — deformação por frame com iluminação Three

SRC-016, consultado em 4/11/2026. Fonte `FarazzShaikh/THREE-CustomShaderMaterial` em `cf86e956715bd6cd97e7ae61ffdf459e4a4c822e`; pacote executado `three-custom-shader-material@6.4.0`, Three `0.187.0`. [Arquivos, URLs imutáveis e hashes](evidencias.json). Licença MIT (`LICENSE.md`, Faraz Shaikh); o shader do experimento é original deste projeto. A raiz é um workspace privado; a versão útil é a de `package/package.json`.

## Caminho reconstruído

Em `package/src/index.ts`, o construtor recebe uma classe ou instância de material base e conserva sua identidade/propriedades. ShaderMaterial/RawShaderMaterial são recusados. `update` retira comentários, extrai o corpo de `main`, cria o hook `onBeforeCompile` e preserva o hook anterior. `defaults.ts` fornece declarações/inicialização; os mapas de keywords, disponibilidade, propriedades e patches controlam quais trechos são inseridos nos chunks do Three. Uniforms são mesclados por referência. A chave do programa considera o código e a chave anterior; mudar somente o valor de um uniform não exige outro shader.

`csm_Position` é posição no espaço do objeto, antes da projeção. A deformação precisa de normais compatíveis: apenas mover vértices deixa a iluminação representar a superfície antiga. `csm_DiffuseColor` altera a cor que entra no cálculo do material; `csm_FragColor` pode substituir a saída iluminada (com `csm_UnlitFac`). Escolhemos a primeira opção para preservar MeshStandardMaterial/PBR.

O wrapper React em `package/src/React/index.tsx` memoiza o material e atualiza/descarta em efeitos. Nossa ponte usa a entrada vanilla, sem adicionar outra raiz R3F. O código depende dos chunks GLSL do Three: o peer amplo `three >=0.159` não comprova compatibilidade com toda versão futura. O lockfile e a compilação real fazem parte da validação.

## Integração entregue

[`csm-material.ts`](../../demos/remotion-codex/src/studies/csm-material.ts) calcula uma onda `z = 0.22 sin(3x+2t) cos(4y-t)` e a normal por derivadas analíticas. Cores variam com UV; tempo vem exclusivamente de frame/fps. [`CustomShaderMaterialStudy.tsx`](../../demos/remotion-codex/src/studies/CustomShaderMaterialStudy.tsx) cria plano subdividido, câmera e luzes, aguarda `compileAsync`, renderiza uma vez e libera geometria, material, renderer e contexto. Não há loop de animação.

```bash
cd demos/remotion-codex
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- custom-shader-material
```

A composição aceita `lightIntensity` entre 0 e 10. O runner captura uma variante com luz direcional zero no mesmo frame 30 e compara pixels centrais, mantendo luz hemisférica. Isso verifica uma consequência da iluminação no navegador, além da inspeção do texto GLSL.

## Evidência observada

- Tipos e **40 testes locais** aprovados. Dois casos novos verificam material/tempo/chave, injeção no ShaderLib real, preservação do chunk de iluminação e referência dos uniforms. O fixture unitário mínimo não simula um renderer completo; a exportação cobre a compilação WebGL.
- [Export](resultados/render.json): 90 frames, 30 fps, H.264/AAC, 3.008 s; mudança média na região central 28.1440 entre frames 0 e 30. Mesmo PNG no frame 30 depois de visitar o fim.
- Luz direcional desligada: diferença média 36.8678 na mesma região. As **13 composições anteriores** conservaram seus frames de referência, respeitando seus backends GL.
- Chromium/SwiftShader emite aviso de ausência de `KHR_parallel_shader_compile`; `compileAsync` funciona por fallback. Não foi comprovada compilação paralela ou GPU física.
- Não encontramos uma suíte dedicada nos arquivos consultados. [Status upstream](resultados/upstream.json): não executado o build completo dos exemplos/workspace; os nossos testes não são uma suíte oficial do pacote.

O callback de erro de shader usa o programa DOM nativo entregue pelo Three. Há uma asserção apenas de tipo porque `@types/three` o nomeia como wrapper interno; a implementação do Three indicada nas evidências confirma o valor em runtime.

## Decisão e limites

Usar CSM como preset de material quando precisamos de deformação/cor próprias e do pipeline de iluminação do Three. Não substitui um compositor de vídeo, editor de nós ou motor de simulação. GLSL arbitrário fornecido por um planejador ainda exige validação e orçamento de recursos.

Este estudo verifica um plano, uma onda e MeshStandardMaterial em WebGL por software. Sombras/depth materials, skinning, morph targets, materiais empilhados, texturas externas, WebGPU e o wrapper React não foram validados. Deslocar vértices na GPU não atualiza automaticamente a geometria CPU usada em bounds/raycast; a onda do preset permanece enquadrada, mas uma ferramenta geral precisará de bounds e seleção coerentes. Próximo ensaio útil: sombras com material de profundidade correspondente e parâmetros versionados do shader.
