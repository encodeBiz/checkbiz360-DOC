# Jornada estrita e jornada flexível

O CheckBiz360 não conta as horas trabalhadas de uma única forma: cada calendário decide se aplica o **horário oficial** ou o **tempo realmente trabalhado**. Essa decisão toma-se com um interruptor, **Jornada estrita / Jornada flexível**, e é provavelmente o ajuste com maior impacto sobre os relatórios de horas.

Existe o mesmo interruptor para os descansos, com a mesma lógica.

---

## Jornada estrita

Com a jornada estrita, **manda o horário configurado**. O sistema não reconhece tempo trabalhado fora da faixa oficial:

- As entradas **antes** do horário não são contabilizadas.
- As entradas tardias e as saídas antecipadas **são descontadas**.
- As saídas **depois** do horário não são contabilizadas como tempo extra.

É a opção adequada quando a jornada está fechada por convenção coletiva ou por política interna e não se quer que o hábito de chegar dez minutos mais cedo acabe por gerar horas extraordinárias no relatório. O funcionário que chega às 08:50 a um turno das 09:00 não acumula esses dez minutos; quem chega às 09:10 vê o atraso descontado.

## Jornada flexível

Com a jornada flexível, **manda o que o funcionário registou**:

- Contabiliza-se a jornada real trabalhada.
- O tempo trabalhado antes ou depois do horário **soma-se como extra**.
- Os atrasos e as saídas antecipadas **são descontados**.

É a opção adequada quando o horário é uma referência e o que se pretende medir é a dedicação efetiva: equipas de campo, serviços com picos de trabalho, turnos que se prolongam por necessidade operacional.

> **Importante:** nenhuma das duas modalidades altera o que o funcionário regista. O registo guarda sempre a hora real; o que muda é como essa hora é contabilizada ao calcular o tempo trabalhado. A rastreabilidade do registo original conserva-se em ambos os casos.

---

## Como se configura

1. Abra o horário que pretende ajustar: o da entidade em **Horários** → **Configurações gerais**, ou o de uma sucursal ou de um funcionário a partir da sua ficha.
2. Em **Regras de jornada e descanso**, localize o cartão da jornada.
3. Escolha **Dia estrito** ou **Jornada flexível**. O texto do cartão resume as regras de cômputo que ficam aplicadas, para que não haja dúvidas sobre o que se está a escolher.
4. Guarde o calendário.

Sendo parte do calendário, segue a mesma **herança** que o resto da configuração: o que se define na entidade desce às sucursais, e o que se define numa sucursal desce aos seus funcionários, salvo se esse nível tiver a sua própria configuração. Consulte [Herança de configuração](./26-heranca-de-configuracao.md).

---

## Descanso estrito e descanso flexível

Os descansos têm o seu próprio interruptor, com uma diferença importante face à jornada: **muda o que o funcionário tem de fazer**.

| Modalidade | Como se contabiliza | O que faz o funcionário |
|---|---|---|
| **Descanso estrito** | Aplica-se exatamente a duração configurada. Não se reconhecem descansos mais longos nem mais curtos | **Não marca** o início nem o fim da pausa |
| **Descanso flexível** | Contabiliza-se o tempo real de descanso, consoante a duração efetiva | **Marca** o início e o fim de cada pausa a partir da aplicação |

Com o descanso estrito indica-se ainda a **duração em minutos** que o sistema descontará da jornada.

A escolha depende da operação real: o descanso estrito simplifica —ninguém tem de se lembrar de registar a pausa— mas não reflete os desvios; o flexível reflete o que aconteceu, à custa de exigir mais dois registos por dia.

---

## Como escolher entre uma e outra

| Situação | Recomendação |
|---|---|
| Jornada fechada por convenção coletiva, sem horas extraordinárias | Jornada estrita |
| Pretende-se evitar que as chegadas antecipadas gerem tempo extra | Jornada estrita |
| Equipas de campo ou serviços com jornada variável | Jornada flexível |
| As horas extraordinárias realmente trabalhadas são pagas ou compensadas | Jornada flexível |
| Pausa fixa para refeição, igual todos os dias | Descanso estrito |
| Pausas variáveis consoante a carga de trabalho | Descanso flexível |

> **Aviso:** mudar de modalidade afeta o cômputo das jornadas que sejam registadas a partir desse momento. Antes de a alterar numa entidade com atividade, pondere fazê-la coincidir com o início de um período de processamento salarial para que o relatório do mês não misture dois critérios de cômputo.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Horários base e turnos](./23-horarios-base-e-turnos.md) | Configuração do horário semanal e de vários turnos por dia |
| [Exceções de horário](./25-excecoes-de-horario.md) | Ajustes pontuais sobre o horário herdado |
| [Herança de configuração](./26-heranca-de-configuracao.md) | Prioridade entre entidade, sucursal e funcionário |
| [Pausas e descansos](../03-controlo-de-horarios/17-pausas-e-descansos.md) | Como se registam as pausas a partir da aplicação |
| [Como funciona o registo de ponto](../03-controlo-de-horarios/13-como-funciona-o-registo-de-ponto.md) | As validações aplicadas em cada registo |
