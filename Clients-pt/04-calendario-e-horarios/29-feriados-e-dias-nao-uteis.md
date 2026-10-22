# Feriados e dias não úteis

A gestão de feriados é um dos aspetos mais delicados do controlo de assiduidade, sobretudo em empresas que operam em várias regiões ou em setores que trabalham habitualmente em dias que para outros são não úteis. O CheckBiz360 oferece um sistema flexível que permite tanto bloquear registos em feriados como ativá-los quando a atividade da empresa assim o exigir.

---

## Tipos de feriado e dia não útil

O CheckBiz360 classifica os dias não úteis em diferentes categorias que determinam o seu âmbito dentro da hierarquia de configuração:

### Feriado nacional

Um feriado nacional é uma data declarada como não útil pela legislação estatal e que se aplica a toda a organização. Configura-se ao nível da entidade e é herdado automaticamente por todas as sucursais e funcionários.

### Feriado regional

Um feriado regional aplica-se unicamente às sucursais situadas na região correspondente. Configura-se ao nível da sucursal para que apenas afete os funcionários desse local.

### Feriado municipal

Semelhante ao regional, o feriado municipal aplica-se a um concelho ou zona concreta. É gerido ao nível da sucursal, permitindo que só os funcionários dessa sucursal fiquem afetados pelo bloqueio de registo.

### Ponte

Um dia de ponte é um dia útil que a empresa, por decisão interna, converte em não útil para facilitar a continuidade de um feriado oficial. Configura-se como um dia não útil interno com uma descrição que o identifique.

### Dia não útil interno

Esta categoria cobre qualquer data que a empresa decida bloquear por motivos próprios: encerramentos para inventário, obras, formações obrigatórias em que não existe jornada regular, etc.

---

## Ausências de um funcionário

As férias, as licenças e os dias livres de uma pessoa concreta registam-se como **ausências** no seu calendário. Adicionam-se a partir da ficha do funcionário ou a partir do [quadro de disponibilidade](98-quadro-de-disponibilidade.md), e consultam-se também no separador **Dias não úteis dos funcionários** de **Horários**.

- **Intervalo de datas.** Uma ausência pode abranger vários dias seguidos. Nas listas aparece como uma só linha com o seu início, o seu fim e o número de dias (por exemplo, «1 – 15 set · 15 dias»), que se expande para ver ou retirar dias soltos.
- **Remunerada.** Cada ausência de funcionário tem uma caixa **Remunerada** com três valores possíveis: *remunerada*, *não remunerada* ou *por definir*. *Por definir* significa que não consta —por exemplo, nas ausências registadas antes de a caixa existir— e é mostrado de forma diferente de *não remunerada* para não confundir um dado em falta com um «não». Os feriados da entidade ou da sucursal não levam esta marca.

Um dia de ausência bloqueia o registo dessa pessoa tal como um feriado.

As pessoas também podem pedir as suas férias ou licenças a partir da aplicação, em **O meu calendário**. Ao aprová-las em **Contacto → Pedidos**, os dias ficam como ausências, com a marca de remunerada que escolher quem aprova. Ver [Férias e licenças a partir da aplicação](115-ferias-e-licencas-a-partir-da-aplicacao.md).

---

## Como o CheckBiz360 bloqueia registos em dias não úteis

Quando um funcionário tenta registar a sua entrada ou saída numa data marcada como não útil no seu calendário efetivo, o sistema devolve o código de erro `checklog/day_disabled` e recusa o registo.

Este bloqueio opera antes de qualquer outra validação. O sistema não verifica a localização nem o turno ativo se o dia estiver marcado como não útil: a recusa é imediata.

As tentativas de registo em dias não úteis ficam gravadas no histórico com o seu timestamp, o dispositivo utilizado e o código de erro, o que permite ao responsável detetar se um funcionário está a tentar registar num dia que não lhe corresponde.

---

## O que acontece se a empresa trabalha em feriado

Existem setores em que trabalhar em feriado é a norma: o comércio a retalho, a restauração, os transportes ou os serviços de emergência operam com normalidade em dias que para outras empresas são não úteis.

Um feriado configurado aplica-se a **todos** os funcionários do seu âmbito: não há forma de o anular só para uma sucursal ou só para uma pessoa. Nem sequer um horário personalizado com turno nesse dia o contorna; o registo é recusado com `checklog/day_disabled`. Por isso, a forma de trabalhar em feriado é não marcar como feriado o que não fecha.

### Toda a sucursal trabalha nesse dia

- Se o feriado estiver na **sucursal**, elimine-o dos seus dias de folga. A data deixa de estar bloqueada para os funcionários dessa sucursal.
- Se o feriado estiver na **entidade**, afeta todas as sucursais. Retire-o da entidade e adicione-o como feriado local apenas nas sucursais que fecham.

### Só uma parte do quadro de pessoal trabalha nesse dia

Se só trabalhar uma parte (por exemplo, o pessoal de apoio ao cliente mas não o da administração):

1. Não marque o dia como feriado na sucursal: trate-o como útil.
2. Registe uma **ausência** nesse dia a quem folga, a partir da sua ficha ou a partir do [quadro de disponibilidade](98-quadro-de-disponibilidade.md).
3. Quem trabalha regista com normalidade; quem tem a ausência fica bloqueado.

> **Aviso:** os feriados de entidade, sucursal e funcionário **somam-se**; não se anulam entre si. A herança em que o nível do funcionário prevalece é a do horário semanal, e não a dos feriados.

---

## Considerações por setor

### Retalho e comércio

O comércio costuma operar durante pontes, feriados municipais e até alguns feriados nacionais. É habitual configurar a sucursal com um calendário sem feriados e gerir os encerramentos pontuais (por exemplo, Natal ou Ano Novo) adicionando manualmente os dias em que a loja permanece fechada.

### Restauração e hotelaria

A restauração trabalha praticamente sem interrupção durante o ano, incluindo os feriados mais assinalados. Neste setor é recomendável deixar o calendário da sucursal sem feriados e acrescentar unicamente os dias de encerramento real do estabelecimento.

### Serviços de saúde e emergência

Nestes setores, o trabalho em feriados faz parte da convenção coletiva. O CheckBiz360 permite registar a jornada em feriado sem bloqueios e, se a empresa precisar de identificar os dias feriados trabalhados para o cálculo de complementos salariais, pode utilizar os relatórios de jornada filtrados por tipo de dia.

### Atividades sazonais

As empresas com atividade sazonal (turismo, agricultura, eventos) podem ter períodos em que operam com normalidade durante feriados e outros em que permanecem encerradas. A configuração recomendada nestes casos é definir o calendário de feriados ao nível da entidade com os feriados nacionais e gerir as particularidades de cada época através do calendário da sucursal ou através de dias não úteis internos.

---

## Gestão de feriados com antecedência

Recomenda-se configurar o calendário de feriados no início de cada ano civil ou com antecedência suficiente em relação a cada feriado. O CheckBiz360 não aplica automaticamente os feriados oficiais do país: o responsável deve introduzi-los manualmente ou importá-los se a plataforma disponibilizar essa funcionalidade no seu plano de subscrição.

> **Nota:** se um feriado não estiver configurado no calendário e os funcionários registarem nesse dia, os registos ficarão como válidos. Não existe forma de marcar retroativamente um registo já gravado como «feriado trabalhado» sem rever e ajustar manualmente os registos afetados. A configuração antecipada do calendário evita este tipo de incidências.

---

## Artigos relacionados

- [Horários base e turnos](23-horarios-base-e-turnos.md)
- [Calendário laboral](24-calendario-laboral.md)
- [Exceções de horário](25-excecoes-de-horario.md)
- [Herança de configuração](26-heranca-de-configuracao.md)
- [Turnos rotativos](27-turnos-rotativos.md) — não disponível na versão atual; alternativas
- [Quadro de disponibilidade](98-quadro-de-disponibilidade.md)
- [Férias e licenças a partir da aplicação](115-ferias-e-licencas-a-partir-da-aplicacao.md)
- [Estados e códigos de erro](../03-controlo-de-horarios/22-estados-e-codigos-de-erro.md)
