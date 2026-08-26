# Análise de custos

## Para que serve

O módulo de análise de custos do CheckBiz360 traduz os dados de assiduidade em informação económica diretamente utilizável pelo controlo de gestão. O objetivo é que a direção possa responder a qualquer momento a perguntas como: quanto custou realmente operar esta sucursal esta semana? Que funcionário tem o maior custo por hora realmente trabalhada? Em que períodos nos estamos a desviar mais do orçamento de pessoal?

O sistema não exige integração com o processamento salarial nem acesso a dados contabilísticos externos. Trabalha unicamente com duas variáveis: as horas reais registadas na plataforma e a tarifa horária configurada para cada funcionário.

## Configurar o custo por hora do funcionário

O ponto de partida é definir a **tarifa horária** de cada funcionário. Configura-se **na associação do funcionário à sua sucursal**, e não nos seus dados pessoais: a mesma pessoa pode ter tarifas distintas em locais distintos, a par da sua função e da sua responsabilidade ali.

Para a configurar:

1. Aceda a **Funcionários** e abra a ficha do funcionário.
2. Vá à secção de sucursais e abra a associação ao local correspondente.
3. Introduza a tarifa juntamente com a função e a responsabilidade.
4. Guarde as alterações.

O valor deve refletir o **custo real para a empresa**, não o salário bruto: inclua a parte proporcional das contribuições sociais a cargo da empresa se quiser um custo total realista.

> **Importante:** sem tarifa configurada não há análise de custos possível. É a causa mais frequente de os indicadores económicos aparecerem vazios ou estranhos. O bloco de **estado dos dados** do painel de Operação indica esta cobertura de configuração: consulte-o antes de dar por boa —ou por má— qualquer cifra de custo.

## O que o sistema calcula

A partir das horas registadas e da tarifa configurada, a ficha do funcionário mostra:

| Indicador | O que mostra |
|---|---|
| **Custo por hora trabalhada** | O custo unitário real de uma hora efetiva |
| **Custo por jornada** | O custo médio de um dia de trabalho |
| **Custo por rendimento** | O custo ponderado pela eficácia observada |
| **Rendimento do custo investido** | O que se obtém por cada unidade de custo |
| **Custo acumulado** | A soma real do período |

Todos se calculam sobre **jornadas validadas** e são comparados contra o histórico consolidado do próprio funcionário ou local, não contra um orçamento: a plataforma não gere orçamentos nem custos planeados.

## Comparações entre sucursais

O painel de Operação permite comparar locais entre si dentro de um período. O custo, esse, deixou de presidir à leitura: não é uma medida de operacionalidade mas uma consequência, e por isso vive dentro do perfil de cada local e de cada pessoa, e não como separador próprio.

As comparações permitem detetar situações que uma análise sucursal a sucursal não revela:

- Uma sucursal com maior presença de funcionários pode ter um custo por hora realmente trabalhada mais alto do que outra com menos pessoal se a primeira acumular mais horas extraordinárias não planeadas.
- Duas sucursais com orçamentos semelhantes podem ter desvios de custo muito diferentes consoante a disciplina horária das suas equipas.
- Identificar a sucursal com maior eficiência de custo não implica que seja mais bem gerida, mas indica onde as práticas de gestão de horários estão a funcionar melhor.

## Alertas de excesso de custo e limiares configuráveis

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

Numa versão futura, o CheckBiz360 permitirá configurar alertas automáticos que serão ativados quando o desvio de custo de uma sucursal ou de um funcionário ultrapassar um limiar definido pelo utilizador. Os alertas serão enviados ao Manager e ao Owner por notificação no backoffice e, opcionalmente, por correio eletrónico. Por agora, a análise de custos é uma métrica visível nos painéis de controlo que deve ser consultada manualmente.

## Exportação para controlo de gestão

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

A exportação dos dados da análise de custos em formato CSV e PDF não está disponível na versão atual. Os dados podem ser consultados diretamente a partir do painel de custos do backoffice, mas não podem ser descarregados neste momento. Esta capacidade de exportação está prevista no roadmap da plataforma.

## Artigos relacionados

- [O que é a inteligência operacional](49-o-que-e-a-inteligencia-operacional.md)
- [Índice de eficiência operacional](52-indice-de-eficiencia.md)
- [O painel de Operação](56-paineis-de-controlo.md)
- [Tipos de relatório](../11-relatorios-e-exportacao/76-tipos-de-relatorio.md)
- [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md)
