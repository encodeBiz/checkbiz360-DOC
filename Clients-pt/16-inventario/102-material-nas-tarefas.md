# Material nas tarefas

O inventário foi pensado para que o material se acompanhe no mesmo sítio onde se acompanha o trabalho: a tarefa. Este guia percorre o ciclo completo, do planeamento ao fecho.

---

## O ciclo, em quatro passos

| Passo | Quem | O que acontece |
|---|---|---|
| **1. Reservar** | Quem planeia | Decide-se o material de que a tarefa precisa. Fica comprometido no armazém, mas ainda não sai. |
| **2. Retirar** (opcional) | Quem gere o armazém | Na ficha do armazém ou do artigo, **Saída para uma tarefa**: o material sai para esse trabalho. Se ninguém o fizer, a saída é registada pelo consumo. |
| **3. Declarar** | O trabalhador | Indica quanto se gastou, previsto ou não. |
| **4. Acertar** | Quem valida | O que ficou por declarar resolve-se: do que saiu, quanto voltou ao armazém; do reservado, quanto se gastou. O resto volta ao armazém. |

Atribuir material não é gastá-lo: enquanto não for declarado ou acertado, a plataforma não o dá por consumido.

---

## 1. Atribuir material ao criar a tarefa

No formulário de **Nova tarefa** aparece o bloco **Material para a tarefa**:

1. Escolha primeiro a **sucursal**: os armazéns saem dela.
2. Clique em **Adicionar material** e procure o artigo.
3. Se se gasta, indique a **quantidade** (e o armazém, se a sucursal tiver vários). Se se empresta, escolha o **exemplar**.
4. Crie a tarefa. O material fica reservado nesse momento.

Se não houver existências suficientes, reserva-se na mesma e há um aviso. Se um exemplar já estiver reservado por outra tarefa nesse período, indica-se com que tarefa coincide.

---

## 2. O material no detalhe da tarefa

O detalhe da tarefa mostra uma tabela com todo o seu material, seja de que tipo for:

- Para o que se gasta: o reservado, o que saiu, o gasto, o devolvido e o **por declarar**.
- Para o que se empresta: o exemplar, o seu período e o estado da reserva.

A partir daí, **Adicionar material** reserva mais e **Declarar consumo** regista o gasto no backoffice, sobre o reservado ou sobre o não previsto, sem registar antes nenhuma saída: é o prático quando a tarefa se planeia e fecha no backoffice. As saídas não se dão a partir da tarefa, mas do armazém ou do artigo. Um exemplar pode ser **libertado** se já não for preciso: a plataforma pergunta **Onde fica?** —na tarefa ou num armazém—, porque libertá-lo não o devolve ao armazém (ver [Onde está cada equipamento](./106-onde-esta-cada-equipamento.md)). Um **fora de regra** pode ser reservado na mesma, depois de aceitar o aviso.

---

## 3. Na aplicação: o trabalhador só declara o consumo

O trabalhador vê o material da tarefa na própria tarefa da aplicação e tem um único botão, **Declarar consumo**: vem pré-preenchido com o reservado; se se gastou tudo, basta confirmar. Pode corrigir quantidades e acrescentar o que gastou sem estar previsto. Não regista nenhuma saída: se o armazém não a deu, a plataforma regista-a ao declarar.

Se a sucursal tiver vários armazéns e acrescentar algo não previsto, a aplicação pergunta de qual saiu.

O cartão de cada equipamento diz onde está. Um supervisor ou superior pode **libertá-lo** a partir da aplicação, dizendo se fica na tarefa ou volta a um armazém; o trabalhador vê que é libertado ao concluir a tarefa.

---

## 4. Acertar ao validar

Ao validar uma tarefa concluída, se houver material por declarar, a plataforma pede para o **acertar** antes de validar:

- Do que **saiu** e ninguém declarou: quanto voltou ao armazém; o resto dá-se por gasto.
- Do **reservado** sem saída registada: quanto se gastou (vem pré-preenchido com todo o reservado); o resto volta ao armazém.

Assim nenhuma tarefa fecha com material perdido pelo caminho. Numa tarefa já fechada, a tabela de material mostra o que se reservou, o que se libertou ao fechar e, se nada foi registado, di-lo.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Existências, armazéns e entradas](./101-existencias-armazens-e-entradas.md) | Como se dá entrada do material |
| [Validação de tarefas](../06-tarefas/45-validacao-de-tarefas.md) | O passo de validação em que se acerta o material |
| [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md) | O material de cada tarefa no relatório |
| [Onde está cada equipamento](./106-onde-esta-cada-equipamento.md) | Libertar um equipamento, o que há para recolher e recebê-lo no armazém |
