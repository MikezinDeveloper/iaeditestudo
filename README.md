# Estudo para uma IA de edição de vídeo, áudio e motion

Base de pesquisa para projetar e construir uma IA de edição com apoio do Codex. O objetivo é transformar repositórios, documentação e experimentos em decisões de engenharia aplicáveis ao produto.

**Escopo confirmado:** vídeo, áudio e motion graphics. O primeiro repositório estudado é o Remotion. Este checkout contém a base de pesquisa e um protótipo audiovisual; ainda não contém uma IA de edição completa.

## Por onde começar

- [Transferir o contexto para outro GPT](CONTEXTO-PARA-OUTRO-GPT.md)

- [Fila sequencial e checkpoints no GitHub](estudo/FILA.md)
- [Capacidades integradas e escolha das pontes](estudo/INTEGRACOES.md)
- [Operar o ambiente no Codex](estudo/AMBIENTE.md)
- [Escopo e critérios de sucesso](estudo/ESCOPO.md)
- [Mapa técnico e perguntas de pesquisa](estudo/MAPA-TECNICO.md)
- [Método de análise e engenharia reversa](estudo/METODO.md)
- [Fontes e estado das análises](estudo/FONTES.md)
- [Plano de trabalho](estudo/PLANO.md)
- [Modelos de análise, experimento e decisão](estudo/MODELOS.md)
- [Estudo aprofundado do Remotion](estudo/remotion/README.md)
- [Demo de Remotion operável pelo Codex](demos/remotion-codex/README.md)
- [Estudo e integração do Anime.js](estudo/animejs/README.md)

## Como o conhecimento será aplicado

`Fonte → evidência → explicação do mecanismo → hipótese de adaptação → experimento → decisão → implementação`

Cada análise deve explicar **o que acontece, como acontece e por que interessa ao editor**. Popularidade de um projeto e quantidade de links não substituem evidência técnica.

O Codex poderá consultar estes arquivos em tarefas futuras. Esta base fornece contexto de projeto; armazenar documentos aqui não treina nem altera os pesos de um modelo. Uma busca semântica ou outro mecanismo de recuperação poderá ser avaliado quando o volume justificar.

## Estado atual

A base de Remotion e Anime.js foi ampliada, na ordem solicitada, com mo.js, Theatre.js, Two.js, D3, Three.js, Babylon.js, Drei, Spark e os itens 11–15: Cables, Taichi, SPlisHSPlasH, Custom Shader Material e OpenToonz/OCA. Cada estudo possui revisão fixa, explicação dos mecanismos, licença, ponte executável, validações e limites. A [fila](estudo/FILA.md) registra os checkpoints de publicação.

- Quinze composições: edição audiovisual base, Anime.js e treze estudos registrados.
- Instalação pelo lockfile, geração de assets, checagem de tipos e **42 testes locais** aprovados.
- [Fechamento verificável dos itens 11–15](estudo/resultados/lote-11-15-final.json).
- Exports por estudo com H.264/AAC, inspeção de movimento, repetição de frame e regressões; relatórios em cada estudo.
- Testes upstream, falhas observadas e suites não executadas são registrados separadamente; não há alegação de auditoria integral.
- O lote 11–15 acrescenta grafo numérico real, tecido Taichi, fluido DFSPH C++ nativo, shader iluminado e exposição OCA/PNG. O estudo OpenToonz usa fixture próprio; aplicativo/roundtrip nativo permanecem não validados.
- O material do X permanece [pendente de conteúdo acessível](estudo/analises/SRC-002-material-chesny.md).

O protótipo ainda não tem planejador por linguagem natural, histórico de edição completo, timeline multifaixa geral ou benchmark de produção. O [catálogo de integrações](estudo/INTEGRACOES.md) explica como o estudo prepara essas próximas capacidades.

A receita [scripts/setup-remotion.sh](scripts/setup-remotion.sh) instala e verifica o projeto. Os clones de pesquisa não são necessários para executar o demo. Leia [o guia do demo](demos/remotion-codex/README.md) para preview e export.

O código e os checkpoints são publicados em [MikezinDeveloper/iaeditestudo](https://github.com/MikezinDeveloper/iaeditestudo), branch `main`. O workflow GitHub Actions está versionado; sua execução remota não foi confirmada nesta sessão.

## Continuação16–22

Pedido recebido e registrado na [fila](estudo/FILA.md). O [item16Qwen3-TTS](estudo/qwen3-tts/README.md) tem estudo e fronteira parcial:9 testes Python próprios e3 sondas com doubles, sem inferência real. Não foram adicionadas composições nem alteradas as15 anteriores.17–22 aguardam fechamento16.

## Estudos17–22 preparados localmente

[Relatório e estados reais](estudo/RELATORIO-LOTE-17-22.md).49testes Python novos passaram; dois ensaios nativos deAuto-Editor/FFmpeg e sondasRIFE/VoiceStudio têm escopos explicitados. Publicação aguarda aprovação;42testes/15composições anteriores preservados. Qwen suspenso pelo usuário.


## Autorização posterior de publicação —04/11/2026

O usuário respondeu **“autorizo”** à criação do commit e publicação deste conjunto17–22 na main. O bloqueio/aguardo descrito acima é histórico e foi superado para este escopo. Registro canônico: `estudo/resultados/lote-17-22-publication-authorization.json` (relativo à raiz). Conferir o commit no históricoGit para confirmação de publicação; aprovação de CI e julgamento artístico continuam separados. Não retomar o testeQwen.
