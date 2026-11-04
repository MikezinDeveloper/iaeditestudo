# D3 — SRC-008, quarto item da fila

Fonte: [d3/d3](https://github.com/d3/d3), commit `db118c93a429e82b83f091dbaa18fd0a82c06130`, versão 7.9.2, licença ISC. Runtime do demo: `d3@7.9.2` e declarações `@types/d3@7.4.3`, fixados no lockfile.

## Reconstrução e papel no projeto

O entrypoint desse repositório é um agregador de cerca de trinta pacotes; não contém sozinho a implementação de todas as escalas, layouts e renderizações. O estudo consultou o agregador, testes e documentação local e os módulos distribuídos efetivamente usados, registrados com versão e integridade. Não se atribui uma auditoria integral a todos os subprojetos.

Escalas separam dados de coordenadas. `scaleLinear` normaliza um domínio quantitativo e interpola sua saída; por padrão pode extrapolar. O nosso contrato usa clamp e um domínio final estável para que o significado dos valores não mude a cada frame. `scaleBand` distribui categorias em bandas uniformes, considerando padding, alinhamento e largura disponível; valores fora do domínio podem devolver undefined.

Selections associam dados a elementos. O join com chave distingue enter, update e exit e preserva identidade por ID, não apenas posição no array. IDs repetidos têm semântica específica no join e podem ocultar a intenção do usuário; o nosso contrato os rejeita. Cada nó recebe dados associados pelo D3, enquanto o array original do domínio permanece intacto no nosso cálculo.

`interpolateNumber` calcula um valor entre origem/destino a partir de progresso; `easeCubicInOut` transforma esse progresso. Essas funções atendem a uma animação calculável por instante. `transition` e `timer`, por outro lado, dirigem updates com o relógio de execução; não foram usados no export.

A documentação também distingue geradores de geometria de um renderer: `line(data)` pode produzir um path SVG ou comandos em um contexto, e certas curvas dependem de ordenação dos dados. Layouts como force simulation possuem estado mutável e iniciam timers por padrão; um futuro uso em vídeo exigiria stop, número definido de ticks e estratégia de seek/cache. Isso não foi confundido com uma função pura de tempo.

## Implementação entregue

`chart-data.json` contém quatro categorias do nosso domínio. `d3-layout.ts` valida dados, produz bandas e alturas e aplica interpolação em 1.600 ms. O domínio do gráfico aceita valores finitos não negativos; não é um componente genérico para séries negativas ou domínios logarítmicos.

`D3Study` cria um SVG e realiza joins por ID para retângulos e rótulos, dentro do host isolado do BrowserStudy. Remotion fornece o tempo e faz o export. Nenhum timer ou transition do D3 é iniciado. Alterar o JSON muda os dados exibidos sem reescrever o JSX da composição.

Testes verificam alturas proporcionais, bandas sem sobreposição, preservação de inputs congelados, conjunto vazio, IDs duplicados, NaN, valores negativos, série de zeros e igualdade ao avaliar 90 frames em ordem embaralhada. A suíte do projeto totaliza 24 aprovações nesta etapa, além da checagem TypeScript.

## Origem, ferramenta e testes não executados

O repositório mantém pnpm-lock.yaml e sua suíte Vitest testa exports do agregador e anchors da documentação. A tentativa de instalação congelada com pnpm 11.25.0 foi recusada pela política ativa de idade mínima de releases, que identificou entradas publicadas dentro da janela de proteção. Não foram relaxadas políticas, reconstruído o lockfile ou executados os pacotes recusados no fluxo upstream.

Assim, a suíte oficial é **não executada**, não “aprovada” nem uma contagem de testes falhos. O projeto de integração mantém seu fluxo npm preexistente, com pacote publicado instalado por versão exata e integridades do lockfile, e suas verificações são relatadas separadamente. O estudo não altera configurações de segurança do pnpm para produzir um resultado verde.

## Reprodução e evidências

```bash
cd demos/remotion-codex
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- d3
```

Inventário: [evidencias.json](evidencias.json). Export e regressões: [relatório](resultados/render-report.json). O cenário comprova um gráfico SVG pequeno, calculado por frame. Não inclui visualizações geográficas, layouts físicos, ingestão remota, eixos de tempo com timezone, interação de zoom, brush ou validação visual de todo o D3.
