> Atualização posterior: teste suspenso por pedido do usuário; ver [registro](RETOMADA-CANCELADA.md). O estado de ambiente descrito abaixo é histórico.17–22 foram liberados para estudo sequencial.

#16 — Qwen3-TTS: estudo técnico e fronteira de narração

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
