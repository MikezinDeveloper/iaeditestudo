# Theatre.js — SRC-006, segundo item da fila

Repositório: [theatre-js/theatre](https://github.com/theatre-js/theatre). Commit público estudado: `6ea82b938ea49609489f6377ded693ccc6ee8f5b`; manifest do core nesse checkout: 0.7.0. A integração utiliza o pacote publicado `@theatre/core@0.7.2`, fixado no lockfile. Não se presume que esses artefatos sejam equivalentes.

## Arquitetura reconstruída

`getProject(id, config)` obtém um singleton por identidade. Reutilizar o mesmo ID com outra configuração é recusado em desenvolvimento. O projeto combina estado serializado, sheets, objetos e armazenamento de assets. `project.ready` representa a prontidão de carregamento; a presença de Studio pode mudar de onde o estado vem.

Uma sheet representa uma cena/instância. Um objeto registra propriedades tipadas e oferece props/pointers, leituras e assinaturas. O resultado combina defaults, initialValue, overrides estáticos e valores sequenciados, nessa ordem de precedência. Isso é importante para que a IA não altere um default e espere sobrescrever uma propriedade já animada.

A sequência guarda posição, comprimento e tracks por objeto. `sequence.position` usa unidades de posição, normalmente segundos; `subUnitsPerUnit` define o grid de edição, não obriga o motor a reproduzir apenas nessa cadência. A posição é limitada ao comprimento. Chamar play aciona um controlador de reprodução; a nossa ponte apenas atribui a posição explícita.

Tracks relacionam caminhos de propriedade a keyframes. A avaliação escolhe o intervalo entre os keyframes, respeita hold/conexão e usa handles de Bézier para a progressão. Antes e depois dos extremos, mantém valores definidos pelos extremos. O estado é um artefato de projeto que pode ser versionado independentemente da cena React.

Dataverse fornece Atom, pointers, prisms e Ticker. Prisms ativos mantêm assinaturas e propagação de mudanças; uma leitura fria isolada pode não executar os efeitos necessários para o caminho sequenciado. O primeiro ensaio com uma leitura simples devolveu defaults e emitiu aviso de prism frio.

`createRafDriver()` permite dirigir o Ticker explicitamente, sem criar um loop de reprodução. `onValuesChange(callback, driver)` ativa a derivação; após atualizar a posição, a ponte chama tick e lê o snapshot entregue ao callback. O unsubscribe libera essa assinatura.

Evidências: coreExports; Project/TheatreProject; SheetTemplate; TheatreSheetObject/SheetObject; Sequence/TheatreSequence; interpolationTripleAtPosition; rafDrivers; e os módulos Atom, prism e Ticker listados no [inventário](evidencias.json).

## Integração entregue

- `theatre-state.json`: estado original deste estudo, com três propriedades, três keyframes por track e sequência de três segundos.
- `theatre-sampler.ts`: aguarda ready, ativa assinatura com driver próprio, define posição em segundos, processa o tick e copia os valores. Não chama play nem carrega Studio.
- `TheatreStudy`: usa posição, ângulo e escala para desenhar um cartão; Remotion continua responsável pelo frame e pelo export.
- Testes: round-trip JSON, amostras conhecidas, todos os 90 quadros em ordem embaralhada e cleanup.

O objeto de projeto é compartilhado pela identidade estável; alterar o arquivo de estado durante HMR pode exigir um novo ID ou recarregar a página. Isso é um contrato do singleton, não um formato universal de histórico para o nosso produto.

## Contratos descobertos durante a validação

O core público no checkout estudado usa estruturas internas PointableSet em tipos privados. O pacote 0.7.2 validado neste estudo aceita arrays de keyframes no estado consumível. O nosso JSON segue o formato efetivamente exercitado no runtime. Não usamos interfaces privadas como contrato de produção nem afirmamos que o HEAD foi compilado para gerar esse pacote.

A distribuição 0.7.2 também tem interop diferente entre Node ESM e o bundler de navegador. Uma importação default funcionou no Node e falhou no browser. A ponte agora normaliza namespace/default e foi submetida aos dois caminhos.

## Licença e escopo

O README e o manifest do core indicam Apache-2.0 para `@theatre/core`; `@theatre/studio` é AGPL-3.0. O root LICENSE reúne textos diferentes. A integração não instala nem redistribui Studio; ela não oferece a interface visual do editor Theatre. O README público informa que uma etapa de desenvolvimento ocorre em repositório privado, cujo conteúdo não foi acessado.

O monorepo inclui app, sync, Prisma e configuração Jest com setup de Studio. Não foi instalado nem declarado aprovado esse sistema inteiro para validar o core. As verificações locais exercitam a dependência publicada; os testes oficiais do monorepo são **não executados**.

## Reprodução e limites

No diretório do demo:

```bash
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- theatre
```

Relatório e mídia em `out/studies/theatre/`; [relatório preservado](resultados/render-report.json). O runner verifica pixels do export, repetição de frame, metadados e referências das composições anteriores.

Não foram integrados Studio, colaboração, servidor de sincronização, editor visual de curvas, assets remotos nem playback de áudio do Theatre. A prova demonstra estado persistido e avaliação temporal do core para a composição escolhida.
