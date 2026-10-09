# Quadro de disponibilidade

O quadro de disponibilidade responde a uma pergunta a que o horário, por si só, não responde: **quantas pessoas estão realmente disponíveis em cada dia em cada sucursal, e quem falta**. Não é um dado que seja preciso manter: o quadro calcula-o cruzando o horário de cada funcionário com os feriados, as suas ausências e o estado da sua ficha.

Encontra-se em **Horários** → separador **Disponibilidade**.

---

## O que mostra

Uma grelha com uma linha por sucursal e uma coluna por dia. Cada célula indica quantas pessoas estão disponíveis nesse dia sobre o total de efetivos dessa sucursal, com a respetiva percentagem de cobertura.

A cor de cada célula resume a situação:

| Cor | Legenda | O que significa |
|---|---|---|
| Verde | **Cobertura ≥ 70%** | Está disponível a maioria de quem deveria trabalhar. |
| Âmbar | **Cobertura ajustada 55 – 70%** | Faltam bastantes pessoas; convém rever. |
| Vermelho | **Cobertura crítica < 55%** | Há pessoas que deveriam estar e não estão: uma lacuna de cobertura. |
| Cinzento | **Descanso ou feriado** | Nesse dia ninguém trabalha nem deveria: a sucursal fecha ou é feriado. |

A diferença entre o cinzento e o vermelho é a mais importante do quadro. Um feriado da empresa aparece a **cinzento**, porque não falta ninguém. Um dia útil em que metade dos efetivos está de férias aparece a **vermelho**, porque é um problema de cobertura.

Os funcionários que não têm sucursal atribuída aparecem agrupados numa linha à parte.

---

## Como se usa

- **Vista mensal ou semanal.** Alterne entre **Mensal** e **Semanal**, e avance ou recue com as setas de período.
- **Filtrar por sucursal.** Por omissão veem-se **Todas**; escolha uma para se centrar nela.
- **Exportar.** O botão **Exportar** descarrega um ficheiro CSV com uma linha por sucursal e dia: equipa, data, disponíveis, efetivos e percentagem de cobertura.

> **Nota:** se os efetivos forem demasiados para serem calculados de uma só vez, o quadro pedir-lhe-á que escolha uma sucursal para ver a sua cobertura.

---

## O detalhe de um dia

Clique numa célula para abrir o detalhe desse dia nessa sucursal. Mostra duas colunas:

- **Disponíveis**: quem está.
- **Indisponíveis**: quem não está, e porquê.

Os motivos possíveis são:

| Motivo | O que significa |
|---|---|
| **Sem turno** | O seu horário não tem turno nesse dia. |
| **Feriado** | É feriado da entidade ou da sucursal. |
| **Ausência** | Tem registada uma ausência própria: férias, licença, dia livre. |
| **Baixa ou licença** | O estado da sua ficha indica que não está no ativo. |

O detalhe inclui uma pesquisa por nome, que ignora acentos e cedilhas e aceita nome e apelidos por qualquer ordem.

---

## Marcar ou retirar um dia livre a partir do detalhe

O gesto mais habitual ao olhar para o quadro é «esta pessoa amanhã não vem». Regista-se a partir do próprio detalhe:

- **Adicionar dia livre**: arraste a pessoa de **Disponíveis** para **Indisponíveis**, ou prima a seta da sua linha.
- **Retirar o dia livre**: arraste a pessoa de volta, ou prima a seta.

Largar não guarda nada por si só: abre-se o formulário habitual, com a pessoa e a data já preenchidas, onde pode indicar se a ausência é **remunerada**. Um arrastamento acidental desfaz-se com **Cancelar**.

Só se pode devolver a disponível quem falta por uma **ausência própria**. Os restantes motivos não se resolvem a partir daqui, e a sua seta aparece desativada com uma explicação:

- Um **feriado** da entidade ou da sucursal afeta todos os efetivos: gere-se no seu calendário.
- **Sem turno** depende do horário dessa pessoa: altera-se no seu calendário.
- **Baixa ou licença** é o estado da sua ficha: altera-se aí.

Depois de cada alteração, o quadro volta a calcular a cobertura com os dados guardados.

---

## Quem pode vê-lo

- Owners, administradores e managers veem a disponibilidade de toda a entidade.
- Os supervisores veem a das suas sucursais.
- Os funcionários sem responsabilidade de gestão não têm acesso.

---

## Limitações atuais

- Quem trabalha em **duas sucursais** conta nas duas: ainda não existe a atribuição de turno por dia e sucursal.
- Se algum feriado tiver uma data que não se consegue ler, o quadro descarta-o e avisa no ecrã; o número de cobertura não o conta.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Horários base e turnos](./23-horarios-base-e-turnos.md) | O horário semanal de que parte o cálculo |
| [Calendário laboral](./24-calendario-laboral.md) | Feriados por níveis e o seu efeito no registo |
| [Feriados e dias não úteis](./29-feriados-e-dias-nao-uteis.md) | Ausências de funcionários, intervalos de datas e marca de remunerada |
| [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md) | De que sucursal faz parte cada pessoa |
