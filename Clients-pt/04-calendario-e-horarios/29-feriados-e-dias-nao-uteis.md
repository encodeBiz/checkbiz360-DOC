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

## Como o CheckBiz360 bloqueia registos em dias não úteis

Quando um funcionário tenta registar a sua entrada ou saída numa data marcada como não útil no seu calendário efetivo, o sistema devolve o código de erro `checklog/day_disabled` e recusa o registo.

Este bloqueio opera antes de qualquer outra validação. O sistema não verifica a localização nem o turno ativo se o dia estiver marcado como não útil: a recusa é imediata.

As tentativas de registo em dias não úteis ficam gravadas no histórico com o seu timestamp, o dispositivo utilizado e o código de erro, o que permite ao responsável detetar se um funcionário está a tentar registar num dia que não lhe corresponde.

---

## O que acontece se a empresa trabalha em feriado

Existem setores em que trabalhar em feriado é a norma: o comércio a retalho, a restauração, os transportes ou os serviços de emergência operam com normalidade em dias que para outras empresas são não úteis.

O CheckBiz360 permite desativar um feriado pontualmente para que os funcionários afetados possam registar com normalidade nesse dia.

### Desativar um feriado de forma pontual para toda a sucursal

1. Aceda ao backoffice com perfil owner ou manager.
2. Navegue até **Sucursais** e selecione a sucursal que trabalha nesse dia.
3. Aceda a **Calendário** no menu lateral.
4. Localize a data do feriado na lista de dias não úteis.
5. Selecione a entrada e prima **Desativar para esta data**.
6. Confirme a ação. A data deixa de estar bloqueada para os funcionários dessa sucursal.

### Desativar um feriado apenas para funcionários concretos

Se apenas uma parte dos funcionários trabalha no feriado (por exemplo, o pessoal de apoio ao cliente mas não o da administração), a forma mais precisa de gerir isto é através de exceções individuais:

1. Aceda à ficha de cada funcionário que trabalha nesse dia.
2. Crie uma exceção pontual para essa data que marque o dia como útil e defina o turno correspondente.
3. Os funcionários com exceção poderão registar nesse dia. Os restantes continuarão com o bloqueio do feriado.

> **Aviso:** recorde que as exceções individuais têm prioridade sobre o calendário da sucursal. Uma exceção individual que marque um feriado como útil permite ao funcionário registar mesmo que esse feriado esteja ativo ao nível da entidade ou da sucursal.

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
- [Estados e códigos de erro](../03-controlo-de-horarios/22-estados-e-codigos-de-erro.md)
