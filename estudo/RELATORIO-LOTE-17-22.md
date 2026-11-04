# Lote17–22 — estudo sequencial, implementação e evidências locais

04/11/2026. O usuário suspendeu o teste16Qwen e solicitou estudar todos os demais em sequência. Foram realizados17→18→19→20→21→22, sem estudos paralelos. O escopo desta rodada é pesquisa de mecanismos, fronteiras executáveis e provas possíveis; aplicativos/serviços/modelos ausentes continuam pendentes, sem serem rebatizados como entregues.

|Item|Entrega verificável|Limite real|
|---|---|---|
|17[Audacity](audacity/README.md)|Protocolo/plano condicionado ao catálogo nativo;9testes|Aplicativo/pipe/DSP nativos não executados|
|18[Subtitle Edit](subtitleedit/README.md)|SRT canônico, roundtrip, tempo racional e retime explícito;10testes|App/OCR/ASR/burn-in/roundtrip nativo pendentes|
|19[Auto-Editor](auto-editor/README.md)|CLI31.8.0 real:6s→2.4s,EDL eWAV;8testes de mapa temporal|Fala real, decisões editoriais eNLE/Remotion pendentes|
|20[RIFE](rife/README.md)|Warp e redes reais com pesos ALEATÓRIOS;7testes de relógio/cuts|Sem checkpoint treinado, qualidade de interpolação ouHDR aprovados|
|21[VoiceStudio](voicestudio/README.md)|PlannerAPI local, validaçãoPCM e sonda de plugin;8testes|Servidor/provedor/voz não chamados; não éElevenLabs/OBS|
|22[FFmpeg](ffmpeg/README.md)|Encode/decode real:180frames/6s,H264/AAC,PTS/DTS/áudio/cor;7testes|Sem certificação artística/mobile/HDR/VFR reais|

O registro[local estruturado](resultados/lote-17-22-local.json) e[49testes Python](resultados/lote-17-22-python-tests.json) distinguem os resultados. Os42testesTypeScript anteriores são históricos e não foram reexecutados; as15composições,src/package/lock e seus contratos foram preservados. Nenhum novo estudo foi adicionado como composiçãoRemotion aprovada por nome apenas.

## Conhecimentos importantes

- Audacity4/au3 exigem descobrir comandos reais; pico,LUFS, perfil de ruído e compressor são operações diferentes.
- SRT usa tempo, nãoFPS implícito. Manter texto/negações, sobreposição legítima e limites de arredondamento.
- Auto-Editor mede intensidade, não intenção; manterEDL exata, margens e revisão de pausa. Aplicar1.2× uma vez à fonte/fala, não a todos assets no export.
- IFNet básico não usa timestep;_m o incorpora. Não interpolar entre cortes nem tratar retiming como ganho de nitidez. Redes sem pesos só demonstram execução de arquitetura.
- VoiceStudio é um estúdio de engines. O exemploElevenLabs temSDK/chave e ignora language/speed nos argumentos ao provedor desta revisão. Não atribuir32idiomas ou controles pela propaganda/assinatura.
- FFmpeg: tags não convertemHDR; scope de timebase deve ser porstream, AAC pode ter priming e toda entrega precisa decode e conferência de relógio/áudio. Falhas de metadata do fixture foram preservadas.

## Integração futura consciente

O catálogo executável de fronteiras está em scripts/media-bridges.json. As novas rotinas não escolhem automaticamente direção de arte nem autorizam cortar fala ou gerar voz. Próxima evolução proposta: ligar somente os mecanismos necessários a uma edição de referência com estado/EDL/camadas versionados e operações reversíveis, respeitando o briefing/aprovação existente. Não enfileirar todas bibliotecas em todojob e não substituir aCentral anterior por este protótipo.

Não foram habilitados módulos noAudacity do usuário, iniciados serviçosVoiceStudio, usadosAPIkeys, retomada a sínteseQwen, alteradosoriginais ou instalados modelosRIFE. O runtimeTorch existente foi reaproveitado para o ensaioRIFE limitado. O testeQwen anterior, incluindo falhas/artefato não revisado, está em[qwen cancelado](qwen3-tts/RETOMADA-CANCELADA.md).

## Publicação e retomada

A revisão automática REJEITOU a criação do commit remoto por falta de autorização explícita atual e regra de não criar commits automaticamente. A ação não foi contornada porGit,PR ou outroexecutor. Este conjunto está LOCAL e aguarda aprovação humana paracommit/push. O último checkpoint remoto confirmado continua7e89f4a333b3e533ed43c4f4587362f379a8f685; não chamar17–22 de publicados.

Antes de publicar: conferir diff/manifest local, verificar novamenteHEAD remoto, não sobrescrever alterações alheias e obter aprovação explícita para ocommit deste conjunto. CI remoto destas alterações ainda não executado. A validação de código não é aprovação artística e as pendências nativas não foram apagadas.


## Autorização posterior de publicação —04/11/2026

O usuário respondeu **“autorizo”** à criação do commit e publicação deste conjunto17–22 na main. O bloqueio/aguardo descrito acima é histórico e foi superado para este escopo. Registro canônico: `estudo/resultados/lote-17-22-publication-authorization.json` (relativo à raiz). Conferir o commit no históricoGit para confirmação de publicação; aprovação de CI e julgamento artístico continuam separados. Não retomar o testeQwen.
