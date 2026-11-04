# Cables: patch serializado e propagação de valores para motion

SRC-013, consulta em 4/11/2026 (São Paulo). O link recebido aponta para **[cables_electron](https://github.com/cables-gl/cables_electron)**, commit `bde458db4ccd1de8621dd8f99a3c59b14c8b3c25`, manifest `0.0.1-local`. É a aplicação desktop. Seu README e `cables_defaults.json` levam ao runtime **[cables](https://github.com/cables-gl/cables)**, commit `93c81a30abf811f5e2421040dba1ba0ae4f34c8e`, e ao código compartilhado em **[cables_dev](https://github.com/cables-gl/cables_dev)**, commit `9513b65ee409ab1c356e24845f838c9858a287fb`.

[Fontes Electron](evidencias.json), [core](core/evidencias.json) e [shared](shared/evidencias.json) distinguem os três checkouts e os trechos consultados. Inspecionar dependências deste item não inicia estudos dos próximos itens da fila. Não auditamos todas as operações, assets ou linhas desses projetos.

## Decisão de integração

O mecanismo mais útil nesta etapa é **representar motion como um grafo de nós com portas, valores e links**, armazenado em JSON. Implementamos `CablesStudy`: um patch real do kernel Cables, com `Sine` e `Multiply` originais, recebe tempo absoluto e produz o deslocamento de uma figura Canvas 2D. Isso fornece uma base verificável para presets editáveis por grafo, sem incorporar toda a aplicação Electron ao editor web.

O desenho dos três nós e das linhas no vídeo é uma visualização nossa do grafo. A avaliação das portas usa o Cables real, não um interpretador nosso que apenas imita sua API. A integração ainda não possui a interface interativa do cables_ui, importação irrestrita de patches, CGL/WebGPU ou todos os tipos de operação. O render Canvas 2D é uma saída do nosso adaptador, não uma alegação de export oficial Canvas do Cables.

## Caminho do desktop ao runtime

| Etapa | Evidência na fonte | Aplicação |
| --- | --- | --- |
| Aplicação desktop | Electron `src/electron/main.js`, `src_client/cables_electron.js` | Inicializa janelas, IPC e editor; depende de código fora do repo. Não é uma biblioteca web isolada. |
| Distribuição e assets | `cables_defaults.json`, `gulpfile.js` | Copia corelibs/ops/UI/libs de diretórios irmãos. O build não se reduz a instalar o manifest deste repo. |
| Export HTML | `export_html_electron.js` + `patchview_export.html` | Coleta código/assets; o template instancia `CABLES.Patch` e distingue patch carregado de assets finalizados. |
| Export do projeto | `export_patch_electron.js` | Cria arquivo `.cables` e referências às operações/assets. JSON não contém sozinho todo o código necessário para executar um patch arbitrário. |
| Kernel separado | core `src/core/index.js` e `core_patch.js` | O runtime registra Patch, Op, Port, Link, Timer e utilitários. A camada CGL se conecta separadamente por evento. |

A configuração desktop permite Node e IPC em partes do editor. Essas preferências pertencem ao aplicativo; não foram copiadas para o nosso Chromium. O preset usa somente um script local com o kernel selecionado e operações conhecidas. Nenhum recurso do Electron é necessário ao export aqui validado.

## Mecanismo reconstruído

`Patch.deSerialize` cria operações por UUID, restaura portas e conecta links por `objIn/objOut` e `portIn/portOut`. A direção e os nomes importam; uma lista de nós sem links não produz a mesma avaliação. `Op.inFloat/outNumber`, `Port.set` e `Link` propagam mudanças até os consumidores. A operação `Sine` calcula `amplitude × sin(value × frequency + phase)`; `Multiply` recalcula quando uma das entradas muda.

Nosso patch contém:

```text
FrameTime.Time → Sine.value (frequency=2) → Multiply.number1 (number2=100)
```

`FrameTime` é uma pequena operação nossa que expõe uma porta de saída; não possui timer autônomo. A ponte converte milissegundos para segundos, escreve essa porta e lê `Multiply.result`. A fórmula de referência é `100 × sin(2t)`, mas o código da ponte não a calcula: os operadores e os links originais fazem isso. O teste compara o resultado contra a fórmula conhecida.

O core contém `Timer.overwriteTime/setTime`, e o CGL `CglRenderLoop` gerencia RAF, delta e `updateAnims`. O `Timer_v2` de operação também pode acumular estado. Não presumimos que todo patch Cables seja independente do histórico: neste preset, descartamos esses relógios de animação e injetamos o tempo externamente. `doRequestAnimation=false`, `patch.pause()` e `patch.timer.pause()` mantêm o grafo sem avanço autônomo.

O kernel ainda cria um profiler global com intervalo de 2 s. Esse intervalo mede memória e não determina o resultado do motion. O teste VM o encerra no teardown; no navegador há uma instância por página, encerrada ao fechar a página. `Patch.dispose()` libera operações/links, mas não é apresentado como encerramento de todos os singletons globais da biblioteca.

## Build reproduzível e licença

O pacote npm chamado `cables` consultado é outro projeto (gerenciador de CLI), e `cables-shared-client` não estava publicado no registry consultado. Não usamos esses nomes para instalar a integração. O runtime vem das revisões Git acima.

Os manifests Electron, core e shared declaram **MIT**. Electron e cables_dev possuem `LICENCE`; o core não tem arquivo de licença na raiz nessa revisão. O [NOTICE distribuído](../../demos/remotion-codex/public/vendor/cables/NOTICE.txt) preserva essa distinção e inclui a licença do código shared. Não removemos atribuição do runtime. Nenhum asset da biblioteca de exemplos foi copiado.

`scripts/vendor-cables.mjs` verifica HEAD e alterações rastreadas das duas fontes, usa esbuild 0.28.2 e gera `public/vendor/cables/runtime.js`, NOTICE e [proveniência de build](../../demos/remotion-codex/public/vendor/cables/provenance.json). Seleciona exports reais Events/Logger/helper, sem simular suas implementações. Insere os corpos originais Sine/Multiply em classes de registro; a classe FrameTime e a montagem são nossas. O arquivo gerado tem aproximadamente 111 KiB e 34 entradas de origem registradas, incluindo as operações. Isso é inventário de build, não leitura integral de cada entrada.

Para reconstruir, no demo, com os dois caches nas revisões fixadas:

```bash
node scripts/vendor-cables.mjs /workspace/research-cache/cables-core /workspace/research-cache/cables-dev
```

O runtime gerado está versionado; executar o projeto em outra máquina não exige clonar Cables nem construir Electron. Para atualizar, mudar fonte/receita de forma revisável e repetir os testes antes de substituir o artefato. Não há claim de equivalência byte a byte com um export produzido pela aplicação desktop.

## Verificação

No demo:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- cables
```

**34 testes locais aprovados**. Dois novos executam o kernel distribuído em VM com eventos nativos e conferem JSON, propagação, valores em 0/0.5/1 s, ausência de mutação do fixture, 90 seeks reversos, entradas inválidas e descarte. Os stubs VM fornecem ambiente de browser/timers; não substituem os operadores ou links. O [export real](resultados/render.json) verifica vídeo, áudio, movimento central, repetição e frames de regressão anteriores no Chromium.

Separadamente, o `gulpfile_tests.js` oficial foi executado sem modificar seu conteúdo, em um runner externo: **1.821/1.821 arquivos de metadados passaram**. O schema consultado só exige que `id`, quando presente, seja string; essa suíte é fraca como teste de funcionamento do kernel. Não a chamamos de 1.821 testes de runtime. [Resultado e comando](resultados/upstream.json), [log](resultados/upstream.log) e manifests/lockfile no mesmo diretório. Não executamos o build do aplicativo Electron, interface cables_ui, bateria de renders CGL ou o conjunto completo de operações.

## Próximos aprofundamentos

Definir um contrato de grafo editável com IDs únicos, tipos de portas, resolução de links, operações permitidas e tratamento de ciclos. Depois, testar um patch CGL exportado pela interface real, com readiness de assets, restauração e descarte de contexto. Operações com feedback, áudio, input, rede, física ou aleatoriedade precisam de estratégias próprias de snapshot/bake. Nesta etapa, o grafo numérico serializado já controla pixels do nosso vídeo, com testes de ordem temporal e proveniência reproduzível.
