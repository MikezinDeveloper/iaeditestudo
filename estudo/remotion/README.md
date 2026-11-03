# Remotion — estudo de arquitetura e integração com Codex

## Proveniência

- Fonte: [remotion-dev/remotion](https://github.com/remotion-dev/remotion).
- Commit analisado: `fe9f0c372706f2039da6b2a0a92b92aa746e69cf`.
- Versão declarada em `packages/core/src/version.ts`: **4.0.540**.
- Consulta: 3 de novembro de 2026.
- Material recebido: `remotion-main.zip`. A ferramenta de transferência recusou o anexo por exceder 32 MiB. O usuário confirmou que se trata do Remotion oficial, sem alterações; a inspeção foi feita pela fonte pública. A revisão do ZIP não foi comparada com a revisão pública.
- Checkout de pesquisa: `/workspace/research-cache/remotion`, parcial, sem instalação do monorepo. Ele é cache de pesquisa e não faz parte do projeto do usuário.
- Dependências do experimento: pacotes publicados no npm, fixados em 4.0.540. Não foi compilado o checkout de origem; pacote publicado e commit não foram comparados byte a byte.

## Roteiro de leitura

1. [Arquitetura e fluxo completo](ARQUITETURA.md)
2. [Tempo, mídia, áudio e motion](TEMPO-MIDIA-MOTION.md)
3. [Integração com Codex](INTEGRACAO-CODEX.md)
4. [Licença e limites de reutilização](LICENCA-E-LIMITES.md)
5. [Experimento executável](../../demos/remotion-codex/README.md)
6. [Resultados e falhas investigadas](EXPERIMENTO.md)

O inventário [evidencias.json](evidencias.json) registra 53 arquivos consultados integral ou parcialmente, seus hashes e suas URLs na revisão analisada. Ele não representa cobertura integral do monorepo.

## Conclusão de arquitetura

O caminho mais direto para este estudo é usar o Remotion como motor de composição e exportação e o Codex como agente de desenvolvimento/operação do projeto. Há integração oficial para Codex documentada nesta revisão. Entender o código permite construir a camada de edição, validação e conhecimento de que precisamos sem reimplementar o renderizador.

Essa conclusão não significa que uma IA de edição completa já exista: interpretação de pedidos dentro do produto, modelo próprio de projeto, histórico, análise de conteúdo e interface do usuário continuam sendo trabalho de produto.

## Cobertura desta etapa

Inspecionados: registro de composições; relógio de frames; sequências; interpolação e springs; caminho legado de vídeo off-thread e áudio HTML5; seleção de composição; captura e coleta de assets; orquestração de render; plugin e skills para agentes; documentação de timing, SSR, interatividade e WebMCP.

Não auditados integralmente: compositor nativo, pipeline de cor/HDR, novos componentes de `@remotion/media`, WebCodecs, processamento com GPU, backend de nuvem, transcrição, captions e todos os testes oficiais. Esses componentes aparecem no mapa como próximos aprofundamentos, não como capacidades validadas.
