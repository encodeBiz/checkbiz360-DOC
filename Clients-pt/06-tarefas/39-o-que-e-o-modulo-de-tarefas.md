# O que é o módulo de tarefas

O módulo de tarefas do CheckBiz360 permite aos responsáveis da empresa criar, atribuir e acompanhar atividades operacionais concretas. Ao contrário do controlo de horários, que regista quando um funcionário trabalha, o módulo de tarefas regista o que esse funcionário faz durante a sua jornada e se o concluiu corretamente.

Trata-se de uma ferramenta complementar que dá visibilidade sobre o trabalho realmente realizado em cada turno, sucursal ou departamento.

---

## Diferença entre tarefas e registos de ponto

O controlo de horários e o módulo de tarefas têm objetivos distintos e complementam-se.

| Aspeto | Controlo de horários | Módulo de tarefas |
|---|---|---|
| O que regista | Presença: entrada e saída | Atividade: o que foi feito |
| Unidade de medida | Tempo trabalhado | Tarefa concluída ou não |
| Quem atua | O funcionário regista | O funcionário atualiza o estado |
| Para que serve | Processamento salarial e conformidade legal | Acompanhamento operacional e desempenho |

Um funcionário pode ter registado corretamente e ainda assim não ter concluído as tarefas atribuídas para esse turno. O módulo de tarefas permite detetar essa diferença.

---

## Casos de utilização habituais

### Lista de verificação de abertura e fecho do estabelecimento

Os comércios e espaços de atendimento ao público precisam de que se realizem uma série de ações concretas antes de abrir ou ao fechar. O responsável cria uma tarefa de abertura e escreve os passos como **lista de verificação na descrição**, que o funcionário de turno segue a partir da aplicação e confirma ao terminar.

### Tarefas de manutenção

As avarias técnicas ou as revisões periódicas de instalações podem ser geridas como tarefas atribuídas ao responsável de manutenção. O sistema guarda o histórico de execução e permite anexar evidências em foto ou vídeo do resultado.

### Atividades de formação

Quando um funcionário deve concluir um módulo de formação, visualizar um documento corporativo ou assistir a uma sessão interna, essa obrigação pode transformar-se numa tarefa com prazo. O manager pode verificar quem a concluiu e quem não.

### Acompanhamento de objetivos operacionais

Os objetivos de curto prazo —repor stock, contactar uma lista de clientes, concluir um relatório— podem ser decompostos em tarefas atribuídas às pessoas adequadas, com prioridade e prazo claramente definidos.

### Serviços ao domicílio ou em casa do cliente

Quando o trabalho muda de morada todos os dias —uma reparação, uma limpeza, uma visita técnica—, a tarefa pode levar o seu **próprio local de trabalho** sem criar uma sucursal por serviço. O funcionário só a pode iniciar estando nessa morada. Explica-se em [Criar uma tarefa](./40-criar-uma-tarefa.md#local-de-trabalho-próprio).

### Trabalho que se repete

Um trabalho que se repete com poucas variações não precisa de ser escrito de novo: a tarefa **duplica-se** a partir da listagem ou da sua ficha, e a cópia só pede título e datas. Explica-se em [Criar uma tarefa](./40-criar-uma-tarefa.md#duplicar-uma-tarefa).

---

## Perfis que interagem com o módulo

O módulo de tarefas respeita a hierarquia de perfis do CheckBiz360. Cada perfil tem capacidades distintas:

### Owner e Manager

Têm acesso completo ao módulo. Podem criar, atribuir, modificar e cancelar tarefas em qualquer sucursal da entidade, validá-las e avaliar o desempenho do funcionário.

### Supervisor

O seu âmbito decide-se **em cada tarefa**, e não no seu perfil. Toda a tarefa inclui duas opções —**Permitir validação por supervisor** e **Permitir avaliação por supervisor**, ambas ativadas por omissão— que habilitam o supervisor da sucursal a fechar o circuito dessa tarefa concreta. A criação de tarefas por supervisores está desativada por omissão.

### Worker (funcionário)

Recebe as tarefas atribuídas, consulta a sua descrição e as suas evidências, inicia o trabalho, pausa-o e retoma-o quando tem de o interromper, adiciona notas de progresso, carrega evidências e marca a tarefa como concluída. Não pode criar nem atribuir tarefas a outros funcionários.

---

## Relação com o controlo de horários

Tarefas e registos medem coisas distintas, mas não andam em separado: para **iniciar**, **retomar** ou **concluir** uma tarefa, o funcionário tem de ter a **jornada aberta**, ou seja, ter registado a entrada. Estar numa pausa conta como jornada aberta. Se não tiver registado a entrada, a ação é recusada com o erro `task/no_open_session`.

**Pausar** não o exige: pausa-se precisamente no momento de sair.

Os proprietários e administradores que atuam a partir do backoffice não têm jornada para abrir e ficam isentos; assim podem, por exemplo, fechar a tarefa de alguém que já saiu. Um supervisor ou manager que trabalha com a sua própria ficha de funcionário precisa, sim, de ter a jornada aberta.

As datas, pelo contrário, são livres: uma tarefa pode ter o prazo num feriado ou fora do horário habitual, se a operação o exigir.

---

> **Nota:** para aproveitar ao máximo o módulo de tarefas, recomendamos combiná-lo com o módulo de relatórios operacionais. Os dados de conclusão de tarefas alimentam os indicadores de eficiência da equipa na secção de inteligência operacional.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](./40-criar-uma-tarefa.md) | Campos, passos e opções ao criar uma tarefa |
| [Atribuir tarefas a funcionários](./41-atribuir-tarefas-a-funcionarios.md) | Atribuição individual e por equipa |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida completo de uma tarefa |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Iniciar, pausar, retomar e o histórico da tarefa |
| [Validação de tarefas](./45-validacao-de-tarefas.md) | Fluxo de validação e permissões |
| [Relatórios de tarefas](./48-relatorios-de-tarefas.md) | Métricas e exportação de dados |
