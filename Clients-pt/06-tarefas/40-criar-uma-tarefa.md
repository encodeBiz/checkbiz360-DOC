# Criar uma tarefa

Criar uma tarefa no CheckBiz360 é o ponto de partida para atribuir trabalho concreto a um ou vários funcionários. A partir do backoffice, os managers e os supervisores com permissão podem definir todos os detalhes da atividade antes de a enviar à equipa.

Este artigo descreve todos os campos disponíveis ao criar uma tarefa e explica o processo passo a passo.

---

## Campos de uma tarefa

### Campos obrigatórios

- **Título** — Nome breve e descritivo da tarefa. Deve ser suficientemente claro para que o funcionário perceba do que se trata sem ter de ler a descrição completa.
- **Sucursal** — Local de trabalho a que a tarefa pertence. Determina ainda o **fuso horário operacional** com que se interpretam as datas da tarefa; se a sucursal não tiver fuso horário próprio, usa-se o da entidade. **Não pode ser alterada depois de criada a tarefa**: se foi escolhida por engano, cancele a tarefa e crie outra na sucursal correta.
- **Prazo** — Data e hora antes da qual a tarefa deve estar concluída. Se for ultrapassada sem conclusão, a tarefa passa a *vencida* no seu indicador de cumprimento temporal.

### Campos opcionais

- **Descrição** — Explicação detalhada do que há a fazer. Admite formatação: títulos, listas, **listas de tarefas com caixas de verificação**, citações, negrito, itálico e ligações. Não tem limite de extensão.
- **Cliente** — Para quem é a tarefa, entre os clientes atribuídos à sucursal. Só aparece se a sucursal tiver clientes. Com cliente, a tarefa pode usar a sua morada como local de trabalho e leva à equipa as suas indicações e contactos. Ver [O cliente na tarefa](../17-carteira-de-clientes/119-o-cliente-na-tarefa.md).
- **Contrato** — De que contrato do cliente é a tarefa, ou **Sem contrato**. Aparece quando o cliente tem contratos. Ver [Contratos e rentabilidade](../17-carteira-de-clientes/121-contratos-e-rentabilidade.md).
- **Local de trabalho** — Morada onde se faz o trabalho quando não é a própria sucursal, com a sua **margem** em metros. Ver [Local de trabalho próprio](#local-de-trabalho-próprio).
- **Data prevista de início** — Hora a que se espera que o funcionário comece. Não bloqueia nada por si só: a sua utilidade é ativar o aviso de início tardio.
- **Notificar se não iniciar a tempo** — Se for ativada e a tarefa tiver data prevista de início, o sistema avisa quando tiverem passado **5 minutos** dessa hora sem que a tarefa tenha sido iniciada: as pessoas atribuídas na aplicação e os proprietários e administradores por e-mail. Sem data prevista de início, a opção não tem efeito. Ver [Tarefa por iniciar à hora prevista](./126-tarefa-por-iniciar-a-hora-prevista.md).
- **Estado** — Estado com que a tarefa nasce. O habitual é *Rascunho* (ainda não visível para a equipa) ou *Atribuída* (já enviada). Os estados *Validada*, *Recusada* e *Cancelada* não podem ser selecionados manualmente na criação: são o resultado do ciclo de vida da tarefa.
- **Prioridade** — Baixa, média, alta ou **crítica**. Afeta a ordem pela qual a tarefa aparece na aplicação do funcionário.
- **Funcionários atribuídos** — Pessoa ou pessoas responsáveis por a concluir. Podem pesquisar-se e selecionar-se vários.
- **Quem dá a tarefa por terminada?** — *Basta uma pessoa* (por omissão), *Todas as pessoas* ou *Uma pessoa responsável*. Ver [Quem termina a tarefa e fechá-la a partir da administração](./127-quem-termina-a-tarefa-e-fecho-a-partir-da-administracao.md).

### Opções de configuração da tarefa

Três opções controlam como a tarefa é fechada e revista:

| Opção | Por omissão | O que faz |
|---|---|---|
| **Exigir evidência ao concluir** | Desativada | Se a ativar, o funcionário não pode marcar a tarefa como concluída sem anexar pelo menos uma foto ou vídeo. Se o tentar, recebe o erro `task/evidence_required` |
| **Permitir validação por supervisor** | Ativada | Um supervisor da sucursal pode validar ou recusar a tarefa, sem necessidade de um manager |
| **Permitir avaliação por supervisor** | Ativada | Um supervisor pode pontuar o trabalho do funcionário ao fechar a tarefa |

---

## Passos para criar uma tarefa a partir do backoffice

1. Aceda ao backoffice com as suas credenciais de manager, owner ou supervisor com permissão de criação.
2. No menu lateral, selecione **Tarefas** e prima o botão de nova tarefa.
3. Escreva o **título**.
4. Redija a **descrição**. Use a barra de formatação para adicionar listas de verificação, títulos ou ligações se a tarefa tiver vários passos.
5. Procure e selecione a **sucursal**. Sob o campo aparece o fuso horário com que as datas serão enviadas.
6. Se a tarefa for para um cliente, escolha-o em **Cliente** e, se aparecer, o seu **Contrato**. Com **Usar a morada do cliente como local de trabalho**, reveja a **Margem**. Se o trabalho se fizer noutra morada, preencha **Local de trabalho (opcional)** e reveja a **margem**.
7. Se for o caso, indique a **data prevista de início** e ative **Notificar se não iniciar a tempo**.
8. Estabeleça o **prazo** (data e hora).
9. Escolha **estado** e **prioridade**.
10. Procure e selecione os **funcionários atribuídos** e, se forem vários, escolha **Quem dá a tarefa por terminada?**.
11. Reveja as três opções de configuração (evidência, validação e avaliação por supervisor).
12. Prima **Guardar**. Os funcionários atribuídos recebem uma notificação push automática.

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

### As caixas marcam-se a partir da aplicação

As pessoas atribuídas marcam e desmarcam as caixas da lista a partir do detalhe da tarefa na aplicação, à medida que avançam. Assim o senhor vê no painel que passos estão feitos sem perguntar.

- **A lista é uma por tarefa.** Se houver várias pessoas atribuídas, o que uma marca as outras veem.
- **Cada marca fica no histórico**: *Caixa marcada: «Contar caixa»* ou *Caixa desmarcada: …*, com quem e quando.
- **A partir da aplicação só se marcam caixas**: o resto do texto é alterado por quem gere a tarefa, com **Editar**.
- **Com a tarefa fechada** (concluída, validada ou cancelada) a lista já não pode ser alterada a partir da aplicação: é o registo do que foi entregue.
- **Se duas pessoas marcarem ao mesmo tempo**, a aplicação avisa que a lista tinha mudado e mostra a atual para voltar a marcar.
- **Marcar caixas não envia avisos.**
- **Ao duplicar a tarefa**, a cópia nasce com todas as caixas por marcar.

---

## Local de trabalho próprio

Por omissão, uma tarefa faz-se na sua sucursal, e a única verificação de localização é a do registo: a geocerca da sucursal ao abrir a jornada.

Quando o trabalho se faz noutra morada —o domicílio de um cliente, uma obra, um espaço que muda todos os dias—, a tarefa pode levar o seu **próprio local de trabalho**. Assim não é preciso criar uma sucursal para cada trabalho.

### Como se configura

1. No formulário da tarefa, escreva a morada em **Local de trabalho (opcional)** e **escolha-a na lista** de sugestões.
2. Reveja a **margem**: é o raio, em metros, dentro do qual se considera que o funcionário está no local. Por omissão assume a da sucursal e pode ser alargada; uma garagem subterrânea ou um pavilhão precisam de mais margem do que a entrada de um prédio.
3. Guarde a tarefa.

Se a tarefa for para um cliente com morada, pode usar **Usar a morada do cliente como local de trabalho** e ajustar a sua **Margem** por baixo; explica-se em [O cliente na tarefa](../17-carteira-de-clientes/119-o-cliente-na-tarefa.md).

Se a morada não for suficientemente precisa para situar o ponto —por exemplo, falta o número da porta—, a tarefa não é guardada e é indicado o erro `task/worksite_imprecise`. Complete a morada e volte a escolhê-la.

### O que muda para o funcionário

- **Iniciar** a tarefa exige estar dentro da margem. A aplicação envia a posição e o servidor verifica-a; fora da margem, o início é recusado com `task/out_of_worksite`, que indica a distância e a margem permitida, e a tentativa fica anotada no histórico da tarefa.
- **Retomar** uma tarefa em pausa exige o mesmo que iniciá-la.
- **Concluir** não é bloqueado: a posição é registada, mas a tarefa pode ser fechada mesmo que o funcionário já tenha saído do local.
- Na aplicação, o detalhe da tarefa mostra a morada e uma ligação **Ver no Maps** para lá chegar.

No backoffice, o bloco **Local de trabalho** do detalhe da tarefa mostra a sucursal, a morada, a margem e um botão para abrir o mapa.

> **Importante:** uma tarefa com local de trabalho próprio **só pode ser iniciada, retomada ou concluída a partir da aplicação**, porque o backoffice não envia qualquer localização: se se tentar a partir do painel, a ação é recusada com `task/geo_required`. Pausá-la, cancelá-la, validá-la ou recusá-la a partir do backoffice funciona normalmente.

---

## Duplicar uma tarefa

Quando um trabalho se repete, não é preciso voltar a preencher o formulário. Uma tarefa duplica-se com a ação **Duplicar**, disponível na listagem de tarefas e na ficha da tarefa.

A cópia é criada na **mesma sucursal** e herda o trabalho a fazer: descrição (com as caixas por marcar), prioridade, opções de configuração, local de trabalho e documentos anexos. **Não herda** a sua execução: nem funcionários atribuídos, nem evidências, notas, avaliações ou histórico.

### Passos

1. Prima **Duplicar** na tarefa que pretende copiar.
2. Reveja o **título da cópia**, que é proposto com o do original.
3. Indique o **prazo** e, se for o caso, a **data prevista de início**. As datas do original não são herdadas de propósito: uma cópia com o prazo antigo nasceria já vencida. São interpretadas com o fuso horário da sucursal.
4. Prima **Duplicar**.

A cópia nasce em **Rascunho** e sem atribuição. A partir da ficha, duplicar leva-o diretamente à cópia: o passo seguinte é editá-la, atribuir os funcionários e pô-la em **Atribuída**.

Pode duplicar quem pode criar tarefas nessa sucursal. A sucursal tem de estar ativa.

---

## Documentos anexos e evidências

Uma tarefa guarda dois tipos de ficheiro e, na ficha (painel e aplicação), vão em blocos separados:

| | **Documentos anexos** | **Evidências** |
|---|---|---|
| Para quê | O que precisa quem faz a tarefa: um processo, umas instruções, uma planta | A prova de que a tarefa foi feita |
| Quem os carrega, normalmente | A direção, ao preparar a tarefa | A pessoa, ao fazer o trabalho |
| Contam para **Exigir evidência ao concluir** | Não | Sim |
| Ao duplicar a tarefa | São copiados com ela | Não são copiados |
| Podem ser retirados | Sim, com **Retirar desta tarefa** | Não |

### Anexar a partir do painel

1. Na ficha da tarefa, em **Recursos**, prima **Anexar**.
2. Deixe por marcar **É evidência do trabalho feito** para carregar um documento anexo: admite PDF (até 20 MB) e fotos JPG, PNG ou WEBP (até 5 MB).
3. Marque-a só se o ficheiro provar o trabalho feito: nesse caso escolha a que **Funcionário** corresponde; como evidência admitem-se fotos.
4. Se quiser, escreva uma **Descrição** e confirme.

### A partir da aplicação

- Ao **criar ou editar** uma tarefa a partir da aplicação, «Adjuntar documento» acrescenta PDF ou fotos, que são carregados ao guardar.
- No detalhe da tarefa, o cartão «Archivos y gastos» tem «Añadir → Archivo» para carregar uma foto ou um PDF que acompanha a tarefa.
- As evidências carregam-se como sempre: foto ou vídeo (até **25 MB**) a partir da câmara ou da galeria.

Anexar documentos de Word ou Excel não está disponível: converta-os para PDF.

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
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Iniciar, pausar e retomar uma tarefa |
| [O cliente na tarefa](../17-carteira-de-clientes/119-o-cliente-na-tarefa.md) | Escolher cliente e contrato, e o que a equipa vê do cliente |
| [Geocercas e raio de registo](../03-controlo-de-horarios/16-geocercas-e-raio-de-registo.md) | A verificação de localização ao registar |
| [Notificações de tarefas](./47-notificacoes-de-tarefas.md) | Que notificações recebem os funcionários |
| [Quem termina a tarefa e fechá-la a partir da administração](./127-quem-termina-a-tarefa-e-fecho-a-partir-da-administracao.md) | Uma, todas ou uma responsável; concluir com horas a partir do painel |
| [Tarefa por iniciar à hora prevista](./126-tarefa-por-iniciar-a-hora-prevista.md) | O aviso aos 5 minutos |
