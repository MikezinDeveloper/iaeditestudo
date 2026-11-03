# DEC-001 — Avaliar Anime.js com estado novo por quadro

- Estado: aceita para o protótipo; não define a arquitetura final de produção.
- Fonte: SRC-004, Anime.js 4.5.0.
- Experimento: EXP-002, em `estudo/animejs/EXPERIMENTO.md`.

## Problema

O Remotion precisa de uma imagem correta para um frame arbitrário, inclusive fora de ordem. O Anime.js normalmente mantém estado de animação e um relógio autônomo.

## Alternativas

1. Usar somente interpolação/spring nativos do Remotion. Continua sendo uma boa opção para movimentos simples.
2. Usar easings do Anime.js como funções sobre progresso calculado pelo frame. Precisa de um contrato para cada curva e atenção a easings com estado/callback.
3. Reutilizar uma timeline pausada e chamar `seek()` em diferentes tempos. Falhou no desenho com entrada e saída da mesma propriedade.
4. Construir targets e timeline privados para cada amostra, obter valores e descartar a instância.

## Escolha

Usar a alternativa 4 para o experimento de timeline/stagger do Anime.js, sem alterar globalmente o engine. React continua responsável pelo DOM. O motor audiovisual continua sendo Remotion.

## Evidência

A timeline reutilizada falhou ao voltar do frame 111 para o 28. O registro compara seus valores com uma instância nova. O adaptador corrigido mantém o teste de igualdade e percorre todos os 120 quadros em ordem embaralhada.

## Consequências

Ganhamos uma integração funcional para o cenário selecionado e evitamos depender do histórico de reprodução. Há alocação e construção de tweens por amostra; custos em grandes cenas ainda não foram medidos. A decisão não autoriza generalizar o resultado para DOM, WAAPI, springs com callbacks, aleatoriedade ou todas as opções de timeline.

## Quando revisar

Se uma versão futura mudar o comportamento de seek; se uma cena grande apresentar custo alto; se uma representação de curvas pura atender ao mesmo recurso com menor custo; ou se o produto exigir edição visual independente que esse contrato não contemple.
