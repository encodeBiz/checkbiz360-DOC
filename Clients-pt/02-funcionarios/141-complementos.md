# Complementos: condução, feriado, trabalho noturno

A convenção coletiva ou o acordo com o pessoal dizem que certos trabalhos se pagam à parte: conduzir mais de cem quilómetros, trabalhar num feriado, fazer noite, um subsídio de perigosidade. Até agora isso anotava-se fora e o custo da tarefa saía curto.

Os **complementos** são o que uma pessoa recebe **além** do preço do seu posto por uma tarefa ou um turno concreto. Definem-se uma vez no catálogo da sua empresa e escolhem-se depois, ao atribuir a tarefa ou ao carregar o turno de quem os recebe. O registo guarda-os, e o relatório de tarefas, os contratos e as análises somam-nos ao custo, discriminados.

---

## O que resolve

- **Custear a tarefa com o que de facto custa**, subsídios incluídos.
- **Não teclar quantias de cada vez.** O complemento define-se uma vez; na tarefa só se escolhe.
- **Ter o rasto.** O relatório diz que complemento recebeu cada pessoa, em que tarefa, por que registo e quanto importou.

---

## Os três tipos

| Tipo | O que significa | Exemplo |
|---|---|---|
| **Fixo** | Um valor por tarefa ou por sessão de registo, sem olhar às horas. | Subsídio de condução: uma quantia pelo dia em que conduz. |
| **Por hora** | Um valor por cada hora trabalhada, além do preço do posto. | Trabalho noturno como quantia por hora. |
| **Percentagem** | Uma percentagem sobre o preço por hora do posto. | Feriado: *25* significa 25 % a mais sobre o preço por hora. |

Uma percentagem calcula-se sobre o preço do posto com que se fez o trabalho, por isso um mesmo «Feriado, 25 %» vale diferente para um oficial e para um servente. É o que a convenção costuma dizer.

---

## Criar o catálogo

Os complementos estão em **Entidade**, separador **Complementos**. O mesmo catálogo abre-se também numa janela a partir de onde se usa: o botão **Catálogo de complementos** está ao atribuir a tarefa, em **Posto e complementos** e no editor do turno, para criar o que falta sem sair do que estava a fazer.

1. Prima **Adicionar complemento**.
2. Escreva o **Nome**, tal como a sua convenção o designa: *Subsídio de condução*, *Feriado*, *Trabalho noturno*.
3. Escolha o **Tipo**: *Fixo*, *Por hora* ou *Percentagem*.
4. Indique o **Valor** (ou a **Percentagem**, de 0 a 500).
5. Guarde.

Não pode haver dois complementos com o mesmo nome. **Editar** altera nome, tipo ou valor para o que se escolher a partir de então: **o que já foi atribuído conserva o valor que tinha ao ser escolhido**. **Dar baixa** retira-o dos seletores sem apagar nada; o que já o tinha não muda, e pode **Reativar**.

O valor dos complementos só o veem e editam o **proprietário e os administradores**. Os gestores veem o catálogo pelo nome e podem escolhê-los em tarefas e turnos, sem ver valores.

---

## Escolhê-los na tarefa ou no turno

Um complemento é **de uma pessoa num trabalho concreto**, não da tarefa inteira: numa tarefa de três pessoas pode recebê-lo só quem conduz.

| Onde | Como |
|---|---|
| **Ao atribuir uma tarefa** | Na linha de cada pessoa atribuída, prima **Complemento** e escolha um do catálogo; repita se receber mais de um. Cada um aparece como uma etiqueta que se pode retirar. Ver [Atribuir tarefas a funcionários](../06-tarefas/41-atribuir-tarefas-a-funcionarios.md#com-que-posto-e-que-complementos). |
| **A partir da ficha da tarefa** | Em **Equipa atribuída**, a ação **Posto e complementos** de cada pessoa permite alterá-los enquanto a tarefa não estiver concluída. |
| **Ao carregar um turno** | Em **Mais opções** do editor do turno, o campo **Complementos**. Vale para os turnos da escala e para a semana tipo. Ver [Por turnos](../04-calendario-e-horarios/114-calendario-de-turnos-por-data.md#o-posto-e-os-complementos-do-turno). |

Se uma pessoa tiver além disso [vários postos](./140-varios-postos-para-a-mesma-pessoa.md), na mesma linha escolhe com qual vai.

Quando a pessoa regista, o registo guarda os complementos que correspondiam: os da tarefa que inicia ou, se não, os do turno. Cada um guarda-se com o valor que tinha nesse momento.

Um complemento **fixo** recebe-se uma vez por sessão de registo (ou uma vez pela atribuição, se a tarefa não teve registos). Os de **por hora** e **percentagem** vão com as horas dessa pessoa nessa tarefa.

---

## Onde se nota

- **Relatório de tarefas**: cada linha de pessoa leva **Complementos** (os nomes com o seu valor) e **Complementos (valor)**, e o custo da pessoa inclui-os. A folha **Complementos** é o rasto, linha a linha. Ver [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md).
- **Contratos e análise do cliente**: o custo bruto do contrato soma os complementos como rubrica própria, ao lado do pessoal, do material e das despesas. Ver [Contratos e rentabilidade](../17-carteira-de-clientes/121-contratos-e-rentabilidade.md).
- **Estatísticas e custos**: o custo da sucursal, o custo por hora e o desvio económico incluem-nos e indicam-nos à parte.

O relatório de assiduidade não os leva: é de tempo, não de dinheiro.

---

## O que a pessoa vê na aplicação

Nada: nem valores nem quantias. Os complementos são uma ferramenta de administração.

---

## Problemas frequentes

**Não vejo o separador «Complementos» nem os valores.** A sua conta é de gestor. O proprietário e os administradores criam o catálogo; o utilizador gestor pode escolhê-los pelo nome em tarefas e turnos.

**Não consigo escolher um complemento na tarefa.** O catálogo está vazio ou todos estão de baixa. Crie-o em **Entidade → Complementos**, ou carregue em **Catálogo de complementos** na própria atribuição.

**Corrigi o valor de um complemento e o relatório não muda.** O que já foi escolhido conserva o seu valor. Se foi um erro numa tarefa concreta, retire o complemento dessa pessoa a partir de **Posto e complementos** e volte a adicioná-lo: entra com o valor novo.

**Quero que o feriado ou a noite se apliquem sozinhos.** Hoje os complementos escolhem-se à mão na tarefa ou no turno: a plataforma não decide por si que dia é feriado para a sua convenção. Carregue o turno do feriado com o seu complemento.

**Um subsídio que é uma quantia por quilómetro.** Defina-o como fixo com o valor do percurso habitual, ou crie dois (*Condução curta*, *Condução longa*). A quantia exata por quilómetro não se calcula.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Vários postos para a mesma pessoa](./140-varios-postos-para-a-mesma-pessoa.md) | Postos com o seu preço e o predefinido |
| [Atribuir tarefas a funcionários](../06-tarefas/41-atribuir-tarefas-a-funcionarios.md) | Escolher posto e complementos ao atribuir |
| [Por turnos: o horário são os turnos que carrega](../04-calendario-e-horarios/114-calendario-de-turnos-por-data.md) | «Mais opções» do turno |
| [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md) | As folhas Por pessoa e Complementos |
| [Contratos e rentabilidade](../17-carteira-de-clientes/121-contratos-e-rentabilidade.md) | Os complementos no custo do contrato |
