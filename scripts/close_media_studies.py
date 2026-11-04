"""Close the local research round with measured states, not a remote publication claim."""
from pathlib import Path
import json,subprocess,sys,hashlib,difflib
R=Path(__file__).resolve().parents[1];S=R/'estudo';E=S/'resultados';E.mkdir(exist_ok=True)
modules=['test_audacity_bridge','test_subtitle_bridge','test_auto_editor_bridge','test_rife_bridge','test_voicestudio_bridge','test_ffmpeg_delivery']
p=subprocess.run([sys.executable,'-m','unittest',*modules,'-v'],cwd=R/'scripts',capture_output=True,text=True)
test={'command':[sys.executable,'-m','unittest',*modules,'-v'],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'scope':'49 own tests for17–22; does not rerun Qwen synthesis or original42TypeScript tests'}
(E/'lote-17-22-python-tests.json').write_text(json.dumps(test,ensure_ascii=False,indent=2),encoding='utf8')
if p.returncode:raise RuntimeError('New boundary regressions failed')
keys=['audacity','subtitleedit','auto-editor','rife','voicestudio','ffmpeg'];entries=[]
for k in keys:
 status=json.loads((S/k/'resultados/status.json').read_text(encoding='utf8'))
 entries.append({'item':status['item'],'key':k,'state':status['state'],'revision':status['revision'],'adapter':'scripts/'+{'audacity':'audacity_bridge.py','subtitleedit':'subtitle_bridge.py','auto-editor':'auto_editor_bridge.py','rife':'rife_bridge.py','voicestudio':'voicestudio_bridge.py','ffmpeg':'ffmpeg_delivery.py'}[k],'evidence':'estudo/'+k+'/resultados/status.json','pending':status['pending']})
(R/'scripts/media-bridges.json').write_text(json.dumps({'schema_version':1,'scope':'Bounded scripts/adapters, not a universal editor/orchestrator','entries':entries},ensure_ascii=False,indent=2),encoding='utf8')
result={'date':'2026-11-04','order':[17,18,19,20,21,22],'state':'local_research_round_complete_native_gaps_explicit','qwen16':'test_suspended_by_user_do_not_resume','new_python_tests':49,'new_python_exit':p.returncode,'original_typescript_tests':'42 historical, not rerun this round; no TS/package/lock changes','original_compositions':15,'remote_publication':'blocked_by_automatic_review_pending_explicit_user_approval','remote_base':'7e89f4a333b3e533ed43c4f4587362f379a8f685','entries':entries,'artistic_quality':'not evaluated/certified','scope':'Six sequential bounded studies; not six fully integrated native applications or a complete AI editor'}
(E/'lote-17-22-local.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
body='''# Lote17–22 — estudo sequencial, implementação e evidências locais

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
'''
(S/'RELATORIO-LOTE-17-22.md').write_text(body,encoding='utf8')
for rel,note in [('README.md','## Estudos17–22 preparados localmente\n\n[Relatório e estados reais](estudo/RELATORIO-LOTE-17-22.md).49testes Python novos passaram; dois ensaios nativos deAuto-Editor/FFmpeg e sondasRIFE/VoiceStudio têm escopos explicitados. Publicação aguarda aprovação;42testes/15composições anteriores preservados. Qwen suspenso pelo usuário.'),('CONTEXTO-PARA-OUTRO-GPT.md','## Estado mais recente —17–22 estudados em sequência\n\nLeia [o relatório local](estudo/RELATORIO-LOTE-17-22.md), a fila e scripts/media-bridges.json. O usuário suspendeu o testeQwen16; não retomá-lo sem pedido.17–22 tiveram estudos delimitados,49testes próprios e ensaios possíveis; várias capacidades nativas/perceptivas continuam pendentes. Não confundir arquiteturaRIFE sem pesos, contratos deAPI ou catálogo com integração pronta de todoaplicativo. Não publicarcommits automaticamente: revisão automática rejeitou ocommit remoto e aguarda aprovação humana explícita deste conjunto. Alterações estão locais, não afirmar publicaçãoGitHub ouCI aprovados.'),('estudo/PLANO.md','## Fechamento local17–22\n\nO usuário suspendeu o teste16 e pediu prosseguir;17→22 foram estudados sequencialmente com limites registrados. Consultar [relatório](RELATORIO-LOTE-17-22.md) e resultados/lote-17-22-local.json. Próximo passo de produto segue proposto, não implementado. Publicaçãoremota aguarda aprovação explícita após rejeição automática; não contornar.')]:
 path=R/rel;text=path.read_text(encoding='utf8')
 if note not in text:path.write_text(text.rstrip()+'\n\n'+note+'\n',encoding='utf8')
print(json.dumps({'new_tests':49,'exit':p.returncode,'entries':len(entries),'remote_publication':'pending_user_approval'},indent=2))

# A later, actual human authorization supersedes the earlier publication block.
authorization=E/'lote-17-22-publication-authorization.json'
if authorization.is_file():
 result['remote_publication']='user_authorized_snapshot_for_publication'
 result['authorization']='estudo/resultados/lote-17-22-publication-authorization.json'
 (E/'lote-17-22-local.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 for rel in ('README.md','CONTEXTO-PARA-OUTRO-GPT.md','estudo/PLANO.md','estudo/RELATORIO-LOTE-17-22.md'):
  doc=R/rel;text=doc.read_text(encoding='utf8')
  if '## Autorização posterior de publicação' not in text:
   doc.write_text(text+'\n\n## Autorização posterior de publicação —04/11/2026\n\nO usuário autorizou expressamente publicar este conjunto na main. Consultar estudo/resultados/lote-17-22-publication-authorization.json na raiz e o históricoGit; o bloqueio anterior é histórico. CI e arte continuam separados.\n',encoding='utf8')
