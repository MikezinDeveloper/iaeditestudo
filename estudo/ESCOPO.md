# Escopo

## Confirmado pelo usuário

- A IA editará **vídeo e áudio com mescla de motion**.
- O estudo usará repositórios e documentação para entender mecanismos e orientar a construção do produto no Codex.
- O usuário enviará os repositórios de referência.
- O conhecimento deve ficar organizado e persistido, permitindo ampliar o estudo ao longo de várias tarefas.
- O usuário indicou Remotion como primeira referência de repositório e pediu engenharia reversa para funcionar com Codex. Isso inclui um protótipo que exercita as APIs públicas e sua validação; não equivale a reimplementar o motor ou a concluir o produto inteiro.

Neste estudo, “motion” será tratado inicialmente como motion graphics: animação de propriedades, texto, elementos gráficos e composição com vídeo. O significado poderá ser refinado com os exemplos do usuário.

## Perguntas que a pesquisa precisa responder

1. Como representar uma edição sem destruir o material original?
2. Como manter vídeo, áudio e animação sincronizados?
3. Como transformar uma instrução em operações válidas e revisáveis?
4. Como produzir preview e exportação com resultados coerentes?
5. Quais componentes existentes vale integrar, adaptar ou implementar?
6. Como verificar qualidade, desempenho e correção de uma edição?

## Capacidades candidatas, ainda não prometidas

- Cortar, ordenar e sobrepor clipes em uma timeline.
- Trabalhar com voz, música, efeitos e automação de volume.
- Animar posição, escala, rotação, opacidade, texto e outros parâmetros.
- Criar legendas e sincronizar elementos ao conteúdo.
- Editar por linguagem natural com histórico e possibilidade de desfazer.
- Gerar preview e exportar um resultado reproduzível.

## Decisões abertas

Plataforma de destino, interface, uso local ou em servidor, necessidade de GPU, modelos de IA, formatos de projeto, requisitos de privacidade, orçamento e metas de latência. Não são pré-requisitos para começar a analisar os repositórios; tornam-se decisões necessárias antes dos protótipos correspondentes.

## Critério de utilidade

Uma descoberta deve ajudar a escolher uma solução, implementar uma capacidade, evitar uma falha ou definir um teste. Informações interessantes sem aplicação imediata podem ser registradas com prioridade menor.
