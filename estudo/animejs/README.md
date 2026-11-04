# Anime.js — estudo e integração com Remotion/Codex

## Fonte e cobertura

- Repositório indicado: <https://github.com/juliangarnier/anime>.
- Commit estudado: `01b81be1df6843ccfe0a71c0699a746bf740dd77`.
- Versão do manifest: **4.5.0**; licença MIT.
- Data de consulta: 3 de novembro de 2026.
- Fonte local de pesquisa: `/workspace/research-cache/anime`, checkout parcial. O cache não é uma dependência de execução do nosso projeto.
- Integração: pacote npm `animejs@4.5.0`, fixado no lockfile do demo. Não foi feita uma comparação byte a byte entre pacote publicado e commit.

Foram consultados código, declarações, testes e exemplos de API no README. Os registros de [evidências](evidencias.json) distinguem leitura integral/parcial; não representam auditoria de todas as linhas, branches, issues, exemplos ou módulos do projeto. A documentação externa em animejs.com e o wiki de migração são referências indicadas pelo README, não conteúdos consultados nesta etapa.

## Resultado aplicável ao projeto

Anime.js é uma camada de animação útil para títulos, infográficos, stagger e sequências de motion. No nosso experimento, ele calcula valores numéricos; React aplica esses valores à cena, e Remotion mantém o relógio, a mídia e a exportação.

Foi adicionada a composição **AnimeMotionStudy**, com uma timeline pausada, sem reprodução autônoma. Um teste encontrou estado incorreto ao reutilizar a mesma timeline depois de visitar o final; a ponte foi ajustada para reconstruir a avaliação de cada instante.

## Leituras

- [Arquitetura e mecanismos](ARQUITETURA.md)
- [Contrato da integração com Remotion e Codex](INTEGRACAO.md)
- [Experimento, falhas e resultados](EXPERIMENTO.md)
- [Decisão de usar avaliação independente por quadro](../decisoes/DEC-001-animejs-por-quadro.md)
- [Projeto executável](../../demos/remotion-codex/README.md)

## Limites que permanecem

Não foram auditados nem integrados integralmente WAAPI, drag, scroll, layout, splitText, morfismo SVG e adapters 3D. O teste do nosso desenho numérico não comprova que essas APIs tenham o mesmo comportamento em exportação.

Na suíte Node oficial executada sem alterar as asserções, houve **10 aprovações e 2 falhas** em verificações do estado de otimização do V8. O setup pelo lockfile upstream também falhou por divergência com o manifest. Esses resultados estão separados dos testes da nossa integração.

## Anexo recebido em 4/11/2026

O ZIP `anime-master.zip` identifica a revisão `01b81be1df6843ccfe0a71c0699a746bf740dd77` no comentário do arquivo e contém Anime.js 4.5.0. Seus 70 arquivos `src/` foram comparados byte a byte com o checkout já estudado: nenhuma diferença. [Recibo com SHA-256 e resultado](anexo-2026-11-04.json). O anexo confirma esta fonte; não introduz uma nova versão ou instruções adicionais para o projeto.
