# Operar este ambiente no Codex

Checkout: `/workspace/iaeditestudo`. Leia `AGENTS.md`, `estudo/FILA.md`, `estudo/INTEGRACOES.md` e o estudo da capacidade alterada. Preserve o checkout e as mudanças existentes. Não crie worktrees sem solicitação explícita.

## Instalação e verificações

A imagem validada fornece Node 24, npm, FFmpeg/FFprobe e `/usr/bin/chromium`. Na raiz:

```bash
bash scripts/setup-remotion.sh
```

A receita instala pelo lock, gera os três assets sintéticos de teste, confere tipos e executa os testes. Não baixa os clones de pesquisa: eles são caches externos e não são necessários para executar o protótipo. As dependências de Remotion devem permanecer alinhadas em 4.0.540.

## Preview

No diretório `demos/remotion-codex`:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run studio -- --port=3000
```

Mantenha o processo em sessão persistente. Só reutilize uma porta após confirmar que pertence a este projeto. Em outro processo:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run smoke:studio
```

O smoke verifica a composição base e o recorte de mídia; não comprova WebMCP, plugin oficial ou interação completa de todas as composições. Processos precisam ser reiniciados após restauração; a persistência de arquivos não implica um servidor em execução.

## Exportações

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render
npm run verify
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:anime
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- spark
```

O catálogo `scripts/studies.json` do demo contém, na ordem, `mojs`, `theatre`, `two`, `d3`, `three`, `babylon`, `drei`, `spark`. Troque a última chave para exportar outro estudo. Para comparar regressões, gere os baselines anteriores na mesma instalação/ambiente. Ausência de baseline é reportada como não executada, sem aprovação fictícia.

O runner usa `angle` para os estudos iniciais e `swangle` para os estudos WebGL. Ele mantém o backend original de cada composição durante regressões. `swangle` usa renderização por software neste ambiente. Não confunda seus tempos com performance de GPU física ou seus hashes com determinismo entre plataformas.

## Contratos e evidências

Tempo de motion vem de frames/fps. Não introduza autoplay, Math.random ou estado acumulado sem provar seek fora de ordem. Readiness e cleanup são específicos: mo.js precisa de inicialização em zero; Theatre usa driver; R3F aguarda layout e avança manualmente; Spark aguarda sort. Consulte o estudo antes de generalizar uma ponte.

Saídas locais em `out/`; relatórios históricos em `estudo/<biblioteca>/resultados/`. A suíte local atual tem 32 casos; os testes oficiais das fontes têm resultados e limites próprios. Os avisos de depreciação de Three/R3F e de engines do mo.js estão registrados, sem alterar o lock apenas para suprimi-los.

O guia `.agents/skills/remotion-codex-estudo/SKILL.md` é próprio do projeto. A existência desse arquivo não instala automaticamente um plugin. A configuração de ambiente salva pelo onboarding é um rascunho até o usuário salvá-la/publicá-la nas configurações. A publicação do código em GitHub é um processo separado e tem checkpoints na fila. Não afirmamos restauração de tarefa nova ou GitHub Actions aprovado sem observação independente.
