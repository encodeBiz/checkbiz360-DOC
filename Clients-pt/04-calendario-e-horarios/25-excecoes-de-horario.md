# Exceções de horário

O horário base de uma sucursal ou entidade define as condições padrão de trabalho para a generalidade dos funcionários. Existem, porém, situações legítimas em que um funcionário precisa de um horário diferente do dos restantes: uma redução de jornada por motivos familiares, uma adaptação temporária durante um período de recuperação, ou um horário especial acordado contratualmente.

Para dar resposta a estes casos, o CheckBiz360 permite configurar exceções individuais de horário. Uma exceção é uma regra de horário associada exclusivamente a um funcionário concreto que prevalece sobre o horário herdado da sucursal ou da entidade.

---

## Tipos de exceção

### Exceção pontual

Uma exceção pontual aplica-se a um único dia concreto. É útil para casos isolados: o funcionário entra mais cedo ou mais tarde do que o habitual num dia específico, ou esse dia está marcado como não útil apenas para ele.

Exemplo: a 15 de junho, o funcionário tem uma consulta médica e a sua jornada começa às 11:00 em vez das 09:00. Cria-se uma exceção pontual para essa data com o turno ajustado.

### Exceção periódica

Uma exceção periódica repete-se de forma sistemática, geralmente com uma cadência semanal. É a modalidade mais adequada para situações de longa duração, como uma jornada reduzida por assistência à família ou um horário de adaptação laboral após uma baixa.

Exemplo: todas as sextas-feiras, o funcionário tem jornada contínua e sai às 15:00 em vez das 17:00. Configura-se uma exceção periódica que se aplica todas as sextas-feiras enquanto vigorar o período de adaptação.

---

## Como criar uma exceção de horário

1. Aceda ao backoffice com perfil owner ou manager.
2. Navegue até **Funcionários** e selecione o funcionário correspondente.
3. Aceda à secção **Horário e calendário**.
4. Prima o botão **Nova exceção**.
5. Selecione o tipo de exceção: **Pontual** ou **Periódica**.
6. Se for pontual, indique a data concreta.
7. Se for periódica, selecione os dias da semana a que se aplica e defina a data de início e, opcionalmente, a data de fim.
8. Configure a faixa horária da exceção: hora de início (`start.hour`, `start.minute`) e hora de fim (`end.hour`, `end.minute`).
9. Se a exceção marcar o dia como não útil para esse funcionário, ative a opção **Dia não útil**.
10. Guarde a exceção.

Depois de guardada, a exceção entra em vigor de imediato. O sistema usá-la-á nos próximos registos do funcionário.

> **Aviso:** as exceções de horário não têm efeito retroativo sobre registos já gravados. Afetam apenas os registos efetuados a partir do momento da sua criação.

---

## Casos de utilização habituais

### Funcionário com jornada reduzida

Um funcionário com redução de jornada por conciliação familiar trabalha das 09:00 às 14:00 em vez do horário padrão das 09:00 às 17:00. Configura-se uma exceção periódica que se aplica de segunda a sexta-feira com o turno reduzido. Os restantes funcionários da sucursal mantêm o seu horário habitual sem qualquer alteração.

### Horário de adaptação laboral

Um funcionário que se reintegra após uma baixa longa começa com jornadas mais curtas durante as primeiras semanas. Cria-se uma exceção periódica com uma data de fim definida. Quando chega essa data, o sistema deixa de aplicar a exceção e o funcionário regressa automaticamente ao horário da sucursal.

### Dia pontual não útil

Um funcionário pede um dia de licença sem vencimento. O responsável pode criar uma exceção pontual que marque esse dia como não útil para esse funcionário. Qualquer tentativa de registo nesse dia gerará o código `checklog/day_disabled`, tal como acontece nos feriados do calendário geral.

---

## Prioridade das exceções individuais

Quando o sistema resolve o calendário efetivo de um funcionário, segue uma ordem de prioridade. As exceções individuais têm a prioridade mais alta e prevalecem sempre sobre o horário da sucursal e o da entidade.

A lógica é a seguinte:

1. O sistema verifica se o funcionário tem uma exceção individual ativa para esse dia.
2. Se existir uma exceção, usa-a como referência para validar o registo.
3. Se não existir qualquer exceção, consulta o horário da sucursal.
4. Se a sucursal não tiver um horário próprio configurado, utiliza o horário da entidade.

Isto significa que uma exceção individual pode tanto restringir como alargar o horário herdado. Se o horário da sucursal definir um turno das 09:00 às 17:00 mas o funcionário tiver uma exceção das 07:00 às 15:00, o sistema utilizará o turno das 07:00 às 15:00 para esse funcionário.

> **Nota:** para uma explicação completa do algoritmo de resolução hierárquica, consulte o artigo [Herança de configuração](26-heranca-de-configuracao.md).

---

## Gestão e revisão de exceções ativas

O responsável pode consultar a qualquer momento as exceções ativas de um funcionário a partir da ficha do funcionário no backoffice. A secção **Horário e calendário** mostra a lista de exceções em vigor com o seu tipo, datas de aplicação e a faixa horária configurada.

Para desativar uma exceção antes da sua data de fim prevista, selecione-a e prima **Desativar**. A exceção fica arquivada e o funcionário recupera o horário herdado da sucursal ou da entidade.

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Calendário laboral](24-calendario-laboral.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Jornada estrita e jornada flexível](28-horario-flexivel.md)
- [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md)
