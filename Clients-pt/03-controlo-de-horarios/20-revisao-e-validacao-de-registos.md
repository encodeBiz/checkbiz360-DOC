# Revisão e validação de registos

Alguns registos de assiduidade no CheckBiz360 não se consolidam de forma automática, exigindo uma confirmação explícita por parte do funcionário antes de serem considerados válidos. Este mecanismo garante que nenhuma modificação ou atribuição de jornada ocorre sem o conhecimento e a aceitação da pessoa afetada. Este artigo explica quando este processo é ativado, como o funcionário o gere e que opções têm os responsáveis.

---

## O estado «pendente de validação do funcionário»

O estado `pending-employee-validation` indica que um registo ou jornada existe no sistema mas está à espera de que o funcionário o confirme. Enquanto permanece neste estado, o registo **não conta como tempo trabalhado**.

Este estado é visível tanto para o funcionário (através da aplicação) como para o responsável (a partir do backoffice).

---

## Quando se gera um registo pendente de validação

Existem duas situações principais em que um registo entra no estado `pending-employee-validation`:

**Pedido de jornada manual:** quando um manager ou supervisor cria uma jornada em nome do funcionário (Modo A ou Modo B), o sistema atribui automaticamente este estado até que o funcionário responda. Consulte o artigo [Solicitar jornada manual](19-solicitar-jornada-manual.md) para mais detalhe.

**Correção do gestor:** quando um responsável modifica um registo existente do funcionário (por exemplo, ajusta a hora de entrada ou de saída), o sistema pode exigir que o funcionário valide a alteração antes de a aplicar de forma definitiva, consoante a configuração da entidade.

---

## Como o funcionário valida ou recusa um registo pendente

O funcionário recebe uma notificação push no seu dispositivo móvel quando há um registo pendente de validação. Para o tratar:

1. Toque na notificação ou abra a aplicação do CheckBiz360.
2. Navegue até à secção **Notificações** e selecione a notificação de atualização de registo.
3. Reveja os detalhes do registo: data, hora de entrada, hora de saída, sucursal e motivo indicado pelo responsável.
4. Selecione **Aceitar** ou **Recusar**, consoante o caso.

O ecrã de revisão está disponível na rota `/notifications/checklog-update/:id`, onde `:id` corresponde ao identificador único do registo de assiduidade.

---

## O que acontece se o funcionário aceitar

O registo passa ao estado `valid`. A partir desse momento, conta como tempo trabalhado e fica incorporado no cálculo de horas da jornada. O sistema regista a ação de validação no histórico de auditoria com a data, a hora e o identificador do funcionário que a realizou.

---

## O que acontece se o funcionário recusar

O registo fica marcado com o estado `failed` e é guardado o motivo da recusa. O registo permanece no sistema para auditoria, mas não conta como horas trabalhadas. O responsável recebe uma notificação da recusa e pode iniciar um novo pedido corrigido ou resolver a incidência manualmente.

---

## O que acontece se o funcionário não responder

Se o funcionário não validar nem recusar o registo, este permanece indefinidamente no estado `pending-employee-validation`. Não existe um prazo de expiração automática por omissão.

Nestes casos, o registo aparece como pendente no backoffice e tem de ser resolvido manualmente. Os responsáveis com perfil **manager** ou **owner** podem:

- Aprovar o registo diretamente a partir do backoffice, sem necessidade da validação do funcionário.
- Recusá-lo e encerrar a incidência com um motivo gravado.
- Contactar o funcionário para que resolva a validação pendente a partir da aplicação.

---

## Vista de pendentes no backoffice

O backoffice do CheckBiz360 inclui uma vista específica para gerir os registos pendentes de validação. A partir deste ecrã, o responsável pode:

- Ver todos os registos no estado `pending-employee-validation` da sua sucursal ou entidade.
- Filtrar por funcionário, data ou sucursal.
- Aceder ao detalhe de cada registo para rever o histórico de alterações.
- Aprovar ou recusar registos de forma individual ou em massa.

Esta vista foi pensada para que o responsável tenha uma visão centralizada de todas as incidências pendentes e as possa resolver sem ter de percorrer registo a registo o histórico de cada funcionário.

---

> **Aviso de conformidade:** a validação por parte do funcionário é um mecanismo de proteção laboral. A aprovação unilateral por parte do responsável sem ter contactado o funcionário deve ser devidamente documentada e usada apenas em casos excecionais. Em ambientes sujeitos a auditorias laborais, recomenda-se conservar o motivo da aprovação unilateral no campo de observações.

---

## Perfis com acesso a esta funcionalidade

Os utilizadores com perfil **funcionário** podem validar ou recusar registos pendentes a partir da aplicação. Os utilizadores com perfil **manager** ou **owner** podem resolver pendentes a partir do backoffice, incluindo a aprovação sem validação do funcionário.

---

## Artigos relacionados

- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Rastreabilidade e histórico de alterações](21-rastreabilidade-e-historico-de-alteracoes.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
