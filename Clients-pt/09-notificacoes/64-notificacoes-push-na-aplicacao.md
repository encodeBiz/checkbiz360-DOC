# Notificações push na aplicação

As notificações push são o canal principal através do qual o CheckBiz360 comunica eventos relevantes aos funcionários em tempo real. Quando ocorre um evento que exige a atenção do funcionário —uma tarefa atribuída, um documento pendente de confirmação de leitura, uma aprovação de jornada— o sistema envia uma notificação diretamente para o dispositivo móvel, mesmo que a aplicação não esteja aberta nesse momento. Este artigo explica como funcionam estas notificações, que informação contêm e o que fazer se não chegarem corretamente.

## Como as notificações push chegam ao dispositivo

Quando é gerado um evento no CheckBiz360 que tem um funcionário como destinatário, o servidor envia uma notificação push através do serviço de mensagens do sistema operativo do dispositivo: APNs (Apple Push Notification service) para dispositivos iOS e FCM (Firebase Cloud Messaging) para dispositivos Android.

O processo completo, desde que o evento é gerado até que a notificação aparece no ecrã do funcionário, demora habitualmente menos de cinco segundos se o dispositivo estiver ligado à internet. Se o dispositivo estiver sem ligação no momento do envio, a notificação será entregue assim que recuperar a conectividade, desde que não tenha decorrido o tempo de expiração do sistema operativo (geralmente 24 horas).

## Que informação contém cada notificação

O conteúdo de cada notificação varia consoante o seu tipo, mas todas incluem no mínimo:

- **Título**: identifica o tipo de evento de forma concisa (por exemplo, «Novo documento disponível» ou «Tarefa atribuída»).
- **Corpo**: breve descrição do evento com o dado mais relevante (nome do documento, nome da tarefa, nome do responsável que aprovou a jornada).
- **Marca temporal**: momento em que o evento foi gerado.

Alguns tipos de notificação incluem informação adicional:

- As notificações de **documentos pendentes de confirmação de leitura** incluem o nome do documento.
- As notificações de **tarefas** incluem o nome da tarefa, a data de vencimento e a sucursal ou projeto a que está associada.
- As notificações de **jornada** incluem o resultado da validação (aprovada ou recusada) e, em caso de recusa, o motivo indicado pelo responsável.

## Comportamento ao tocar na notificação

Tocar numa notificação push abre a aplicação CheckBiz360 e navega diretamente para o recurso a que essa notificação se refere. Não é necessário procurar manualmente a informação dentro da aplicação; o sistema leva o funcionário ao local exato onde deve agir.

| Tipo de notificação | Destino na aplicação |
|---|---|
| Novo documento / Confirmação pendente | Ecrã de detalhe do documento com o botão de confirmação de leitura visível |
| Tarefa atribuída / Lembrete de vencimento | Ecrã de detalhe da tarefa com as ações disponíveis |
| Jornada aprovada / recusada | Registo de jornada correspondente |
| Alerta de segurança | Ecrã de segurança da conta |

Se a aplicação não estiver instalada no dispositivo ou o funcionário não tiver iniciado sessão, tocar na notificação abrirá a loja de aplicações ou o ecrã de início de sessão, consoante o caso.

## Requisitos para receber notificações push

Para que as notificações push funcionem corretamente devem cumprir-se as seguintes condições:

1. **A aplicação CheckBiz360 tem de estar instalada** no dispositivo do funcionário (iOS ou Android).
2. **O funcionário tem de ter iniciado sessão** pelo menos uma vez na aplicação, para que o sistema registe o token de dispositivo necessário para o envio.
3. **As permissões de notificação têm de estar concedidas** no sistema operativo do dispositivo. Se o funcionário recusou as permissões durante a instalação, as notificações não chegarão ainda que o sistema as envie corretamente.
4. **O dispositivo tem de ter ligação à internet** nalgum momento dentro do período de validade da notificação.

> **Aviso:** o sistema operativo do dispositivo pode limitar ou atrasar as notificações em função do modo de poupança de bateria, do modo não incomodar ou de restrições de segundo plano da aplicação. Se o funcionário tiver algum destes modos ativado, pode não receber as notificações de forma imediata.

## O que fazer se as notificações não chegarem

Se um funcionário não receber as notificações push, siga estes passos de diagnóstico por ordem:

### 1. Verificar as permissões do sistema operativo

**Em iOS:**
1. Abra **Definições** no iPhone ou iPad.
2. Desça até à aplicação **CheckBiz360** e toque nela.
3. Aceda a **Notificações** e verifique que o interruptor principal está ativado.
4. Certifique-se de que o tipo de alerta selecionado é **Ecrã bloqueado**, **Centro de notificações** ou **Faixas**, ou todos eles.

**Em Android:**
1. Mantenha premido o ícone da aplicação **CheckBiz360** e selecione **Informação da aplicação**.
2. Toque em **Notificações** e verifique que estão ativadas.
3. Confirme que não há canais de notificação específicos desativados.

### 2. Verificar que a sessão está ativa

O funcionário deve ter uma sessão ativa na aplicação. Se a sessão tiver expirado por inatividade prolongada, o token de dispositivo pode ter ficado desatualizado. Terminar sessão e voltar a iniciá-la regenera o token e restabelece a receção de notificações.

### 3. Verificar a ligação à internet

Certifique-se de que o dispositivo tem ligação ativa à internet, seja por WiFi seja por dados móveis.

### 4. Contactar o apoio

Se os passos anteriores não resolverem o problema, contacte a equipa de apoio do CheckBiz360 indicando o sistema operativo e a versão do dispositivo, a versão da aplicação instalada e o tipo de notificação que não está a receber.

---

> **Nota de perfil:** as notificações push na aplicação destinam-se principalmente ao perfil **Worker**. Os perfis **Manager** e **Supervisor** também podem receber notificações push se tiverem a aplicação instalada, embora o seu canal principal de notificações seja o backoffice web.

## Artigos relacionados

- [Tipos de notificação](63-tipos-de-notificacao.md)
- [Configurar preferências de notificação](65-configurar-preferencias-de-notificacao.md)
- [Histórico de notificações](67-historico-de-notificacoes.md)
- [Notificações por email](68-notificacoes-por-email.md)
