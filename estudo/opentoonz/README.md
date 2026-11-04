# OpenToonz — desenhos separados de suas exposições

SRC-017, consultado em 4/11/2026. Fonte `opentoonz/opentoonz`, revisão `572d59ac5fedfeaf7910967b439c6b8d73c9c3e1`; `tversion.h` identifica 1.8.0. Não se presume que HEAD seja o commit do release de mesmo número. [21 referências imutáveis com hashes](evidencias.json). Licença principal BSD-3-Clause; thirdparty, brushes MyPaint e trechos Tahoma2D possuem avisos próprios. Não copiamos o aplicativo nem seus desenhos/brushes; o fixture visual é original deste projeto.

## Reconstrução do modelo e do render

`TXshSimpleLevel` mantém o conjunto ordenado de `TFrameId` e o caminho do nível; identificadores podem ter sufixos, e não precisam ser índices contíguos da timeline. `TXshCell` guarda referência ao nível mais o frame ID. Sua igualdade exige os dois; vazio significa ausência de nível. `getImage` busca a imagem correspondente através do nível/ImageManager.

`TXsheet::getCell(row,col)` consulta uma coluna; `setCell` seleciona o tipo conforme o nível, verifica lock, atualiza a contagem e notifica a mudança. Uma exposição longa corresponde a células repetidas apontando para o mesmo desenho, sem duplicar o arquivo. Trocar um desenho compartilhado pode alterar várias exposições: é diferente de editar apenas uma posição da timeline.

`ToonzScene::save` grava propriedades, levelSet e xsheet no formato nativo `.tnz`. O projeto e os caminhos decodificados participam da resolução dos assets; um `.tnz` isolado não deve ser tratado como vídeo autocontido. Em `tcomposer.cpp`, QApplication, pastas/configuração, IO e plugins são inicializados antes de carregar o projeto e a cena. O intervalo de CLI é convertido das convenções externas para a avaliação interna; `generateMovie` chama `buildSceneFx` por frame, entrega os pares de efeitos ao MovieRenderer e usa listeners/loop de aplicação. O compositor nativo não é uma função JavaScript portátil.

`exportlevelcommand.cpp` distingue raster full-color, Toonz raster com paleta e vetores: converter paleta para cores e rasterizar vetores são operações diferentes. O caminho vetorial usa contexto GL offline, câmera e antialias. A ponte deste ensaio recebe imagens já rasterizadas; não interpreta `.pli`/`.tlv`.

## Por que escolher OCA

Em `toonz/sources/toonz/ocaio.cpp`, `OCAData::build` percorre as colunas; `frameLen` comprime células consecutivas com mesmo nível/frame ID. `buildLayer` escreve `frameNumber`, `duration`, posição, opacidade e referência ao arquivo; `_blank` tem caminho vazio. `saveCell` usa `IoCmd::exportedImage` e writer de imagem, com cache por nome da célula. O cabeçalho informa frameRate, dimensões, fundo e OCA 1.1.0. Neste exportador, startTime é zero, endTime recebe getFrameCount e as linhas percorridas satisfazem `row < endTime`; seguimos esse intervalo exclusivo.

OCA oferece imagens e exposições sem exigir o aplicativo no bundle. XDTS, também inspecionado, oferece outra possibilidade para timing: `getCellFrameIdTrack` ordena instruções e estende a célula anterior nas lacunas; ticks/hífen e null cell têm semânticas próprias. Não implementamos XDTS, pois precisaríamos resolver separadamente seus níveis/desenhos. Não se deve aplicar a regra de lacuna XDTS automaticamente a uma lista OCA.

O importador OCA nativo cria um nível a partir do primeiro arquivo, deriva frame IDs dos nomes e expõe cada duração via setCell. Nomes como `Cat.0001.png` conservam a convenção de sequência. Isso orienta o fixture, mas não comprova que ele foi aberto pelo aplicativo.

## Ponte implementada e contrato

[`oca-exposure.ts`](../../demos/remotion-codex/src/studies/oca-exposure.ts) recebe dados desconhecidos, valida o subconjunto e resolve a célula por tempo absoluto. Suporta OCA 1.1.0/U8, início zero, camadas planas paintlayer, PNG do tamanho da cena centralizado, blending normal, opacidade da camada e flags visible/reference. Exposições são intervalos sem sobreposição; lacunas e cels vazias não desenham. Tempo além do fim não desenha; voltar a um frame anterior recupera sua exposição sem histórico.

Amostra por `floor(timeMs * sourceFps / 1000)`, com tolerância numérica na fronteira. Duas exposições a 24 fps resultam em holds de dois ou três quadros na composição a 30 fps. Não interpolamos poses nem geramos desenhos intermediários. Grupos, vetores, EXR, posições não centralizadas, blending diferente e opacidade por cel diferente de 1 são recusados explicitamente. Os caminhos devem ser PNGs relativos locais.

[`OpenToonzStudy.tsx`](../../demos/remotion-codex/src/studies/OpenToonzStudy.tsx) aguarda fetch/validação do OCA e decode dos PNGs, verifica dimensões reais, compõe do fundo para a frente e aplica opacidade. O host isolado é removido no cleanup; os poucos assets decodificados são reutilizados na página. Readiness impede capturar imagens ainda não carregadas.

## Fixture e reprodução

[`generate_fixture.py`](../../simulations/opentoonz/generate_fixture.py), Pillow 13.0.0, cria oito poses de um personagem e um chão em RGBA, por primitivas de desenho com supersampling. O OCA de duas camadas contém 72 quadros a 24 fps, holds de duas exposições e um intervalo vazio. **É um fixture original compatível com o subconjunto inspecionado, não um export produzido pelo OpenToonz.** `originApp` é CodexStudy. Os nove PNGs e `walk.oca` são versionados, com [hashes e receita](resultados/fixture.json).

Para reproduzir o preset, Python não é necessário:

```bash
cd demos/remotion-codex
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- opentoonz
```

Para regenerar apenas os nossos desenhos, na raiz, usando um venv próprio:

```bash
python -m venv /tmp/opentoonz-artwork-venv
/tmp/opentoonz-artwork-venv/bin/pip install -r simulations/opentoonz/requirements.txt
/tmp/opentoonz-artwork-venv/bin/python simulations/opentoonz/generate_fixture.py
```

Isso substitui somente os arquivos de fixture/relatório definidos pela receita. Um export OCA real com o mesmo subconjunto pode substituir `public/opentoonz/walk.oca` e seus assets locais; ajustar os metadados da composição e atualizar hashes/verificações é necessário para outros tamanhos/durações.

## Validação e limites

Os dois testes novos verificam holds 24→30, blank, ordem de camadas, opacidade/flags, busca reversa dos 90 frames e retorno após o fim. Rejeitam sobreposição, duração inválida e recursos fora do contrato; conferem hashes da receita/OCA/PNGs e cabeçalhos RGBA/U8. A suíte do projeto tem **42 casos aprovados**, com tipos aprovados.

O [export](resultados/render.json) aprovou 90 frames H.264/AAC, 30 fps e 3.008 s; a diferença média central entre frames 0 e 30 foi 0.4720, com repetição exata após visitar o fim. As 14 composições anteriores conservaram os baselines. Os cinco pares de exposição passaram: diferenças zero nos holds 0/1, 1/2 e 58/59; 2.9582 na troca 2/3 e 16.3492 no retorno 59/60. O contador fica fora da região de comparação: holds precisam conservar todos os pixels centrais; trocas de pose e retorno do blank precisam alterá-los. Os baselines anteriores têm seus próprios backends preservados.

[Verificação de disponibilidade e status upstream](resultados/upstream.json): não há executável OpenToonz/tcomposer, nem Qt5Core via pkg-config. O release oficial v1.8.0 consultado lista instaladores Windows/macOS; não lista Linux. Não tentamos o build completo, não executamos a suíte upstream e não abrimos o fixture no aplicativo. A ponte OCA funcional é o escopo entregue; um roundtrip nativo continua pendente.

O OCA do próprio OpenToonz não representa seu render integral: buildLayer grava posições centrais constantes e blending normal; Transparency Fx e outros nós não são serializados como o grafo nativo. O importador avisa e achata grouplayers. Áudio, rig/plastic, câmera animada, efeitos, grupos, paletas editáveis e projetos nativos não atravessam esta ponte. Mesmo export OCA real precisará de comparação contra a referência renderizada quando esses recursos estiverem na cena.

## Aplicação ao editor e próximo ensaio

Separar identidade do desenho, exposição e asset permite à IA propor operações como prolongar uma pose ou trocar um desenho sem inventar frames. Um contrato futuro deve distinguir edição do desenho compartilhado de substituição de uma exposição. A implementação atual demonstra avaliação e composição, não contém planejador de linguagem natural.

O próximo ensaio útil é criar uma cena pequena em OpenToonz instalado, exportar OCA/PNG e uma referência nativa, importar no nosso compositor e comparar imagem/timing/alpha. Só após esse ensaio poderemos declarar interoperabilidade validada com o aplicativo, ou ampliar o subconjunto para outras transformações e níveis.
