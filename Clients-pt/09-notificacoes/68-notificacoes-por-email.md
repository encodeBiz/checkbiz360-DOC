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

### Saber se chegou e reenviar o acesso

Na ficha de cada funcionário, o bloco **Acesso à app** diz o que aconteceu ao seu correio de boas-vindas: entregue, devolvido, marcado como spam ou não enviado. Também diz se a pessoa já usou a aplicação. Se o correio não chegou, a página inicial do painel avisa com o alerta **Acesso que não chegou**.

Para o enviar outra vez:

1. Navegue até **Funcionários** e abra a ficha do funcionário.
2. Em **Acesso à app**, prima **Reenviar acesso**.
3. Confirme. O sistema envia um novo correio de boas-vindas com uma palavra-passe nova.

> **Aviso:** reenviar o acesso invalida a palavra-passe anterior, também para o painel se a pessoa o usar. Se o correio foi devolvido, o endereço está errado: altere-o com **Alterar e-mail** e envie o acesso para o novo.

Explica-se por inteiro em [Acesso à aplicação e alteração de e-mail](../02-funcionarios/116-acesso-a-aplicacao-e-alteracao-de-email.md).

### Cartão do ponto de registo

Com o [ponto de registo](../03-controlo-de-horarios/113-ponto-de-registo.md) contratado, cada pessoa pode receber por correio o seu cartão, com o seu QR e o seu código de 6 dígitos. Envia-se a partir da ficha do funcionário ou, para uma sucursal inteira, a partir de **Ponto de registo → Cartões QR**.

### Reposição de palavra-passe

Quando um utilizador solicita repor a sua palavra-passe (a partir do ecrã de início de sessão, premindo «Esqueci-me da palavra-passe»), o sistema envia um correio com uma ligação segura de reposição. Esta ligação é válida durante 30 minutos a contar do momento do envio. Uma vez expirada, o utilizador deve solicitar uma nova ligação.

O correio inclui:
- Um botão com a ligação de reposição.
- A hora de expiração da ligação.
- Um aviso de que, se o utilizador não solicitou a reposição, pode ignorar o correio.

---

## Avisos de trabalho por correio, para quem não usa a aplicação

Há pessoas que não usam a aplicação, ou que não a consultam. Para elas, em **Horários e feriados** da sua ficha existe a caixa **Enviar notificações por email**. Com ela marcada, além dos avisos da aplicação, a pessoa recebe por correio:

- **As suas tarefas**: as que lhe são atribuídas, alteradas ou retiradas. Chegam agrupadas para não lhe encher a caixa de correio: o correio sai quando passam 15 minutos sem alterações novas. Se a tarefa começar nas próximas 24 horas, o aviso sai de imediato.
- **O seu horário da semana seguinte**, ao domingo às 18:00 na hora da empresa, com os seus turnos, as suas tarefas e o local de cada uma. Se nada tiver mudado desde o último envio, não se repete.

Nada do registo de ponto vai por correio. A caixa vem desmarcada e marca-se pessoa a pessoa.

## Aviso de armazenamento

Quando a sua empresa chega aos 90 % do armazenamento incluído no seu plano, o proprietário recebe um correio no endereço de faturação. Envia-se uma única vez. Só volta a ser enviado se o uso descer abaixo dos 80 % e depois voltar a subir. Ver [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md#armazenamento).

## Alertas operacionais por correio

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

O envio por correio dos alertas da página inicial aos responsáveis, e o recurso automático por correio quando uma notificação push não chega ao dispositivo, estão planeados para uma versão futura.

---

## O que fazer se o correio não chegar

Se um funcionário ou responsável não receber um correio esperado do sistema, siga estes passos:

1. **Verifique a pasta de spam ou correio não solicitado** no cliente de correio. Os correios de `hola@encodebiz.com` podem ser classificados incorretamente na primeira vez.
2. **Confirme o endereço de email** do destinatário no backoffice. Aceda à ficha do funcionário ou utilizador e confirme que o endereço está escrito corretamente e sem espaços adicionais.
3. **Veja o bloco Acesso à app** da ficha se se tratar do correio de boas-vindas: diz se foi entregue, se foi devolvido ou se foi marcado como spam. Depois, **reenvie o acesso** (ver a secção anterior).
4. **Contacte o administrador de TI** da sua organização para verificar que o domínio `encodebiz.com` não está bloqueado ou em quarentena.
5. Se o problema persistir, contacte o apoio do CheckBiz360 indicando o endereço de email do destinatário e o tipo de correio que não está a chegar.

---

> **Nota de perfil:** os correios de boas-vindas e de reposição de palavra-passe destinam-se a todos os utilizadores, independentemente do seu perfil. Reenviar o acesso e alterar o e-mail pode ser feito por quem edita as fichas dos funcionários: o **Owner**, os administradores e o **Manager**.

## Artigos relacionados

- [Tipos de notificação](63-tipos-de-notificacao.md)
- [Notificações push na aplicação](64-notificacoes-push-na-aplicacao.md)
- [Configurar preferências de notificação](65-configurar-preferencias-de-notificacao.md)
- [Histórico de notificações](67-historico-de-notificacoes.md)
