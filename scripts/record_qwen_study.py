"""Record this bounded study and actual tests, retaining prior batch evidence."""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime
R=Path(__file__).resolve().parents[1];S=R/'estudo/qwen3-tts';E=S/'resultados';E.mkdir(parents=True,exist_ok=True)
U=R.parent/'upstream-qwen3-tts';SHA='022e286b98fbec7e1e916cb940cdf532cd9f488e'
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf8')
def save(path,data):write(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
metadata=json.loads((E/'model-metadata.json').read_text(encoding='utf8'))
request=dict(schema_version=1,purpose='new_voiceover',text='Cada decisão muda o resultado.',language='Portuguese',speaker='Ryan',model_size='1.7B',model_snapshot='models/qwen3-tts-1.7b-customvoice',model_revision=metadata['revision'],instruct='Tom sério e natural, com firmeza, sem gritar.',max_new_tokens=256,seed=1,device='cpu',dtype='float32')
save(S/'request.example.json',request)
for name,args,cwd in [('environment',['scripts/probe-local.py'],R),('boundary-tests',['-m','unittest','test_qwen_voiceover','-v'],R/'scripts'),('preflight',['scripts/qwen_voiceover.py','estudo/qwen3-tts/request.example.json','--preflight'],R)]:
 p=subprocess.run([sys.executable,*args],cwd=cwd,capture_output=True,text=True)
 save(E/(name+'.json'),{'command':[sys.executable,*args],'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'date':'2026-11-04'})
environment=json.loads(json.loads((E/'environment.json').read_text())['stdout'])
files=['README.md','LICENSE','pyproject.toml','qwen_tts/inference/qwen3_tts_model.py','qwen_tts/inference/qwen3_tts_tokenizer.py','qwen_tts/core/models/configuration_qwen3_tts.py','qwen_tts/core/models/modeling_qwen3_tts.py','examples/test_model_12hz_custom_voice.py','finetuning/README.md']
save(S/'evidencias.json',{'date':'2026-11-04','source':'https://github.com/QwenLM/Qwen3-TTS','revision':SHA,'coverage':'README/pyproject and selected wrapper/core/tokenizer/config/example/finetuning paths; not whole-repo audit','files':[{'path':p,'sha256':hashlib.sha256((U/p).read_bytes()).hexdigest(),'url':f'https://github.com/QwenLM/Qwen3-TTS/blob/{SHA}/{p}'} for p in files]})
readme='''#16 — Qwen3-TTS: estudo técnico e fronteira de narração

Estado: **parcial / bloqueado para síntese real**. Não fechado como integração de locução validada. Nenhum áudio Qwen foi gerado, ouvido ou exportado. Itens17–22 aguardam, conforme a fila sequencial.

## Proveniência e licença

Fonte [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS), revisão `022e286b98fbec7e1e916cb940cdf532cd9f488e`; manifest qwen-tts0.1.1. Consulta04/11/2026. Código Apache-2.0; cartão/metadata do modelo também declara Apache-2.0, registrado separadamente em resultados/model-metadata.json. Nenhum código upstream foi vendorizado; scripts da ponte são próprios. Revisão do código não identifica a revisão dos pesos. [Inventário com hashes e URLs](evidencias.json).

## Mecanismo seguido no código

`Qwen3TTSModel.from_pretrained` registra AutoConfig/AutoModel/AutoProcessor, carrega pesos, processador e defaults. O core também carrega speech_tokenizer e generation_config. Isso exige snapshot completo, não apenas um arquivo de pesos. O caminho upstream aceita downloads implícitos; nossa fronteira exige snapshot local e modo offline.

`generate_custom_voice` valida família custom_voice, normaliza escalares/listas e verifica idiomas/speakers. Texto e instrução recebem wrappers de conversa e são tokenizados separadamente; language/speaker e instruct_ids condicionam o core. O talker gera códigos acústicos; o code predictor trata codebooks adicionais; speech_tokenizer.decode retorna waveforms e sample rate. O tempo de fala não é comprimento de texto nem max_new_tokens. Medir amostras reais; alinhar palavras somente após ASR/alinhamento e revisão.

CustomVoice fornece timbres predefinidos; VoiceDesign requer outro modelo e descreve uma voz; Base oferece referência/clonagem. Não são modos intercambiáveis da mesma chamada. A ponte inicial implementa somente a preparação de CustomVoice; não substitui sua voz gravada, não clona vozes e não limpa ruído.

## Descobertas relevantes

- Idioma Portuguese é documentado entre dez idiomas, mas nenhum dos nove speakers publicados tem português como idioma nativo. Compatibilidade linguística não comprova naturalidade brasileira: escuta/PT-BR ainda necessária.
- Na revisão consultada, generate_custom_voice descarta `instruct` quando tts_model_size é0b6. Nosso contrato REJEITA pedido expressivo0.6B, em vez de dar uma aprovação falsa. O controle textual da1.7B precisa validação perceptiva real.
- O wrapper descreve non_streaming_mode=False como simulação de entrada streaming; essa API retorna a waveform completa. Não transferir automaticamente os97ms publicitários para este runner batch/CPU.
- FlashAttention2 é recomendação condicional da fonte, não dependência obrigatória universal. A ponte usa eager configurado para uma primeira prova de viabilidade; CUDA/bfloat16/FlashAttention não foram testados.
- Sampling/seed não garantem mesma onda entre hardware, versões e backends. Não prometer determinismo do TTS só porque Remotion é dirigido por frames.
- Reuso de prompt/clonagem, fine-tuning, vLLM e API comercial foram identificados, mas não integrados. Nenhum serviço pago, conta ou mídia de cliente foi usado.

## Implementação delimitada

[scripts/qwen_voiceover.py](../../scripts/qwen_voiceover.py) fornece contrato de nova narração, rejeição de combinação errada de modelo/instrução, preflight leve, caminho de geração offline preparado, gravação PCM24 exclusiva e sidecar de proveniência/duração. O caminho `synthesize` ainda NÃO executou com modelo real; tratá-lo como implementação preparada, não inferência comprovada. Seed, texto, idioma, voz, instrução e revisão são conservados; timestamps por palavra permanecem ausentes; truncamento por limite de tokens precisa revisão. Não há medição automática LUFS ou nota de qualidade.

O WAV pode ser usado como asset local na cama de áudio já existente do demo após revisão. Não alterei project.json nem anunciei multifaixas. A composição base continua com uma faixa contígua e uma cama. Inserção da nova fala, ducking com música,1.2× editorial e sync com motion não foram implementados nesta etapa. Não acelerar o TTS por acidente nem substituir fonte gravada.

## Validação realmente executada

-9 testes da nossa fronteira: idioma/texto, emoção0.6B, finalidade de nova voz, snapshot ausente, parâmetros inválidos, duração PCM medida, não sobrescrita e rejeição de onda inválida. Um WAV sintético de contrato é temporário e não é TTS. [Log](resultados/boundary-tests.json).
-3 verificações do controle de fluxo da função upstream, extraída por AST e executada com doubles: instrução1.7B, descarte0.6B e rejeição de famíliaBase. [Relatório](resultados/upstream-control-flow.json). Isso não executa redes neurais, tokenizer ou inferência e não é suíte oficial upstream.
-Preflight real retornou exit2/bloqueado por dependências e snapshot ausentes. Não é falha escondida nem geração aprovada. [Resultado](resultados/preflight.json).
-Os42 testes Remotion anteriores são históricos; não foram reexecutados nesta etapa. Não os somar aos9 Python como uma mesma suíte aprovada. Nenhuma dependência npm/lock/composição anterior foi alterada.

## Bloqueio real e critério de retomada

O probe observou Windows, Python3.12 e RAM disponível inferior ao tamanho dos próprios pesos publicados. [Ambiente medido](resultados/environment.json). O metadata público lista4.515.695.644bytes de safetensors no snapshot1.7B consultado, antes de buffers/ativação/duplicação. Esse tamanho em disco não é medição de pico deRAM/VRAM; float32CPU pode demandar mais. Não concluí que todo uso é impossível; concluí que não há viabilidade demonstrada para iniciar a carga neste estado. Nenhum download de pesos ou instalação pesada foi iniciado.

Para fechar16: ambiente isolado com memória suficiente e runtime compatível; snapshot completo da revisão fixada; medir RAM/VRAM/latência numa frase curta portuguesa, confirmar fim não truncado e sample rate; comparar mesma frase neutra/expressiva por escuta; importar WAV separado no demo e validar export/sincronismo sem regressão; registrar comando/hash e só então publicar fechamento e iniciar17. Ambiente CPU maior ou máquina GPU adequada são alternativas; serviço externo não está autorizado automaticamente.

## Comandos preparados

Na raiz: `python scripts/qwen_voiceover.py estudo/qwen3-tts/request.example.json --preflight`. O exemplo aponta a pasta local esperada e falha honestamente até que exista. Com snapshot/runtime devidamente preparados: adicionar `--output demos/remotion-codex/public/qwen-narration.wav` sem --preflight. A saída deve ser nova e fica pendente de escuta. Não executar em ambiente insuficiente nem instalar pesos em diretórios do sistema.

Pesquisa não representa treinamento dos pesos do nosso agente. Nenhuma qualidade artística, expressividade, clonagem ou uso comercial completo foi certificada por testes de contrato.
'''
write(S/'README.md',readme)
status={'date':'2026-11-04','item':16,'state':'blocked_real_inference','study_source_revision':SHA,'model_revision':metadata['revision'],'implemented':['request validation','optional-runtime preflight','offline synthesis path prepared but not executed','PCM24 no-overwrite writer and provenance'],'tested':['9 local Python boundary tests','3 upstream wrapper control-flow probes with doubles'],'not_validated':['neural inference','Portuguese perceptual quality','expressiveness','model runtime install','real voice Remotion export','memory peak/GPU'],'environment_available_ram_gb':environment['available_gb'],'published_weights_bytes':sum(f['size'] or 0 for f in metadata['files'] if f['path'].endswith('.safetensors')),'next_item':17,'may_start_next':False,'reason':'Sequential completion requires actual inference and export; no synthetic or mock substitutes.'}
save(E/'status.json',status)
fila=R/'estudo/FILA.md';text=fila.read_text(encoding='utf8')
header='''## Novo lote — itens16–22, recebido em04/11/2026

Fila do pedido atual, preservada sequencialmente. Itens11–15 e anteriores continuam encerrados. Não abrir17 antes de fechar16 ou receber mudança explícita do usuário. Nenhum item deste novo lote é declarado concluído por apenas documentar uma API.

|Item|Fonte recebida|Estado atual|
|---|---|---|
|16|[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)|[Estudo/ponte parcial; síntese real bloqueada por ambiente](qwen3-tts/README.md)|
|17|[Audacity](https://github.com/audacity/audacity)|Aguardando16; não estudado neste lote|
|18|[Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit)|Aguardando sequência|
|19|[Auto-Editor](https://github.com/WyattBlue/auto-editor)|Aguardando sequência|
|20|[RIFE](https://github.com/hzwer/ECCV2022-RIFE)|Aguardando sequência|
|21|[VoiceStudio](https://github.com/debpalash/VoiceStudio)|Aguardando; rótulo enviado citaElevenLabs/OBS, endereço éVoiceStudio; capacidades ainda não verificadas|
|22|[FFmpeg](https://github.com/FFmpeg/FFmpeg)|Aguardando sequência|

Checkpoint16 é PARCIAL:9 testes da fronteira e3 sondas com doubles passaram; modelo não executado, expressividade/voz/export não validados. Resultado em [status](qwen3-tts/resultados/status.json). Pesos, runtime pesado e serviços externos não foram instalados/acionados. Os demais links foram apenas registrados, sem estudo paralelo. Próximo passo: viabilizar e validar inferência16, não iniciar17 silenciosamente.

'''
if '## Novo lote — itens16–22' not in text:write(fila,text.replace('\n\n','\n\n'+header,1))
for path,extra in [
 ('estudo/FONTES.md','\n## SRC-018 — Qwen3-TTS, item16\n\nFonte https://github.com/QwenLM/Qwen3-TTS, revisão022e286b98fbec7e1e916cb940cdf532cd9f488e, manifest0.1.1. Código e caminhos específicos inspecionados; nove testes próprios e três sondas do wrapper com doubles; inferência real bloqueada. [Estudo e evidências](qwen3-tts/README.md). Modelo/versão/licença registrados separadamente, sem baixar pesos. Itens17–22 recebidos na fila, ainda não consultados.\n'),
 ('estudo/INTEGRACOES.md','\n## Novo lote16–22: narração Qwen ainda parcial\n\n[Qwen3-TTS](qwen3-tts/README.md): contrato/preflight e escrita PCM24 testados; caminho de síntese offline preparado, ainda não executado. Não é ponte de locução validada no Remotion nem nova composição aprovada. Ambiente/pesos impedem o fechamento16; itens17–22 aguardam. Preservar distinção entre áudio original, TTS, limpeza e mix.0.6B não aceita controle expressivo por instruct na revisão consultada.\n'),
 ('estudo/PLANO.md','\n## Pedido16–22 em04/11/2026\n\nA fila foi ampliada.16Qwen tem estudo técnico e fronteira executável parcial; inferência real/export pendentes por ambiente. Não retomar11–15 nem abrir17 até fechar16 ou o usuário redefinir o escopo. [Estado atual](qwen3-tts/resultados/status.json).\n'),
 ('README.md','\n## Continuação16–22\n\nPedido recebido e registrado na [fila](estudo/FILA.md). O [item16Qwen3-TTS](estudo/qwen3-tts/README.md) tem estudo e fronteira parcial:9 testes Python próprios e3 sondas com doubles, sem inferência real. Não foram adicionadas composições nem alteradas as15 anteriores.17–22 aguardam fechamento16.\n'),
 ('CONTEXTO-PARA-OUTRO-GPT.md','\n## Atualização posterior — novo lote16–22\n\nO usuário enviou16Qwen3-TTS,17Audacity,18SubtitleEdit,19Auto-Editor,20RIFE,21VoiceStudio(link diverge do rótuloElevenLabs/OBS) e22FFmpeg. A [fila](estudo/FILA.md) agora registra esses itens.16 foi inspecionado em revisão fixa e recebeu contrato/preflight/escritaWAV preparados, com9 testes próprios e3 sondas do wrapper com doubles. Inferência real, áudio expressivo e export não ocorreram: runtime/pesos ausentes e poucaRAM disponível. Ver [status](estudo/qwen3-tts/resultados/status.json). NÃO interpretar como integração deTTS concluída.17–22 ainda não estudados; manter sequência. Os42 testes antigos permanecem resultados históricos, não reexecutados nesta rodada. Checkout localWindows preparado a partir do remoto, sem substituir Central anterior, sem instalação pesada ou envio de mídia do usuário.\n')]:
 p=R/path;t=p.read_text(encoding='utf8')
 if extra.strip() not in t:write(p,t.rstrip()+'\n'+extra)
print(json.dumps(status,ensure_ascii=False,indent=2))
