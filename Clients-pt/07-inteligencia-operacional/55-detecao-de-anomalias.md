# Deteção de anomalias

## O que é o indicador de anomalia

O CheckBiz360 inclui um mecanismo de deteção automática de padrões de registo anómalos. Quando o sistema identifica comportamentos que se desviam significativamente do expectável num trabalhador real, ativa um indicador de anomalia no perfil do funcionário.

Este indicador não é uma acusação nem constitui prova de qualquer irregularidade. É um sinal de alerta que indica que o comportamento de registo desse funcionário merece uma revisão manual. A responsabilidade de investigar, interpretar e agir recai sempre no responsável humano.

## Porque existe este mecanismo

O registo digital resolve o problema do controlo manual, mas abre a possibilidade de novas formas de irregularidade difíceis de detetar visualmente: funcionários que pedem a um colega que registe por eles, registos gerados por dispositivos não autorizados ou comportamentos automatizados que simulam uma presença que não existe.

Estas situações têm duas características comuns: individualmente, cada registo parece correto; no conjunto, o padrão é demasiado regular para ser produto do comportamento humano natural. A deteção de anomalias analisa precisamente isso: não cada registo isolado, mas o padrão que todos eles formam ao longo do tempo.

## Que padrões ativam a deteção

O sistema analisa de forma contínua os registos de cada funcionário à procura dos seguintes sinais:

**Precisão temporal excessiva.** Um funcionário real regista com variações naturais: um dia chega dois minutos antes, outro chega um minuto depois, por vezes demora mais a abrir a aplicação. Se os registos de um funcionário ocorrem sistematicamente à mesma hora com uma precisão ao segundo, durante um número suficiente de dias, o sistema considera-o estatisticamente improvável e ativa o alerta.

**Geolocalização estática ou idêntica.** Se o funcionário regista sempre a partir de exatamente as mesmas coordenadas GPS, dia após dia, sem qualquer variação nas casas decimais, pode indicar que o registo não está a ser feito a partir do dispositivo móvel do próprio funcionário na sua localização real, mas a partir de um sistema que reproduz sempre a mesma posição.

**Padrões de regularidade excessiva.** O comportamento humano tem variabilidade inerente. Se todos os parâmetros do registo de um funcionário (hora, coordenadas, duração da jornada) forem demasiado constantes durante um período prolongado, o sistema identifica essa regularidade como estatisticamente anómala.

> **Importante:** nenhum destes padrões é, por si só, prova de qualquer irregularidade. Existem situações legítimas que podem produzir comportamentos semelhantes: funcionários que trabalham sempre a partir do mesmo posto fixo, dispositivos com GPS pouco preciso que reportam sempre as mesmas coordenadas, pessoas com rotinas muito estáveis. O indicador de anomalia é o início de uma investigação, não a sua conclusão.

## O que deve fazer o responsável quando surge um funcionário assinalado

Quando o sistema ativa o indicador de anomalia para um funcionário, o fluxo de atuação recomendado é o seguinte:

1. **Reveja o histórico completo.** Aceda à ficha do funcionário no módulo de inteligência operacional e examine os registos dos últimos meses. Identifique desde quando aparece o padrão anómalo e se coincide com alguma alteração nas circunstâncias do funcionário ou da equipa.

2. **Confronte com o contexto operacional.** Confirme com o supervisor direto se existe alguma explicação operacional: o funcionário trabalha sempre a partir da mesma localização fixa? Houve alguma alteração nas suas condições de trabalho que explique a regularidade?

3. **Compare com outros funcionários do mesmo local.** Se o padrão anómalo coincidir com outros funcionários da mesma sucursal, pode indicar um problema sistémico (por exemplo, um dispositivo de registo partilhado num lugar fixo) em vez de uma conduta individual.

4. **Se a irregularidade não tiver explicação evidente, convoque o funcionário.** A entrevista deve ser feita com cautela: apresente os dados observados, ouça a explicação do funcionário e documente a conversa. Não confronte com acusações diretas baseadas unicamente no indicador do sistema.

5. **Documente a resolução externamente.** Quer a anomalia tenha uma explicação legítima, quer se confirme uma irregularidade, registe o resultado da revisão nos sistemas ou procedimentos que a sua organização tiver estabelecidos. A plataforma mostra o indicador, mas o acompanhamento do estado da revisão deve ser feito fora do CheckBiz360 na versão atual.

## Fluxo de revisão e alertas configuráveis

> **Estado: Planeado**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

Numa versão futura, o indicador de anomalia estará integrado num fluxo de revisão com estados geríveis diretamente na plataforma (pendente de revisão, revisto, arquivado), o que permitirá acompanhar o ciclo de vida de cada alerta sem sair do backoffice. Prevê-se igualmente a possibilidade de configurar notificações de alerta para que os responsáveis sejam avisados de forma automática quando um novo indicador for ativado. Por agora, o responsável deve rever o painel de Operação de forma proativa: o separador **Análise** reúne onde e quando o registo falha, que é onde estes padrões afloram.

## O que o indicador de anomalia não implica

O indicador de anomalia não é uma sanção, não gera notificação ao funcionário e não tem efeitos automáticos sobre o seu perfil, os seus direitos ou o seu contrato. É exclusivamente uma ferramenta de alerta interna para os responsáveis com acesso ao módulo.

Em caso algum deve o indicador de anomalia ser usado como única base para iniciar um procedimento disciplinar. Qualquer ação desse tipo deve sustentar-se num processo de investigação conforme à convenção coletiva e à legislação laboral aplicável, com a participação, se for caso disso, da área de recursos humanos ou de consultoria jurídica.

> **Nota:** o acesso ao indicador de anomalia está restrito aos perfis de Manager e Owner. Os supervisores não têm visibilidade sobre esta informação nas suas vistas habituais.

## Artigos relacionados

- [O que é a inteligência operacional](49-o-que-e-a-inteligencia-operacional.md)
- [O padrão de comportamento do funcionário](50-padrao-de-comportamento.md)
- [O painel de Operação](56-paineis-de-controlo.md)
- [Preparar uma inspeção do trabalho](../12-conformidade-legal/84-preparar-uma-inspecao-do-trabalho.md)
