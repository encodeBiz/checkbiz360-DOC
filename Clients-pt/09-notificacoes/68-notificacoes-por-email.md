# Notificações por email

O CheckBiz360 envia correios eletrónicos automáticos em determinados eventos do ciclo de vida da conta. Este artigo descreve que correios o sistema envia, quando e a partir de que endereço, e o que fazer se algum destes correios não chegar ao destinatário.

## Remetente dos correios do sistema

Todos os correios automáticos do CheckBiz360 são enviados a partir do endereço `hola@encodebiz.com`. Se algum membro da sua organização não encontrar um correio esperado, deve verificar a pasta de spam ou de correio não solicitado e confirmar que este endereço não está bloqueado pelo filtro de correio empresarial.

> **Aviso:** alguns sistemas de correio empresarial com filtros estritos (como o Microsoft 365 com políticas de segurança avançadas) podem classificar os correios de `hola@encodebiz.com` como spam ou retê-los em quarentena. Se isto acontecer de forma sistemática, peça ao administrador de TI da sua organização que adicione o domínio `encodebiz.com` à lista de remetentes de confiança.

## Correios automáticos do sistema

### Boas-vindas ao novo funcionário

Quando o Owner ou um Manager adiciona um novo funcionário à plataforma e envia o convite, o sistema gera automaticamente um correio de boas-vindas dirigido ao endereço de email do funcionário. Este correio contém:

- Uma mensagem de boas-vindas à plataforma em nome da empresa.
- As credenciais de acesso iniciais: endereço de email e palavra-passe temporária.
- Uma ligação direta para descarregar a aplicação CheckBiz360 em iOS e Android.
- Instruções básicas para completar o primeiro acesso e alterar a palavra-passe temporária.

Este correio é o primeiro ponto de contacto do funcionário com a plataforma e é fundamental para que possa ativar a sua conta. Por isso, é especialmente importante que o endereço de email do funcionário esteja correto no momento de criar a sua ficha.

### Reenvio de convite

Se o funcionário não conseguiu ativar a sua conta (não encontrou o correio, a ligação expirou ou introduziu dados incorretos), o responsável pode reenviar o convite a partir do backoffice:

1. Navegue até **Funcionários** e abra a ficha do funcionário cujo convite pretende reenviar.
2. Localize o indicador de estado da conta. Se a conta não estiver ativada, aparecerá o botão **Reenviar convite**.
3. Prima o botão. O sistema enviará um novo correio de boas-vindas com uma nova palavra-passe temporária para o endereço de email do funcionário.

> **Aviso:** reenviar o convite invalida a palavra-passe temporária anterior. Se o funcionário já tinha recebido o primeiro convite e o estava a usar, terá de utilizar a nova palavra-passe do segundo envio.

### Reposição de palavra-passe

Quando um utilizador solicita repor a sua palavra-passe (a partir do ecrã de início de sessão, premindo «Esqueci-me da palavra-passe»), o sistema envia um correio com uma ligação segura de reposição. Esta ligação é válida durante 30 minutos a contar do momento do envio. Uma vez expirada, o utilizador deve solicitar uma nova ligação.

O correio inclui:
- Um botão com a ligação de reposição.
- A hora de expiração da ligação.
- Um aviso de que, se o utilizador não solicitou a reposição, pode ignorar o correio.

---

## Notificações por email adicionais e recurso

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

O envio de notificações operacionais por email (alertas de eventos, lembretes de confirmação de leitura, avisos de tarefas, etc.) e o mecanismo de recurso automático por email quando uma notificação push não pode ser entregue no dispositivo do utilizador estão planeados para uma versão futura da plataforma.

---

## O que fazer se o correio não chegar

Se um funcionário ou responsável não receber um correio esperado do sistema, siga estes passos:

1. **Verifique a pasta de spam ou correio não solicitado** no cliente de correio. Os correios de `hola@encodebiz.com` podem ser classificados incorretamente na primeira vez.
2. **Confirme o endereço de email** do destinatário no backoffice. Aceda à ficha do funcionário ou utilizador e confirme que o endereço está escrito corretamente e sem espaços adicionais.
3. **Reenvie o convite** se se tratar do correio de boas-vindas (ver a secção anterior).
4. **Contacte o administrador de TI** da sua organização para verificar que o domínio `encodebiz.com` não está bloqueado ou em quarentena.
5. Se o problema persistir, contacte o apoio do CheckBiz360 indicando o endereço de email do destinatário e o tipo de correio que não está a chegar.

---

> **Nota de perfil:** os correios de boas-vindas e de reposição de palavra-passe destinam-se a todos os utilizadores, independentemente do seu perfil. O reenvio de convites pode ser feito pelo **Owner** e pelo **Manager**.

## Artigos relacionados

- [Tipos de notificação](63-tipos-de-notificacao.md)
- [Notificações push na aplicação](64-notificacoes-push-na-aplicacao.md)
- [Configurar preferências de notificação](65-configurar-preferencias-de-notificacao.md)
- [Histórico de notificações](67-historico-de-notificacoes.md)
