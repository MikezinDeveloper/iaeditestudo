#17 — Audacity: cleanup, dinâmica, mix e fronteira de automação

Fonte https://github.com/audacity/audacity, revisão`3afc48a26d37cefad5772ee6c4c5fb88c9e402b3`, consulta04/11/2026. Licença raizGPLv3, arquivos individuaisGPLv2-or-later e exceções; documentaçãoCC-BY3.0. CódigoDSP não foi copiado. Fronteira escolhida: aplicação externa e artefatosWAV, sem linkar motorGPL aoRemotion. Isso é decisão técnica, não parecer jurídico sobre distribuição.

## Mecanismos e mudança de versão

O master consultado preparaAudacity4, coexistindo com au3. A release consultada é4.0.2; não confundir fonte master com binário da release. PipeServer.cpp eScripterCallback.cpp estão na árvoreau3. Presença nessa árvore não prova que um instalador4.0.2 exponha a mesma automação. O checkout foi seletivo, não auditamos todo editor.

O script server recebe comandosUTF-8 por IPC local e repassa aoScriptCommandRelay. Windows usa dois named pipes ToSrvPipe/FromSrvPipe; o exemplo oficial termina pedidos comCRLF+NUL, POSIX usaFIFOs porUID eLF. Pedidos precisam ser serializados; respostas podem vir em fragmentos. O cliente deve respeitar timeout, status de conclusão e falha, não assumir que escrever no pipe produziu efeito. O transporte nativo não foi conectado nesta sessão.

Import2 recebeFilename. Export2 usa extensão para selecionar exportador, NumChannels, seleção temporal e sample rate do projeto; parâmetros do encoder vêm das preferências nativas. Portanto exportarWAV não garante automaticamentePCM24 nem sample rate de entrega. Conferir arquivo porffprobe e manter saída nova. A ponte não altera preferências nem projeto aberto do usuário.

A UI deNoiseReduction possui duas etapas: capturar perfil e reduzir/isolar/resíduo. Um perfil deve vir de ruído representativo; capturar fala como perfil ou reduzir agressivamente pode remover informação vocal. Não foi feita inferência de parâmetros universais nem cleanup nativo. A UI deLoudness distingueLUFS; normalizar pico não é normalizar loudness. CompressorProcessor mostra threshold, knee, ratio, make-up, attack/release em segundos e look-ahead com reinit quando atraso muda. Compressão muda dinâmica e pode exigir compensar latência; não é removedor de ruído.

## Ponte implementada e validação

scripts/audacity_bridge.py prepara framing, rejeita delimitadores/injeção e pedidos acima do buffer inspecionado, exige catálogo de comandos/parâmetros informado pelo aplicativo e conserva original/saída nova. O plano mínimo deNormalize é só proposta condicionada ao catálogo: não foi aplicado. Rejeita respostas sem confirmação terminal de sucesso. A consulta de presença dos pipes retornou indisponível. O parser do contrato foi validado com fixtures, não resposta de umAudacity real.

Nove testes próprios verificam contrato, ausência de processamento implícito, preservação, parâmetros nativos, tamanhoUTF-8, respostas falhas, ganho não finito e caminhos. Não háAudacity instalado no caminho/CLI consultados. Não instalamos outro editor nem habilitamos módulo na máquina do usuário. Subconjuntos oficiais upstream não foram compilados ou executados.

## Aplicação ao produto e próxima prova

Usar Audacity quando for necessária revisão humana multifaixa, plugins ou ajustes editoriais de áudio. Para trabalho em lote reprodutível, a ponte deve primeiro descobrir versão/comandos, abrir sessão dedicada e confirmar export por medições e escuta. Voz gravada é preservada; música/SFX ficam separados. Nenhuma paleta visual ou valor deEQ/ruído é universal.

Implementado: fronteira de protocolo e plano condicionado. Pendente: transporte real com timeout, compatibilidade por versão, sessão dedicada, denoise em duas etapas, compressor/mix nativos, comparação de waveforms/loudness e escuta. Não anunciar cleanup entregue a partir destes testes. A pedido do usuário, o estudo seguinte começa após este registro delimitado, sem ocultar essas pendências.
