# Teste suspenso por solicitação do usuário

04/11/2026. O usuário pediu deixar o teste de voz de lado e estudar17–22 em sequência. Nenhuma inferência adicional foi iniciada após essa instrução; os processos específicos foram verificados e nenhum permaneceu ativo.

O ambiente isolado e os pesos já baixados foram preservados, fora do Git. RuntimePyTorchCPU2.9.1 eQwen-TTS0.1.1 instalado. O download verificou tamanhos e hashesLFS. A primeira tentativa foi encerrada por memória baixa; tentativas de offload tiveram erros meta registrados. Existe umWAV da última tentativa, concluído antes da verificação de encerramento, mas não foi ouvido ou analisado e não certifica expressividade. Manter esse arquivo como artefato não revisado. Não continuar o teste sem novo pedido.

Os helpers de offload são experimentais e não são padrão de produção. A amostragem de memória da primeira tentativa mediu o launcherWindows, não o worker real; guard posterior passou a acompanhar descendentes. Não tratar aquele número como pico real do modelo.

O bloqueio anterior da fila foi explicitamente dispensado para continuar os demais estudos. Síntese expressiva e export integrado do16 continuam pendentes.
