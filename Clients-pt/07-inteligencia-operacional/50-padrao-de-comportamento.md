# O padrão de comportamento do funcionário

## O que é o EmployeePattern

O EmployeePattern é o perfil de comportamento que o CheckBiz360 constrói para cada funcionário de forma automática e contínua. Não se trata de um relatório pontual nem de um resumo mensal; é um modelo acumulativo que reúne como o funcionário trabalha dia após dia e permite identificar tendências que uma análise isolada não revelaria.

Enquanto um relatório tradicional lhe diz que um funcionário chegou tarde quatro vezes em março, o EmployeePattern diz-lhe se esses quatro atrasos são uma exceção num histórico impecável ou se fazem parte de uma tendência que há meses vem a piorar. Essa diferença de perspetiva é o que transforma o dado bruto em inteligência útil.

## Como se constrói o padrão

O sistema processa de forma automática os dados que já existem na plataforma. Não exige configuração adicional; ativa-se a partir do momento em que a entidade tem funcionários com registos de assiduidade e horários atribuídos.

As fontes de dados que alimentam o padrão são as seguintes:

**Registos de assiduidade.** Cada registo de entrada e de saída fornece informação sobre pontualidade, duração real da jornada e presença efetiva. O sistema acumula estes dados e calcula médias, desvios e tendências.

**Horários planeados.** O padrão não analisa o comportamento em abstrato, mas sempre em relação ao que estava previsto. Uma saída às 18:00 é diferente consoante o turno terminasse às 18:00 ou às 17:00.

**Tarefas e avaliações.** As tarefas concluídas e as avaliações atribuídas pelo manager complementam a análise de presença. Um funcionário com assiduidade perfeita mas com baixa produtividade em tarefas gera um perfil diferente do de um funcionário que falta pouco e resolve bem as suas responsabilidades.

**Tempo acumulado.** O padrão precisa de dados suficientes para ser representativo. Durante as primeiras semanas de trabalho de um funcionário, os índices devem ser interpretados com cautela. A partir de vários meses de histórico, o padrão reflete com maior precisão o comportamento real.

## Porque é que o padrão vale mais do que um relatório pontual

Um relatório pontual capta o estado num momento determinado. O EmployeePattern capta a direção em que esse estado evolui. Essa diferença é crítica para a gestão de pessoas.

Um funcionário pode ter um bom mês isolado depois de uma conversa com o seu responsável, mas se o seu padrão acumulado mostrar uma tendência negativa sustentada, o dado do bom mês não deve gerar uma falsa sensação de problema resolvido. Do mesmo modo, um funcionário que atravessa um mau trimestre por razões externas mas tem um histórico sólido merece uma avaliação diferente da de alguém com um perfil cronicamente irregular.

## Exemplos de padrões

### Padrões positivos

Um padrão positivo caracteriza-se pela consistência e pela estabilidade. O funcionário chega dentro da margem de pontualidade de forma habitual, completa as suas jornadas com poucos desvios, não acumula ausências injustificadas e as suas avaliações de tarefas são regularmente boas. Este perfil gera indicadores de fiabilidade e de eficiência altos e é o que a avaliação operacional assinala como candidato a promoção.

Outro padrão positivo relevante é o de melhoria progressiva: um funcionário cujos índices eram moderados há seis meses mas mostram uma tendência clara de melhoria. Este perfil indica que as ações de gestão estão a funcionar e que o funcionário tem capacidade de desenvolvimento.

### Padrões negativos

Um padrão negativo não se define por um incidente isolado, mas pela repetição. Chegadas tardias concentradas em certos dias da semana, saídas antecipadas frequentes, ausências recorrentes sem justificação formal ou uma tendência de deterioração nos índices ao longo dos meses.

O padrão mais difícil de detetar sem um sistema é o de deterioração lenta: um funcionário que vai acumulando pequenos desvios semana a semana, nenhum deles suficientemente notório por si só, mas que no conjunto representam uma deriva significativa.

## Como se visualiza no backoffice

O EmployeePattern é apresentado na ficha de cada funcionário dentro do módulo de inteligência operacional. Os responsáveis com acesso ao módulo podem consultar:

- Os indicadores calculados —fiabilidade, eficiência operacional, custo e fiabilidade do padrão— com a sua evolução temporal em gráfico.
- O histórico de comportamento com os eventos mais relevantes.
- O estado atual do sinalizador de anomalia, se estiver ativo.

> **Nota:** o acesso aos dados do EmployeePattern está limitado aos perfis de Manager e Owner. Os supervisores podem consultar os indicadores da sua equipa direta, mas não têm acesso à vista de padrão completo. Consulte o artigo sobre painéis de controlo para mais detalhe sobre permissões.

## Artigos relacionados

- [O que é a inteligência operacional](49-o-que-e-a-inteligencia-operacional.md)
- [Índice de fiabilidade](51-indice-de-fiabilidade.md)
- [Índice de eficiência operacional](52-indice-de-eficiencia.md)
- [Avaliação operacional do funcionário](53-pontuacao-de-promocao.md)
- [Deteção de anomalias](55-detecao-de-anomalias.md)
- [O painel de Operação](56-paineis-de-controlo.md)
