# Método de estudo e engenharia reversa

## 1. Receber e identificar a fonte

Registrar URL, finalidade, licença, versão ou commit, data de consulta e relação com vídeo, áudio, motion ou integração com IA. Começar pelas fontes indicadas pelo usuário.

Usar código e documentação públicos ou materiais disponibilizados com autorização. Quando só houver acesso ao comportamento, registrar a análise como observação de entradas e saídas, sem inventar detalhes internos.

## 2. Fazer a triagem

Ler README, documentação de arquitetura, manifestos, exemplos, testes e instruções de execução. Identificar quais componentes merecem uma análise profunda e quais são apenas referências adjacentes.

Estrelas, demonstrações e descrições comerciais não comprovam qualidade técnica. Registrar atividade recente, compatibilidade e manutenção com evidências consultadas, sem supor que uma versão antiga represente o estado atual.

## 3. Seguir um fluxo concreto no código

Escolher uma operação relevante, por exemplo “cortar um clipe” ou “avaliar um keyframe”. Localizar a entrada, estruturas de dados, validações, transformações, chamada de renderização e saída. Anotar símbolos e caminhos na revisão analisada.

Explicar o mecanismo em linguagem própria. Trechos pontuais de código podem ilustrar uma conclusão, mas uma cópia de arquivos não substitui análise.

## 4. Reproduzir o comportamento

Executar um exemplo ou teste significativo quando o ambiente permitir. Registrar versões, comandos, assets, resultados e limitações. Separar problemas de setup de defeitos do projeto. Uma porta aberta ou instalação concluída não demonstra que a edição funciona.

## 5. Avaliar a adaptação

Para cada mecanismo útil, indicar problema resolvido, dependências, contrato de dados, custo, limitações e alternativas. Distinguir integração direta, adaptação de uma ideia e implementação independente. Conferir a licença antes de recomendar reutilização de código.

## 6. Comparar e decidir

Comparar soluções com base no mesmo caso de uso e em critérios explícitos. Formular uma hipótese, executar um experimento e só então registrar a decisão e suas condições de revisão.

## Tipos de afirmação

| Tipo | Exigência |
| --- | --- |
| Documentado | Link para a seção ou arquivo consultado |
| Inspecionado no código | Revisão, caminho e símbolo relevante |
| Observado em execução | Experimento, ambiente e resultado |
| Inferido | Evidências que motivam a inferência e incerteza restante |
| Proposto | Benefício esperado e teste necessário |

## Estados de uma análise

`Recebida → triada → documentada → código inspecionado → experimentada → sintetizada`

Os estados registram trabalho feito, não qualidade presumida. Uma fonte pode ser útil apenas documentalmente; nesse caso, declarar o limite sem avançar seu estado artificialmente.

## Organização e recuperação

- `FONTES.md`: índice e proveniência.
- `analises/`: uma síntese por fonte ou mecanismo.
- `experimentos/`: adicionar quando houver execução reproduzível e resultados.
- `decisoes/`: adicionar quando houver uma escolha justificada.

Evitar duplicar documentos inteiros e repetir a mesma conclusão em vários arquivos. Preferir links e sínteses úteis. Se a fonte mudar, criar uma revisão da análise e registrar o que foi revalidado.
