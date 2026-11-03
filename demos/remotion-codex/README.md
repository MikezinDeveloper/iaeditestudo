# Remotion no Codex — experimento reproduzível

Um projeto mínimo para demonstrar vídeo, áudio e motion controlados por dados e comandos que o Codex consegue operar. Não é uma IA de edição completa.

## Dependências

- Node.js 24 ou superior e npm.
- FFmpeg e FFprobe no PATH, com encoder H.264 disponível.
- Navegador compatível com Remotion. O ambiente deste estudo tem `/usr/bin/chromium`; em outras máquinas, deixar o override ausente usa o navegador padrão baixado pelo Remotion.

Os pacotes Remotion estão fixados em **4.0.540** e o lockfile deve ser preservado. O demo usa React 19.2.0 e TypeScript 5.9.3.

## Instalar e verificar

A partir da raiz do repositório:

```bash
cd demos/remotion-codex
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
```

O gerador cria apenas `public/source-01.mp4`, `public/source-02.mp4` e `public/tone.wav`; executá-lo novamente substitui esses assets sintéticos. Não utiliza arquivos do usuário.

## Renderizar e validar

Neste ambiente Linux:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render
npm run verify
```

Sem override em uma máquina configurada para o navegador padrão:

```bash
npm run render
npm run verify
```

O script faz bundle, seleciona a composição, captura frames, testa repetição e alteração de título e exporta H.264/AAC. Ao variar props, seleciona a composição novamente, pois o objeto selecionado contém props resolvidas.

Em executores que bloqueiem subprocessos ou Chromium, solicitar a permissão de execução oferecida pela plataforma para o comando afetado. Não desativar verificações TLS, ignorar erros ou modificar o resultado do teste.

## Preview

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run studio
```

O comando inicia Studio sem abrir o navegador do sistema. Usar o navegador/preview suportado pelo cliente quando disponível. Um servidor HTTP iniciado não comprova reprodução, interatividade ou integração WebMCP.

Com Studio na porta 3000, `REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run smoke:studio` abre uma página em Chromium e confirma que a composição montou e o primeiro vídeo decodificou na posição esperada. O probe usa a interface de navegador da versão fixada do renderer; não é um teste do plugin ou de WebMCP.

## O que é editável

`project.json` define título, cor, metadados, dois clipes e áudio. O contrato em `src/project.ts` aceita uma única faixa de vídeo contígua e uma cama de áudio. O experimento automatizado mantém 640×360, 30 fps e 180 frames para que suas verificações sejam comparáveis.

Para outra configuração, é possível fornecer um caminho:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render -- outra-configuracao.json
npm run verify
```

O verificador assume os limites e o ponto de corte do cenário original. Para alterar cortes, dimensões, duração, tipo de mídia ou áreas com overlays, adaptar o experimento e seus critérios antes de interpretar o resultado. Arquivos referidos devem estar em `public/` e respeitar o contrato de nomes locais.

O uso de `.map()` é uma escolha para edição por dados. Não comprova edição independente de cada clipe por análise estática no Studio.

## Saídas

- `out/codex-study.mp4`: vídeo de seis segundos.
- `out/frame-0.png`, `frame-30.png`, `frame-89.png`, `frame-90.png`, `frame-120.png`, `frame-179.png`: capturas.
- `out/frame-30-repeat.png`: repetição do mesmo frame.
- `out/frame-30-variant.png`: nova seleção com outro título.
- `out/render-report.json`: configuração, metadados, hashes e tempo do comando.
- `out/verification-report.json`: resultado de inspeção da mídia exportada.

Saídas, cache, dependências e assets gerados são ignorados pelo Git; a receita, o código e o lockfile são versionáveis. Os relatórios do ensaio documentado são preservados em `estudo/remotion/resultados/`.

## Critérios verificáveis

1. Seis casos do contrato de dados enumerados pelo runner.
2. MP4 com 180 frames a 30 fps, 640×360 e duração próxima de seis segundos.
3. Uma stream H.264 e uma AAC a 48 kHz.
4. Recortes corretos imediatamente antes e depois do corte, comparando pixels com as fontes.
5. Áudio não silencioso, fade-in e fade-out mensuráveis.
6. Mesmo frame com mesmo hash no mesmo ambiente; mudar título muda os pixels.

Os testes não certificam sincronização labial, percepção estética, determinismo entre plataformas, comportamento de mídias reais ou todos os recursos do Remotion.

## Experimento adicional: Anime.js

O projeto também inclui `AnimeMotionStudy`: quatro segundos de motion calculado com `animejs@4.5.0`. A ponte em `src/anime-motion.ts` transforma o frame em milissegundos, avalia uma timeline pausada sobre objetos privados e devolve números para o React.

```bash
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:anime
```

O comando captura frames fora de ordem, compara o frame 30 após visitar o fim, exporta H.264/AAC e verifica os metadados e a região animada. Quando há baseline local da composição original, compara seu frame 30 e registra o resultado. Saídas em `out/anime/`; relatório em `out/anime/report.json`.

São 14 testes no projeto: seis do contrato original e oito da ponte de motion. A timeline é reconstruída para cada amostra porque o teste com instância reutilizada encontrou valores incorretos ao voltar do fim. Leia o [estudo do Anime.js](../../estudo/animejs/README.md) e a [decisão de integração](../../estudo/decisoes/DEC-001-animejs-por-quadro.md) antes de generalizar o mecanismo.

## Estudos registrados da fila

`scripts/studies.json` é o catálogo executável. Para cada estudo concluído:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- mojs
```

O runner verifica frames, codecs, duração, movimento numa região sem contadores, repetição após o fim e regressões quando existem baselines locais, incluindo estudos anteriores do catálogo. Saídas em `out/studies/<chave>/`. Execute `npm test` para obter a contagem atual da suíte. O mo.js inicializa sua timeline em zero antes de aplicar o progresso pedido. Theatre.js restaura keyframes de JSON e usa driver explícito; Studio não integra o bundle. As bibliotecas controlam somente hosts isolados; os efeitos são liberados pelo cleanup.

O workflow `.github/workflows/validate.yml` descreve instalação, testes e exports sequenciais no GitHub Actions, com upload dos resultados como artifacts. A existência do workflow não comprova uma execução remota aprovada; os resultados citados nos estudos são das execuções locais registradas.
