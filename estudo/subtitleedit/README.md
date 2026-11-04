#18 — Subtitle Edit: texto, tempo e intercâmbio verificável

Fonte https://github.com/SubtitleEdit/subtitleedit, revisão`99b87e4f14d59294d579ed18b48382644a157fe3`, consulta04/11/2026. Licença raizMIT. O README desta revisão descreve a geração5.x multiplataforma e builds self-contained; não presumir a antiga arquiteturaWinForms4.x ou que o runtime.NET7 disponível compila.NET10. Não haviaSDK.NET no ambiente e o aplicativo não foi executado.

## Mecanismo reconstruído

SubRip.cs lê linhas de timecode e acumula texto entre elas, tolerando números/linhas em branco ausentes e várias formas danificadas de seta/separador. O writer emite start/end e texto porParagraph. Paragraph eTimeCode mantêm o tempo; TotalMilliseconds é unidade-base, não frame do vídeo. A conversão HHMMSSFF consultaFPS/configuração específica. WebVTT tem gramática, cue settings, estilos/classes e timestamps próprios. Não basta trocar vírgulas por pontos e chamar a conversão universal.

Isso orientou uma fronteira menor e estrita: nosso parser aceita apenasSRT canônico. Arquivos danificados devem ser reparados noSubtitleEdit, não corrigidos por heurísticas silenciosas da IA. IDs, acentos, negações e quebras de linha são conservados. Intervalos inválidos/zero ou IDs duplicados são rejeitados; sobreposições são aviso, pois podem representar falas simultâneas legítimas.

## Implementação e testes

scripts/subtitle_bridge.py importa/exporta o subconjuntoSRT e produz cuesJSON com temposms e frames half-open. Início éfloor e fim éceil em FPS racional, incluindo30000/1001; arredondamento externo pode gerar um frame de contato entre cues e deve ser revisado visualmente. Escolher outroFPS para render NÃO altera os timestampsms originais. Retime só ocorre por operação explícita, por exemplo após acelerar a fala1,2×, com validação de offsets; a função não sabe se a aceleração já foi aplicada e não deve ser chamada duas vezes.

Dez testes próprios passaram: roundtripUnicode/multilinha/BOM/CRLF, dados inválidos, IDs, sobreposição, frames racionais, retime não destrutivo e offset negativo rejeitado. Esses testes não executam o parserC# original nem certificam o aplicativo. Nenhum código de parser foi copiado do upstream. A ponte é deliberadamente menos permissiva que oSubtitleEdit e não implementaASS, tagsVTT, karaoke ou legendas por palavra.

## Integração operacional

Fluxo: áudio/transcrição revisada → SRT canônico → revisão noSubtitleEdit quando necessário → JSON de cues → composiçãoRemotion. Não há ainda componente de burn-in ou integração visual ao demo original; nenhuma das15composições anteriores foi reescrita. TextoJSON é dado, nunca HTML executado. ASR, OCR, tradução e serviçosTTS opcionais são recursos distintos; não foram ativados ou considerados capacidades já conectadas.

SRT pode atravessar cortes; nesse caso é necessário mapear pelaEDL e revisar texto/fragmentação. Não duplicar a frase inteira em cada pedaço nem deslocar tudo por umoffset fixo depois de múltiplos cortes. A relação entre legenda, fala e câmera deve usar o tempo final. Escuta, leitura mobile, quebras semânticas e conflitos com motion permanecem revisão humana.

## Próximo ensaio delimitado

Abrir umSRT exportado pelo aplicativo real, fazer uma correção pequena e confirmar roundtrip; renderizar cues no vídeo com áudio revisado; inspecionar entrada/saída/intermediários e frases cortadas. Native app, OCR, alinhamento palavra-a-palavra, estilos e export combinado ainda não validados. Estudo encerrado neste escopo com código/evidência, mantendo essas pendências visíveis para a próxima solicitação.
