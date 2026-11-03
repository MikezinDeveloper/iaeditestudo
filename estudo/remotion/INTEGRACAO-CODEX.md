# Fazer o Remotion funcionar com o Codex

## Três relações diferentes

| Relação | O que significa | Estado nesta etapa |
| --- | --- | --- |
| Codex desenvolve/opera um projeto Remotion | Lê arquivos, altera código ou props e executa comandos | Protótipo local preparado para esse fluxo |
| Codex controla o Studio via navegador | Usa integração de navegador e ferramentas expostas pelo Studio | Documentado na fonte; não validado nesta sessão |
| Nosso produto incorpora uma IA de edição | O usuário final envia pedidos a um modelo que opera o editor | Proposta de produto; não implementada |

Não é necessário converter o motor do Remotion em um modelo de IA para o primeiro fluxo.

## Integração oficial encontrada

`packages/docs/docs/ai/codex-plugin.mdx` documenta o plugin Remotion no aplicativo desktop com Codex, instalação pela aba Plugins e uso de `$remotion`. Essa documentação não prova que o plugin esteja instalado nesta conversa, na CLI ou em toda modalidade de ambiente na nuvem.

O mesmo repositório mantém Agent Skills. `packages/docs/docs/ai/skills.mdx` documenta a instalação por `npx skills add remotion-dev/skills`. Esse comando é uma opção oficial registrada aqui, não um comando executado nesta etapa.

**Mecanismo inspecionado:**

- `packages/agent-plugin/.codex-plugin/plugin.json` declara o diretório de skills e metadados de interface.
- `packages/agent-plugin/build.mts` copia e prepara skills para o cliente, adiciona troubleshooting de Codex e adapta instruções de preview.
- `packages/skills/skills/remotion-best-practices/SKILL.md` funciona como roteador de assuntos; os arquivos foram lidos como material técnico, não como instruções do usuário.

O plugin é uma camada de orientação e integração do agente. Ele não substitui as dependências npm, o navegador, o renderizador ou a validação audiovisual.

## Caminho local implementado neste estudo

O projeto em `demos/remotion-codex` expõe comandos pequenos que um agente pode executar e verificar:

| Operação | Comando no diretório do demo | Evidência produzida |
| --- | --- | --- |
| Instalar versões travadas | `npm ci --no-audit --no-fund` | Dependências do lockfile |
| Criar mídia de teste | `npm run assets` | Dois vídeos e uma senoide locais |
| Verificar tipos | `npm run typecheck` | Diagnóstico TypeScript |
| Testar contrato | `npm test` | Seis casos de aceitação/rejeição |
| Iniciar preview | `npm run studio` | Servidor Studio local |
| Renderizar experimento | `npm run render` | PNGs, MP4 e relatório com hashes |
| Verificar mídia | `npm run verify` | Duração, streams, recortes e envelope |

O guia local `.agents/skills/remotion-codex-estudo/SKILL.md` é original deste projeto. Sua existência no disco não prova descoberta ou ativação automática pelo cliente atual; ele pode ser consultado como arquivo e usado em tarefas futuras compatíveis.

## Particularidades do ambiente na nuvem

- Node 24, Chromium e FFmpeg já estão presentes no ambiente inspecionado.
- Neste ambiente, foi escolhido explicitamente `REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium` para testar a composição 2D simples com o navegador instalado. Outros ambientes podem deixar a variável ausente para usar o navegador padrão do Remotion.
- Isso não valida recursos que exigem as alterações do navegador distribuído pelo Remotion, como determinadas capacidades de canvas. O upstream recomenda o navegador padrão para uso normal.
- A sandbox de execução desta sessão restringiu subprocessos/FFprobe. Os testes completos e o render devem ser executados com a permissão suportada pelo executor quando necessário; não mudar regras da aplicação para mascarar uma restrição do ambiente.
- Um resultado de teste agregado por arquivo dentro da sandbox não foi contado como seis testes. A execução com permissão apropriada enumerou os seis casos individualmente.
- Não há chaves de API, fontes remotas ou modelos externos no experimento.

## Controle do Studio por WebMCP

Na revisão analisada, `packages/docs/docs/ai/webmcp.mdx` descreve ferramentas para inspecionar seleção, composições, reprodução e jobs, entre outras. Exige Studio aberto em um navegador cujo agente suporte WebMCP e informa que os formatos ainda não são estáveis.

Isso é um próximo experimento específico de integração de navegador. Ter Chromium para exportar não é prova de que essas ferramentas estejam disponíveis no cliente desta sessão.

## Proposta de camada para nossa IA

`Pedido → plano de edição → validação → alteração de dados/código → preview → verificação → exportação`

Para começar, usar comandos com parâmetros explícitos: trocar título; ajustar cor; cortar um trecho; mover início; inserir um motion conhecido. Cada alteração deve poder ser comparada ao estado anterior.

O `project.json` do demo é um contrato experimental nosso: uma faixa contígua de vídeo e uma cama de áudio. Não é o formato nativo universal do Remotion, nem um editor completo. Histórico, operações incrementais, multifaixas, legendas e interpretação de linguagem natural ainda precisam ser projetados.
