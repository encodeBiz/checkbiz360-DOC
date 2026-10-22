# Tipos de notificação

O CheckBiz360 gera notificações automáticas para informar os vários utilizadores da plataforma sobre eventos relevantes em tempo real. As notificações estão organizadas por categorias consoante a área operacional a que pertencem, e cada tipo tem destinatários predefinidos consoante o perfil de cada utilizador. Este artigo descreve todas as categorias e tipos de notificação disponíveis no sistema.

## Categorias de notificação

### Notificações de assiduidade

As notificações de assiduidade informam sobre eventos relacionados com o registo de jornada dos funcionários.

| Tipo | Descrição | Destinatários |
|---|---|---|
| Funcionário que não registou | Gerada quando um funcionário com turno ativo não registou a entrada passada a hora configurada como limiar | Manager, Supervisor |
| Jornada incompleta | Gerada no fim do turno se o funcionário não tiver registado a saída | Manager, Supervisor, Worker |
| Registo suspeito | Gerada quando o sistema deteta que um registo apresenta um indicador de anomalia | Manager |
| Registo fora da geocerca | O funcionário registou a partir de uma localização fora do raio definido para a sua sucursal | Manager, Supervisor |
| Jornada manual aprovada | Notifica o funcionário de que o seu pedido de jornada manual foi aprovado pelo responsável | Worker |
| Jornada manual recusada | Notifica o funcionário de que o seu pedido de jornada manual foi recusado | Worker |

### Notificações de documentos

As notificações de documentos gerem a distribuição de documentos e o acompanhamento da confirmação de leitura.

| Tipo | Descrição | Destinatários |
|---|---|---|
| Novo documento disponível | Enviada ao funcionário quando lhe é atribuído um documento para consulta | Worker |
| Confirmação de leitura pendente | Lembrete de que um documento atribuído está pendente de confirmação | Worker |

> **Nota:** a plataforma gere **confirmação de leitura**, não assinatura eletrónica. Não existe, portanto, uma notificação de «documento assinado» nem de recusa de assinatura.

### Notificações de tarefas

As notificações de tarefas mantêm funcionários e responsáveis informados sobre o estado das tarefas atribuídas.

| Tipo | Descrição | Destinatários |
|---|---|---|
| Nova tarefa atribuída | Enviada ao funcionário quando lhe é atribuída uma nova tarefa | Worker |
| Tarefa retirada | A tarefa foi apagada, cancelada ou já não está atribuída ao funcionário | Worker |
| Lembrete de vencimento | Alerta de que uma tarefa atribuída vence nas próximas horas ou no dia seguinte | Worker |
| Tarefa concluída | Notifica o responsável de que o funcionário marcou a tarefa como concluída | Manager, Supervisor |
| Tarefa pendente de validação | O funcionário concluiu a tarefa e o sistema aguarda a validação do responsável | Manager, Supervisor |
| Tarefa validada | Notifica o funcionário de que a sua tarefa foi validada pelo responsável | Worker |
| Tarefa recusada | Notifica o funcionário de que a sua tarefa foi recusada e exige revisão | Worker |

### Alertas de segurança

Os alertas de segurança são notificações de alta prioridade relacionadas com a integridade do sistema e a autenticação. Não podem ser desativados.

| Tipo | Descrição | Destinatários |
|---|---|---|
| Registo suspeito | Registo marcado como potencialmente fraudulento pelo motor de análise | Manager, Owner |
| Dispositivo não autorizado | É detetada uma tentativa de registo a partir de um dispositivo que não foi autorizado para o funcionário | Manager, Owner |
| Acesso a partir de nova localização | Início de sessão no backoffice a partir de um endereço IP ou localização invulgar | Utilizador afetado, Owner |
| Tentativa de acesso falhada repetida | Ocorreram várias tentativas falhadas consecutivas de acesso a uma conta | Utilizador afetado, Owner |

> **Aviso:** os alertas de segurança não podem ser desativados por nenhum utilizador, independentemente do seu perfil ou configuração de preferências. A sua receção está garantida por conceção, para proteger a integridade operacional da plataforma.

### Notificações administrativas

As notificações administrativas informam sobre processos que exigem intervenção manual por parte dos responsáveis.

| Tipo | Descrição | Destinatários |
|---|---|---|
| Jornada manual pendente de aprovação | Um funcionário solicitou o registo manual de uma jornada que exige validação | Manager, Supervisor |
| Pedido de férias ou licença | Não se envia aviso: o pedido aparece em **Contacto → Pedidos**, com o número de pendentes no separador | Owner, administradores |
| Férias ou licença aprovadas / recusadas | Avisa a pessoa da decisão e leva-a a **O meu calendário** (com a próxima versão da aplicação) | Worker |
| Novo funcionário ativado | Um novo funcionário completou o processo de ativação da sua conta | Manager, Owner |
| Acesso que não chegou | Alerta da página inicial do painel quando o e-mail de acesso de alguém foi devolvido, marcado como spam ou não saiu | Owner, administradores |

## Canais de entrega

As notificações do CheckBiz360 são enviadas através de dois canais principais:

- **Notificação push na aplicação**: para os funcionários (Workers) e, quando é o caso, para os responsáveis que tenham a aplicação instalada.
- **Notificação no backoffice**: aparece no centro de notificações do painel de administração, visível para Manager, Supervisor e Owner.

Alguns tipos de notificação dispõem adicionalmente de um canal de recurso por correio eletrónico para garantir a sua entrega mesmo quando o dispositivo não está disponível. Os detalhes sobre configuração de canais e preferências são descritos nos artigos correspondentes desta secção.

---

> **Nota de perfil:** a visualização de notificações depende do perfil do utilizador. Cada perfil recebe apenas as notificações que lhe dizem respeito segundo a tabela acima. O Owner recebe todas as notificações administrativas e de segurança de forma consolidada para toda a entidade.

## Artigos relacionados

- [Notificações push na aplicação](64-notificacoes-push-na-aplicacao.md)
- [Configurar preferências de notificação](65-configurar-preferencias-de-notificacao.md)
- [Alertas para responsáveis](66-alertas-para-responsaveis.md)
- [Histórico de notificações](67-historico-de-notificacoes.md)
- [Notificações por email](68-notificacoes-por-email.md)
