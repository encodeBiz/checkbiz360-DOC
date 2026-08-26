# Alertas para responsáveis

Os alertas para responsáveis são notificações de carácter operacional que o sistema envia aos perfis Manager e Supervisor quando ocorrem eventos que exigem atenção ou ação por parte da equipa de gestão. Ao contrário das notificações dirigidas aos funcionários, estes alertas foram concebidos para detetar irregularidades, garantir o cumprimento dos processos e permitir uma resposta rápida perante situações que possam afetar a operação. Este artigo descreve os tipos de alerta disponíveis, como configurá-los e como ajustar os limiares de ativação.

## Tipos de alerta para responsáveis

### Funcionário que não registou

Este alerta é enviado ao Manager e ao Supervisor da sucursal quando um funcionário com turno ativo não registou a entrada passada uma determinada hora. É o alerta mais utilizado em operações com turnos definidos, uma vez que permite ao responsável saber de imediato quem falta antes de a ausência afetar a operação.

O alerta inclui:
- Nome do funcionário.
- Sucursal e turno a que se devia ter apresentado.
- Hora de início do turno e tempo decorrido desde então.

### Jornada manual pendente de aprovação

Quando um funcionário solicita o registo manual de uma jornada (por não ter conseguido registar no momento correspondente), o sistema envia um alerta ao responsável para que reveja e aprove ou recuse o pedido. O alerta inclui o motivo indicado pelo funcionário e uma ligação direta ao registo para tratar do pedido.

> **Aviso:** os pedidos de jornada manual não aprovados no prazo de 48 horas geram um alerta adicional de lembrete. Se o período de processamento salarial fechar com pedidos pendentes, o sistema assinalá-lo-á como uma incidência de conformidade.

### Registo marcado como suspeito

O motor de análise do CheckBiz360 avalia cada registo em contexto e pode marcá-lo com um indicador de anomalia quando deteta características irregulares, como:

- Mudança abrupta de localização GPS entre registos consecutivos.
- Coordenadas GPS inconsistentes com o movimento físico possível no tempo decorrido.
- Padrões de registo que coincidem com comportamentos conhecidos de evasão ao controlo.
- Registo a partir de um dispositivo diferente do habitual sem autorização prévia.

Quando este alerta é gerado, o responsável recebe a notificação com o detalhe do registo suspeito e pode decidir validá-lo, modificá-lo ou escaloná-lo para investigação.

### Funcionário fora da geocerca de forma repetida

Se um funcionário efetuar registos fora do raio definido para a sua sucursal de forma recorrente (o limiar por omissão é três vezes numa semana), o sistema gera um alerta consolidado dirigido ao Manager. Este alerta é diferente da notificação individual de «registo fora da geocerca»: não é gerado em cada ocorrência individual, mas quando o padrão se torna sistemático.

## Como configurar que alertas cada responsável recebe

O Owner e o Manager podem ajustar a distribuição de alertas a partir do backoffice:

1. Aceda a **Sucursais** e abra a sucursal para a qual pretende configurar alertas.
2. Selecione o separador **Responsáveis** ou **Configuração de alertas**.
3. Verá a lista de Managers e Supervisores atribuídos a essa sucursal.
4. Prima o ícone de configuração junto ao nome do responsável para ajustar que tipos de alerta recebe.
5. Ative ou desative os tipos de alerta consoante as responsabilidades desse responsável.
6. Prima **Guardar**.

Esta configuração permite, por exemplo, que o Supervisor receba os alertas de registo e ausência do dia a dia, enquanto o Manager recebe apenas os alertas de registos suspeitos e jornadas manuais pendentes.

## Configurar o limiar de hora limite de entrada

O alerta de «funcionário que não registou» exige que se defina uma hora limite de entrada para cada turno. Se o turno começar às 08:00 e a hora limite estiver configurada em 30 minutos, o alerta será gerado às 08:30 se o funcionário não tiver registado.

Para configurar este limiar:

1. Aceda a **Organização** > **Calendários** e abra o calendário que contém o turno que pretende configurar.
2. Selecione o turno específico e localize o campo **Tolerância de alerta de entrada** (expresso em minutos).
3. Introduza o número de minutos após a hora de início do turno a partir do qual o sistema deve gerar o alerta.
4. Guarde as alterações. O novo limiar aplicar-se-á a partir do dia seguinte.

> **Aviso:** um limiar demasiado baixo (por exemplo, 5 minutos) pode gerar um volume excessivo de alertas por atrasos menores e normais nos transportes ou no acesso ao local. Recomenda-se começar com um limiar entre 15 e 30 minutos e ajustá-lo em função da operação real da sucursal.

## Receção de alertas: backoffice e notificação push

Os responsáveis recebem os alertas através de dois canais em simultâneo:

- **Centro de notificações do backoffice**: visível no ícone de sino da barra superior. Os alertas não lidos são mostrados com um indicador numérico e permanecem no centro até que o responsável os reveja.
- **Notificação push na aplicação**: se o Manager ou o Supervisor tiver a aplicação CheckBiz360 instalada e tiver iniciado sessão, os alertas também são recebidos como notificações push no seu dispositivo móvel.

Os alertas críticos (registo suspeito, dispositivo não autorizado) dispõem adicionalmente de um canal de recurso por correio eletrónico que garante a sua entrega ainda que o responsável não tenha a aplicação ativa.

## Gestão dos alertas recebidos

A partir do centro de notificações do backoffice, o responsável pode:

- **Marcar como revisto**: indica que o alerta foi visto e processado.
- **Aceder ao recurso**: navegar diretamente para o registo, a jornada ou o funcionário a que o alerta se refere.
- **Acrescentar comentário interno**: registar uma nota sobre a gestão realizada, visível para outros responsáveis da mesma sucursal.

Os alertas revistos são arquivados automaticamente e ficam disponíveis no histórico de notificações.

---

> **Nota de perfil:** os alertas para responsáveis estão disponíveis para os perfis **Manager** e **Supervisor**. O **Owner** recebe os alertas críticos de segurança para toda a entidade. O perfil **Worker** não tem acesso aos alertas operacionais.

## Artigos relacionados

- [Tipos de notificação](63-tipos-de-notificacao.md)
- [Configurar preferências de notificação](65-configurar-preferencias-de-notificacao.md)
- [Histórico de notificações](67-historico-de-notificacoes.md)
- [Vista global multi-sucursal](../08-sucursais-e-entidade/62-vista-global-multi-sucursal.md)
