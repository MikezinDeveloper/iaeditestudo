#22 — FFmpeg: encadeamento, cor, áudio, relógios e entrega

Fonte oficial https://github.com/FFmpeg/FFmpeg, tagn9.0.2, revisão`946fcce07b6dcd0331c8cc609192aeff5e1924f8`, consulta04/11/2026. A fonte foi alinhada ao release do executável9.0.2-essentials_build-www.gyan.dev; isso não comprova igualdade binária a um build nosso. Não compilamos oFFmpeg nem executamos a suíteFATE. Hash e configuração do binário real estão no ensaio.

Licença: raiz descreveLGPL2.1+ e componentes opcionaisGPL. O binário usado anunciaenable-gpl/enable-version3/libx264/etc; não tratá-lo como buildLGPLmínimo. Ele permanece ferramenta externa existente, não redistribuída neste projeto. Conferir condições específicas se houver distribuição do produto.

## Caminho seguido na fonte

fftools orquestra demux/decodificação, grafos de filtros, encode e mux. libavformat trata containers/streams, libavcodec codecs, libavfilter filtros, swresample áudio e swscale/zimg transformações apropriadas. Stream-copy não aplica filtro nem cria cortes arbitrários sem considerar keyframes/timestamps. Renderizações intermediárias devem preservar fonte/matriz de projeto e evitar gerações sucessivas com perdas.

time_base do encoder e do mux não sãoFPS nem relógio universal do áudio. A opçãoenc_time_base é perstream; nesta ponte fica restrita a:v. AAC pode ter primeiroDTS negativo por priming; o teste exige crescimento dosDTS, não que todos sejam não negativos. PTS de pacotes de vídeo comBframes podem vir em ordem de decode; conferir frames decodificados eDTS adequadamente.

af_loudnorm mantém medições de entrada e parâmetros de destino distintos, com caminhos linear/dinâmico. Não anunciar dois passes apenas por usar o filtro uma vez. Nosso ensaio mede input_i/truepeak/etc num sinknull, sem aplicar normalização ao arquivo entregue. O alvo usado na sonda é dofixture, não diretriz universal de fala ou música. Medição não substitui escuta ou mix comducking.

zscale e tonemap distinguem matriz/primárias/transferência/faixa. Tags não convertem pixels. HDR/HLG/PQ exigem caminho explícito e validado, não rótulo709. A ponte atual REJEITA fonte que não esteja declaradamenteSDR709; o tratamentoHDR permanece no sistema anterior e não foi reimplementado neste estudo.

## Ponte e ensaio real

scripts/ffmpeg_delivery.py constrói argumentos como lista, protege original/saída existente, preserva dimensões pares semresize implícito e preparaMP4/H264yuv420p/AAC48k/faststart a partir de masterSDR. CRF é parâmetro explícito, não promessa de nitidez máxima. Matchingavg/rFPS é apenas pré-verificação; fonteVFR precisa avaliação real dePTS antes deste caminhoCFR delimitado.

Ensaio real: master sintético6s/320×180/30fps, H264lossless10bit444 ePCM24, convertido uma vez para deliveryH264/AAC. Testsrc foi promovido de8para10bits para exercitar o caminho; isso NÃO demonstra detalhe de câmera10bits. O master permaneceu byte-idêntico. Saída180frames/6s, tags709, decodificação integralexit0, intervalos dePTS conferidos eDTS estritamente crescentes por stream. loudness input_i da saída=-21.75LUFS para o tom sintético, sem conclusão sobre timbre de voz. [Relatório](resultados/native-delivery.json).

Dois fixtures iniciais (FFV1 eH264) tinham matriz709 mas sem primárias/transferência esperadas no probe, apesar das opções de saída. O guard bloqueou, e NÃO foi enfraquecido. Propriedades explícitas de frame via setparams resolveram o fixtureSDR conhecido; [falhas preservadas](resultados/metadata-failures.json). Não generalizar como bug universal de codec nem usarsetparams como tonemap de imagem desconhecida. Essa distinção evita apagarHLG por rotulagem.

Sete testes próprios cobrem timebase porstream, paths, não sobrescrita, dimensão, clock e recusaHDR/unknown. A qualidade artística, retenção, perfilHDR e reprodução física mobile não foram certificados. AAC é com perdas: hash de áudioAAC não deve ser comparado como se fossePCM original lossless. Guardar stems originais e distinguir transformação deliberada de regressão.

## Aplicação ao editor

Demux/probe → projeto/EDL/áudio/motion → intermediários de qualidade → master → entrega → decode/metadata/timestamps/loudness → revisão humana. Usar mapas explícitos de streams; cortar voz, música eSFX conforme seu papel e tempo final. Não acelerar tudo novamente para1.2× no export. Container correto ouMain10 não cria precisão ou foco inexistentes.

Implementado e testado: presetSDR delimitado e export/QA real de fixture. Pendente:VFR,HDR e áudio multifaixa real, renderRemotion completo com novas pontes, teste de celular e avaliação visual/sonora contínua. Foco da rodada é estudo operacional incremental; o produto deIA e a direção de arte ainda têm trabalhos próprios.
