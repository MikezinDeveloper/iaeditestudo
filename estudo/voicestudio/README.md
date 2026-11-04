#21 — VoiceStudio: aplicação de voz, engines e APIs

Fonte recebida https://github.com/debpalash/VoiceStudio, revisão`7a896ed455e116d734f26437393a92cad090aadb`, consulta04/11/2026. O rótulo original mencionaElevenLabs/32idiomas e o texto visívelOBS, mas o endereço éVoiceStudio. O estudo usa esse endereço, sem trocar de repositório silenciosamente. Não é o código do serviçoElevenLabs nem doOBS.

Licença da aplicaçãoAGPL-3.0-only conformeLICENSE/NOTICE. Modelos, tokenizers e assets têm termos separados; a licença do aplicativo não certifica pesos ou direito comercial de todo modelo. O NOTICE distingue o pacoteOmniVoice e pesos/defaults com outras condições. Registramos as declarações, sem dar liberação comercial ou copiar o servidor para nosso produto.

## Arquitetura e seleção

O README apresenta frontend/Electron, backendFastAPI, gerência de modelos, engines/subprocessos, narração e dublagem. Isso é escopo da aplicação externa, não capacidade já incorporada aoiaeditestudo. Opyproject0.5.7 exigeTransformers>=5.10, incompatível com oQwen estudado que fixa4.57.3. Não instalar tudo no mesmo ambiente nem atualizar as dependências do nosso demo por arrasto.

O caminho/api/routers/openai_compat.py oferece POST/v1/audio/speech: resolve engine, valida disponibilidade/licença, verificaffmpeg quando há formato comprimido e propaga voz/linguagem/instrução conformeengine. Não é endpoint daOpenAI: compatibilidade de contrato não identifica fornecedor. A conversão de formato deve falhar quando indisponível, não devolver bytes de outro container com extensão falsa. A aplicação tem tarefas, cancelamento, aquecimento de modelos e rotas; não auditamos integralmente as milhares de linhas nem todas as engines.

## ElevenLabs: o que o exemplo realmente faz

plugin_sdk.py registra umElevenLabsPlugin com requires_api_key=True/is_local=False. is_available exigeELEVENLABS_API_KEY e pacoteelevenlabs. generate pede eleven_multilingual_v2 e mp3_44100_128, encaminhando texto evoice_id. Embora receba language e speed na assinatura, nesta revisão NÃO os repassa aoSDK. Ohint de idiomas é metadado da UI, não consulta ao provedor nem prova de32idiomas. Não atribuir controle de velocidade só pela assinatura.

A sonda executou somente esse método extraído porAST comSDK/chave fictícios e sem rede, confirmando campos e omissões; isso é [controle de fluxo](resultados/plugin-control-flow.json), não geração de áudio. Nenhuma credencial real foi lida, nenhum serviço foi contratado e nenhum pacote/servidorVoiceStudio foi instalado. A capacidadeElevenLabs do nosso projeto continua não conectada.

## Ponte local preparada

scripts/voicestudio_bridge.py constrói um pedido inspecionável ao servidorloopback explicitamente escolhido. Exigeengine, texto/voz, velocidade finita e formatoWAV; denoise/preprocess ficamFalse. Não enviaHTTP e não presume que engine local significa cálculo local: engine pode chamar nuvem, e autorização/custo precisariam estar claros na execução futura.

O validador de resposta verificaRIFF/WAVE e dadosPCM medidos, rejeitandoMP3,JSON/HTML, arquivo vazio ou truncado em vez de renomear bytes. O subconjuntoPCM é intencional: outrosWAV válidos exigem decoder explícito. Oito testes passaram. Não há previsão de duração por número de caracteres; medir o áudio devolvido e manter metadados da engine/voz/modelo.

## Conhecimento reutilizável

Separar contrato de pedido, readiness, geração, resultado e revisão. Umworker não deve carregar todos modelos ou fazer fallbackCPU silencioso. A contenção deSystemExit observada em utils/containment.py ilustra uma fronteira útil para bibliotecas que tentam instalar componentes; não importamos esse códigoAGPL nem seus executores. Planejamento de recursos/cancelamento deve acompanhar cada job e conservar logs, falhas e origem do áudio.

Implementado: planner deAPI local e verificaçãoPCM, testes e sonda do exemploElevenLabs. Pendente: servidor real autenticado, versão/engine/modelo escolhidos, job/cancel real, custos/provedor, áudio, dublagem e avaliação perceptiva. Como o usuário suspendeu o teste de voz, nenhum novo ensaio de síntese foi iniciado aqui. Não considerar oVoiceStudio um editor audiovisual completo já integrado nem substituir nossaCentral.
