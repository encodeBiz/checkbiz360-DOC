# Incidência na tarefa

Às vezes o trabalho não pode ser feito por algo que não depende de quem o vai fazer: não lhe abrem a porta, falta o material, o cliente anulou a visita. Com a **incidência na tarefa**, essa pessoa di-lo no momento, com uma nota e, se quiser, uma foto. O senhor fica a saber de imediato, por e-mail e no painel, sem esperar que alguém abra a tarefa, e decide o que se faz: replaneia-se, cancela-se ou dá-se por resolvida.

---

## O que resolve

- **Fica a saber quando ainda há remédio**, não no dia seguinte a rever a lista.
- **Sabe o que aconteceu**, com as palavras de quem lá estava e a foto, se a tirou.
- **Ninguém paga pelo que não dependia de si**: enquanto a incidência está aberta, a tarefa não conta nos alertas de vencidas nem de atrasadas.
- **Fica registado**: quem a marcou, quando, o que disse e como se resolveu, no histórico e no relatório de tarefas.

---

## Marcar uma incidência

Podem marcá-la as pessoas atribuídas à tarefa e, a partir da aplicação, também os supervisores e cargos superiores. A partir do painel, quem gere a tarefa. Só se pode marcar enquanto a tarefa está por fazer: não numa concluída, validada, recusada ou cancelada.

### A partir da aplicação

1. Abra a tarefa.
2. Prima os **três pontos** em cima à direita e escolha «Reportar incidencia».
3. Em «¿Qué ha pasado?» conte o que o impediu de fazer a tarefa. É obrigatório, até 1.000 caracteres. Por exemplo: *não me abriram a porta e não consegui entrar*.
4. Se quiser, junte em «Foto o archivo (opcional)» uma foto (JPG, PNG ou WEBP) ou um PDF de até 20 MB.
5. Prima «Reportar incidencia».

Se não vir a opção, atualize a aplicação para a última versão.

### A partir do painel

Na ficha da tarefa, o botão vermelho **Marcar incidência**, o primeiro em cima. Pede o mesmo: a nota e, se quiser, uma foto ou um ficheiro.

Uma tarefa só tem **uma incidência aberta de cada vez**. Se já houver uma, a aplicação indica-o e mostra a que existe.

---

## Quem é avisado

Assim que é marcada, sem esperar por nada:

| Quem | Como fica a saber |
|---|---|
| **Proprietários e administradores** | Um e-mail com quem a marcou, a tarefa, a sucursal, a nota e um botão **Ver a tarefa**. |
| **Proprietários e administradores, no painel** | O alerta vermelho **Incidência numa tarefa**, o primeiro de **Requer atenção** em **Início**, com o título da tarefa e a nota. |
| **Responsáveis da sucursal e supervisores** | Um aviso na aplicação com quem a marcou, a tarefa e a nota. |

O e-mail pode ser desativado em **Ferramentas → Alertas por e-mail → Configurar alertas**, no grupo **Pendentes da sua decisão**, com a caixa **Incidência numa tarefa**. O alerta de **Início** e o aviso na aplicação não dependem dessa caixa.

---

## Como se vê a tarefa com incidência

- **Na ficha** (painel e aplicação): uma faixa vermelha em cima, **Incidência aberta**, com a nota, *Marcada por … · data* e a ligação para o ficheiro, se houver.
- **Em Gerenciamento de tarefas** (painel): a linha aparece a vermelho com a etiqueta **Incidência**. Em cima aparece um chip vermelho com o número, por exemplo *2 tarefas com incidência*, que conta as de toda a empresa. Prima-o para ver só essas; com o seu **X**, ou mudando qualquer outro filtro, volta à lista completa. O chip só aparece se houver alguma.
- **Na aplicação**: o cartão tem o contorno vermelho e, se houver alguma aberta, no topo da lista aparece o filtro «Con incidencia».

---

## Resolver a incidência

Resolve-se **a partir do painel**, por quem gere a tarefa.

1. Abra a tarefa: a partir do alerta de **Início**, da ligação do e-mail ou do chip de **Gerenciamento de tarefas**.
2. Na faixa vermelha, prima **Resolver incidência**.
3. Em **Como foi resolvida?**, escolha:

| Opção | O que faz |
|---|---|
| **Replaneada** | Muda as datas, as pessoas ou as duas: **Novo início previsto**, **Nova data limite** e **Pessoas atribuídas**. É preciso mudar alguma coisa; se não for necessário, escolha *Resolvida*. |
| **Cancelada** | A tarefa é cancelada, com o texto de **Motivo do cancelamento**. |
| **Resolvida** | Resolveu-se sem mexer na tarefa, que continua como estava. |

4. Se quiser, deixe uma **Nota (opcional)**.
5. Prima **Resolver incidência**.

A faixa vermelha desaparece, o alerta de **Início** também e a tarefa volta a contar normalmente, com as novas datas se foi replaneada.

---

## O que acontece à tarefa entretanto

- **Não muda de estado.** Continua atribuída ou em curso, como estava.
- **Não conta como vencida nem como atrasada** em **Início**, nos alertas por e-mail de tarefas vencidas ou de tarefas de um cliente por fazer, nem entre as tarefas por iniciar à hora prevista. A pessoa foi e não conseguiu: não faz sentido que isso lhe pese.
- **Não é enviado o aviso de tarefa por começar.**

---

## No histórico e no relatório

O histórico da tarefa anota **Incidência marcada** (com *Com foto ou ficheiro* se o levava) e **Incidência resolvida: Replaneada**, *Cancelada* ou *Resolvida*, com quem e quando. É o mesmo na aplicação e no painel.

O [relatório de tarefas](./48-relatorios-de-tarefas.md) em Excel recolhe-as, abertas ou já resolvidas:

- Na folha **Tarefas**, a coluna **Incidência** (*Aberta* ou *Resolvida · como*), só se alguma tarefa do período teve uma.
- A folha **Incidências**, com uma linha por incidência: local, cliente, tarefa, estado da tarefa, quando e quem a marcou, a nota, se levava ficheiro, se continua aberta, como se resolveu, quando, quem e a sua nota.

---

## Problemas frequentes

| Situação | O que fazer |
|---|---|
| Na aplicação não aparece «Reportar incidencia» | Atualize a aplicação. Verifique também que a tarefa não está já concluída ou fechada, que não tem outra incidência aberta e que a pessoa está atribuída a ela ou é supervisora. |
| «Esta tarea ya tiene una incidencia abierta» | Só cabe uma de cada vez. Que a resolvam a partir do painel e, se acontecer outra coisa, marca-se depois. |
| Não chega o e-mail | Verifique em **Ferramentas → Alertas por e-mail** que a caixa **Incidência numa tarefa** está marcada e que os alertas por e-mail estão ativados. O alerta de **Início** aparece na mesma. |
| Antes deixava-se uma nota do tipo «Incidência» | Já não se criam: para avisar de um problema usa-se **Marcar incidência**, que avisa. As notas antigas desse tipo continuam visíveis. |

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Estados de uma tarefa](./42-estados-de-uma-tarefa.md) | Ciclo de vida e cumprimento temporal |
| [Acompanhamento e atualizações](./43-acompanhamento-e-atualizacoes.md) | Notas, histórico e acompanhamento a partir do painel |
| [Tarefa por iniciar à hora prevista](./126-tarefa-por-iniciar-a-hora-prevista.md) | O aviso aos 5 minutos, pela aplicação, por e-mail e em Início |
| [Relatórios de tarefas](./48-relatorios-de-tarefas.md) | O Excel, com a coluna e a folha de incidências |
| [A página inicial: o hoje, os alertas e as últimas semanas](../07-inteligencia-operacional/112-a-pagina-inicial-o-hoje-os-alertas-e-as-ultimas-semanas.md) | Onde aparece o alerta vermelho |
