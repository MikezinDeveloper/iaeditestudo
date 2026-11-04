# Contexto para continuar este projeto em outro GPT

Atualizado em 4 de novembro de 2026. Projeto: [MikezinDeveloper/iaeditestudo](https://github.com/MikezinDeveloper/iaeditestudo), branch `main`. Base técnica deste repasse: commit `bc9e83f3d39a17219d05cf4184049354837ddd5a`; a adição deste guia é posterior, sem alterar a implementação.

## Objetivo e preferências do usuário

Construir uma IA para editar **vídeo e áudio com motion graphics**, operável pelo Codex. Transformar estudos de repositórios em mecanismos compreendidos, decisões, código executável e evidências persistidas. O usuário prefere profundidade e continuidade: concluir estudo, integração, validação e publicação de cada repositório antes de começar o próximo. Não trabalhar em repositórios da fila em paralelo. As regras locais estão em `AGENTS.md`.

## Ordem de leitura

1. Este guia e `AGENTS.md`.
2. `README.md`, `estudo/ESCOPO.md` e `estudo/PLANO.md`.
3. `estudo/FILA.md`: ordem, estados e commits confirmados no GitHub.
4. `estudo/INTEGRACOES.md`: capacidades, contratos e próximos desenvolvimentos propostos.
5. `estudo/FONTES.md`: revisões, versões e limites das fontes.
6. `estudo/AMBIENTE.md` e `demos/remotion-codex/README.md`: instalação, preview e export.
7. Estudo específico em `estudo/<biblioteca>/` antes de modificar uma ponte.

Cada estudo conserva arquivos próprios de evidência/resultados. As contagens antigas são históricas da etapa; não contradizem automaticamente a contagem da suíte atual. Não substituir o acervo por um resumo genérico.

## O que já existe

Base de pesquisa mais protótipo em `demos/remotion-codex`, com Remotion 4.0.540, React 19.2.0, TypeScript 5.9.3 e lockfile versionado. Há 15 composições: a edição audiovisual base, Anime.js e treze estudos registrados em `scripts/studies.json` do demo.

| Referência | Aplicação implementada |
| --- | --- |
| Remotion | Vídeo/áudio por dados, recortes, motion, captura e export |
| Anime.js | Timeline numérica avaliada de novo por amostra, sem autoplay |
| mo.js | Shape/Burst com progresso absoluto e inicialização em zero |
| Theatre | Core com JSON de keyframes, posição explícita e driver; sem Studio |
| Two.js | Cena vetorial SVG e transformações |
| D3 | Gráfico por dados, escalas e joins sem timers de transição |
| Three.js | Cena procedural, câmera, PBR e render manual |
| Babylon.js | AnimationGroup pausado avaliado por goToFrame |
| Drei / R3F | RoundedBox/Center, raiz sem loop e readiness de layout |
| Spark | Splats procedurais com update/sort e worker/WASM aguardados |
| Cables | Patch JSON com kernel e operadores numéricos reais selecionados |
| Taichi | Bake de tecido por kernels CPU e reprodução de snapshots |
| SPlisHSPlasH | Núcleo C++ DFSPH compilado, bake de fluido e cache |
| Custom Shader Material | Deformação GLSL com normais e iluminação preservada |
| OpenToonz / OCA | Subconjunto OCA/PNG com exposições, blank e conversão de FPS |

Os itens 11–15 foram fechados e publicados, em sequência. Não há novo repositório pendente nesses lotes. O ZIP Anime enviado pelo usuário corresponde à revisão já estudada; o recibo da comparação está em `estudo/animejs/anexo-2026-11-04.json`.

## Evidência atual e limites

- Instalação pelo lockfile, assets sintéticos e checagem de tipos aprovados; **42 testes locais** aprovados na última execução registrada.
- Cinco exports novos aprovados no lote 11–15. O último ensaio aprovou cinco comparações de exposição e os frames de referência das 14 composições anteriores.
- `estudo/resultados/lote-11-15-final.json` aponta os resultados, hashes e checkpoints; os relatórios detalhados ficam em cada estudo.
- Após reinstalar, o smoke do Studio comprovou a composição base e a mídia na posição de recorte esperada; o verificador de mídia confirmou vídeo, cortes e áudio. Isso não certifica toda interação do Studio.
- Testes upstream são distintos dos nossos testes. Há suites não executadas e falhas documentadas, inclusive Anime/Two. Não converter esses resultados em aprovação integral.
- Taichi foi executado em CPU, com fonte 1.8.0 e wheel 1.7.4 identificados separadamente; GPU física não foi validada.
- Wheels Python do SPlisHSPlasH falharam ao importar. A implementação funcional usa seu núcleo C++ compilado; não declarar que o wheel foi corrigido.
- OpenToonz nativo/tcomposer não foram executados e não há roundtrip nativo aprovado. O fixture OCA é original deste projeto, gerado com Pillow, não exportado pelo aplicativo.
- A licença do Theatre Studio difere da do core, e Remotion tem condições próprias. Consultar as licenças nos estudos antes de distribuir.
- Posts do X não recuperados continuam pendentes. Nenhuma tese foi atribuída a um post inacessível.
- CI remoto e restauração em tarefa nova não foram verificados. As instruções de ambiente foram salvas como rascunho; ativação depende de revisar/salvar/publicar nas configurações da plataforma.

## Decisões que precisam ser preservadas

Motion para export depende de frame/fps, não do tempo real. As pontes precisam suportar seek fora de ordem e liberar recursos. Consultar `estudo/decisoes/DEC-001-animejs-por-quadro.md`: reutilizar a timeline Anime depois de visitar o fim falhou; o adapter reconstrói a avaliação.

Distinguir avaliação direta (parâmetros, shader, grafo), simulação com bake (Taichi/DFSPH) e exposição de desenho (OCA). Não fazer um solver físico avançar arbitrariamente segundo a ordem de captura do renderer. Conservar hashes, parâmetros e versões do gerador junto com os caches.

WebGL foi validado por software com `swangle`; preservar o backend original de cada composição nas regressões. Baseline ausente é não executado, sem aprovação fictícia. Readiness de workers, loaders, layout e compilação pertence a cada ponte.

O estado do demo base tem uma faixa de vídeo contígua e uma cama de áudio. Os presets estão separados. Ainda não existe timeline multifaixa geral, planejador por linguagem natural, histórico completo de edição ou treinamento de modelo. Os documentos fornecem contexto; não alteram os pesos de um GPT.

## Retomar em um ambiente com execução

Pré-requisitos: Node.js 24+, npm, FFmpeg/FFprobe e Chromium compatível. No diretório raiz extraído/clonado:

```bash
cd demos/remotion-codex
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
```

No ambiente Linux registrado:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run studio -- --port=3000
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- opentoonz
```

Em outra máquina, escolher o caminho real do navegador ou seguir o mecanismo padrão do Remotion descrito no guia. O script `scripts/setup-remotion.sh` usa o caminho absoluto do ambiente Codex original; usar os comandos relativos acima em outro checkout.

Cables selecionado, caches Taichi/DFSPH e PNGs OCA estão versionados; seus ambientes de geração não são necessários para reproduzir o demo. Para regenerar, seguir a receita de cada estudo. Não copiar `node_modules` entre máquinas.

## Próximo desenvolvimento proposto, ainda não entregue

O catálogo recomenda um estado versionado com camadas/assets/presets e operações de edição pequenas, validadas e reversíveis. Depois, ligar um planejador de linguagem natural a essas operações, com preview e export de uma edição audiovisual real. A prioridade seguinte deve acompanhar a nova solicitação do usuário; não reiniciar estudos concluídos nem presumir autorização para serviços externos.

## O que a transferência preserva

O repositório preserva documentação, código, lockfile, receitas, fixtures, caches selecionados e relatórios versionados. O ZIP do GitHub é um retrato desses arquivos; o histórico de commits permanece no GitHub.

Outra conversa não recebe automaticamente o histórico completo deste chat, processos em execução, credenciais, dependências instaladas, clones externos, vídeos renderizados ignorados pelo Git ou a configuração ativa da plataforma. Os renders podem ser reproduzidos pelas receitas; relatórios e hashes já estão no acervo. Este guia registra o contexto técnico e as preferências relevantes para a continuidade.

## Mensagem para colar no outro GPT

> Estou construindo uma IA de edição de vídeo e áudio com motion no projeto MikezinDeveloper/iaeditestudo. Use os arquivos anexados como contexto de referência. Leia primeiro CONTEXTO-PARA-OUTRO-GPT.md e siga a ordem de leitura indicada. Separe o que já foi implementado e testado do que está proposto ou pendente. Preserve o acervo, as fontes, as licenças e a fila sequencial. Não afirme ter executado verificações sem executá-las. Depois, continue a partir da minha próxima solicitação.

Em um GPT com análise de arquivos, anexar o ZIP ou o Markdown consolidado e pedir a leitura dos arquivos relevantes. Se o GPT não conseguir abrir ZIPs, usar o Markdown consolidado. No Codex, conectar o repositório e fornecer a mensagem acima; apenas enviar um link não garante que um GPT tenha acesso ao conteúdo.

## Atualização posterior — novo lote16–22

O usuário enviou16Qwen3-TTS,17Audacity,18SubtitleEdit,19Auto-Editor,20RIFE,21VoiceStudio(link diverge do rótuloElevenLabs/OBS) e22FFmpeg. A [fila](estudo/FILA.md) agora registra esses itens.16 foi inspecionado em revisão fixa e recebeu contrato/preflight/escritaWAV preparados, com9 testes próprios e3 sondas do wrapper com doubles. Inferência real, áudio expressivo e export não ocorreram: runtime/pesos ausentes e poucaRAM disponível. Ver [status](estudo/qwen3-tts/resultados/status.json). NÃO interpretar como integração deTTS concluída.17–22 ainda não estudados; manter sequência. Os42 testes antigos permanecem resultados históricos, não reexecutados nesta rodada. Checkout localWindows preparado a partir do remoto, sem substituir Central anterior, sem instalação pesada ou envio de mídia do usuário.
