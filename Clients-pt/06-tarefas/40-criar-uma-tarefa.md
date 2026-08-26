# Criar uma tarefa

Criar uma tarefa no CheckBiz360 é o ponto de partida para atribuir trabalho concreto a um ou vários funcionários. A partir do backoffice, os managers e os supervisores com permissão podem definir todos os detalhes da atividade antes de a enviar à equipa.

Este artigo descreve todos os campos disponíveis ao criar uma tarefa e explica o processo passo a passo.

---

## Campos de uma tarefa

### Campos obrigatórios

- **Título** — Nome breve e descritivo da tarefa. Deve ser suficientemente claro para que o funcionário perceba do que se trata sem ter de ler a descrição completa.
- **Sucursal** — Local de trabalho a que a tarefa pertence. Determina ainda o **fuso horário operacional** com que se interpretam as datas da tarefa; se a sucursal não tiver fuso horário próprio, usa-se o da entidade.
- **Prazo** — Data e hora antes da qual a tarefa deve estar concluída. Se for ultrapassada sem conclusão, a tarefa passa a *vencida* no seu indicador de cumprimento temporal.

### Campos opcionais

- **Descrição** — Explicação detalhada do que há a fazer. Admite formatação: títulos, listas, **listas de tarefas com caixas de verificação**, citações, negrito, itálico e ligações. Não tem limite de extensão.
- **Data prevista de início** — Hora a que se espera que o funcionário comece. Não bloqueia nada por si só: a sua utilidade é ativar o aviso de início tardio.
- **Notificar se não iniciar a tempo** — Se for ativada e a tarefa tiver data prevista de início, o sistema envia uma notificação automática quando tiverem passado **15 minutos** dessa hora sem que a tarefa tenha sido iniciada. Sem data prevista de início, a opção não tem efeito.
- **Estado** — Estado com que a tarefa nasce. O habitual é *Rascunho* (ainda não visível para a equipa) ou *Atribuída* (já enviada). Os estados *Validada*, *Recusada* e *Cancelada* não podem ser selecionados manualmente na criação: são o resultado do ciclo de vida da tarefa.
- **Prioridade** — Baixa, média, alta ou **crítica**. Afeta a ordem pela qual a tarefa aparece na aplicação do funcionário.
- **Funcionários atribuídos** — Pessoa ou pessoas responsáveis por a concluir. Podem pesquisar-se e selecionar-se vários.

### Opções de configuração da tarefa

Três opções controlam como a tarefa é fechada e revista:

| Opção | Por omissão | O que faz |
|---|---|---|
| **Exigir evidência ao concluir** | Ativada | O funcionário não pode marcar a tarefa como concluída sem anexar pelo menos uma foto ou vídeo. Se o tentar, recebe o erro `task/evidence_required` |
| **Permitir validação por supervisor** | Ativada | Um supervisor da sucursal pode validar ou recusar a tarefa, sem necessidade de um manager |
| **Permitir avaliação por supervisor** | Ativada | Um supervisor pode pontuar o trabalho do funcionário ao fechar a tarefa |

---

## Passos para criar uma tarefa a partir do backoffice

1. Aceda ao backoffice com as suas credenciais de manager, owner ou supervisor com permissão de criação.
2. No menu lateral, selecione **Tarefas** e prima o botão de nova tarefa.
3. Escreva o **título**.
4. Redija a **descrição**. Use a barra de formatação para adicionar listas de verificação, títulos ou ligações se a tarefa tiver vários passos.
5. Procure e selecione a **sucursal**. Sob o campo aparece o fuso horário com que as datas serão enviadas.
6. Se for o caso, indique a **data prevista de início** e ative **Notificar se não iniciar a tempo**.
7. Estabeleça o **prazo** (data e hora).
8. Escolha **estado** e **prioridade**.
9. Procure e selecione os **funcionários atribuídos**.
10. Reveja as três opções de configuração (evidência, validação e avaliação por supervisor).
11. Prima **Guardar**. Os funcionários atribuídos recebem uma notificação push automática.

> **Sugestão:** para tarefas com vários passos —uma abertura de loja, uma revisão de material, um protocolo de limpeza— use uma lista de tarefas na descrição. O funcionário lê a sequência completa na aplicação sem que seja preciso criar uma tarefa por passo.

---

## Redigir a descrição com formatação

O campo de descrição inclui uma barra de ferramentas com negrito, itálico, código, título, lista com marcas, lista numerada, **lista de tarefas**, citação e ligação. Ao premir Enter dentro de uma lista, a lista continua automaticamente.

O separador **Pré-visualização** mostra como o texto ficará depois de guardado.

Um exemplo de descrição com lista de verificação:

```
## Abertura da loja
- [ ] Verificar câmaras
- [ ] Contar caixa
- [ ] Abrir estore

**Importante:** avisar o supervisor se faltar numerário.
```

> **Nota:** as caixas de verificação da descrição fazem parte do texto da tarefa, não são um estado guardado. Servem de guião de trabalho para o funcionário; o avanço real da tarefa reflete-se nas mudanças de estado, nas notas e nas evidências.

---

## Evidências e anexos

As evidências não se anexam ao criar a tarefa: carregam-se durante a sua execução, a partir da aplicação do funcionário ou do detalhe da tarefa no backoffice.

- A partir do **backoffice** anexam-se fotos em formato JPG, PNG ou WEBP, com um máximo de **5 MB** por ficheiro.
- A partir da **aplicação do funcionário** admitem-se ainda vídeos, com um máximo de **25 MB** por ficheiro.

Os limites são os valores por omissão da plataforma e podem ser ajustados por configuração.

### Anexos de tipo documento

> **Estado: Planeado**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

Anexar documentos em formato PDF, Word ou Excel a uma tarefa está planeado para uma versão futura. Quando estiver disponível, permitirá incluir protocolos, formulários e folhas de dados diretamente no detalhe da tarefa.

---

## Atribuição a vários funcionários

A mesma tarefa pode ser atribuída a mais do que um funcionário. Por omissão, **qualquer um dos atribuídos a pode concluir**: é útil quando a atividade é resolvida pelo primeiro que estiver disponível.

Se precisar de que cada funcionário a conclua de forma independente, crie uma tarefa por funcionário.

> **Nota:** quando atribui uma tarefa a vários funcionários, cada um recebe a sua própria notificação push, e o histórico de ações de cada um fica registado em separado na atividade da tarefa.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [O que é o módulo de tarefas](./39-o-que-e-o-modulo-de-tarefas.md) | Visão geral do módulo e dos seus casos de utilização |
| [Atribuir tarefas a funcionários](./41-atribuir-tarefas-a-funcionarios.md) | Atribuição individual e por equipa |
| [Prioridades e prazos](./44-prioridades-e-prazos.md) | Como gerir a urgência e os prazos |
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida de uma tarefa |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Que notificações recebem os funcionários |
