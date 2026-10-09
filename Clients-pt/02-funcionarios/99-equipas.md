# Equipas

Uma **equipa** guarda quem trabalha junto, com que responsabilidade, em que função e a que valor por hora. Serve para adicionar toda uma equipa de trabalho a uma sucursal —ou a um projeto ou obra, conforme o nome que a sua entidade dá aos seus locais— de uma só vez, em vez de o fazer pessoa a pessoa.

Está pensada para empresas que levam as mesmas pessoas de um projeto para outro: configura-se a equipa uma vez e aplica-se a cada projeto novo.

---

## Como funciona

- **Uma equipa é um modelo.** Cada membro leva a sua responsabilidade (trabalhador, supervisor, gerente ou proprietário), a sua função e o seu valor por hora, mas não uma sucursal.
- **Aplicá-la a uma sucursal** adiciona cada membro a essa sucursal com esses dados, exatamente como se tivesse sido feito à mão.
- **A sucursal prevalece sobre o modelo.** Alterar uma função ou um valor na equipa não altera as sucursais onde já foi aplicada: isso ajusta-se em cada sucursal. O valor usado nos custos e nos relatórios é sempre o da sucursal.
- **O horário não faz parte da equipa.** Configura-se na sucursal, como sempre.
- Uma mesma pessoa pode estar em **várias equipas**, mas não duas vezes na mesma.

As equipas encontram-se em **Funcionários**, separador **Equipas**.

---

## Criar uma equipa

1. No menu lateral, abra **Funcionários** e vá ao separador **Equipas**.
2. Prima **Criar equipa** e indique o **Nome da equipa**. Não pode haver duas equipas com o mesmo nome; na comparação não contam as maiúsculas, os acentos nem os espaços a mais.
3. Abra a equipa com **Ver equipa** e prima **Adicionar membro**.
4. Escolha o **Funcionário**, a sua **Responsabilidade**, a sua função em **Ocupação atual** —do catálogo de funções ou escrevendo uma nova— e o seu **Salário por hora**.
5. Guarde. Repita o passo 4 com cada membro.

Na ficha da equipa também pode **editar um membro** ou **retirá-lo da equipa** e, na lista, **renomear** ou **eliminar** a equipa.

- Adicionar ou retirar alguém de uma equipa **não avisa ninguém** nem lhe dá acesso a nada: só altera o modelo.
- Retirar uma pessoa da equipa não a retira das sucursais onde a equipa já foi aplicada.
- Eliminar uma equipa elimina o modelo; quem já foi adicionado a uma sucursal com essa equipa fica onde está.
- Não é possível adicionar um funcionário que saiu da empresa (`employee/fired`). Estar de férias, de baixa médica ou com a ficha **Pendente** não impede estar numa equipa.

> **Sugestão:** se já tem um projeto com a equipa de trabalho criada, o mais rápido é não começar do zero: guarde o pessoal dessa sucursal como equipa (ver mais abaixo).

---

## Aplicar uma equipa a uma sucursal

1. Abra a ficha da sucursal e, na sua lista de funcionários, prima **Aplicar equipa**.
2. Escolha a **Equipa**. Antes de confirmar, são mostrados os seus membros com a função e o valor.
3. Reveja a lista e confirme com **Aplicar a N pessoas**.
4. No fim, o ecrã mostra quem foi **adicionado** e quem **não**, com o motivo.

O que acontece ao aplicar:

- Cada pessoa adicionada fica associada à sucursal com a responsabilidade, a função e o valor da equipa. A partir desse momento pode registar ponto nela e podem ser-lhe atribuídas as tarefas dessa sucursal.
- Cada pessoa adicionada **recebe o aviso** habitual de nova atribuição.
- **Aplicar nunca substitui o que já existe.** Quem já estava nessa sucursal é ignorado e mantém a sua função e o seu valor. Também é ignorado quem saiu, quem tem a ficha incompleta e quem já não tem ficha.

Os motivos que pode ver em «Não adicionadas» são:

| Motivo | O que significa |
|---|---|
| **Já estava nesta sucursal** | Tinha uma responsabilidade nela; mantém-se tal como estava. |
| **Saiu ou tem a ficha incompleta** | O seu estado é de saída ou *pendente*: ainda não pode trabalhar. |
| **A ficha já não existe** | O funcionário foi eliminado depois de ser adicionado à equipa. |

> **Importante:** reveja a lista antes de confirmar. Aplicar a equipa errada à sucursal errada envia um aviso a cada pessoa, e desfazê-lo obriga a retirar cada uma da sucursal.

Se, enquanto a equipa está a ser aplicada, alguém adicionar um dos membros a essa sucursal, a operação para sem alterar nada e aparece `team/apply_conflict`. Volte a aplicar a equipa: essa pessoa será ignorada.

---

## Guardar o pessoal de uma sucursal como equipa

1. Abra a ficha da sucursal e, na sua lista de funcionários, prima **Guardar como equipa**.
2. Dê-lhe um nome e confirme.

Copia-se quem está ativo nessa sucursal, com a sua responsabilidade, a sua função e o seu valor. **O horário não é copiado**, e quem saiu da empresa é ignorado. Uma sucursal sem ninguém ativo não pode ser guardada como equipa (`team/branch_without_staff`).

---

## Equipas e tarefas

As equipas aplicam-se a **sucursais**, não a tarefas. Depois de aplicada a equipa, os seus membros fazem parte da sucursal e selecionam-se um a um no formulário da tarefa, como qualquer outro funcionário dessa sucursal.

> **Estado: Planeado**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

Escolher na tarefa todo o pessoal da sucursal, filtrar por função ou adicionar uma equipa inteira de uma vez está planeado para uma versão futura.

---

## A aplicação do funcionário

Nada muda para o funcionário. Quem entra numa sucursal através de uma equipa vê essa sucursal na aplicação exatamente como se tivesse sido adicionado à mão, sem necessidade de a atualizar.

---

## Quem pode gerir equipas

Criar, editar e eliminar equipas, aplicá-las e guardar uma sucursal como equipa está reservado aos **proprietários e administradores** da entidade com acesso ativo ao backoffice.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md) | Responsabilidades, multi-sucursal e atribuição pessoa a pessoa |
| [Perfis e níveis de responsabilidade](./07-perfis-e-niveis-de-responsabilidade.md) | Os níveis que cada membro leva |
| [Criar e gerir funcionários](./06-criar-e-gerir-funcionarios.md) | Registo de funcionários e estados, incluindo o estado pendente |
| [Atribuir tarefas a funcionários](../06-tarefas/41-atribuir-tarefas-a-funcionarios.md) | Como se atribuem as tarefas às pessoas de uma sucursal |
| [Análise de custos](../07-inteligencia-operacional/54-analise-de-custos.md) | Porque é que o valor que conta é o da sucursal |
