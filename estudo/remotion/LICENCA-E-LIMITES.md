# Licença e limites observados

## Motor Remotion

O `LICENSE.md` da revisão estudada usa uma licença própria, com categorias Free License e Company License. Ela permite avaliação e determinados usos, incluindo pessoas físicas, organizações sem fins lucrativos e empresas de até três empregados nos termos do arquivo. Também restringe copiar/modificar o código para vender, alugar ou relicenciar um derivado do Remotion.

**Fonte:** [LICENSE.md na revisão analisada](https://github.com/remotion-dev/remotion/blob/fe9f0c372706f2039da6b2a0a92b92aa746e69cf/LICENSE.md).

Logo, estudar o mecanismo e usar suas APIs não implica permissão irrestrita para redistribuir um clone comercial do motor. Antes de definir a distribuição do produto, conferir o enquadramento com a licença correspondente à versão adotada.

## Plugin e skills não devem ser confundidos com o motor

O diretório `packages/agent-plugin` contém `LICENSE` em MIT e os manifestos `plugin.json` e `.codex-plugin/plugin.json` declaram MIT. O `package.json` desse mesmo pacote declara “Remotion License”. Há, portanto, metadados divergentes na revisão analisada; não se deve generalizar a licença de um manifesto para todo o monorepo ou para todas as skills.

O guia e o demo deste estudo foram escritos para este projeto usando as APIs públicas; não foi copiado o pacote de skills nem o código do motor para dentro do repositório do usuário. As dependências publicadas continuam sujeitas às suas próprias licenças.

## Escopo da engenharia reversa

O trabalho reconstrói arquitetura e comportamento a partir de código disponível, documentação e experimentos. A integração proposta usa o motor existente. Não foram alteradas verificações de licença, extraídas credenciais ou substituídas dependências por versões com verificações removidas.

## Limites técnicos da prova

- Composição 2D, 640×360, 30 fps, seis segundos.
- Dois clipes sintéticos; uma faixa de áudio; título animado.
- Export em H.264/AAC; navegador e ambiente registrados no experimento.
- Sem certificação de HDR, GPU, qualidade profissional, edição multifaixa, longas durações ou codecs arbitrários.
- Sem instalação comprovada do plugin oficial e sem ativação comprovada de WebMCP.

Esses limites definem o que ainda precisa ser testado antes de decisões de produto e de escala.
