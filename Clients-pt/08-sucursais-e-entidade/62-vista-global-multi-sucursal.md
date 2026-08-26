# Vista global multi-sucursal

O painel global do CheckBiz360 é a ferramenta de supervisão consolidada para organizações que operam em várias sucursais. A partir de um único ecrã, os responsáveis podem ver o estado de assiduidade de toda a organização em tempo real, comparar o desempenho entre locais, detetar anomalias e exportar dados consolidados sem necessidade de navegar sucursal a sucursal. Este artigo descreve as funcionalidades do painel global e como tirar delas o maior partido.

## A quem se dirige esta vista

A vista global foi concebida para perfis que supervisionam operações à escala: diretores de operações com várias lojas, responsáveis de recursos humanos de empresas multi-local, gestores regionais ou qualquer pessoa que precise de uma visão de conjunto antes de entrar no detalhe de cada sucursal.

Um exemplo de caso de utilização típico é o de um diretor de operações com 20 lojas que, às 9:30 da manhã, quer saber em menos de um minuto quantas lojas têm funcionários que ainda não registaram, que locais estão a operar com o pessoal completo e em qual há uma anomalia crítica que exige atenção imediata.

## Como aceder ao painel global

1. Aceda ao backoffice web e inicie sessão com um perfil de **Owner** ou **Manager** com acesso a várias sucursais.
2. No menu lateral, selecione **Painel global** ou **Dashboard**.
3. O sistema carregará automaticamente a vista consolidada com os dados do dia em curso.

## Vista de assiduidade consolidada hoje

A secção principal do painel global mostra, para o dia em curso, o estado de assiduidade de todos os funcionários de todas as sucursais a que o utilizador tem acesso. A informação organiza-se por sucursal e permite identificar de forma imediata a situação de cada local.

### KPI globais

Na parte superior do painel são apresentados os indicadores-chave de assiduidade do dia:

- **Funcionários presentes**: número e percentagem de funcionários que registaram entrada e estão atualmente ao turno.
- **Ausências**: funcionários que deviam ter registado e não o fizeram. Distingue-se entre ausências justificadas (registadas com licença aprovada) e não justificadas (sem registo nem justificação).
- **Anomalias**: registos marcados automaticamente pelo sistema como suspeitos ou irregulares, incluindo entradas tardias, saídas antecipadas, registos fora da geocerca e jornadas incompletas.
- **Pausas ativas**: funcionários que se encontram em pausa neste momento.

Os KPI atualizam-se em tempo real à medida que os funcionários vão registando ao longo do dia.

## Filtros por sucursal

O painel global permite filtrar os dados para visualizar apenas as sucursais que lhe interessam em cada momento. Os filtros disponíveis são:

- **Por sucursal específica**: selecione uma ou várias sucursais da listagem para ver apenas os seus dados.
- **Por região ou grupo**: se a sua organização tiver agrupado as sucursais por regiões ou tipologias, pode filtrar por esse agrupamento.
- **Por estado**: ative o filtro de anomalias para ver apenas as sucursais com incidências ativas.

Os filtros são acumuláveis e persistentes durante a sessão. Se abandonar o painel global e regressar, os filtros aplicados manter-se-ão.

## Comparações entre sucursais

A secção de comparações permite analisar o desempenho relativo das sucursais ao longo do tempo. As métricas disponíveis para comparação incluem:

### Custo e eficiência

- **Custo horário total**: soma do custo das horas trabalhadas por todos os funcionários de cada sucursal no período selecionado.
- **Custo médio por funcionário**: custo horário dividido pelo número de funcionários ativos na sucursal.
- **Horas trabalhadas vs. horas previstas**: percentagem de cumprimento do horário planeado.

### Assiduidade e pontualidade

- **Taxa de pontualidade**: percentagem de registos de entrada efetuados dentro da margem de tolerância configurada.
- **Taxa de ausência**: percentagem de ausências sobre o total de jornadas previstas no período.
- **Anomalias por funcionário**: número médio de anomalias por funcionário no período, útil para identificar sucursais com problemas sistemáticos de cumprimento.

As comparações podem ser visualizadas em formato de tabela ou de gráfico de barras. O período de análise é configurável: hoje, esta semana, este mês ou um intervalo personalizado.

> **Aviso:** as comparações de custo são mais precisas quando todos os funcionários têm o custo horário corretamente configurado nas suas fichas. Se algum funcionário não tiver custo configurado, essas horas são contabilizadas como custo zero e podem distorcer as métricas da sucursal.

## Exportação de dados consolidados

A partir do painel global pode exportar um relatório com os dados de todas as sucursais selecionadas num único ficheiro. O processo é o seguinte:

1. Aplique os filtros de sucursal e de período que pretende incluir no relatório.
2. Prima o botão **Exportar** no canto superior direito do painel.
3. Selecione o formato de exportação: CSV para análise em folhas de cálculo ou PDF para relatórios executivos.
4. O sistema gerará o ficheiro e descarregá-lo-á automaticamente. Para volumes grandes de dados (mais de 90 dias ou mais de 50 sucursais), a geração pode demorar alguns segundos e o ficheiro será também enviado por correio eletrónico para o endereço do utilizador.

O relatório consolidado inclui, para cada sucursal, o resumo de horas trabalhadas, ausências, anomalias e custo do período selecionado.

## Alertas ativos no painel global

O painel global integra uma secção de alertas que agrupa todas as incidências ativas em tempo real de toda a organização. A partir daqui pode:

- Ver que sucursais têm alertas por resolver.
- Aceder diretamente ao registo problemático com um único clique.
- Atribuir a gestão de um alerta a um responsável concreto.

---

> **Nota de perfil:** o painel global está disponível para os perfis **Owner** e **Manager**. O Owner vê todas as sucursais da entidade. O Manager vê apenas as sucursais a que está atribuído. O perfil **Supervisor** não tem acesso ao painel global; acede unicamente à vista da sua sucursal.

## Artigos relacionados

- [Criar e gerir sucursais](57-criar-e-gerir-sucursais.md)
- [Atribuir funcionários a sucursais](60-atribuir-funcionarios-a-sucursais.md)
- [Configuração da entidade](61-configuracao-da-entidade.md)
- [Tipos de notificação](../09-notificacoes/63-tipos-de-notificacao.md)
- [Alertas para responsáveis](../09-notificacoes/66-alertas-para-responsaveis.md)
