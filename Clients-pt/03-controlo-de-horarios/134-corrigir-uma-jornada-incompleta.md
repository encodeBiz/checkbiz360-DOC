# Corrigir uma jornada incompleta de uma só vez

Quando alguém se esquece de registar a saída, a jornada fica incompleta e abre-se uma incidência. Se a jornada era repartida, com vários turnos, pode haver vários registos a corrigir. A partir da incidência corrige-se a jornada inteira num único ecrã, com um único motivo, e a pessoa recebe um único aviso para a aceitar ou recusar.

---

## O que resolve

- **Uma jornada repartida de cinco turnos não são cinco correções.** Veem-se todos os turnos do dia juntos e corrigem-se de uma só vez.
- **Um único motivo** para todos os registos corrigidos, em vez de o escrever em cada um.
- **Um único aviso à pessoa**, que aceita ou recusa a jornada inteira a partir da aplicação.
- **A incidência fecha-se sozinha** quando a pessoa aceita.

A correção não altera nada até que a pessoa a aceite: o registo de jornada continua a ser o que ela dá por bom.

---

## Corrigir a jornada a partir do painel

1. Abra a incidência da jornada incompleta, em **Contacto → Incidentes**.
2. Prima **Corrigir jornada**. Abre-se uma janela com o nome da pessoa e o dia e, por baixo, cada **Turno** dessa jornada com os seus registos (entrada, descansos e saída) e o seu estado: *Jornada incompleta*, *Válido* ou *Pendente de validação*.
3. Marque os turnos que quer corrigir e ajuste as horas. Se a saída foi definida pelo sistema à hora planeada, isso é indicado: *Definida pelo sistema à hora planeada*. As horas estão no fuso horário que a própria janela indica.
4. Escreva o motivo em **Razões para a mudança**. É um só para todos os registos corrigidos.
5. Prima **Corrigir e enviar**. O botão indica quantos registos são enviados.

A partir desse momento, a incidência diz *Correção enviada. À espera de que [pessoa] a aceite.* Enquanto espera, não é possível enviar outra correção da mesma jornada.

> **Aviso:** não é possível indicar uma hora no futuro. Se alguma estiver, a janela avisa antes de enviar.

---

## O que a pessoa faz na aplicação

Recebe um único aviso. Ao abri-lo vê «Corrección de tu jornada», com um cartão por cada turno: o que foi corrigido aparece riscado junto à hora nova, e a saída que faltava aparece como «sin fichar» seguida da hora proposta.

- **«Aceptar jornada»**: aplicam-se todas as correções da jornada. Os registos ficam válidos e a incidência fecha-se.
- **«Rechazar»**: a jornada inteira volta à empresa para que a reveja. Pode escrever porque não está de acordo; é opcional.

Para ver a jornada inteira num único ecrã, a pessoa precisa da última versão da aplicação. Com uma versão anterior, as alterações chegam-lhe como avisos soltos e aceita-as registo a registo; quando aceita o último, a correção fica igualmente fechada.

---

## O que o senhor vê depois

Na própria incidência:

| Mensagem | O que aconteceu |
|---|---|
| *[Pessoa] aceitou a correção da jornada.* | Registos válidos com as horas corrigidas e incidência resolvida. |
| *[Pessoa] rejeitou a correção.* | Os registos continuam como estavam e a incidência continua aberta, com o motivo se o escreveu. Pode enviar outra correção. |
| *A correção foi aceite só em parte. Reveja os registos da jornada.* | A pessoa, com uma versão anterior da aplicação, aceitou uns registos e outros não. |

Cada registo corrigido deixa a sua entrada no histórico de alterações, com o motivo, quem o propôs e quem o aceitou. Ver [Rastreabilidade e histórico de alterações](./21-rastreabilidade-e-historico-de-alteracoes.md).

---

## Quem o pode fazer

Corrige a jornada o proprietário, um administrador ou um responsável com perfil de manager. Aceitar ou recusar só o pode fazer a própria pessoa, a partir da sua aplicação.

---

## Problemas frequentes

**Não vejo o botão Corrigir jornada.** Só aparece nas incidências de jornada incompleta que continuam abertas e sem uma correção à espera de resposta.

**A pessoa diz que não lhe chegou nada.** Peça-lhe que abra a aplicação e veja os seus avisos; se tiver as notificações do telemóvel desativadas, o aviso está igualmente na aplicação. Se usar uma versão antiga, que a atualize.

**Já aceitou e o registo continua marcado como suspeito.** Aceitar a correção não altera essa marca. Ver [Deteção de anomalias](../07-inteligencia-operacional/55-detecao-de-anomalias.md).

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Revisão e validação de registos](./20-revisao-e-validacao-de-registos.md) | Correções de um só registo e jornadas manuais |
| [Estados e códigos de erro](./22-estados-e-codigos-de-erro.md) | O que significa uma jornada incompleta |
| [Rastreabilidade e histórico de alterações](./21-rastreabilidade-e-historico-de-alteracoes.md) | O que fica registado de cada correção |
| [Alertas por e-mail](../09-notificacoes/133-alertas-por-email.md) | O aviso de jornadas por fechar no resumo da manhã |
