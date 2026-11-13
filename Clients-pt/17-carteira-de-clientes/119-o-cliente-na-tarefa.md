# O cliente na tarefa

Uma tarefa com o seu cliente sabe onde se faz, leva a quem vai trabalhar o que precisa de saber à chegada e conta nas horas, no contrato e na análise desse cliente. Tudo se decide no formulário de sempre, o da nova tarefa.

---

## O que resolve

- **Não voltar a escrever a morada.** A do cliente serve como local de trabalho, com a sua margem.
- **Que a equipa chegue a saber.** Indicações, contactos a quem telefonar e a ficha do cliente, na própria tarefa da aplicação.
- **Proteger o que não deve sair.** O nome do cliente só se mostra se o senhor o autorizar.
- **Saber de que contrato é cada trabalho**, ou deixar claro que não é de nenhum.

---

## Escolher o cliente ao criar uma tarefa

1. Em **Gerenciamento de tarefas**, prima o botão de nova tarefa.
2. Escolha primeiro a **sucursal**: os clientes saem dela.
3. Em **Cliente**, escolha um dos clientes atribuídos a essa sucursal, ou deixe **Sem cliente**. Se a sucursal não tiver clientes, o campo não aparece.
4. Se o cliente tiver contratos, aparece **Contrato**: escolha de qual é a tarefa ou **Sem contrato** (ver mais abaixo).
5. Se o cliente tiver morada, aparece marcada **Usar a morada do cliente como local de trabalho**, com a morada por baixo e a sua **Margem** em metros.
6. Preencha o resto da tarefa como sempre e guarde.

Se mudar de sucursal, o cliente e o contrato esvaziam-se: é preciso voltar a escolhê-los.

Uma tarefa interna (uma reunião, um trabalho de escritório) não é de nenhum cliente: deixe-a em **Sem cliente**.

---

## A morada do cliente como local de trabalho

Com **Usar a morada do cliente como local de trabalho** marcada, a tarefa só pode ser iniciada a partir dessa morada, tal como com um [local de trabalho próprio](../06-tarefas/40-criar-uma-tarefa.md#local-de-trabalho-próprio).

- **Margem.** Os metros à volta da morada a partir dos quais se pode iniciar. Se não a alterar, assume a da sucursal. *Uma garagem ou um pavilhão precisam de mais margem do que a entrada de um prédio.* A margem que indicar fica guardada com a tarefa e conserva-se ao voltar a editá-la.
- **Outra morada.** Se o trabalho de hoje não for na morada do cliente, desmarque a caixa e escreva a morada em **Local de trabalho (opcional)**.

---

## O contrato da tarefa

A lista **Contrato** aparece assim que o cliente tem algum contrato:

- **Ao criar a tarefa**, se o cliente tiver um único contrato em vigor nessas datas, vem proposto. Pode mudá-lo.
- **Sem contrato** deixa a tarefa fora de todos os contratos. É respeitado: criar um contrato novo mais tarde não a leva.
- Uma tarefa só muda de contrato quando o senhor o escolhe nela.

As tarefas que não passam por este formulário (importadas, criadas a partir da aplicação ou do assistente) assumem ao ser criadas o contrato em vigor do cliente se só tiver um. Se não era desse contrato, edite-a e escolha outro ou **Sem contrato**.

Mais sobre contratos em [Contratos e rentabilidade](./121-contratos-e-rentabilidade.md).

---

## O cartão do cliente na ficha da tarefa

Na ficha de uma tarefa com cliente aparece o cartão **Cliente**, com tudo o que o acompanha:

- O nome do cliente e uma marca que indica se **A equipa vê o nome** ou **A equipa não vê o nome**. **Ver ficha** leva à ficha do cliente.
- O **Contrato**, como ligação: abre a ficha do cliente com esse contrato expandido.
- A **Morada do cliente**.
- As **Notas de campo**.
- As **Pessoas de contacto**, com as visíveis para a equipa marcadas **Visível no terreno**, e os botões **Ligar** e **Enviar um e-mail**.
- Os **Documentos** que a equipa vê a partir da tarefa, para os abrir ou descarregar.

Se a tarefa tiver cliente, a ficha mostra também o bloco **Despesas** (só a proprietários e administradores). Ver [Despesas do contrato e da tarefa](./122-despesas-do-contrato-e-da-tarefa.md).

---

## O que a equipa vê na aplicação

No detalhe da tarefa, a pessoa atribuída vê o cartão «Datos complementarios», por cima de «Equipo», com:

- As notas de campo do cliente («Notas de campo»).
- Os contactos marcados como visíveis («Contactos»), com o botão «Llamar».
- Os documentos do cliente marcados para trabalhadores («Documentos del cliente»).

O **nome do cliente** só aparece se na sua ficha estiver marcada **Mostrar o nome do cliente à equipa**. Se o cliente não tiver nenhum dado para a equipa, o cartão não aparece. Os contratos, os orçamentos e tudo o que estiver marcado «Administração» nunca se veem a partir da aplicação.

Para ver o cartão, a equipa tem de ter a aplicação atualizada para a última versão.

---

## Procurar tarefas por cliente

- **Lista de tarefas.** Assim que a empresa tem clientes, aparece o filtro **Cliente** junto ao de funcionário.
- **Relatório de tarefas.** Se alguma tarefa do relatório tiver cliente, o Excel acrescenta a coluna **Cliente** a seguir a **Local**. Ver [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md).

---

## Problemas frequentes

**Não aparece o campo Cliente.** A sucursal escolhida não tem clientes atribuídos. Atribua o cliente a essa sucursal a partir da sua ficha.

**Não aparece a lista Contrato.** O cliente não tem contratos ativos.

**A equipa não consegue iniciar a tarefa.** Com a morada do cliente como local de trabalho, só se pode iniciar dentro da margem. Se o sítio for grande (um pavilhão, um parque de estacionamento), aumente a **Margem**.

**A equipa não vê os dados do cliente.** Verifique que a aplicação está atualizada, que os contactos estão marcados **Visível para quem vai trabalhar** e que os documentos estão marcados para trabalhadores.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma tarefa](../06-tarefas/40-criar-uma-tarefa.md) | Todos os campos do formulário da tarefa |
| [Dar entrada a clientes](./118-dar-entrada-a-clientes.md) | Morada, contactos, notas de campo e a caixa do nome |
| [Contratos e rentabilidade](./121-contratos-e-rentabilidade.md) | De que contrato é cada tarefa e quanto deixa |
| [Despesas do contrato e da tarefa](./122-despesas-do-contrato-e-da-tarefa.md) | O que se paga fora para a tarefa |
