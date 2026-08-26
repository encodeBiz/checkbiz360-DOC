# Tipos de relatório disponíveis no CheckBiz360

O CheckBiz360 centraliza a informação operacional da sua empresa de duas formas distintas, e convém não as confundir:

- **Relatórios descarregáveis**, que se geram a pedido a partir da secção **Relatórios**, ficam arquivados no histórico e são descarregados como ficheiro. Hoje são dois: o **relatório de assiduidade** (PDF ou Excel) e o **relatório de tarefas** (Excel).
- **Análises no ecrã**, que se consultam no painel operacional e nas fichas de sucursal e de funcionário: pontualidade, custos e anomalias. Não geram ficheiro descarregável na versão atual.

Este guia descreve cada um e os perfis que têm acesso.

---

## Relatório de assiduidade

O relatório de assiduidade é o documento base do módulo. Reúne os dados de presença dos funcionários num período determinado e permite obter uma visão completa do comportamento horário da equipa.

### O que inclui

- Listagem de presenças e ausências por funcionário e dia.
- Horas trabalhadas totais por funcionário no período selecionado.
- Desagregação por turno, sucursal ou período.
- Estado de cada jornada: completa, ausência justificada, ausência não justificada, jornada parcial.

### Para que serve

É o relatório mais utilizado para a supervisão operacional diária e para o cálculo de variáveis salariais como horas extraordinárias ou descontos por ausência. É também a base do relatório de conformidade legal descrito no artigo [79](./79-relatorio-de-conformidade-legal.md).

### Acesso por perfil

| Perfil | Acesso |
|---|---|
| Owner | Todas as sucursais e todos os funcionários |
| Manager | Funcionários das sucursais que gere |
| Supervisor | Funcionários da sua equipa direta, se o manager o tiver ativado |
| Worker | Apenas os seus próprios dados de assiduidade a partir da aplicação |

---

## Análises no ecrã: pontualidade, custos e anomalias

Estas três leituras **não são relatórios descarregáveis**: consultam-se no painel de Operação e nas fichas de sucursal e de funcionário. A exportação dos seus dados está no roadmap.

### Pontualidade e desvios de horário

Reúne os atrasos, as saídas antecipadas e o desvio acumulado entre as horas previstas e as efetivamente trabalhadas. Permite distinguir se a impontualidade é pontual ou um padrão, e se é de uma pessoa ou de um local inteiro.

### Custos

Cruza a assiduidade com a tarifa horária configurada na associação de cada funcionário à sua sucursal: custo por hora trabalhada, por jornada, por rendimento e acumulado do período.

Contém informação sensível e só é acessível a **Owner** e **Manager**. Requer que as tarifas estejam configuradas: sem elas, os indicadores económicos aparecem vazios.

### Anomalias

Reúne os registos que o sistema identificou como potencialmente irregulares —precisão temporal excessiva, geolocalização estática, dispositivos não autorizados— juntamente com as correções manuais efetuadas sobre registos, com o seu autor, o seu momento e o seu motivo.

Afloram no separador **Análise** do painel, que ordena a leitura do menos para o mais assinalável: primeiro o processo e a configuração, no fim as pessoas. Exclusivo de **Owner** e **Manager**.

---

## Relatório de tarefas

O relatório de tarefas reúne as tarefas do período com o seu estado e o seu cumprimento de prazo. É um **relatório descarregável em Excel (XLSX)**.

### O que inclui

- As tarefas cujo **prazo** cai dentro do período selecionado, com o seu estado e o seu cumprimento temporal.
- Filtros por sucursal e por estado da tarefa.
- Os dados necessários para calcular na folha de cálculo o que for preciso: concluídas face a atribuídas, vencidas, recusadas.

> **Nota:** as métricas agregadas já calculadas —percentagem de conclusão, tempo médio de resolução, avaliação média— estão no roadmap. Hoje o relatório entrega o detalhe e o cálculo faz-se na folha.

### Para que serve

Complementa o controlo de presenças com dados sobre a atividade real realizada durante a jornada. Permite avaliar o desempenho da equipa com critérios objetivos e documentados.

### Acesso por perfil

| Perfil | Acesso |
|---|---|
| Owner | Todas as sucursais |
| Manager | Sucursais que gere |
| Supervisor | A sua equipa direta, se o manager o ativar |
| Worker | Apenas as suas próprias tarefas a partir da aplicação |

---

> **Nota:** as análises de custos e de anomalias contêm informação especialmente sensível. Certifique-se de que apenas os perfis com acesso autorizado têm credenciais ativas na plataforma. Reveja periodicamente os utilizadores com perfil de Manager ou Owner na secção de gestão de equipa.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Gerar e filtrar relatórios](./77-gerar-e-filtrar-relatorios.md) | Passos para gerar um relatório com filtros personalizados |
| [Exportar dados](./78-exportar-para-excel-e-csv.md) | Formatos de exportação e considerações de utilização |
| [Relatório de conformidade legal](./79-relatorio-de-conformidade-legal.md) | O relatório para o RDL 8/2019 e a Inspeção do Trabalho |
| [Relatórios automáticos](./80-relatorios-automaticos.md) | Envio periódico por email: planeado, não disponível |
| [Deteção de anomalias](../07-inteligencia-operacional/55-detecao-de-anomalias.md) | Como funciona o mecanismo de deteção automática |
