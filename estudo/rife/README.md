#20 — RIFE: fluxo intermediário, oclusão e relógio de entrega

Fonte https://github.com/hzwer/ECCV2022-RIFE, revisão`5d8adbdd40e12c2c8f91930eff838aebe561c086`, consulta04/11/2026. Licença raizMIT/Megvii. Código foi executado do checkout de pesquisa, sem vendorizá-lo. Pesos pré-treinados não estão noGit; o README distingue checkpointHD do modelo do paper e referencia variantes mais novas em outro repositório. Nenhum deles foi presumido instalado, intercambiável ou validado. Não substituí a fonte enviada porPractical-RIFE.

## Mecanismo reconstruído

IFBlocks recebem frames e estimativas progressivas, produzem incrementos de fluxo/máscara em escalas sucessivas. warplayer usa grid_sample bilinear, grid normalizado, align_corners=True e paddingborder. Os dois frames são warpados, combinados pela máscara, passam por contexto/refinement e residual limitado ao intervalo0–1. Isso é reconstrução de imagem, não recuperação garantida de movimento real ou detalhe perdido.

IFNet recebe timestep na assinatura, mas o corpo desta revisão não o usa. IFNet_m cria um mapa temporal e o incorpora aos blocos. O ensaio executou ambas comt=.25/.75: basic produziu diferença0; variante_m produziu diferença nãozero. Portanto não anunciar arbitrariedade só porque existe parâmetro público. model.RIFE.Model escolhe a variante conforme arbitrary.

Outro limite observável: inference altera a lista scale_list fornecida pelo chamador. Usar uma lista nova por amostra evita escala acumulada. O loader converte nomesDDP e filtra apenas chaves com module.; não presumir que aceita qualquer state_dict. A migração paraTorch atual exige validar checkpoint/weights_only e compatibilidade sem executar pickle arbitrário. Não carregamoscheckpoint neste estudo.

## Execução realmente realizada

PyTorch2.9.1CPU já existente no ambiente isolado foi reutilizado, sem instalar outro runtime. Warping de fluxo zero preservou tensor64×64 dentro de7.1e-6. As duas redes executaram, retornando tensores[1,3,64,64] finitos. Os pesos eram aleatórios; o relatório [architecture-only](resultados/architecture-only.json) declara explicitamente que NÃO é teste de qualidade ou benchmark de modelo treinado. Não exibir essas imagens como demo de interpolação. CUDA, desempenhoHD/4K, checkpoints e benchmarks do paper não foram executados.

Sete testes próprios da ponte cobrem relógio, contagem, preservação de frames, cuts e áudio. scripts/rife_bridge.py agenda candidatos sem fazer passar duplicação por inferência: 2× no mesmo tempo produzN×2frames aFPS×2; o último intervalo éhold do último frame, explicitamente. Em slow motion,FPS se mantém e duração cresce; a política exige esticar/mutar áudio por escolha explícita. Não remover áudio silenciosamente nem tratar frames mais numerosos como aumento de nitidez.

## Aplicação e preservação

Não interpolar através de corte, mudança de take, máscara mal recortada ou texto que muda semanticamente. A ponte usa fronteiras de shot fornecidas; não há detector automático de cena aprovado. Objetos que se revelam, mãos, cabelos, linhas, legendas e letras podem gerar deformações/duplicações; conferir frames intermediários reais. Não aplicarRIFE a toda fala para mascarar easing ruim. Motion criado em código pode ser renderizado noFPS final diretamente, preservando geometria e custo de cor.

Os scripts do upstream usam frames normalizados e fluxo8bit/BGR de ferramentas de vídeo; não foram certificados paraHDR/10bit ou sinal linear. Nosso master precisa preservar entrada/saída de cor e converter conscientemente. Shells de transferência de áudio e diretórios temporários do CLI original não foram incorporados: a integração futura deve usar argumentos estruturados, saídas novas e política de áudio declarada.

Implementado: agendamento temporal/cuts/áudio e ensaio de arquitetura real. Pendente: selecionar e verificar um checkpoint pré-treinado da arquitetura correta, loader seguro, par de frames real comgroundtruth/oclusão, corHDR, vídeo com áudio e avaliação perceptiva. Estudo delimitado registrado; não declarar slow motion de qualidade entregue.
