# Taichi: simulação com passos fixos e cache de quadros

SRC-014: [taichi-dev/taichi](https://github.com/taichi-dev/taichi), fonte `ba0e81dce559fb63a5958bf82feb1d00c55c02fe`, manifest `version.txt` **1.8.0**. Consulta em 4/11/2026 (São Paulo). Executamos o wheel público **Taichi 1.7.4**, commit interno informado `b4b956fd`, LLVM 15.0.4, Python 3.12.14 e NumPy 1.26.4. A fonte consultada e o binário executado são revisões diferentes; os resultados não certificam um build 1.8.0. [Inventário e links imutáveis](evidencias.json).

Licença **Apache-2.0**. O solver mass-spring e seus dados de exemplo são nossos; não copiamos assets ou cenas de terceiros. Taichi permanece no processo Python de geração, não é incluído no JavaScript do navegador.

## Decisão e capacidade implementada

Usar Taichi para **bake de simulação**, depois reproduzir posições em Remotion por tempo absoluto. Implementamos um tecido 2D com 120 partículas, molas estruturais/diagonais, gravidade, amortecimento, duas âncoras e contato com um piso. A composição `TaichiStudy` desenha os quadriláteros da malha a partir do cache validado.

O executor não expõe GPU. Rodamos kernels reais no backend **CPU x64**, com dois threads; CUDA, Vulkan e demais backends não foram validados. O suporte a GPU vem da arquitetura/documentação, não de um ensaio de GPU nosso. Não fornecemos números de speedup ou de performance de hardware gráfico.

## Do Python ao cálculo nativo

| Camada | Trechos consultados | Mecanismo e implicação |
| --- | --- | --- |
| Entrada Python | `python/taichi/lang/kernel_impl.py`, Kernel/materialização/launch | `@ti.kernel` captura a função, extrai argumentos, especializa e conserva kernels compilados; o corpo numérico não é simplesmente um loop Python interpretado. |
| AST | `lang/ast/ast_transformer.py`, `build_For` | Loops estáticos, ndrange e iteração de fields têm transformações diferentes. `ti.static` permite expandir os oito vizinhos conhecidos em compilação. |
| IR e offload | `taichi/transforms/compile_to_offloads.cpp` | Checagem de tipos, lowering, simplificação, verificações e offload transformam o programa antes da execução do backend. Não reimplementamos o compilador. |
| Runtime e memória | `lang/impl.py`, materialize/sync; `lang/field.py`, `to_numpy` | Fields precisam ser materializados; cópia para NumPy sincroniza os dados. O bake guarda cópias independentes, não views mutáveis do mesmo field. |
| Tipos e precisão | fields do solver em f32 | A precisão e a ordem das operações são parte do ensaio; determinismo observado não garante identidade entre CPU/GPU ou arquiteturas. |

O README contém uma lista antiga de versões Python, mas o metadata do PyPI ofereceu wheel CPython 3.12 e sua execução foi comprovada. Também distingue a linguagem Taichi dos pacotes nightly; não instalamos nightly nem afrouxamos verificações de rede/TLS.

## Solver e tempo

`simulations/taichi/bake_cloth.py` inicializa uma grade 10×12 e integra **oito subpassos por frame a 30 fps**, com `dt=1/240 s`. Para cada ligação, aplica força de mola na direção da separação, proporcional ao alongamento em relação ao repouso. A soma inclui gravidade; amortecimento exponencial reduz a velocidade. Depois, integra posição e resolve o piso. Não há aleatoriedade de inicialização.

Forças leem todas as posições antigas e escrevem um field separado de velocidade; só um segundo kernel atualiza posições. Isso evita que um loop paralelo observe vizinhos já atualizados no mesmo passo. Os dois pontos superiores permanecem fixos. O primeiro frame é o estado inicial e o frame 30 corresponde a 240 subpassos, independentemente do tempo real gasto para executar os kernels.

A simulação depende de seu estado anterior. Buscar frame 89 e depois 30 no solver vivo não restaura o estado inicial automaticamente. Por isso, a aplicação lê um **cache imutável de posições por frame**, e não tenta simular a partir da ordem de renderização do Remotion.

O modelo é um demonstrador de tecido elástico. Não é uma calibração de tecido real nem prova de acurácia de um solver de produção. O limite de alongamento usado no ensaio é um critério deste preset, não uma demonstração geral de estabilidade numérica.

## Artefatos e ponte

- `simulations/taichi/requirements.txt`: Taichi/NumPy fixados; venv separado do Node.
- `src/studies/taichi-cloth.json`: 90 snapshots de 120 posições 2D, arredondadas a seis casas após simulação f32, com fps/topologia/âncoras/versão/backend.
- `cloth-cache.ts`: valida schema, dimensões, fps, âncoras, contagens e números finitos. A busca converte milissegundos pelo fps do cache, seleciona o frame mais próximo e limita no último; sem interpolação de subframes.
- `TaichiStudy.tsx`: desenha a malha em Canvas 2D sob o relógio da composição. Nenhum Taichi/JIT precisa executar durante preview/export de um cache já existente.
- [Relatório físico](resultados/simulation.json): hashes do cache e do gerador, parâmetros, repetição, deslocamento e limites medidos. Os testes verificam ambos os hashes, evitando cache antigo após modificar o gerador sem rebake.

Esse contrato separa uma tarefa potencialmente cara de uma operação rápida de seek. Para alterar massa, rigidez, gravidade, resolução ou duração, atualizar a receita e gerar um novo cache de maneira revisável.

## Reprodução

Na raiz, para gerar com o backend CPU:

```bash
python -m venv /tmp/iaeditestudo-taichi
/tmp/iaeditestudo-taichi/bin/pip install -r simulations/taichi/requirements.txt
/tmp/iaeditestudo-taichi/bin/python simulations/taichi/bake_cloth.py
```

O programa sempre verifica o caso inicial de queda livre com molas relaxadas, duas execuções após reset, valores finitos, âncoras, piso, movimento e limite de alongamento do preset. No ensaio: erro do primeiro passo ≈6.1×10⁻⁹; repetição bit a bit aprovada; deslocamento máximo no frame 30 ≈0.176; maior ligação estrutural ≈0.145 para repouso 0.06. Unidades são as do demonstrador, não parâmetros medidos de um material.

No demo, sem Python para apenas reproduzir o cache:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- taichi
```

**36 testes locais aprovados**, incluindo dois que conferem proveniência, integridade do cache, âncoras, movimento, 90 buscas reversas, clamp e dados/tempos inválidos. O [export](resultados/render.json) aprovou H.264/AAC, 90 frames/30 fps, movimento na região central, repetição depois do fim e onze regressões anteriores. O teste de pixels prova reprodução do cache, não recalcula física no browser.

Separadamente, **8/8 casos de `tests/python/test_basics.py` passaram**, com arquivo e conftest originais, `TI_WANTED_ARCHS=cpu`, runtime instalado 1.7.4 e fonte de teste da revisão consultada. [Resultado](resultados/upstream.json), [JUnit](resultados/upstream.xml), [log](resultados/upstream.log) e [ambiente Python exato](resultados/python-environment.txt). Primeiro faltavam plugins de pytest; foram instalados com versões fixadas, sem editar os testes. Houve um aviso de depreciação de `locale.getdefaultlocale`, preservado no log. Não executamos toda a suíte, build C++ do zero, autodiff ou testes GPU.

Para repetir o subconjunto, instalar pytest 8.4.2, pytest-rerunfailures 15.1 e pytest-xdist 3.8.0 no venv; usar `TI_WANTED_ARCHS=cpu PYTHONPATH=/caminho/taichi python -m pytest /caminho/taichi/tests/python/test_basics.py -q`. O clone deve estar na revisão citada. Não confundir compatibilidade desses oito casos com equivalência completa entre fonte 1.8.0 e wheel 1.7.4.

## Limites e próximos estudos

Não validamos autocolisão, roupa 3D, costura, skinning, fluidos, grandes meshes, GPU ou sincronização de caches entre máquinas. O próximo passo útil seria um formato comum de cache com resolução, duração, unidades e transformação espacial explícitas, mais operações para bake/invalidação no estado do projeto. Uma simulação alterada precisa ser rebakeada; ler frames prontos não permite modificar a física interativamente sem novo cálculo.
