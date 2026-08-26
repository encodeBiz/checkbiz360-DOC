# Calendário laboral no CheckBiz360

O calendário laboral é o registo de dias não úteis que o sistema consulta em cada registo de ponto para determinar se esse dia está ativo para trabalhar. No CheckBiz360, este calendário pode ser configurado a diferentes níveis hierárquicos, o que permite que a mesma organização faça a gestão de feriados nacionais comuns a par de feriados locais específicos de cada sucursal.

---

## O que é o calendário laboral

O calendário laboral no CheckBiz360 é uma lista de datas que o sistema marca como não úteis. Quando um funcionário tenta registar numa dessas datas, o sistema deteta-o e devolve o código `checklog/day_disabled`, recusando o registo.

Este mecanismo protege a integridade dos registos de assiduidade e evita que se gerem jornadas em dias em que a empresa, por regulamentação ou por política interna, não opera.

---

## Tipos de dia não útil

O CheckBiz360 permite classificar cada entrada do calendário em função do seu âmbito:

- **Feriado nacional:** aplica-se a toda a entidade e, por herança, a todas as suas sucursais e funcionários.
- **Feriado regional ou municipal:** configura-se ao nível da sucursal. Só afeta os funcionários dessa sucursal concreta.
- **Dia não útil interno:** pode ser qualquer data que a empresa decida marcar como não útil por motivos próprios (encerramento para inventário, ponte de empresa, etc.).

Cada tipo tem um âmbito diferente dentro da hierarquia de configuração, o que se detalha na secção seguinte.

---

## Hierarquia entity → branch → employee

O calendário laboral segue a mesma hierarquia de três níveis que o resto da configuração no CheckBiz360: entidade, sucursal e funcionário.

### Nível entidade

Os feriados configurados na entidade aplicam-se por omissão a todos os funcionários da organização, independentemente da sucursal a que pertençam. Este é o nível adequado para gerir feriados nacionais ou encerramentos corporativos.

### Nível sucursal

Cada sucursal pode ter o seu próprio calendário de dias não úteis adicionais. Estes dias somam-se aos feriados herdados da entidade. Um feriado configurado numa sucursal não afeta as restantes sucursais.

### Nível funcionário

Um funcionário concreto pode ter exceções individuais que marquem dias específicos como não úteis (ou, pelo contrário, como úteis se a sucursal os tiver marcados como feriados). As exceções individuais têm a prioridade mais alta na hierarquia.

> **Nota:** a resolução hierárquica segue a regra de que a configuração mais próxima do funcionário prevalece sobre a mais geral. Se uma data for feriado na entidade mas o funcionário tiver uma exceção individual que a marque como útil, o funcionário poderá registar nesse dia.

---

## Como adicionar um feriado

Para adicionar um feriado ao calendário laboral, siga estes passos:

**Ao nível da entidade:**

1. Aceda ao backoffice com perfil owner.
2. Navegue até **Calendário** e coloque-se no separador **Configuração geral**.
3. Prima o botão **Adicionar dia não útil**.
4. Selecione a data no seletor de calendário.
5. Indique o tipo (feriado nacional, ponte, encerramento interno, etc.) e, opcionalmente, adicione uma descrição.
6. Guarde o registo.

**Ao nível da sucursal:**

1. Aceda ao backoffice com perfil owner ou manager.
2. Navegue até **Sucursais** e selecione a sucursal correspondente.
3. Aceda a **Calendário** e coloque-se no separador **Sucursal**.
4. Siga os passos 3 a 6 do procedimento anterior.

As alterações são efetivas de imediato. Uma vez guardado o feriado, qualquer tentativa de registo nessa data por parte dos funcionários afetados será bloqueada.

---

## Impacto nos registos

Quando um funcionário tenta registar a sua entrada ou saída numa data marcada como não útil no seu calendário efetivo, o sistema devolve o código de erro `checklog/day_disabled`.

Este erro fica gravado no histórico do funcionário com o seu timestamp e os dados da tentativa. Não se gera qualquer jornada nem se contam horas.

| Situação | Resultado |
|---|---|
| Registo em dia útil ativo | Processo de validação normal. |
| Registo em feriado da entidade | `checklog/day_disabled`. Registo recusado. |
| Registo em feriado da sucursal | `checklog/day_disabled`. Registo recusado. |
| Registo em dia desativado no horário base | `checklog/day_disabled`. Registo recusado. |

> **Aviso:** se a sua empresa trabalha habitualmente em feriados (por exemplo, nos setores do retalho ou da restauração), deve rever a configuração do calendário para não bloquear registos válidos. Consulte o artigo [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md) para saber como gerir este caso.

---

## Consultar o calendário de um funcionário

A partir do backoffice, o responsável pode consultar que dias estão marcados como não úteis para um funcionário concreto:

1. Aceda a **Funcionários** e selecione o funcionário.
2. Abra a secção **Calendário efetivo**.
3. O sistema mostra o calendário mensal com os dias úteis, os feriados herdados da entidade e da sucursal, e as exceções individuais do funcionário.

Esta vista é especialmente útil para depurar situações em que um funcionário reporta que não conseguiu registar numa determinada data.

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Exceções de horário](25-excecoes-de-horario.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md)
- [Estados e códigos de erro](../03-controlo-de-horarios/22-estados-e-codigos-de-erro.md)
