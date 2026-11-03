# EXP-001 — Vídeo, áudio e motion operados no Codex

## Hipótese

Um projeto pequeno, apoiado nas APIs públicas do Remotion e em um contrato de dados explícito, permite ao Codex alterar uma composição, produzir uma saída e verificar propriedades audiovisuais sem modificar o motor.

## Ambiente e entradas

- Linux x86-64; Node.js 24.22.1; npm 11.9.0.
- Remotion, renderer, bundler e CLI: 4.0.540; React 19.2.0.
- Chromium instalado: 155.0.8059.79; FFmpeg/FFprobe 7.1.5.
- Fonte inspecionada: `fe9f0c372706f2039da6b2a0a92b92aa746e69cf`.
- Dois assets de quatro segundos gerados com `testsrc2`, sendo o segundo com rotação de matiz.
- Senoide de 440 Hz, seis segundos, 48 kHz, gerada localmente.
- Sem mídia de terceiros, chamadas a modelos ou serviços de geração.
- Uma faixa de vídeo contígua e uma cama de áudio; composição 640×360, 180 frames, 30 fps.

## Comandos

Diretório: `/workspace/iaeditestudo/demos/remotion-codex`.

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render
npm run verify
```

Para Studio, iniciar em um processo separado:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run studio -- --port=3000
```

Com Studio iniciado:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run smoke:studio
```

O executor desta sessão exigiu permissão para subprocessos, Chromium e acesso de instalação. Não foram desativadas verificações de TLS ou integridade dos pacotes.

## Critérios e resultados observados

| Critério | Resultado |
| --- | --- |
| Checagem TypeScript | Aprovada |
| Contrato de dados | 6 testes individuais aprovados, nenhum ignorado |
| Contagem e taxa | 180 frames, 30 fps |
| Resolução e codecs | 640×360, H.264 e AAC a 48 kHz |
| Duração do container | 6,016 s; duração nominal dos frames: 6 s |
| Frame 89 da saída | Corresponde à fonte 01, frame 104, após trim de 15 |
| Frame 90 da saída | Corresponde à fonte 02, frame 30, após trim de 30 |
| Repetição do frame 30 | SHA-256 idêntico em duas capturas no mesmo ambiente |
| Variação de título | SHA-256 diferente após nova seleção de composição |
| Áudio | Não silencioso; início e fim com RMS inferior a 35% do trecho constante |
| Studio em Chromium | Composição identificada; primeiro vídeo com `readyState=4` e posição de mídia 0,5 s |

Os recortes são comparados em uma região de 160×70 pixels sem overlays. O erro médio por canal foi aproximadamente 0,234 no frame 89 e 1,693 no frame 90; ambos abaixo do limite de 12 em uma escala de 0 a 255 e mais próximos do frame esperado do que do mesmo trecho sem trim. Isso demonstra o cenário selecionado, não uma certificação geral de precisão para qualquer codec ou taxa.

RMS do áudio decodificado: início `0,00279`, trecho constante `0,03101`, final `0,00375`. Essas medidas demonstram o envelope de referência; não avaliam inteligibilidade, loudness profissional nem sincronização labial.

O comando de render registrado levou aproximadamente 45,2 segundos, incluindo bundle, capturas, variante e export. Não é benchmark isolado do encoder nem estimativa de custo para produção.

A receita `scripts/setup-remotion.sh` também foi executada integralmente: reinstalação com `npm ci`, regeneração de assets, TypeScript e seis testes aprovados. A verificação audiovisual foi repetida após regenerar os assets. O Studio foi parado e reiniciado por esta sessão, e o smoke voltou a passar.

## Falhas investigadas durante o ensaio

1. **Transferência do ZIP:** limite de 32 MiB; a fonte pública foi usada após confirmação do usuário. A revisão exata do anexo continua sem comparação.
2. **Sandbox e subprocessos:** `ffprobe` retornou `EPERM`, e o runner dentro da sandbox exibiu só um agregado por arquivo. A execução pela permissão suportada enumerou os seis testes e permitiu o render.
3. **Props da variante:** o primeiro ensaio reutilizou uma composição com props resolvidas para outro título. A imagem não mudou. O código foi corrigido para selecionar uma composição para cada conjunto de props, e o ensaio passou. Não foi caracterizado como defeito do Remotion.

## Artefatos preservados

- [Relatório de render](resultados/render-report.json)
- [Verificação audiovisual](resultados/verification-report.json)
- [Verificação do Studio](resultados/studio-report.json)
- Demo e receitas em `demos/remotion-codex/`.

O MP4 e os PNGs ficam em `demos/remotion-codex/out/`, ignorados pelo Git e regeneráveis. Os relatórios preservados identificam o ensaio; novos renders não devem ser confundidos com ele sem atualizar a documentação.

## Conclusão e limites

A hipótese é sustentada para o fluxo local e a composição de referência. Foram exercitados edição por props, corte seco, recorte de origem, título animado, áudio com envelope, exportação e montagem da preview no Studio.

Não foram testados controle via WebMCP, instalação do plugin oficial, interpretação autônoma de pedidos, transcrição, múltiplas faixas de áudio, transições sobrepostas, mídia VFR, HDR, GPU ou grandes jobs. O smoke do Studio não testa play/pause, seek arbitrário ou toda a interface de edição.

## Configuração reutilizável

Os campos `install_script` e `start_skill` foram salvos no rascunho do ambiente, com confirmação de persistência. A instalação usa a receita testada e o início registra comandos, diretórios e verificação de prontidão. O salvamento não publica a configuração nem comprova restauração em outra tarefa; é necessário revisar, salvar e publicar nas configurações do ambiente para ativar a versão preparada.
