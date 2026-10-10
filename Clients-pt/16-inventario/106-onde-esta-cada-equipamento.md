# Onde está cada equipamento

Um equipamento —uma lavadora, uma carrinha, um andaime— pode estar livre e, mesmo assim, não estar no armazém: foi usado numa obra e ficou lá. Este guia explica como a plataforma sabe onde está cada um e como se recolhe. Requer o complemento de inventário contratado ou em período de experiência.

---

## Livre não é o mesmo que no armazém

A plataforma separa duas coisas:

- **Se pode ser reservado.** Um equipamento deixa de estar reservado quando é libertado: liberta-o a tarefa ao fechar, ou um supervisor à mão.
- **Onde está.** Libertar um equipamento não o devolve ao armazém. Continua onde estava até alguém dizer outra coisa, e a plataforma regista-o.

Assim, um equipamento livre pode ser reservado logo para outra tarefa e, ao mesmo tempo, sabe-se que continua na obra e que alguém tem de o ir buscar.

---

## O que muda um equipamento de sítio

| O que acontece | Onde fica |
|---|---|
| É registado | No seu armazém base. |
| A sua tarefa começa | No local da tarefa. |
| A sua tarefa fecha | Continua no local da tarefa. |
| É libertado à mão | Onde disser quem o liberta: na tarefa ou num armazém. |
| É entregue a uma pessoa | Com essa pessoa. |
| É devolvido ou recebido num armazém | Nesse armazém. |
| Muda o seu armazém base | Se estava na base, na nova. |

Cada um destes factos fica registado com quem o disse e quando.

---

## Libertar um equipamento de uma tarefa

Quando um equipamento já não é preciso numa tarefa —foi reservado para o dia inteiro e só se usou de manhã—, um supervisor ou superior pode libertá-lo para que outra tarefa o use.

No detalhe da tarefa, ou no cartão do equipamento na aplicação, clique em **Libertar equipamento**. A plataforma pergunta **Onde fica?**:

- **Fica na tarefa**: o equipamento continua no local da tarefa até alguém o recolher.
- **Volta ao armazém**: escolha para que armazém. O seu armazém base aparece primeiro.

Entregar um equipamento a uma pessoa não é libertá-lo: faz-se com **Entregar**, como se explica em [Equipamentos: documentos, inspeções e entregas](./104-equipamentos-documentos-inspecoes-e-entregas.md).

Na aplicação, o trabalhador não liberta equipamentos: vê **É libertado ao concluir a tarefa**.

---

## O que há para recolher

Um equipamento livre que não está no seu armazém base aparece marcado **Fora da base**:

- Em **Existências**, o filtro de estado **Fora da base** deixa só os equipamentos livres que estão fora. Cada linha diz quantos exemplares há para recolher.
- No calendário do artigo, a linha do exemplar diz **Livre · fora da base** e onde está.

É a lista do que o armazém tem de ir buscar. Estar fora da base não impede reservá-lo para outra tarefa.

---

## Receber um equipamento no armazém

Quando o equipamento volta, quem o recebe regista-o a partir da ficha do artigo, na linha do exemplar:

1. Clique em **Receber no armazém**.
2. Escolha o **Armazém que recebe**.
3. Indique o **Estado**: **Bom**, **Danificado** ou **Perdido**, e uma nota se quiser.
4. Clique em **Receber**.

Se chegar danificado ou se tiver perdido, fica **indisponível** com esse motivo e não é oferecido para novas tarefas até alguém o voltar a pôr disponível a partir da sua ficha. Se o equipamento estava entregue a uma pessoa, recebê-lo fecha também essa entrega.

Não se pode receber um equipamento que a sua tarefa tem em uso: primeiro é preciso libertá-lo.

---

## Onde esteve

Na ficha do artigo, cada exemplar diz **onde está** agora e desde quando. Em **Onde esteve** vê-se a sua história completa: cada vez que mudou de sítio, porquê e quem o disse.

---

## Quem pode fazer o quê

| Função | Pode |
|---|---|
| Worker | Ver onde está o equipamento das suas tarefas |
| Supervisor, Manager, Owner | Além disso, libertar equipamentos de uma tarefa e recebê-los num armazém |

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Material nas tarefas](./102-material-nas-tarefas.md) | Como se reserva e acompanha o material de cada tarefa |
| [Equipamentos: documentos, inspeções e entregas](./104-equipamentos-documentos-inspecoes-e-entregas.md) | Entregar um equipamento a uma pessoa e devolvê-lo |
| [Existências, armazéns e entradas](./101-existencias-armazens-e-entradas.md) | O controlo do que há |
