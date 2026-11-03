# Estudo para uma IA de edição de vídeo, áudio e motion

Base de pesquisa para projetar e construir uma IA de edição com apoio do Codex. O objetivo é transformar repositórios, documentação e experimentos em decisões de engenharia aplicáveis ao produto.

**Escopo confirmado:** vídeo, áudio e motion graphics. O primeiro repositório estudado é o Remotion. Este checkout contém a base de pesquisa e um protótipo audiovisual; ainda não contém uma IA de edição completa.

## Por onde começar

- [Fila sequencial dos oito repositórios](estudo/FILA.md)
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

- Estrutura de pesquisa criada em 3 de novembro de 2026.
- Primeira leitura documental do repositório oficial do Codex registrada com revisão fixa.
- [Primeiro material enviado pelo usuário](estudo/analises/SRC-002-material-chesny.md) registrado; leitura bloqueada pelo acesso de rede ao X.
- Remotion 4.0.540 analisado em revisão fixa; 53 arquivos de origem registrados com hashes, sem alegação de auditoria integral.
- Demo com vídeo, áudio, motion e exportação executado; seis testes do contrato, checagem de tipos, inspeção audiovisual e smoke do Studio aprovados.
- Sem benchmark de produção, interpretação de linguagem natural implementada ou escolha final da arquitetura do produto.
- Anime.js 4.5.0 estudado com 38 arquivos inventariados; nova composição de motion exportada. O projeto agora tem 14 testes aprovados. A suíte Node upstream teve 10 aprovações e 2 falhas, registradas separadamente.

O demo tem dependências travadas e comandos documentados. A receita [scripts/setup-remotion.sh](scripts/setup-remotion.sh) foi executada com instalação pelo lockfile. Consulte os [resultados e limites](estudo/remotion/EXPERIMENTO.md) antes de generalizar o experimento.

Os arquivos estão no checkout local. Commits e envio ao GitHub ainda não foram feitos.
