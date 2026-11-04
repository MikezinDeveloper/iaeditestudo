# SPlisHSPlasH: fluido DFSPH nativo e exportação de partículas

SRC-015: [InteractiveComputerGraphics/SPlisHSPlasH](https://github.com/InteractiveComputerGraphics/SPlisHSPlasH), revisão `dba6b26b9387ab6bdd187d6df0a7c9d490d03500`, **2.19.1** em `version.txt`, consultada em 4/11/2026 (São Paulo). [34 arquivos consultados e seus hashes](evidencias.json). A execução final usa **a fonte C++ dessa revisão**, compilada neste executor, sem modificar o upstream.

Licença principal **MIT**, copyright Jan Bender. Dependências têm termos próprios. O exemplo usa partículas e paredes construídas por nós, sem cenas/meshes de terceiros. Não redistribuímos binários das bibliotecas: versionamos receita, código de integração, cache e relatórios.

## Decisão e capacidade entregue

Simular um pequeno **dam-break 2D com DFSPH**, usando o núcleo real do SPlisHSPlasH, e exportar posições para um cache reproduzível. A composição `SplishsplashStudy` mostra as partículas no recipiente sob o relógio Remotion. O solver de pressão e a busca de vizinhos são do upstream; o programa de configuração/export JSON e a visualização Canvas são nossos.

São 168 partículas fluidas, paredes estáticas amostradas, gravidade, 90 snapshots a 30 fps e oito subpassos de 1/240 s. O preset cobre fluido e respingos por partículas. **Espuma, reconstrução de superfície, render fotográfico e fluido 3D não foram implementados**. O cache permite seek sem repetir simulação, mas uma mudança física exige rebake.

## Reconstrução do mecanismo

| Etapa | Fonte/símbolos | Consequência |
| --- | --- | --- |
| Organização da cena | `doc/architecture.md`, `Simulation.h/.cpp` | Simulation é singleton, possui TimeStep, FluidModels e BoundaryModels. Criar modelos não encerra toda a inicialização. |
| Partículas | `FluidModel.cpp`, `initModel`, `deferredInit` | Mantém posições, velocidades, massas e IDs; o deferredInit registra o point set no buscador de vizinhos. Registrar duas vezes quebra o mapeamento esperado. |
| Vizinhança | `NeighborhoodSearch.h`, `CMake/NeighborhoodSearch.cmake` | Wrapper sobre CompactNSearch/cuNSearch/TreeNSearch. Usamos CompactNSearch CPU na revisão fixada pelo próprio CMake. |
| Kernel SPH | `Simulation.initParameters`, `setKernel`, `setGradKernel` | O conjunto de enums muda entre 2D/3D; nosso caminho direto seleciona explicitamente o cúbico 2D e seu gradiente. |
| Parede | `BoundaryModel_Akinci2012.cpp` | Partículas de parede têm volumes computados da vizinhança; contribuem à densidade e às forças de pressão. Não são colisores de círculos implementados no nosso Canvas. |
| Passo DFSPH | `DFSPH/TimeStepDFSPH.cpp`, `step` | Busca vizinhos, calcula densidades/fatores, corrige divergência, aplica forças não pressurizadas, resolve pressão e integra posições. Os comentários remetem aos algoritmos da publicação citada pela fonte; não declaramos leitura independente do paper. |
| Gravidade/densidade | `TimeStep.cpp`, `clearAccelerations`, `computeDensities` | A aceleração inicial é gravidade; densidade soma contribuições locais de fluido e paredes. Não se trata de uma queda livre de pontos sem interação. |
| Tempo | `TimeManager.h`, `Simulation.updateTimeStepSize` | O motor pode usar CFL adaptativo. Desligamos CFL e conferimos o tempo nativo de cada snapshot contra frame/fps. |
| Export | README, exemplos `custom_exporter.py` e nosso programa | O projeto oferece Partio/VTK; nosso JSON é um formato de integração próprio. Partio/VTK não foram validados nesta etapa. |

Os links por revisão e os hashes dos arquivos da tabela estão no inventário. A documentação contém opções históricas; as opções efetivas foram confirmadas no CMake da revisão, não inferidas apenas do texto.

## Problemas encontrados e solução efetiva

O wheel `pysplishsplash==2.19.1` instalou, mas **segfaultou durante import** no Python 3.12.14 e num ambiente Python 3.11.17 separado, antes de abrir GUI ou configurar a cena. Importar NumPy primeiro e limitar OpenMP não resolveu. [Log 3.12](resultados/wheel-python312.log), [log 3.11](resultados/wheel-python311.log). Não determinamos a causa do wheel nem o usamos como runtime da integração entregue.

Compilamos o núcleo C++ com `SPH_LIBS_ONLY=ON`, precisão double, caminho AVX explícito desativado e sem bindings/GUI. O upstream utiliza `-march=native`; o nosso consumidor usa flags e padrão C++11 compatíveis, incluindo `USE_DOUBLE` e `USE_CompactNSearch`. Esse binário é específico do host; não é uma distribuição portátil. O próprio wrapper exige a revisão esperada antes de configurar.

Nosso primeiro exportador direto também falhou na inicialização. A investigação do código revelou dois requisitos corrigidos **na nossa ponte**:

1. No modo 2D, selecionar explicitamente `setKernel(0)` e `setGradKernel(0)`; o enum do precomputado 3D não pertence à lista 2D.
2. Seguir a ordem do `SimulatorBase`: definir o solver; `setSimulationInitialized(true)` já executa o deferredInit dos fluidos; depois inicializar as paredes. Não chamar deferredInit de fluido novamente.

Os modelos passaram a registrar seus point sets uma única vez, e o caso nativo executou até o fim. Essas falhas do adaptador não explicam automaticamente a falha independente de import do wheel.

Ninja também recusou a ligação de um artefato ExternalProject sem regra de byproduct. A receita usa **Unix Makefiles**, sem modificar o CMake upstream. As revisões das três dependências efetivamente compiladas e os flags estão em [native-build.json](resultados/native-build.json); [configuração](resultados/native-configure.log) e [build](resultados/native-build.log) acompanham o registro.

## Código e contrato da integração

- `simulations/splishsplash/CMakeLists.txt`: configura núcleo e alvos do exportador/testes; outputs no diretório de build.
- `bake_fluid.cpp`: cria o fluido e paredes, escolhe DFSPH, desliga CFL/z-sort e exporta posições/tempos/contagens/massa. Não implementa outro solver de pressão.
- `bake_verify.py`: executa dois processos nativos novos com `OMP_NUM_THREADS=1`, verifica o resultado e grava cache/relatório. Compara o cache serializado (posições arredondadas a seis casas), não todos os bits internos do estado do solver.
- `src/studies/splish-fluid.json`: dados para reprodução no navegador, com fonte/solver/backend/fps/dt/limites e snapshots.
- `fluid-cache.ts`: valida metadados, massa, contagem, números finitos, limites e correspondência dos tempos com o relógio dos frames. Usa seleção do frame mais próximo, com clamp no fim; não faz interpolação física.
- `SplishsplashStudy.tsx`: desenha partículas e recipiente. A biblioteca C++ não precisa estar carregada durante export/preview do cache pronto.

O relatório físico conserva SHA-256 do cache, das três fontes do gerador e do binário executado. Os testes Node conferem o cache e os fontes versionados contra esse recibo. Modificar a receita sem atualizar o bake é detectado.

## Reproduzir o build e o bake

Pré-requisitos: Linux, Git, g++, Make, Python e acesso às dependências GitHub fixadas pelo CMake. Neste executor: GNU 14.2, CMake 3.31.6; Eigen vem no checkout. Na raiz, com o upstream na revisão citada:

```bash
python -m venv /tmp/iaeditestudo-sph-tools
/tmp/iaeditestudo-sph-tools/bin/pip install -r simulations/splishsplash/requirements-build.txt
/tmp/iaeditestudo-sph-tools/bin/cmake -S simulations/splishsplash -B /tmp/iaeditestudo-sph-build -G 'Unix Makefiles' -DSPLISH_SOURCE_DIR=/caminho/para/SPlisHSPlasH -DCMAKE_BUILD_TYPE=Release
/tmp/iaeditestudo-sph-tools/bin/cmake --build /tmp/iaeditestudo-sph-build --target bake_fluid sph_kernel_tests --parallel 4
python simulations/splishsplash/bake_verify.py --binary /tmp/iaeditestudo-sph-build/bin/bake_fluid
OMP_NUM_THREADS=1 /tmp/iaeditestudo-sph-build/bin/sph_kernel_tests
```

Os targets são específicos: não constroem o aplicativo gráfico ou os bindings. O diretório de fonte do upstream deve permanecer intacto; o build fica fora dele. A integração JavaScript usa o cache versionado e não necessita desses compiladores para apenas reproduzir o vídeo.

## Resultados e critérios

[Relatório físico](resultados/simulation.json): 90 frames, 168 partículas, duas execuções com cache igual; massa inicial/final ≈420 em ambas; erro máximo do relógio ≈4.2×10⁻¹⁴ s. A largura do fluido passa de 0.55 para ≈2.234 em 1 s, e o centro de massa y cai de 0.425 para ≈0.181. Todas as posições ficaram dentro da tolerância de uma camada de parede; densidade máxima observada ≈1028.6. São verificações deste preset, não uma certificação de acurácia ou incompressibilidade de toda configuração SPH.

O arquivo original **`Tests/Kernel/KernelTests.cpp` aprovou 8 casos parametrizados e 24 assertions** de normalização, gradiente integral e positividade dos kernels 2D/3D. [Resumo](resultados/upstream.json), [JUnit](resultados/upstream.xml). Não confundir o atributo `tests=24` do JUnit Catch2 com 24 casos: há oito elementos testcase. Não executamos todas as suites de estado/AVX ou benchmarks.

No demo:

```bash
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- splishsplash
```

**38 testes locais aprovados**, incluindo integridade/proveniência, massa, 90 buscas reversas, clamp, tempo, contagem e dados inválidos do cache. O [export](resultados/render.json) verifica H.264/AAC, 90 frames/30 fps, movimento, repetição depois do fim e doze regressões anteriores. A imagem mostra partículas; isso não prova reconstrução de superfície contínua, espuma ou um render de água finalizado.

## Limites e próximos aprofundamentos

Não validamos espuma/whitewater, multiphase, corpos rígidos dinâmicos, tensão superficial, viscosidade calibrada, cache de grande escala, GPU, simulações 3D ou editor gráfico. O próximo passo útil é um contrato de job de simulação com parâmetros, arquivos de entrada, build/runtime e hashes explícitos; depois, meshing de superfície e comparação entre resoluções/subpassos. Repetição local e conservação de massa são requisitos úteis, mas não substituem uma análise física de convergência.
