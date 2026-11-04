# Drei: helpers declarativos e render controlado do React Three Fiber

SRC-011: [pmndrs/drei](https://github.com/pmndrs/drei), commit `bf6f4addf47467d3885de272d94ca5127f6ef68f`, consultado em 3/11/2026, São Paulo. O manifest da fonte usa `0.0.0-semantic-release`; runtime **@react-three/drei 10.7.9**, **@react-three/fiber 9.8.2**, **three 0.187.0**, React **19.2.0**. Ferramenta de teste **@react-three/test-renderer 9.1.1**. Versões fixadas no lockfile; [inventário](evidencias.json) distingue a fonte do código distribuído consultado.

Licença **MIT**. Preservar avisos ao redistribuir código substancial. O README informa o uso de `three-stdlib` separado dos addons do Three. Não copiamos assets de Storybook, fontes ou mapas de ambiente.

## Decisão de integração

Drei reúne helpers sobre React Three Fiber; não é outro backend de renderização. Incorporamos **RoundedBox + Center** na composição `DreiStudy`: uma forma de cartão com bevel e normais suavizadas, centralizada automaticamente mesmo quando sua malha nasce deslocada. Isso serve à futura autoria de elementos 3D para títulos/cards.

R3F reconcilia a árvore React em objetos Three. Remotion continua calculando o tempo, e o R3F renderiza somente sob pedido. Não substituímos a composição Three imperativa existente. Esta etapa demonstra o caminho declarativo e seu ciclo de vida, sem criar um editor 3D interativo completo.

## Mecanismos reconstruídos

| Recurso | Fonte e mecanismo | Implicação |
| --- | --- | --- |
| RoundedBox | `src/core/RoundedBox.tsx`: `createShape`, Shape/ExtrudeGeometry, bevel e `toCreasedNormals` | Largura/altura/profundidade geram uma extrusão com cantos arredondados. No layout effect, a geometria é centralizada e normais são ajustadas. Mais segmentos custam mais vértices; o raio precisa caber nas dimensões. |
| Center | `src/core/Center.tsx`: Box3/Sphere em layout effect, grupos outer/inner | Mede os filhos, calcula centro/extensões e compensa a posição no grupo externo. `precise` afeta a medição. `onCentered` ocorre depois da medição; mudanças exigem dependências/cacheKey adequados. |
| Float, consultado e não integrado | `src/core/Float.tsx`: `Math.random` na fase inicial, `useFrame` e `clock.elapsedTime` | Remontar pode mudar a fase. Uma timeline determinística precisaria de semente e relógio explícitos; o preset não usa Float. |
| Relógio do renderer | Código distribuído R3F, `update`/`advance` | Em `frameloop='never'`, o timestamp fornecido atualiza `clock.elapsedTime`; `advance` executa os subscribers e render. Usamos segundos, sem loops autônomos e sem efeitos globais. |
| Propriedade dos recursos | R3F `createRoot`, `releaseRenderer`, `unmountComponentAtNode` | Root configurado com opções de GL cria e possui o renderer. O unmount libera filhos e renderer. Não entregamos um renderer compartilhado nem o destruímos por fora durante a reconciliação. |

As três primeiras linhas são sustentadas por código fonte e docs `docs/shapes/rounded-box.mdx` e `docs/staging/center.mdx`. As duas últimas foram inspecionadas no pacote R3F executado, com hash no inventário; não constituem um estudo completo de outro repositório.

## Ponte implementada e sequência de captura

1. `DreiStudy.tsx` cria canvas isolado e registra no catálogo R3F apenas os construtores usados.
2. `createRoot.configure` define 640×360, DPR=1, câmera, buffer preservado e `frameloop: 'never'`.
3. `drei-scene.ts` monta luzes, grupo com rotação absoluta e os helpers. O layout effect do pai sinaliza readiness após os efeitos dos filhos que constroem/centralizam a geometria.
4. O host aguarda essa montagem, com limite de 10 s, e chama `advance(timeMs / 1000, false, estadoDaRaiz)` uma vez. Só então libera a captura Remotion.
5. Cleanup desmonta a raiz e remove o canvas; erro de inicialização também segue cleanup. O isolamento por frame evita apagar outra montagem assíncrona.

O preset usa dimensões fixas e raio 0.15 para um cartão 2.4×1.4×0.6. Ainda não expõe dados arbitrários do usuário: quando houver um contrato editável, deverá validar dimensões/raio/segmentos antes de construir geometria.

## Validação reproduzível

No demo:

```bash
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npm run render:study -- drei
```

**30 testes locais aprovados**, incluindo dois novos que montam os helpers reais com o test renderer: verificam existência de geometria, normais finitas, centralização de uma malha deslocada, mudança de matriz no tempo e reprodução após remontar um frame anterior. O mock WebGL do test renderer não comprova pixels; o [export em Chromium](resultados/render.json) é a verificação separada da imagem, do movimento, da repetição e das regressões. `npm ls` confirmou as versões principais sem conflito de peers de primeiro nível.

O e2e upstream **não foi executado**. Inspecionamos `test/e2e/e2e.sh`, `App.tsx` e `snapshot.test.ts`: constroem distribuição, criam app, usam Environment/CameraControls e comparam screenshot com tolerância. Isso cobre outro cenário, com pré-requisitos distintos; nossos resultados não são apresentados como aprovação daquela suíte. O status explícito está em [resultados/upstream.json](resultados/upstream.json).

## Limites observados

O teste Node emitiu avisos de depreciação `THREE.Clock` e do caminho CommonJS de Three usado por dependências. Os testes passaram; os avisos ficam registrados como dívida de compatibilidade, sem alterar dependências para escondê-los. A ponte browser usa imports ESM profundos dos helpers. Uma atualização de Three/R3F deverá repetir esses testes e os exports antes de trocar o lockfile.

Não validamos Html, fontes/texto, instâncias, GLTF, loaders, controles de mouse, Environment com HDR, Float, Springs ou performance de muitas raízes. Esses helpers têm estratégias de cache, carregamento e relógio diferentes. Recriar raiz por frame simplifica seek, mas não representa um preview otimizado; reuso e edição de propriedades precisam de ensaio próprio. O Chromium usa WebGL por software, sem resultado de benchmark de GPU física.
