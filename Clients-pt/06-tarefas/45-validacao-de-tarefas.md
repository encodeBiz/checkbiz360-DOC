# Validação de tarefas

A validação é o passo pelo qual um responsável confirma que o trabalho realizado pelo funcionário cumpre os requisitos exigidos. O CheckBiz360 separa a ação de concluir uma tarefa (que o funcionário realiza) da de a validar (que o responsável realiza), garantindo um duplo nível de controlo sobre a qualidade do trabalho.

---

## Fluxo de validação

O processo segue sempre a mesma ordem:

1. O funcionário executa a tarefa e marca-a como **concluída** a partir da aplicação.
2. O sistema avisa o responsável de que há trabalho pendente de revisão.
3. O responsável acede ao backoffice, revê o trabalho e decide se o **aceita** ou o **recusa**.
4. Se aceitar, a tarefa passa a **validada** e fica encerrada.
5. Se recusar, a tarefa passa a **recusada**, com o motivo visível para o funcionário.

---

## Aceitar uma tarefa concluída

Para validar uma tarefa, o responsável deve:

1. Aceder ao backoffice e abrir a secção **Tarefas**.
2. Filtrar por estado **Concluída** para ver as que estão à espera de revisão.
3. Abrir o detalhe da tarefa.
4. Ler as notas do funcionário e rever as evidências apresentadas.
5. Validar a tarefa.

Uma vez validada, a tarefa fica encerrada: o estado *validada* não se atribui nem se reverte à mão a partir do formulário de edição. Se a avaliação estiver ativada, pode em seguida pontuar o trabalho do funcionário.

---

## Recusar uma tarefa concluída

Se o responsável considerar que o trabalho não está correto, pode recusá-lo.

### Passos para recusar uma tarefa

1. A partir do detalhe da tarefa no backoffice, prima **Recusar**.
2. Escreva o motivo da recusa. **É obrigatório**: sem texto, a ação não pode ser confirmada.
3. Confirme a recusa.

A tarefa passa ao estado **recusada** e o motivo fica visível para o funcionário juntamente com o histórico completo da tarefa.

> **Importante:** o motivo da recusa é obrigatório. Uma explicação clara é o que permite ao funcionário corrigir o trabalho e não repetir o erro.

---

## Consequências da recusa

Quando uma tarefa é recusada:

- Fica no estado **recusada**, que é um encerramento com motivo: a tarefa não volta sozinha à lista de trabalho do funcionário.
- O indicador de cumprimento temporal passa a mostrar *Recusada*, porque o cumprimento do prazo deixa de ser o relevante.
- O histórico regista a recusa, o motivo, o autor e a data, de modo que fica evidência do ciclo completo.

**Se o trabalho tiver de ser refeito**, o responsável edita a tarefa e devolve-a ao estado **atribuída**, ajustando o prazo se for caso disso. O funcionário recupera-a na sua lista e o ciclo recomeça.

---

## Quem pode validar

Por omissão, validam **managers e owners**. Cada tarefa incorpora ainda a opção **Permitir validação por supervisor**, ativada por omissão, que habilita os supervisores da sucursal a validar ou recusar essa tarefa.

É uma decisão **por tarefa**, não uma permissão do perfil do funcionário: marca-se ao criar a tarefa ou ao editá-la, a par das opções de avaliação e de evidência obrigatória. Isto permite descentralizar a operação do dia a dia e reservar a validação das tarefas sensíveis para o manager.

> **Nota:** o manager mantém sempre visibilidade completa sobre as validações dos seus supervisores. Toda a ação fica registada no histórico com o nome de quem a executou e o seu nível de responsabilidade.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida e significado de cada estado |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Como o funcionário atualiza o progresso |
| [Avaliação do trabalhador](./46-avaliacao-do-trabalhador.md) | Pontuação de desempenho após a validação |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Avisos ao validar ou recusar uma tarefa |
| [Perfis e níveis de responsabilidade](../02-funcionarios/07-perfis-e-niveis-de-responsabilidade.md) | Descrição de permissões por perfil |
