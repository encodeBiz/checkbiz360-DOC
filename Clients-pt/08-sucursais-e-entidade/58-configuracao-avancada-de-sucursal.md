# Configuração avançada de sucursal

Cada sucursal no CheckBiz360 admite ajustes que adaptam o comportamento do sistema às particularidades desse local de trabalho: até onde chega a zona de registo, como se contabilizam as horas e como se registam as pausas. Este artigo descreve cada parâmetro, onde se configura, o seu efeito e quando convém modificá-lo.

## Onde encontrar cada ajuste

A configuração avançada de uma sucursal está repartida por dois sítios, consoante o que se pretenda ajustar:

- **A ficha da sucursal** (**Sucursais** no menu lateral → editar) contém os dados do local e a **configuração operacional**: a zona de verificação.
- **O calendário** (na ficha da sucursal, ou **Horários** → **Configurações gerais** se for herdado da entidade) contém o horário semanal, as pausas, a modalidade de jornada e a de descanso.

## Tabela de parâmetros

| Parâmetro | Onde | Tipo | Descrição |
|---|---|---|---|
| Zona de verificação em metros | Ficha da sucursal | Inteiro (metros) | Raio em torno das coordenadas dentro do qual se aceita o registo |
| Zona de verificação ativa | Ficha da sucursal | Booleano | Quando é desativada, a geocerca deixa de ser validada nesta sucursal |
| Estado | Ficha da sucursal | Ativa / Inativa | Uma sucursal inativa não admite registos |
| Dados adicionais | Ficha da sucursal | Chave/valor | Campos livres próprios da sua organização |
| Horário semanal e pausas | Calendário | Faixas horárias | Turnos por dia e pausas dentro de cada turno |
| Jornada estrita / flexível | Calendário | Booleano | Contabilizar o horário oficial ou o tempo real trabalhado |
| Descanso estrito / flexível | Calendário | Booleano | Descontar uma duração fixa ou o tempo real de pausa |
| Tempo de descanso (minutos) | Calendário | Inteiro (minutos) | Duração descontada quando o descanso é estrito |

> **Nota:** não existe um parâmetro de «tolerância de entrada» nem de «ajuste automático do timestamp». O que decide se o tempo trabalhado fora da faixa conta ou não é a modalidade de jornada. Consulte [Jornada estrita e jornada flexível](../04-calendario-e-horarios/28-horario-flexivel.md).

## Descrição detalhada de cada parâmetro

### Zona de verificação ativa

Quando esta opção é desativada, o sistema aceita registos a partir de qualquer localização GPS sem verificar se o funcionário está dentro do raio definido. A coordenada GPS continua a ser gravada no sistema, mas não é utilizada como critério de validação.

**Quando usá-lo:** sucursais onde os funcionários trabalham em itinerância, em domicílios de clientes ou em espaços cuja cobertura GPS é deficiente (caves, armazéns com paredes espessas). Também é útil durante o período de configuração inicial, quando ainda não se ajustou o raio com precisão.

> **Aviso:** desativar a geocerca elimina uma camada de controlo antifraude. Utilize este parâmetro apenas quando existirem razões operacionais justificadas e comunique-o à equipa de conformidade se a sua empresa estiver sujeita a auditorias de controlo de horários.

### Modalidade de descanso

Os descansos têm duas modalidades, que se escolhem no calendário da sucursal:

- **Descanso estrito**: o sistema desconta exatamente os minutos configurados. O funcionário **não marca** início nem fim da pausa, e não se reconhecem descansos mais longos nem mais curtos.
- **Descanso flexível**: o funcionário **marca** o início e o fim de cada pausa a partir da aplicação, e o sistema contabiliza a duração efetiva.

**Quando usar o estrito:** pausas fixas por convenção coletiva, iguais todos os dias, onde exigir mais dois registos por dia não acrescenta nada. **Quando usar o flexível:** pausas variáveis consoante a carga de trabalho, ou quando é necessário comprovar a duração real dos descansos.

### Tempo de descanso

Quando o descanso é estrito, este valor —em minutos— é o que se desconta da jornada. Ajuste-o ao tempo de pausa estipulado na convenção aplicável a essa sucursal.

Com o descanso flexível o campo não se aplica: manda o tempo que o funcionário registar.

### Modalidade de jornada

Decide se a contabilização segue o horário oficial (**jornada estrita**) ou o tempo realmente trabalhado (**jornada flexível**). É o ajuste com maior impacto sobre os relatórios de horas e está explicado em detalhe em [Jornada estrita e jornada flexível](../04-calendario-e-horarios/28-horario-flexivel.md).

## Interação entre parâmetros

- A **modalidade de jornada** e a **de descanso** são independentes: pode ter jornada estrita com descanso flexível, ou o contrário.
- O **tempo de descanso** só se aplica com o descanso estrito; com o flexível é ignorado.
- **Desativar a zona de verificação** é independente do resto e pode combinar-se com qualquer configuração.
- Tudo o que é do calendário segue a **herança** entidade → sucursal → funcionário: o que a sucursal não definir, herda-o da entidade.

> **Aviso:** as alterações produzem efeito sobre os registos posteriores. Não modificam os registos já existentes no histórico.

---

> **Nota de perfil:** a configuração avançada de sucursal está disponível unicamente para os perfis **Owner** e **Manager** com permissões de administração de organização. Os perfis **Supervisor** e **Worker** não têm acesso a esta secção.

## Artigos relacionados

- [Criar e gerir sucursais](57-criar-e-gerir-sucursais.md)
- [Estados de uma sucursal](59-estados-de-uma-sucursal.md)
- [Atribuir funcionários a sucursais](60-atribuir-funcionarios-a-sucursais.md)
- [Configuração da entidade](61-configuracao-da-entidade.md)
