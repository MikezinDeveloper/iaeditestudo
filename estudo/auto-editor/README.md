#19 — Auto-Editor: análise, margens, EDL e montagem não destrutiva

Fonte https://github.com/WyattBlue/auto-editor, release31.8.0, revisão`654a5138cd50767a63a6644c89c667e75d894d88`, consulta04/11/2026. A leitura inicial deHEAD foi substituída pelo tag do binário testado; não misturar os novos formatos/ações deHEAD com a release. Licença da raizUnlicense; o README distingue artefatosbinários/dependências e aplicações online com condições próprias. O executável portátil oficial foi baixado fora do repositório e seuSHA está no ensaio; não foi redistribuído.

## Mecanismo seguido

O projeto atual éNim, não a antiga aplicaçãoPython que muitos tutoriais descrevem. O decoder/resampler organiza áudio em buckets do tempo de análise; readChunk calcula máximo absoluto normalizado, com variantesSIMD, e nãoLUFS ou reconhecimento de fala. A análise aplica limiar e expressões, smoothing modifica runs curtos e margin expande/contrai fronteiras. A decisão é primeiro uma máscara temporal e depois ações/timeline. Música, clique ou ruído alto podem ser mantidos; sussurro pode cair abaixo do limiar. Isso exige revisão semântica e escuta.

O exportv1 contémsource,timebase racional e chunks[start,end,speed];99999 marca corte. v3 representa pistas/efeitos/transições mais ricos. O código deexport avisa quev1/v2 não representam transições e podem descartá-las. Nossa ponte REJEITAv3, para não achatá-lo silenciosamente. Não usar v1 como formato universal de projeto.

## Ponte e experimento real

scripts/auto_editor_bridge.py importa o subconjunto linearv1, valida chunks inteiros contíguos, velocidades finitas/positivas e preserva duas escalas: tempo de fonte e de saída. Fractions evitam erro acumulado; pontos em trechos cortados retornamNone, e intervalos são half-open. Aceleração global1,2× é operação explícita; a opçãoalready_retimed rejeita aplicá-la outra vez. Música/motion criados no tempo final não entram nessa aceleração. A ponte não inventa sincronização de legenda atravessando corte.

Executado o binário31.8.0 noWAV sintético6s/48kHz: tons1–2s e3–4s, resto zero. Limiar0.05, margem0.1s e smoothing0. A EDL manteve[27,63] e[87,123] ticks a30Hz; duração2.4s. Em seguida, a mesmaEDL foi renderizada emcut.wav e ffprobe confirmou duração compatível. Original conservado porhash. [Ensaio nativo](resultados/native-experiment.json). Não houve cliente, voz real, ASR ou decisão política/editorial no fixture.

Oito testes da ponte verificam duração, pontos cortados, limites half-open,1.2× uma vez, versões inválidas e chunks/gains danificados. A suíte oficialNim e todos encoders não foram compilados/testados. O arquivoeditado é teste técnico; a qualidade de cortes na fala real e a retenção não foram medidas.

## Como aplicar sem repetir falhas

Usar análise para propor selects eEDL, não para autorizar corte final sem ouvir. Separar pausa expressiva, respiração, erro e silêncio técnico. Inspecionar ondas/caudas, contexto antes/depois e negações; preservar roomtone e evitar cliques. Recalcular âncoras visuais/legendas usando aEDL inteira; offset global é insuficiente quando há múltiplos cortes. O original de alta resolução deve continuar fonte do master; o preview automático não substitui esse master.

O CLI oferece dissolvências opcionais. Elas não são default da identidadeGiorgio e não foram usadas no ensaio. IntegraçõesPremiere/Resolve/etc são exportadores com capacidades/limites distintos, não garantia de roundtrip desses editores. Nosso demoRemotion não foi convertido para editor multifaixa nesta etapa.

Implementado e testado: EDLv1, mapa temporal exato e ensaio nativo de corte/render deWAV. Pendente: fala real revisada por escuta, aplicação visual noRemotion, legendas através de cortes, exportNLE e regressões de mídia real comVFR/clock diverso. Não afirmar um editor inteligente completo a partir dessa análise de amplitude.
