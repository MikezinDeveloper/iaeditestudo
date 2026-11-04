# Babylon.js: engine, cena e keyframes com seek explícito

SRC-010: [BabylonJS/Babylon.js](https://github.com/BabylonJS/Babylon.js), commit `fff529b3cd08c5e1f62a9e10335611b4f69b1b7c`. Consulta em 3/11/2026, São Paulo. O manifest privado `@dev/core` usa 1.0.0; o pacote executado é **@babylonjs/core 9.33.2**, com tipos incluídos. Não são identificadores intercambiáveis nem prova de artefatos byte a byte iguais. [Fontes e hashes](evidencias.json).

Licença **Apache-2.0**. Preservar licença, avisos e indicar alterações ao redistribuir código derivado; o pacote inclui `NOTICE.md` com componentes adicionais. Nosso preset não carrega decoders, modelos, texturas ou servidores externos. A configuração do harness de testes foi adaptada da configuração Apache-2.0 da fonte, com atribuição no arquivo.

## Decisão e utilidade

Adicionar `BabylonStudy`, cena procedural controlada por um **AnimationGroup nativo pausado**, para provar a integração do modelo de animação da engine ao tempo do Remotion. A engine é uma alternativa para recursos que precisem da infraestrutura de cena do Babylon. Não migramos o Three nem misturamos objetos de ambas as engines: cada uma possui materiais, coordenadas, recursos e ciclo de vida próprios.

Three já cobre geometria/câmera/render explícito. A contribuição distinta validada aqui é o percurso de keyframes nativos até o objeto, mais a separação entre engine real e `NullEngine` para testar estado. Nenhuma decisão de engine definitiva para o produto foi tomada.

## Mecanismo reconstruído

| Camada | Caminho e símbolo na fonte | Comportamento e implicação |
| --- | --- | --- |
| Registro e módulos | `src/scene.ts`, `Engines/engine.ts`, `Materials/standardMaterial.ts` | Alguns pontos de entrada reexportam implementação `.pure` e registram efeitos necessários. Importar só classes puras exige reconstruir registros; preferimos entradas públicas profundas testadas. |
| Backend | `Engines/abstractEngine.pure.ts`, `runRenderLoop`, `dispose`; `nullEngine.ts` | Loop e recursos pertencem à engine. Não iniciamos `runRenderLoop`; `NullEngine` verifica estado sem comprovar pixels. |
| Dados de geometria | `Meshes/Builders/boxBuilder.pure.ts`, `CreateBoxVertexData` | Dimensões escalam positions; lados/UVs/normais viram VertexData da malha. O box selecionado tem 24 vértices. |
| Trilha | `Animations/animation.pure.ts`, `setKeys`, `_interpolate` | Tipo, fps e keys determinam interpolação. Escolhemos float linear para `rotation.y`, frames 0, 45 e 90 com 0, π e 2π. |
| Grupo → alvo | `animationGroup.pure.ts`, `start`, `pause`, `goToFrame` | `goToFrame` não faz nada antes de o grupo iniciar. Iniciamos uma vez, pausamos e então buscamos; o grupo encaminha para seus animatables. |
| Aplicação | `animatable.core.ts` e `runtimeAnimation.ts`, `goToFrame` | O runtime limita à extensão dos keys, interpola o valor e o aplica ao alvo. Há estado de eventos e sincronização; não presumimos que todo tipo de animação será independente do histórico. |
| Readiness → imagem | `scene.pure.ts`, `whenReadyAsync`, `render(updateCameras, ignoreAnimations)` | Aguardar materiais prontos antes da captura; `render(true, true)` atualiza câmera e evita o avanço automático de animações. |
| Descarte | `scene.pure.ts`, `dispose`; `abstractEngine.pure.ts`, `dispose` | Cena libera grupos, materiais, malhas, câmeras e texturas. Engine para loops e libera recursos; nosso canvas e contexto também são encerrados. |

Links imutáveis de todos esses arquivos estão no inventário. O README do upstream demonstra um loop e câmera com input; esses exemplos informam a API, mas não comandam o relógio do nosso editor.

## Implementação no protótipo

`babylon-scene.ts` constrói câmera em z negativo olhando para a origem, luz hemisférica, box não cúbico e material. A convenção de coordenadas padrão difere do preset Three. `seek(ms)` valida tempo, converte para a trilha de 30 fps, limita em 90 e força a matriz da malha. O descarte é idempotente e impede seek posterior.

`BabylonStudy.tsx` possui canvas 640×360, escala de hardware 1 e buffer preservado. Aguarda `whenReadyAsync`, faz um render e entrega cleanup ao host isolado do frame. O catálogo seleciona Chromium `swangle` para o backend WebGL por software. Áudio e MP4 continuam sob Remotion.

O fps da trilha nativa é 30; convertemos milissegundos para essa base explicitamente. Uma futura composição a outro fps deve preservar essa conversão, em vez de tratar seu número de frame como frame nativo do asset.

## Verificações

No demo:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- babylon
```

**28 testes locais aprovados**. Os dois novos verificam vértices, pausa, ângulo conhecido a 1 s, 90 buscas em ordem reversa no mesmo grupo, clamp, entradas inválidas e descarte. O [export real](resultados/render.json) aprovou 90 frames/30 fps, 640×360, H.264/AAC, movimento na região central, retorno ao frame 30 e sete regressões anteriores. Não substitui teste de sincronia perceptual ou performance em GPU física.

**1.231/1.231 testes oficiais selecionados passaram** (1.230 de vetores/matrizes e um de animação com um key). O ensaio oficial selecionado está em [resultados/upstream.json](resultados/upstream.json); a receita e o histórico de execução estão nos arquivos adjacentes. Ele é separado dos 28 testes do produto. Não executamos a instalação/build de todo o monorepo, lint, suites visuais, integração, física ou serviços. O primeiro harness externo falhou na coleta por decorators não transformados; incorporamos a mesma estratégia esbuild/TC39 documentada em `vitest.config.mts`, sem alterar testes ou asserts.

## Proveniência e reprodução da fonte

O clone parcial fixou o SHA, mas a busca posterior de blobs por Git falhou por credenciais do transporte. Obtivemos o arquivo público `https://codeload.github.com/BabylonJS/Babylon.js/tar.gz/<SHA>` e extraímos somente core e testes. Os 22 arquivos inventariados foram conferidos com o hash de blob esperado na árvore Git; não atribuímos a falha de transporte ao código do Babylon. O arquivo de distribuição é volumoso; uma cópia completa já disponível evita novo download.

A receita do subconjunto usa Vitest 5.0.3 e esbuild 0.28.2 num diretório externo, aliases `core` para a fonte e `vitest` para a ferramenta, globals e pool forks. Preserva a fonte, seu lockfile e sua política de instalação. A fonte usa decorators TC39 e o setup provê Symbol.metadata. Essa configuração não deve ser confundida com a configuração completa do monorepo, que também contém aliases e pré-requisitos de outros pacotes.

## Limites

A ponte cobre uma trilha float e uma câmera fixa, sem física, partículas, blending, root motion, eventos de animação, IK ou carregamento de cenas. Esses mecanismos podem depender do histórico e exigem snapshots/simulação próprios. Renderizar engine nova por frame favorece isolamento, com custo perceptível: o tempo do comando está registrado no relatório, sem valor de benchmark geral. WebGPU, consumo real de memória sob sessões longas, formatos de cena e edição interativa permanecem aprofundamentos separados.
