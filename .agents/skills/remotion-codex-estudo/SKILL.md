---
name: remotion-codex-estudo
description: Consultar o estudo do Remotion e operar o demo de vídeo, áudio e motion deste repositório com verificações reproduzíveis.
---

# Remotion e Codex neste projeto

Este guia é próprio do `iaeditestudo`; não é o plugin oficial do Remotion.

## Contexto

Leia `estudo/INTEGRACOES.md`, `estudo/AMBIENTE.md`, `estudo/remotion/README.md` e `estudo/remotion/INTEGRACAO-CODEX.md`, relativos à raiz do repositório. Use o checkout existente; não crie worktrees sem solicitação explícita.

O motor estudado é Remotion 4.0.540. Não atualize só um pacote Remotion: as versões do demo devem permanecer alinhadas. Não atribua ao produto funcionalidades que só foram descritas pela documentação.

## Operação

Trabalhe em `demos/remotion-codex`:

1. Se as dependências estiverem ausentes ou o lockfile mudar, execute `npm ci --no-audit --no-fund`.
2. Se os assets de referência estiverem ausentes, execute `npm run assets`.
3. Edite `project.json` para alterações de dados; edite `src/StudyVideo.tsx` para modificar os mecanismos de motion/composição. Preserve mudanças do usuário.
4. Execute `npm run typecheck` e `npm test` após alterações de código ou contrato. Confirme os casos individuais e a contagem atual; o executor desta sessão já retornou apenas um agregado por arquivo dentro da sandbox.
5. Para preview, execute `npm run studio` e use o navegador suportado pelo cliente, se disponível. Não descreva WebMCP como funcional sem testar a integração.
6. Para validar um export ou quando solicitado, execute `npm run render` e `npm run verify`. No ambiente inspecionado, prefixe o render com `REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium`. Sem essa variável, usa-se o navegador padrão do Remotion.
7. Se subprocessos forem bloqueados, use o fluxo de permissão do executor para o comando afetado. Não trate isso como defeito do projeto nem suprima os erros.

## Contratos que devem ser preservados

- O demo aceita uma faixa de vídeo contígua e uma cama de áudio.
- `from` posiciona; `trimBefore` recorta a fonte.
- As verificações usam 640×360, 30 fps, 180 frames e corte no frame 90.
- Ao mudar input props, refaça `selectComposition()` e use a composição correspondente na captura/render.
- Motion deve depender de frame e props, sem depender do tempo real da execução.
- Componentes criados com `.map()` não comprovam edição visual independente no Studio.
- Novos cenários precisam de critérios e verificações adequados aos dados, sem forçar o verificador atual a aprovar uma configuração diferente.

## Motion com Anime.js

Leia `estudo/animejs/README.md` e `estudo/decisoes/DEC-001-animejs-por-quadro.md`. A versão fixada é 4.5.0. Para validar a composição `AnimeMotionStudy`, execute `REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:anime` no diretório do demo. Os resultados ficam em `out/anime/`.

Anime.js avalia objetos numéricos novos por quadro e React aplica os valores. Não introduza autoplay, mutações diretas do DOM ou cache de uma timeline sem testar novamente seek fora de ordem. A composição original continua sendo `CodexStudy`.

## Entrega

O lote atual segue `estudo/FILA.md` em sequência. Os estudos registrados em `scripts/studies.json` do demo usam `npm run render:study -- <chave>`. Leia o estudo correspondente antes de modificar a ponte. Publique e confirme o checkpoint do item atual antes de iniciar o próximo.

Informe o que foi alterado e o que os relatórios comprovam. Separe render aprovado, inspeção visual, preview interativo e integração com IA. Não conclua que um MP4 válido demonstra qualidade estética ou edição inteligente.

Para os estudos 3D, respeite o backend `swangle` registrado e as regras de readiness/cleanup de cada ponte. R3F usa raiz sem loop e aguarda layout; Spark aguarda sort. Não use o scratch object de `getSplat` como snapshot persistente. Avisos e limitações ficam no estudo correspondente.
