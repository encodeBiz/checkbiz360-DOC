# Vários postos para a mesma pessoa

Em muitas empresas uma pessoa não faz sempre o mesmo. O montador que um dia conduz a carrinha, a auxiliar que substitui a coordenadora, o empregado de mesa que num evento faz de chefe de sala. Cada posto costuma ter o seu preço por hora, e até agora a ficha só admitia um por sucursal: o custo desse dia saía com o preço errado.

Agora uma pessoa pode ter **vários postos na mesma sucursal**, cada um com o seu preço por hora. Um deles é o **predefinido**, o que se aplica quando ninguém escolhe outro. Ao atribuir-lhe uma tarefa ou carregar-lhe um turno escolhe-se com que posto vai, e as horas desse trabalho valorizam-se com esse preço.

---

## O que resolve

- **Pagar e custear cada trabalho com o seu preço**, não com o do posto habitual.
- **Não duplicar fichas.** Uma só pessoa, uma só ficha, vários postos.
- **Saber depois o que fez cada um.** O relatório de tarefas diz o posto com que cada pessoa trabalhou em cada tarefa.

---

## Onde se configura

Na ficha da pessoa, bloco da sucursal, junto à sua responsabilidade. Todos os seus postos nesse local estão numa só lista, **Postos nesta sucursal**, cada um com a sua **Ocupação** e o seu **Preço por hora**:

1. Abra **Funcionários**, entre na ficha da pessoa e abra a sucursal correspondente.
2. O primeiro posto da lista é o **predefinido**, e assim o marca a etiqueta *Predefinido*. Se a pessoa tiver um só, é esse.
3. Prima **Adicionar posto** e indique a **Ocupação** (do catálogo de postos da sua empresa ou uma nova) e o seu **Preço por hora**. Ao escolher uma ocupação do catálogo, o seu preço habitual entra sozinho. O ícone da calculadora converte um salário mensal ou semanal em preço por hora.
4. Repita com cada posto. **Remover posto** retira-o da lista.
5. Guarde.

Para que outro posto passe a ser o habitual, prima **Tornar predefinido** na sua linha: os dois trocam de lugar e o predefinido antigo passa para a lista de adicionais. Um posto não pode estar duas vezes na mesma sucursal nem repetir o predefinido.

Os postos são **por sucursal**: a mesma pessoa pode ter em cada centro os seus.

O preço de cada posto só o veem e editam o **proprietário e os administradores**. Os gestores veem os nomes dos postos, sem preço.

---

## Onde se escolhe o posto

Com um só posto não há nada a escolher: tudo vai com esse. Assim que uma pessoa tem mais de um numa sucursal, aparece um seletor **Como** em três sítios:

| Onde | O que acontece |
|---|---|
| **Ao atribuir uma tarefa** | Na linha de cada pessoa atribuída, **Como** oferece os seus postos dessa sucursal, com o predefinido marcado. Pode alterar-se depois a partir de **Equipa atribuída** na ficha da tarefa. Ver [Atribuir tarefas a funcionários](../06-tarefas/41-atribuir-tarefas-a-funcionarios.md#com-que-posto-e-que-complementos). |
| **Ao carregar um turno** | Em **Mais opções** do editor do turno, o campo **Posto**. Vale para os turnos da escala e para a semana tipo. Ver [Por turnos](../04-calendario-e-horarios/114-calendario-de-turnos-por-data.md#o-posto-e-os-complementos-do-turno). |
| **Se não se escolher nada** | Aplica-se o predefinido. |

Quando a pessoa regista, o registo guarda o posto que correspondia nesse dia: o da tarefa que inicia, se não o do turno, se não o predefinido. Alterar depois o preço de um posto na ficha **não altera** o que já foi registado.

---

## Onde se nota

- **Relatório de tarefas**: a coluna **Posto** de cada linha diz com que posto a pessoa trabalhou, e o preço por hora é o desse posto. Ver [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md).
- **Rentabilidade dos contratos** e **análise do cliente**: as horas valorizam-se com o posto com que foram feitas. Ver [Contratos e rentabilidade](../17-carteira-de-clientes/121-contratos-e-rentabilidade.md).
- **Estatísticas e custos**: o custo por hora de uma pessoa passa a ser o efetivo, o dos postos que de facto ocupou.
- **Equipas**: uma equipa leva um posto por pessoa, aquele com que é dada entrada como predefinido. Os adicionais acrescentam-se depois na sucursal. Ver [Equipas](./99-equipas.md).

O relatório de assiduidade não muda: é de tempo, não de dinheiro.

---

## O que a pessoa vê na aplicação

Nada de preços. Se quiser, o posto com que vai cada tarefa poderá aparecer no seu detalhe numa versão próxima da aplicação; hoje a aplicação não o mostra e não é preciso atualizá-la para usar isto.

---

## Problemas frequentes

**Não vejo a lista de postos.** Abra a sucursal dentro da ficha da pessoa, por baixo da responsabilidade. Se não vê preços, a sua conta é de gestor.

**Não me aparece o seletor «Como» na tarefa.** Essa pessoa tem um só posto nessa sucursal. Acrescente-lhe o segundo na sua ficha.

**Alterei o preço e o relatório do mês passado continua igual.** É o esperado: cada registo guarda o preço que tinha ao ser feito. O novo vale para os registos a partir de agora.

**Quero que o predefinido seja outro.** **Tornar predefinido** na linha do posto, e guardar.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Complementos](./141-complementos.md) | O que uma pessoa recebe além do preço do seu posto |
| [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md) | Onde se indica a responsabilidade, o posto e o salário por hora |
| [Atribuir tarefas a funcionários](../06-tarefas/41-atribuir-tarefas-a-funcionarios.md) | O seletor «Como» na atribuição |
| [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md) | Uma linha por tarefa e pessoa, com o seu posto |
| [Análise de custos](../07-inteligencia-operacional/54-analise-de-custos.md) | De onde sai o custo por hora |
