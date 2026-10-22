# Herança de configuração: como se resolve o calendário efetivo

Quando um funcionário regista, o sistema precisa de determinar que horário deve aplicar nesse momento concreto. Esta determinação não se faz consultando um único valor: o sistema percorre uma cadeia hierárquica de configurações e aplica a regra que estiver mais próxima do funcionário. Este mecanismo designa-se herança de configuração ou cascata de horários.

---

## Os três níveis da hierarquia

O CheckBiz360 organiza a configuração de horários em três níveis:

1. **Entidade:** o nível mais geral. Define os parâmetros que se aplicam a toda a organização.
2. **Sucursal:** o nível intermédio. Uma sucursal pode ter a sua própria configuração que substitui parcial ou totalmente a da entidade.
3. **Funcionário:** o nível mais específico. As exceções individuais de um funcionário têm prioridade absoluta sobre qualquer configuração de nível superior.

A regra fundamental é que a configuração mais próxima do funcionário ganha sempre.

---

## Algoritmo de resolução em cascata

Quando o sistema precisa de conhecer o horário efetivo de um funcionário para uma data e hora concretas, executa o seguinte processo:

1. Verifica se o funcionário tem uma exceção individual ativa para esse dia (exceção pontual) ou para esse dia da semana (exceção periódica).
2. Se existir uma exceção individual, utiliza-a como horário efetivo e interrompe a procura. Não consulta os níveis superiores.
3. Se não existir exceção individual, verifica se a sucursal do funcionário tem um horário próprio configurado.
4. Se a sucursal tiver horário próprio, utiliza-o como horário efetivo e interrompe a procura.
5. Se a sucursal não tiver horário próprio, consulta o horário da entidade e utiliza-o.

Este processo garante que existe sempre um horário efetivo válido, mesmo que os níveis intermédios não tenham configuração própria.

---

## Exemplo concreto com três níveis distintos

Suponha a seguinte configuração numa empresa com uma entidade principal e uma sucursal numa cidade diferente:

| Nível | Dia | Início | Fim |
|---|---|---|---|
| Entidade | Segunda a sexta | 09:00 | 17:00 |
| Sucursal Madrid | Segunda a sexta | 08:30 | 16:30 |
| Funcionário García | Segunda a sexta | 07:00 | 15:00 (exceção periódica) |

O funcionário García trabalha na sucursal Madrid. O seu horário efetivo não é o da entidade (09:00–17:00) nem o da sucursal (08:30–16:30), mas sim a sua exceção individual (07:00–15:00). Se García registar às 07:05, o sistema aceita porque cai dentro do seu turno efetivo.

Um funcionário da sucursal Madrid sem exceção individual registará com o horário da sucursal (08:30–16:30). Um funcionário de uma sucursal sem configuração própria herdará diretamente o horário da entidade (09:00–17:00).

---

## Que configurações se herdam e quais não

A herança não funciona da mesma forma para todos os parâmetros. Em termos gerais:

- O **calendário de feriados** acumula-se: os feriados da entidade mais os feriados próprios da sucursal formam o calendário de dias não úteis dos funcionários dessa sucursal.
- O **horário de turnos** substitui-se: se a sucursal tiver um horário próprio, substitui completamente o da entidade. Não se misturam.
- As **exceções individuais** de um funcionário substituem completamente o horário do nível superior para as datas ou dias a que se aplicam.
- A forma de **organizar o horário** também se herda: se uma sucursal estiver em **Calendário**, os seus funcionários também estão, exceto quem tiver outro modo na sua ficha. **Horário por tarefas** é a exceção: só se escolhe na ficha de cada pessoa. Ver [Calendário: turnos carregados por data](114-calendario-de-turnos-por-data.md).

> **Nota:** o comportamento de acumulação de feriados significa que um funcionário de uma sucursal local pode herdar tanto os feriados nacionais da entidade como os feriados locais da sua sucursal. Isto é intencional e reflete a realidade legal da maioria das empresas.

---

## Como depurar o horário efetivo de um funcionário no backoffice

Se um responsável precisar de verificar que horário está a ser usado por um funcionário num determinado momento, pode consultá-lo a partir do backoffice seguindo estes passos:

1. Aceda ao backoffice com perfil owner ou manager.
2. Navegue até **Funcionários** e selecione o funcionário cujo horário pretende rever.
3. Abra a secção **Calendário efetivo**.
4. O sistema mostra o calendário do mês em curso com a origem de cada configuração: fica claramente indicado se o dia usa o horário da entidade, o da sucursal ou uma exceção individual.
5. Para consultar um mês diferente, use os controlos de navegação do calendário.
6. Para ver o detalhe de um dia concreto (turnos ativos, faixas horárias, exceções aplicadas), clique na célula do dia.

Esta ferramenta é a primeira referência quando um funcionário reporta que não conseguiu registar ou que o sistema validou a sua entrada num horário inesperado.

---

## Erros habituais relacionados com a herança

### O funcionário não consegue registar quando deveria conseguir

Verifique que não existe uma exceção individual que marque esse dia como não útil. As exceções individuais prevalecem sobre o horário da sucursal, pelo que uma exceção ativa pode estar a bloquear registos válidos.

### O funcionário consegue registar num horário que não lhe corresponde

Verifique se existe uma exceção periódica ativa com uma faixa horária mais ampla do que a do horário da sucursal. Se existir, o sistema utilizá-la-á em vez do horário padrão.

### A sucursal tem feriado mas o funcionário consegue registar

O funcionário pode ter uma exceção individual que marque esse dia como útil. As exceções individuais anulam os feriados de nível superior quando estão configuradas explicitamente.

> **Aviso:** antes de contactar o apoio por um comportamento inesperado no registo de um funcionário, reveja sempre o calendário efetivo a partir do backoffice. A maioria das incidências tem origem numa exceção individual configurada incorretamente ou num feriado que não foi removido depois de ficar obsoleto.

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Calendário laboral](24-calendario-laboral.md)
- [Exceções de horário](25-excecoes-de-horario.md)
- [Turnos rotativos](27-turnos-rotativos.md) — não disponível na versão atual; alternativas
- [Jornada estrita e jornada flexível](28-horario-flexivel.md)
- [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md)
- [Calendário: turnos carregados por data](114-calendario-de-turnos-por-data.md)
