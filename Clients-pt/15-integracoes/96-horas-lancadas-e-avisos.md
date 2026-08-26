# Horas lançadas e avisos

Depois de ligada a integração, o ecrã do Rentman mostra o que está a acontecer com as suas horas. Este artigo explica o que significa cada número e o que fazer quando algo exige a sua atenção.

## O que vai ver

| Indicador | O que lhe diz |
|---|---|
| **Jornadas lançadas** | Quantas jornadas fechadas foram enviadas para o Rentman |
| **Horas lançadas** | O total de horas líquidas enviadas no período |
| **Cobertura de emparelhamento** | Quantos dos seus colaboradores têm ficha do Rentman associada |
| **Divergências abertas** | Jornadas que alguém alterou no Rentman depois de enviadas |

## Sincronizar de imediato

A sincronização corre sozinha a cada 15 minutos, mas logo após ligar — ou quando quiser verificar algo — pode carregar em **Sincronizar agora** e não esperar. Se carregar duas vezes seguidas, a plataforma pedirá que aguarde alguns segundos: é uma proteção para não sobrecarregar o Rentman, não um erro.

E se o resultado vier a zero, também não é uma falha: pode não haver jornadas fechadas novas ou faltar emparelhar essas pessoas.

## Porque as horas coincidem com o relatório legal

As horas enviadas para o Rentman são as **líquidas**: a diferença entre a entrada e a saída, menos o intervalo.

O intervalo não viaja dentro do registo de ponto. Vem da configuração da sucursal: ou é um intervalo fixo definido no centro de trabalho, ou é calculado somando as pausas que o trabalhador registou. A integração aplica **exatamente a mesma regra do relatório de controlo de horários**, para que o valor que vê no Rentman e o que certifica perante uma inspeção sejam o mesmo.

Se alguma vez esses dois valores não coincidirem, avise-nos: é um problema que queremos conhecer.

## As divergências

Uma divergência surge quando alguém **altera no Rentman** horas que o CheckBiz360 já tinha enviado, ou as apaga.

Nesse caso a plataforma:

1. Deteta a alteração ao rever o registo, o que faz a cada 24 horas.
2. Assinala essa jornada e mostra-lhe as duas versões: a sua e a do Rentman.
3. **Não altera o seu registo de ponto.** O registo legal permanece intacto.
4. Também não desfaz a alteração feita no Rentman: a decisão é sua.

O que fazer depende de quem tem razão:

- **Se o registo de ponto está correto** e a alteração no Rentman foi um erro, corrija-a no Rentman.
- **Se o registo é que está errado** (por exemplo, um trabalhador esqueceu-se de registar a saída), corrija-o primeiro no CheckBiz360. A jornada será reenviada com os valores novos.

## Estados de uma jornada

| Estado | O que significa | Exige ação |
|---|---|---|
| Em fila | Detetada, à espera de envio | Não |
| Enviada | Já está no Rentman | Não |
| Com erro | Falha temporária de ligação | Não, repete sozinha |
| Rejeitada | O Rentman não a aceita | Sim, veja o motivo |
| Divergente | Alterada no Rentman | Sim, reveja as duas versões |

## Perguntas frequentes

**Um trabalhador registou o ponto mas as horas não aparecem no Rentman.**
Verifique três coisas por esta ordem: que a jornada está **fechada** (com saída registada), que o trabalhador está **emparelhado** com a sua ficha do Rentman, e que passaram pelo menos 15 minutos.

**Aparece uma jornada "rejeitada" pelo Rentman.**
O motivo mais habitual é já existirem no Rentman horas ou uma ausência para essa pessoa nesse mesmo período; o Rentman não admite registos sobrepostos. Reveja essas datas: normalmente são horas introduzidas à mão antes de ligar a integração.

**As jornadas incompletas são enviadas?**
Não. Uma jornada sem saída registada não é uma jornada fechada. Se for frequente na sua empresa, reveja os avisos de fecho automático no módulo de controlo de horários.

**Posso alterar no Rentman as horas que o CheckBiz360 envia?**
Pode, mas não é recomendável. A sua alteração não volta ao CheckBiz360 e gera uma divergência. Se a jornada estiver errada, corrija-a no CheckBiz360 e deixe a correção viajar sozinha.

**O que acontece se o Rentman estiver em baixo?**
Nada de grave. Os registos de ponto continuam a funcionar normalmente — a integração nunca bloqueia o controlo de horários — e as jornadas pendentes são enviadas quando o serviço voltar.

**As horas podem duplicar-se?**
Não. Cada jornada tem uma marca interna que impede enviá-la duas vezes, por mais vezes que a sincronização corra.

## Artigos relacionados

- [RentmanBiz](94-rentmanbiz.md)
- [Ligar o RentmanBiz passo a passo](95-ligar-o-rentmanbiz.md)
