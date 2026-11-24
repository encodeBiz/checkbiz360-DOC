# Relatórios de tarefas

O CheckBiz360 oferece duas vias para analisar a execução de tarefas: as métricas que se consultam diretamente no backoffice e o **relatório de tarefas em Excel**, que é gerado a pedido e fica arquivado no histórico de relatórios.

---

## Métricas visíveis no backoffice

A partir da listagem e do detalhe de tarefas, managers e owners podem consultar:

- **Tarefas por estado:** quantas há em rascunho, atribuídas, em curso, concluídas, validadas, recusadas ou canceladas, para toda a entidade ou filtradas por sucursal.
- **Tarefas por funcionário:** as tarefas atribuídas a cada pessoa com o seu estado atual, o que permite identificar cargas de trabalho desequilibradas ou tarefas paradas à espera de validação.
- **Cumprimento temporal:** para cada tarefa, se vai a tempo, em risco, vencida, ou se foi concluída dentro ou fora do prazo.
- **Avaliações registadas:** a pontuação atribuída ao funcionário fica visível no detalhe da tarefa e no seu perfil.

> **Nota:** as métricas refletem o estado atual à medida que funcionários e responsáveis interagem com as tarefas.

---

## Relatório de tarefas em Excel

O relatório de tarefas é gerado a partir da secção **Relatórios** do backoffice e descarregado em formato **Excel (XLSX)**.

### Como gerá-lo

1. Aceda a **Relatórios** no menu lateral.
2. Prima o botão para gerar um relatório novo.
3. Em **Tipo de relatório**, selecione *Relatório de tarefas*. O formato fica fixado em Excel (XLSX), que é o único disponível para este relatório.
4. Selecione o **período** (data de início e de fim).
5. Se precisar, filtre por **sucursal** e por **estado** das tarefas.
6. Gere o relatório. Quando estiver pronto, aparecerá no histórico de relatórios, de onde o pode descarregar.

> **Importante:** o período do relatório aplica-se ao **prazo** de cada tarefa, não à sua data de criação. Um relatório de julho inclui as tarefas que venciam em julho, ainda que tenham sido criadas em junho.

### O que contém

A folha **Tarefas** leva **uma linha por tarefa e pessoa atribuída**, agrupadas por tarefa. Uma tarefa de três pessoas ocupa três linhas, e as colunas da tarefa (Empresa, Local, Cliente se o houver, Título, Estado, Prioridade, Início, Fim, os tempos, Concluída por, Avaliação e N.º de evidências) repetem-se em cada uma, de modo que ao filtrar por uma pessoa continua a ver-se de que tarefa era cada linha. Cada tarefa fecha com uma linha **Total {tarefa}** e o relatório, com **Total do período**. O sinal **−** da margem esquerda do Excel recolhe as pessoas de uma tarefa e deixa só o seu total.

É o formato pensado para que um contabilista trabalhe com ele: uma linha por pessoa e tarefa permite somar, filtrar e fazer tabelas dinâmicas por pessoa, por posto, por cliente ou por complemento sem desfazer nada à mão.

As colunas da pessoa:

| Coluna | O que é |
|---|---|
| **Pessoa** | Quem estava atribuído. |
| **Posto** | Com que posto trabalhou nessa tarefa: o escolhido ao atribuí-la ou, se não se escolheu, o seu predefinido. Ver [Vários postos para a mesma pessoa](../02-funcionarios/140-varios-postos-para-a-mesma-pessoa.md). |
| **Horas da pessoa** | As suas horas na tarefa. |
| **Origem das horas** | *Registos*, se a pessoa registou na tarefa; *Relógio da tarefa*, se não houve registos e as horas saem de quando foi iniciada e terminada, menos as pausas. Se uma jornada ficou sem saída, indica-o: *Registos · 1 sem saída*. |
| **Preço por hora** | O preço do posto com que trabalhou, tal como estava no dia do registo. |
| **Custo do posto** | Horas pelo preço por hora. |
| **Complementos** | Os que recebeu nessa tarefa, com o seu valor entre parênteses. Ver [Complementos](../02-funcionarios/141-complementos.md). |
| **Complementos (valor)** | O que somam. |
| **Custo da pessoa** | Custo do posto mais complementos. |

A linha **Total** de cada tarefa soma as horas e o custo da sua gente, os complementos, o material se tiver inventário e o **custo bruto** da tarefa.

Se alguma tarefa do relatório tiver cliente, acrescenta-se a coluna **Cliente** a seguir a **Local** (ver [O cliente na tarefa](../17-carteira-de-clientes/119-o-cliente-na-tarefa.md)).

As colunas de dinheiro vê-as quem pode gerar o relatório: o proprietário e os administradores. Os valores **não levam símbolo de moeda**: a moeda da sua empresa indica-se uma vez no cabeçalho de cada folha (*Moneda: EUR*) e configura-se em [Configuração da entidade](../08-sucursais-e-entidade/61-configuracao-da-entidade.md#dados-da-empresa). Uma pessoa sem preço no seu posto deixa o custo vazio, não a zero.

**Concluída por** indica quem fechou a tarefa; se foi fechada a partir do painel, leva *(a partir da administração)*, e o início e o fim são as horas que foram indicadas ao fechá-la. Ver [fechá-la a partir da administração](./127-quem-termina-a-tarefa-e-fecho-a-partir-da-administracao.md).

Convém ler bem as colunas de tempo:

| Coluna | O que mede |
|---|---|
| **Tempo investido (h)** | O tempo decorrido entre o início e o fim da tarefa. Não é tempo trabalhado: uma tarefa que se começa na sexta-feira e se termina na segunda-feira inclui o fim de semana. |
| **Em pausa (h)** | A soma das pausas da tarefa. |
| **N.º de pausas** | Quantas vezes foi pausada. |
| **Tempo investido sem pausas (h)** | O tempo investido menos o tempo em pausa. Desconta as pausas que alguém registou, não as interrupções que ninguém marcou. |

Uma tarefa que ainda não foi iniciada deixa as colunas de pausa vazias. Se uma tarefa estiver em pausa ao gerar o relatório, a pausa aberta conta até esse momento.

### As folhas «Por pessoa» e «Complementos»

O ficheiro traz mais duas folhas, que saem das mesmas linhas:

- **Por pessoa**: o resumo do período, uma linha por pessoa: quantas tarefas, horas, com que postos, custo do posto, complementos (valor), custo total e, em **Complementos do período**, que complementos recebeu e quantas vezes. É a folha para preparar o processamento salarial ou conferir com o gabinete de contabilidade.
- **Complementos**: o rasto. Uma linha por complemento recebido, com a tarefa, o local, o cliente, a pessoa, o seu posto, o complemento, o seu tipo e o seu valor, as horas, o preço por hora, o **valor** e a **origem**: o registo de entrada de que sai ou, se a tarefa não teve registos, a atribuição da tarefa. No fim, como se calcula cada tipo. Se no período não se recebeu nenhum, a folha indica-o.

### Incidências

Se alguma tarefa do período teve uma [incidência](./125-incidencia-na-tarefa.md), a folha **Tarefas** ganha a coluna **Incidência**: *Aberta* (a vermelho) ou *Resolvida · Replaneada*, *Cancelada* ou *Resolvida*.

O ficheiro traz além disso sempre a folha **Incidências**, com uma linha por incidência, aberta ou resolvida: Local, Cliente, Tarefa, Estado da tarefa, Marcada, Marcada por, Nota, Ficheiro, Incidência, Resolução, Resolvida, Resolvida por e Nota de resolução. Se no período não houve nenhuma, a folha indica-o.

### Material de cada tarefa

Se a sua empresa tiver o [inventário](../16-inventario/100-o-que-e-o-inventario.md) contratado (ou em experiência), o relatório responde também a uma pergunta que a folha de trabalho raramente responde: **que material se gastou em cada serviço e quanto custou**.

A folha de tarefas ganha três colunas no fim:

| Coluna | O que é |
|---|---|
| **Material** | O consumido na tarefa: cada artigo com a sua quantidade, e os equipamentos pelo seu exemplar. |
| **Por acertar** | O que saiu e ninguém declarou nem devolveu. É o que convém rever antes de validar. |
| **Custo do material** | O consumido pelo seu custo unitário. Vazio se nenhum artigo tiver custo na ficha. Vai na linha **Total** da tarefa. |

E o ficheiro traz mais uma folha, **Material**, com uma linha por tarefa e artigo ou exemplar: armazém de onde saiu, quantidades reservada, saída, consumida, devolvida e por acertar, custo, e para os equipamentos o seu período de reserva e o seu uso. É a folha para filtrar ou fazer tabelas dinâmicas.

Sem o inventário, o relatório é exatamente o de sempre.

### Se não houver resultados

Se nenhuma tarefa cumprir os filtros selecionados, o sistema indica-o e não gera um ficheiro vazio. Alargue o período ou reveja os filtros de sucursal e estado.

---

## Histórico de relatórios

Todos os relatórios gerados ficam listados na secção **Relatórios**, identificados por tipo (tarefas ou registo de jornada) e por formato (Excel ou PDF), com a data de geração e o período abrangido. A partir daí descarregam-se as vezes que forem necessárias sem os voltar a gerar.

---

## Análise agregada do desempenho

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

As métricas agregadas calculadas pela plataforma —taxa de conclusão, tempo médio de resolução, taxa de recusa e avaliação média por período— e as comparações automáticas entre sucursais estão planeadas para uma versão futura. Hoje essas análises podem ser construídas a partir do relatório em Excel.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Vários postos para a mesma pessoa](../02-funcionarios/140-varios-postos-para-a-mesma-pessoa.md) | De onde sai a coluna Posto e o seu preço por hora |
| [Complementos](../02-funcionarios/141-complementos.md) | O que são, os três tipos e onde se escolhem |
| [Avaliação do trabalhador](./46-avaliacao-do-trabalhador.md) | Como se geram as pontuações de desempenho |
| [Prioridades e prazos](./44-prioridades-e-prazos.md) | Configuração de prazos que afeta o acompanhamento |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Significado dos estados e do cumprimento temporal |
| [Tipos de relatório](../11-relatorios-e-exportacao/76-tipos-de-relatorio.md) | Todos os relatórios disponíveis na plataforma |
| [Exportar dados](../11-relatorios-e-exportacao/78-exportar-para-excel-e-csv.md) | Formatos de exportação disponíveis |
