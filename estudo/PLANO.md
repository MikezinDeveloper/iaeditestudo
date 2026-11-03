# Plano de trabalho

## Lote atual: oito repositórios em sequência

A ordem, os critérios de conclusão e o checkpoint estão em [FILA.md](FILA.md). O usuário autorizou commits e envio a `MikezinDeveloper/iaeditestudo`. O primeiro item é mo.js; só depois de sua conclusão e publicação começa Theatre.js.

## Etapa atual: Anime.js integrado à base de Remotion

- [x] Registrar SRC-004 em revisão fixa e estudar o motor, targets, timelines, easings, stagger e contratos temporais.
- [x] Investigar a divergência manifest/lockfile do upstream sem alterar arquivos rastreados.
- [x] Executar a suíte Node oficial: 10 aprovações e 2 falhas de expectativa sobre otimização do V8.
- [x] Implementar ponte numérica dirigida pelo frame, com Anime.js 4.5.0 fixado.
- [x] Reproduzir o caso de seek incorreto em uma timeline reutilizada e corrigir a nossa integração com avaliação nova por amostra.
- [x] Aprovar 14 testes do projeto, incluindo 120 frames fora de ordem.
- [x] Exportar a composição AnimeMotionStudy e verificar repetição de frame, região animada, streams e duração.
- [x] Comparar o frame de referência da composição original e preservar seu resultado.
- [x] Registrar a decisão, os limites, a revisão e os relatórios.

## Etapa anterior: Remotion e integração com Codex

- [x] Confirmar o domínio: vídeo, áudio e motion.
- [x] Criar escopo, método, mapa técnico e modelos de registro.
- [x] Registrar uma primeira leitura documental do Codex com revisão fixa.
- [x] Registrar o post de @chesny indicado pelo usuário como SRC-002.
- [ ] Obter o texto e eventuais mídias do post: acesso HTTPS recusado pela política de rede do ambiente.
- [ ] Extrair os conceitos e explicações do material, com referência ao trecho ou tempo de vídeo.
- [ ] Relacionar a teoria com vídeo, áudio e motion; distinguir conteúdo da fonte de propostas de aplicação.
- [x] Receber Remotion como primeira referência de repositório e confirmar a origem oficial com o usuário.
- [x] Fixar revisão e registrar a limitação de acesso ao ZIP.
- [x] Inspecionar composição, tempo, mídia, áudio, motion, SSR, plugin e skills de Codex.
- [x] Registrar arquitetura, contratos, licença e limites.
- [x] Criar protótipo com pacotes publicados, sem alterar o motor.
- [x] Reinstalar pelo lockfile; aprovar TypeScript e seis testes individuais.
- [x] Exportar e verificar MP4, recortes, áudio e repetição de frame.
- [x] Abrir Studio em Chromium e verificar montagem e recorte do primeiro clipe.
- [x] Preservar análises, inventário de fontes e relatórios do experimento.

O pedido mais recente adiciona Anime.js (SRC-004) à base de Remotion (SRC-003). O post SRC-002 continua pendente de conteúdo acessível; nenhuma tese lhe foi atribuída.

## Próxima etapa: ampliar os mecanismos do editor

1. Modelar operações de edição e histórico sobre um estado explícito de projeto.
2. Testar transições, múltiplas faixas de áudio e um evento audiovisual sincronizado.
3. Estudar `@remotion/media`, captions e uso de assets reais com taxas distintas.
4. Validar edição independente no Studio e controle por WebMCP no cliente compatível.
5. Definir como o pedido em linguagem natural vira um plano validado e revisável.

O próximo aprofundamento deverá acompanhar uma capacidade concreta do produto; não é necessário implementar todos esses itens de uma vez.

## Receber e mapear novas referências

1. Identificar finalidade, licença, versão e componentes de cada repositório.
2. Separar motores de mídia, editores completos, motion/composição, ferramentas de IA e integrações.
3. Selecionar o que merece aprofundamento com base na capacidade que queremos construir.
4. Publicar uma comparação inicial com evidências, lacunas e ordem sugerida de investigação.

Não é necessário receber todos os links de uma vez. O estudo pode avançar por lotes.

## Aprofundamento: mecanismos antes de escolhas

1. Entender o modelo de tempo, projeto e operações.
2. Traçar uma edição real do comando até o render.
3. Analisar áudio e motion no mesmo fluxo.
4. Investigar preview, exportação, histórico e tratamento de falhas.
5. Comparar maneiras de conectar essas operações à IA e ao Codex.

## Experimentos e síntese

- Definir um cenário pequeno que exercite vídeo, áudio e motion.
- Instalar apenas os componentes necessários para o experimento selecionado.
- Executar exemplos e verificações significativas; registrar falhas e resultados.
- Produzir propostas de arquitetura e decisões com alternativas explícitas.
- Transformar as decisões aceitas em tarefas de implementação e critérios de conclusão.

## Entregáveis esperados

Catálogo rastreável de fontes; análises dos mecanismos relevantes; comparação de alternativas; experimentos reproduzíveis; proposta de arquitetura; backlog de implementação; instruções de contexto para o Codex.

## Limite do que já foi realizado

O experimento Remotion comprovou o fluxo local descrito em `remotion/EXPERIMENTO.md`. Não foram executados benchmarks de produção, comparação de qualidade entre editores ou integração com modelos. Os testes oficiais do monorepo não foram executados; a validação ocorreu no nosso demo com dependências publicadas.

O experimento Anime.js está em `animejs/EXPERIMENTO.md`. Os 14 testes aprovados do nosso projeto devem ser distinguidos dos 12 testes Node upstream, dos quais 2 falharam. As suítes oficiais de navegador do Anime.js continuam não executadas.
