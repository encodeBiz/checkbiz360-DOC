# Estados e códigos de erro do registo

O CheckBiz360 atribui a cada registo de assiduidade um estado que reflete a sua situação no ciclo de vida da jornada. Quando um registo não pode ser processado corretamente, o sistema gera ainda um código de erro que identifica a causa com precisão. Este artigo descreve todos os estados possíveis e os códigos de erro disponíveis, juntamente com as ações recomendadas para os resolver.

---

## Estados de registo

Os estados indicam em que ponto do processo se encontra um registo de assiduidade. São atribuídos automaticamente pelo sistema e podem mudar ao longo do tempo, por exemplo quando um funcionário valida uma jornada manual ou quando um responsável corrige uma incidência.

| Estado | Significado |
|---|---|
| `valid` | Registo correto. Todas as validações ultrapassadas. O registo conta como tempo trabalhado. |
| `failed` | Registo recusado. Uma ou mais validações falharam. O registo fica guardado para auditoria mas não conta horas. Inclui código de erro. |
| `pending-employee-validation` | Registo criado por um responsável ou modificado. À espera da confirmação do funcionário. Não conta horas até ser aceite. |
| `incomplete_workday` | Jornada por fechar. Existe uma entrada válida sem a saída correspondente. Exige resolução manual ou uma saída posterior. |

---

### Estado `valid`

É o estado objetivo de todo o registo. Indica que o registo ultrapassou as validações de geolocalização, horário e autenticação, e que o funcionário o confirmou (se era necessário). Os cálculos de horas trabalhadas realizam-se exclusivamente sobre registos no estado `valid`.

### Estado `failed`

Um registo pode ficar no estado `failed` por diversas razões: o funcionário estava fora do raio, o registo foi efetuado fora de turno, o dispositivo não estava autorizado ou o funcionário recusou uma jornada manual. Em todos os casos, o registo é conservado integralmente para auditoria.

### Estado `pending-employee-validation`

Este estado é temporário. Surge quando se cria uma jornada manual ou quando um responsável modifica um registo e o sistema exige a confirmação do funcionário. Enquanto o registo permanece neste estado, não altera o cômputo de horas.

### Estado `incomplete_workday`

Indica que o funcionário registou a sua entrada mas não a sua saída. A jornada fica em aberto. Este estado pode ser resolvido registando a saída correspondente (manualmente ou a partir da aplicação) ou através da criação de uma saída manual por parte do responsável.

---

## Códigos de erro

Quando um registo fica no estado `failed`, o sistema associa um código de erro que identifica a causa exata da recusa. Estes códigos permitem ao responsável diagnosticar e resolver a incidência de forma eficiente.

| Código | Causa | Ação recomendada |
|---|---|---|
| `checklog/out_of_schedule` | O registo foi efetuado fora do turno ativo do funcionário. | Rever o horário atribuído ao funcionário. Se a presença estava correta, solicitar uma jornada manual. |
| `checklog/out_of_radius` | O dispositivo encontrava-se fora do raio de registo da sucursal no momento do registo. | Rever as coordenadas GPS da sucursal e o valor do raio configurado. Se o raio não cobre a área de trabalho real, alargá-lo. |
| `checklog/day_disabled` | O dia em que se tentou registar está desativado no calendário da sucursal ou do funcionário, é feriado ou é um dia livre do funcionário. | Rever a configuração do calendário. Se o dia deve estar ativo, ativá-lo no calendário efetivo correspondente. Um feriado da entidade ou da sucursal não pode ser anulado para um só funcionário. Se o funcionário trabalhou, registar a jornada manual. |
| `checklog/absence` | O funcionário tem registada uma ausência que abrange esse dia. | Se a ausência estiver correta, não há nada a fazer. Se não estiver, retirá-la do seu calendário e voltar a registar. |
| `checklog/different_branches` | Tentou-se iniciar uma pausa ou registar a saída numa sucursal diferente da da entrada. Uma jornada não se reparte entre locais. | Registar a pausa ou a saída na mesma sucursal da entrada. Se o funcionário mudou de local, fechar a jornada no primeiro e abrir outra no segundo. |
| `checklog_update/future_not_allowed` | Foi proposta uma correção com data ou hora futura. | Indicar uma hora que já tenha passado. |
| `auth/untrusted_device` | O dispositivo a partir do qual se tentou registar não está registado como dispositivo de confiança. O funcionário tem ativada a autenticação de duplo fator. | Registar o dispositivo atual como dispositivo de confiança através do processo de 2FA. |
| `employee/not_found` | O identificador do funcionário não corresponde a nenhum registo ativo no sistema. | Verificar que o funcionário está ativo na plataforma e corretamente atribuído à sucursal. |
| `checklog/overlap_detected` | Já existe um registo para o intervalo horário em que se tenta criar o novo registo. Dois registos do mesmo tipo não podem sobrepor-se. | Rever os registos existentes do funcionário para essa data e resolver a sobreposição antes de criar um novo registo. |

---

## Como consultar o estado e o código de erro de um registo

A partir do backoffice, o responsável pode aceder ao detalhe de qualquer registo e ver:

- O estado atual do registo.
- O código de erro se o estado for `failed`.
- Os dados técnicos da tentativa: coordenadas, distância ao raio, turno ativo no momento do registo, dispositivo utilizado.
- O histórico completo de alterações.

Os funcionários podem ver o estado dos seus registos a partir da secção de histórico de assiduidade na aplicação. No caso de registos falhados, a aplicação mostra uma descrição do motivo em linguagem compreensível. A partir da versão 1.3.2, a aplicação traduz também os códigos de dia não útil, calendário por resolver, sucursal sem localização, sobreposição, pedido duplicado e fecho de jornada, em vez de mostrar o código técnico; e quando o dia não é útil, explica que o funcionário pode pedir uma jornada manual se trabalhou.

---

> **Aviso para responsáveis:** um registo falhado não significa necessariamente que o funcionário agiu de forma incorreta. Em muitos casos, o erro é de configuração: um raio demasiado pequeno, um turno mal atribuído ou um dispositivo não registado. Antes de tomar qualquer ação disciplinar, reveja sempre os detalhes técnicos do erro e confirme com o funcionário.

---

## Perfis com acesso a esta funcionalidade

Todos os utilizadores com perfil **funcionário** podem ver o estado dos seus próprios registos a partir da aplicação. Os utilizadores com perfil **manager** ou **owner** têm acesso completo aos estados, códigos de erro e dados técnicos de todos os registos da sua entidade a partir do backoffice.

---

## Artigos relacionados

- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Geocercas e raio de registo](16-geocercas-e-raio-de-registo.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Rastreabilidade e histórico de alterações](21-rastreabilidade-e-historico-de-alteracoes.md)
