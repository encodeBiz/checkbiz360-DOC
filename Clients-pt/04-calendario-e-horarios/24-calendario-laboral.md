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

Um funcionário concreto pode ter os seus próprios dias não úteis: férias, licenças ou qualquer ausência. Somam-se aos feriados da entidade e da sua sucursal e só o afetam a ele.

> **Importante:** os feriados **somam-se** entre níveis; não se anulam. Um feriado da entidade ou da sucursal aplica-se a todos os seus funcionários mesmo que algum tenha um horário personalizado com turno nesse dia: o registo é recusado na mesma com `checklog/day_disabled`. A herança em que manda o nível mais próximo do funcionário é a do **horário semanal**, e não a dos feriados. Se na sua organização só uma parte do quadro de pessoal trabalha num feriado, consulte [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md#o-que-acontece-se-a-empresa-trabalha-em-feriado).

Cada dia não útil indica de que nível vem —entidade, sucursal ou funcionário—, de modo que na ficha do funcionário se distingue o que a empresa fecha do que é uma ausência própria.

---

## Como adicionar um feriado

Para adicionar um feriado ao calendário laboral, siga estes passos:

**Ao nível da entidade:**

1. Aceda ao backoffice com perfil owner.
2. Abra **Horários** no menu lateral e coloque-se no separador **Configurações gerais**.
3. Em **Feriados da entidade**, prima **Adicionar feriado**.
4. Escreva o nome do feriado e selecione a data; se o desejar, adicione uma descrição.
5. Prima **Salvar feriado**.

**Ao nível da sucursal:**

1. Aceda ao backoffice com perfil owner ou manager.
2. Abra a ficha da sucursal correspondente.
3. No bloco **Dias de folga** da sucursal, adicione o feriado com os mesmos dados.

**Ao nível do funcionário:** as ausências de uma pessoa registam-se a partir da sua ficha ou diretamente a partir do [quadro de disponibilidade](98-quadro-de-disponibilidade.md). O separador **Dias não úteis dos funcionários** de **Horários** permite procurar um funcionário e consultar os seus dias não úteis com a respetiva origem. Uma ausência pode abranger um **intervalo de datas** e levar a marca **Remunerada**; explica-se em [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md#ausências-de-um-funcionário).

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
| Registo num dia não útil próprio do funcionário (férias, licença) | `checklog/day_disabled`. Registo recusado. |
| Registo com uma ausência registada que abrange esse dia | `checklog/absence`. Registo recusado. |

A partir da versão 1.3.2, a aplicação não se limita a mostrar o código: explica num diálogo que esse dia não é útil e que, se o funcionário trabalhou, pode [solicitar uma jornada manual](../03-controlo-de-horarios/19-solicitar-jornada-manual.md). No cartão do dia distingue ainda um **feriado** de um **dia livre**.

> **Aviso:** se a sua empresa trabalha habitualmente em feriados (por exemplo, nos setores do retalho ou da restauração), deve rever a configuração do calendário para não bloquear registos válidos. Consulte o artigo [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md) para saber como gerir este caso.

---

## Consultar o calendário de um funcionário

A partir do backoffice, o responsável pode consultar que dias estão marcados como não úteis para um funcionário concreto:

1. Aceda a **Funcionários** e abra a ficha do funcionário.
2. Abra o separador de horários.
3. Junto ao seu horário, a ficha mostra os seus dias não úteis separados por origem: **Herdados da entidade**, **herdados da sua sucursal** e **próprias do colaborador**. As ausências de vários dias seguidos aparecem agrupadas numa só linha com o respetivo intervalo.

Esta vista é especialmente útil para depurar situações em que um funcionário reporta que não conseguiu registar numa determinada data. Para ver num relance quem está disponível em cada dia em toda uma sucursal, use o [quadro de disponibilidade](98-quadro-de-disponibilidade.md).

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Exceções de horário](25-excecoes-de-horario.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Feriados e dias não úteis](29-feriados-e-dias-nao-uteis.md)
- [Quadro de disponibilidade](98-quadro-de-disponibilidade.md)
- [Estados e códigos de erro](../03-controlo-de-horarios/22-estados-e-codigos-de-erro.md)
