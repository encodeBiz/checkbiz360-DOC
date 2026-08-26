# Turnos rotativos

Em setores como a indústria, a logística, a saúde ou a restauração, a jornada não é uniforme de uma semana para a outra: as equipas alternam faixas horárias seguindo um ciclo. Este artigo explica como essa necessidade é coberta no CheckBiz360.

---

## Estado da funcionalidade

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

O CheckBiz360 **não dispõe de um tipo de horário rotativo** com ciclo de alternância automático: não existe uma configuração de «semana A / semana B» com data de ancoragem que o sistema resolva por si. O horário semanal configurado para uma entidade, sucursal ou funcionário repete-se de forma igual todas as semanas.

---

## Como cobrir a rotação com o que existe hoje

Há duas formas de operar com equipas rotativas. A escolha depende de se a rotação é estável ou muda com frequência.

### Opção 1: uma sucursal por turno (rotação estável)

Se os turnos forem fixos e o que roda forem as pessoas, configure **uma sucursal por faixa horária** —por exemplo «Fábrica - Manhã» e «Fábrica - Tarde», com as mesmas coordenadas e a mesma geocerca— e mude a atribuição do funcionário de uma para a outra quando lhe tocar mudar.

É a opção mais limpa: cada sucursal tem o seu horário, os seus feriados e o seu calendário efetivo, e o histórico de registos fica imputado à faixa em que realmente se trabalhou.

### Opção 2: horário personalizado no funcionário (rotação variável)

Se a rotação for irregular, configure o horário na ficha do **funcionário** em vez de o herdar da sucursal, e ajuste-o ao mudar de ciclo. O calendário do funcionário tem prioridade sobre o da sua sucursal.

É mais flexível, mas exige manter a alteração à mão em cada ciclo e para cada pessoa.

> **Aviso:** em ambos os casos, mude o horário **antes** de começar o ciclo novo. Cada registo é validado contra o calendário efetivo em vigor nesse momento; atualizar o horário depois não reavalia os registos já gravados.

---

## Exemplo: manhã e tarde alternadas

Uma empresa de logística precisa de cobertura das 07:00 às 15:00 e das 15:00 às 23:00, com duas equipas que se alternam todas as semanas.

Com a Opção 1, criam-se duas sucursais sobre o mesmo pavilhão:

| Sucursal | Horário de segunda a sexta |
|---|---|
| Pavilhão - Manhã | 07:00 – 15:00 |
| Pavilhão - Tarde | 15:00 – 23:00 |

Em cada segunda-feira de mudança, o responsável reatribui os funcionários de uma sucursal para a outra. O registo de cada semana é validado contra o horário correto e os relatórios distinguem a atividade de cada faixa.

---

## Rotação e feriados

Os feriados aplicam-se por data, independentemente do turno que calhasse nesse dia: um feriado configurado na entidade ou na sucursal desativa o dia para todos os funcionários que herdem esse calendário, e uma tentativa de registo devolve `checklog/day_disabled`.

Se na sua organização se trabalha em feriado por turnos, não marque o dia como feriado na sucursal: trate-o como útil e registe as ausências de quem folga na ficha de cada funcionário. Consulte [Feriados e dias não úteis](./29-feriados-e-dias-nao-uteis.md).

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Horários base e turnos](./23-horarios-base-e-turnos.md) | Configuração do horário semanal e de vários turnos por dia |
| [Calendário laboral](./24-calendario-laboral.md) | Feriados e calendário efetivo |
| [Exceções de horário](./25-excecoes-de-horario.md) | Ajustes pontuais sobre o horário herdado |
| [Herança de configuração](./26-heranca-de-configuracao.md) | Prioridade entre entidade, sucursal e funcionário |
| [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md) | Mover um funcionário entre locais ou turnos |
