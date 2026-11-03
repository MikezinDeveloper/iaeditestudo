# Two.js — SRC-007, terceiro item da fila

Fonte: [jonobr1/two.js](https://github.com/jonobr1/two.js), commit `cc74b6ae7ab1fa210d900f2c0766a6ae2789af2e`, manifest v0.8.24, licença MIT. O demo utiliza `two.js@0.8.24` do npm. O número de versão não garante igualdade entre o fonte atual, o build versionado e o pacote publicado.

## Modelo reconstruído

Two agrega uma cena, um renderer e métodos de criação. Group organiza a hierarquia e transmite transformações/estilo aos filhos; o grupo não é uma forma desenhada por si só. Shape mantém matrizes locais e globais, posição, escala, rotação e flags de alteração. A rotação da API usa radianos.

Vector publica alterações de coordenadas por eventos. Anchor acrescenta handles e comandos de desenho. Path organiza vértices/curvas e seus caches; formas convenientes produzem essa geometria. Ao mover um filho entre grupos, a propriedade do nó é transferida, em vez de duplicar o nó visual em dois pais.

SVGRenderer percorre a hierarquia, atualiza cálculos dos objetos, escreve atributos e limpa flags. A API também possui renderers Canvas e WebGL; compartilhar modelo não certifica equivalência pixel a pixel entre todos eles.

`update()` mede tempo de execução e dispara evento de update antes de desenhar; `render()` desenha a cena. Autostart/play dirige o loop global. Nosso preset não registra callbacks de acumulação e não usa timeDelta para determinar a pose: as propriedades são funções absolutas do tempo recebido do Remotion.

As referências consultadas estão em [evidencias.json](evidencias.json), incluindo documentação local de Group, ciclo de render, transformações, SVG, âncoras e testes.

## Integração

`TwoStudy` cria uma cena SVG com círculo, estrela e linha em um grupo. Translação, rotação e escala são avaliadas a partir do tempo do frame. A cena é desenhada em host isolado e liberada ao trocar de frame. O desenho é adequado para elementos vetoriais e futuros overlays; não substitui o motor de áudio ou export do Remotion.

O fonte atual apresenta `dispose()`, mas o pacote publicado testado não oferece esse método e suas declarações refletem essa diferença. O cleanup da ponte usa as APIs existentes: pause, release, remoção de listeners e do elemento, além de remover sua própria instância do registro documentado Two.Instances. Não chamamos um método inexistente através de um cast.

## Evidência funcional

- TypeScript e 21 testes locais aprovados, incluindo vetores e transferência de filhos.
- Export: 90 frames a 30 fps, H.264/AAC e container de 3,008 s.
- Movimento da região visual: diferença média aproximada de 15,46/255 entre frames 0 e 30.
- Mesmo frame 30 após o fim: hash idêntico.
- Referências de CodexStudy, AnimeMotionStudy, MojsStudy e TheatreStudy preservadas.
- [Relatório de export](resultados/render-report.json).

## Testes de origem e diagnóstico de versão

Foi selecionado um subconjunto das suítes oficiais QUnit: core, shapes, release, dispose, bounding-box e hit-test. Os arquivos de testes não foram alterados. As bibliotecas do harness foram fixadas em QUnit 2.24.1, Underscore 1.13.7 e Resemble.js 5.0.0, com hashes preservados, em vez de depender do `latest` do HTML upstream.

Um primeiro ensaio usou o build versionado do checkout e encontrou APIs ausentes, como dispose, e diferenças de serialização. Esse resultado é preservado em [upstream-stale-build.json](resultados/upstream-stale-build.json): 125 testes, 98 aprovados e 27 falhos; seus totais de asserções são campos separados. Houve também uma tentativa anterior com fixtures de imagem em caminho incorreto, descartada como diagnóstico de setup e não como evidência de qualidade do motor.

Para distinguir falhas do fonte de artefato antigo, o entrypoint atual foi compilado com esbuild 0.28.2 em um diretório externo, mantendo os arquivos rastreados do checkout intactos. O resultado desse ensaio está em [upstream.json](resultados/upstream.json), incluindo contagem e falhas sem supressão. Não se deve confundir essa distribuição experimental de teste com o pacote npm usado pelo nosso demo.

Resultado final do subconjunto compilado do fonte: **125 testes, 124 aprovados e 1 falho; 997 de 998 asserções aprovadas**. A falha restante compara um bounding box de texto `Hello World` com família genérica `sans-serif` a números exatos. Os números diferiram neste ambiente; métricas de fonte/browser são uma limitação concreta desse teste. Não foi alterado o valor esperado nem comprovada uma causa exclusiva. Nosso preset não usa Two.Text, e seus contratos de geometria/export passaram.

O primeiro ensaio do fonte também expôs ausência de contexto WebGL com o backend `angle` no ambiente sem GPU. Uma prova de capacidade com o backend suportado `swangle` criou WebGL2; a repetição da suíte eliminou essa falha de setup. Os resultados anteriores estão preservados em `upstream-angle.json`. Isso valida a criação de contexto por software, não desempenho de GPU de produção.

O harness serve os assets e as fixtures localmente e usa uma referência ao diretório de testes para resolver os caminhos absolutos esperados. As suítes oficiais de comparação visual de todos os renderers, o build completo de documentação e a instalação de todo o toolchain VuePress não fazem parte desta validação.

## Reprodução do demo

```bash
cd demos/remotion-codex
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- two
```

Saídas em `out/studies/two/`. O preset atual usa SVG e formas sintéticas; não valida importação de SVG arbitrário, filtros, texturas, sprite sheets, motion paths ou render WebGL. O acervo conserva essas capacidades como aprofundamentos separados.
