# Glossário do CheckBiz360

Este glossário reúne os termos operacionais mais relevantes do CheckBiz360, por ordem alfabética. Cada definição inclui o nome em português e uma descrição do seu significado no contexto do sistema.

---

## A

### Acesso à app
Bloco da ficha do funcionário que diz se o correio de boas-vindas chegou e se a pessoa já usa a aplicação, e a partir do qual se reenvia o acesso ou se altera o e-mail. Veja [Acesso à aplicação e alteração de e-mail](../02-funcionarios/116-acesso-a-aplicacao-e-alteracao-de-email.md).

### Ajuste de horário
Conceito que **não se aplica** na versão atual: o registo guarda sempre a hora real e não é arredondado. O que decide se o tempo trabalhado fora da faixa oficial é contabilizado é a modalidade de *jornada estrita ou flexível* do calendário.

### Armazenamento
Espaço ocupado pelo que a sua empresa carrega: documentos, fotos de tarefas, assinaturas, relatórios e fotos do ponto de registo. Há 2 GB incluídos; acima disso, cada GB completo é faturado a 0,25 € por mês se a ampliação estiver ativada. Veja [Planos, preços e funcionalidades](./91-planos-e-funcionalidades.md#armazenamento).

### Assistente de IA (Merlin)
Componente de inteligência artificial que interpreta os dados operacionais e os expõe como um relato acionável no painel operacional, no detalhe de sucursal e no detalhe de funcionário. Narra e prioriza sobre os números que o ecrã já mostra: não recalcula nem gera dados próprios, de forma que a sua leitura não pode contradizer os painéis. Também narra o guia inicial do backoffice.

### Ausência
Dia ou intervalo de dias não úteis próprios de um funcionário: férias, licenças, dias livres. Soma-se aos feriados da sua entidade e da sua sucursal, bloqueia o seu registo nesses dias e pode ser marcada como *remunerada*, *não remunerada* ou *por definir*. Regista-a a empresa, ou nasce ao aprovar um *pedido de férias ou licença*.

---

## C

### Calendário (modo de horário)
Forma de organizar o horário em que cada dia leva os turnos que lhe são carregados por data no *calendário de turnos*. Um dia sem carregar é livre e regista-se com o gesto de sempre. Define-se na empresa, numa sucursal ou numa pessoa. Veja [Calendário: turnos carregados por data](../04-calendario-e-horarios/114-calendario-de-turnos-por-data.md).

### Calendário efetivo
Configuração que define os dias úteis e feriados para uma sucursal ou para um funcionário concreto. O calendário efetivo determina em que dias o sistema espera registos e que dias se consideram livres ou feriados. Configura-se a partir do backoffice na secção de calendários.

### Código de erro
Identificador alfanumérico que o sistema devolve quando uma operação não pode ser concluída. Os códigos de erro seguem o formato `modulo/tipo_de_erro` (por exemplo, `checklog/out_of_radius`). Permitem identificar a causa exata de uma falha sem necessidade de interpretar mensagens de texto. Veja o artigo [Códigos de erro completos](./90-codigos-de-erro-completos.md).

### Colaborador (tipo de relação)
Pessoa externa que trabalha para a empresa sem pertencer ao quadro de pessoal: um trabalhador independente, um freelancer ou um prestador de serviços. Indica-se na ficha do funcionário, por oposição a *Pessoal*. Os colaboradores não aparecem no relatório de registo de jornada. Não deve ser confundido com os *colaboradores* da entidade, que são os utilizadores com acesso ao backoffice.

### Confirmação de leitura
Confirmação explícita de que um funcionário acedeu a um documento que a exige. Fica registada com a data e a versão concreta do documento que foi lida, de modo que uma versão posterior não herda a confirmação da anterior. Não é uma assinatura eletrónica: a assinatura com validade eIDAS está no roadmap.

### Cumprimento temporal
Indicador que acompanha cada tarefa e reflete a sua situação face ao prazo, independentemente do seu estado. Os seus valores são: por iniciar, a tempo, em risco, vencida, concluída a tempo e concluída tarde. Uma tarefa vencida continua no seu estado de trabalho (por exemplo, «em curso»); o vencimento reflete-se neste indicador, e não no estado.

---

## D

### Dependência
Indicador que mede quanta parte da operação de um local recai sobre poucas pessoas. Lê-se de forma direta —*metade da operação depende de 1 pessoa*, *depende de 2 pessoas*, *distribuição saudável*— e é complementado pela vista de substituição por função.

### Disponibilidade (quadro)
Separador de **Horários** que mostra, por sucursal e dia, quantas pessoas estão disponíveis sobre o total, com a respetiva percentagem de cobertura, e permite ver quem falta e porquê. Distingue a cinzento os dias em que ninguém deveria trabalhar (feriado ou encerramento) e a vermelho as lacunas de cobertura. Veja [Quadro de disponibilidade](../04-calendario-e-horarios/98-quadro-de-disponibilidade.md).

### Dispositivo de confiança
Dispositivo móvel autorizado explicitamente pelo Owner ou pelo Manager para que um funcionário concreto possa efetuar registos a partir dele. A plataforma pode ser configurada para recusar registos provenientes de dispositivos não registados como de confiança.

---

## E

### Efeito do local
Indicador que compara o desempenho de cada pessoa **num local concreto** com o seu próprio desempenho global. A média dessas diferenças entre todos os que por lá passam mede o efeito que o local exerce sobre as pessoas, já descontado o talento individual. Responde a se o problema é a pessoa ou o sítio.

### Entidade / Entity
A unidade organizativa raiz do CheckBiz360. Corresponde a uma empresa ou cliente que contratou a plataforma. Cada entidade pode ter várias sucursais, funcionários e configurações próprias. O Owner é o responsável máximo da entidade.

### Entrada / Saída (checkin / checkout)
Registo da hora de entrada (checkin) e de saída (checkout) de um funcionário na sua jornada de trabalho. São os eventos fundamentais do controlo de horários. Uma entrada sem a saída correspondente gera uma jornada incompleta. Veja também: Registo / Checklog.

### Equipa
Modelo de pessoas que trabalham juntas, cada uma com a sua responsabilidade, função e valor por hora, mas sem sucursal. Aplicá-lo a uma sucursal adiciona todos os membros de uma vez e ignora quem já lá estava. Alterar a equipa não modifica as sucursais onde já foi aplicada. Ver [Equipas](../02-funcionarios/99-equipas.md).

### Evidência
Foto ou vídeo que um funcionário anexa a uma tarefa para comprovar o trabalho realizado. Se a tarefa tiver ativada a exigência de evidência, o sistema não permite concluí-la sem pelo menos um ficheiro anexado e devolve o código `task/evidence_required`.

---

## F

### Funcionário / Employee
Utilizador do CheckBiz360 com perfil Worker, Supervisor ou Manager que faz parte do quadro de pessoal de uma entidade. Na plataforma, o termo «employee» refere-se ao registo de dados de uma pessoa na organização, incluindo o seu perfil, atribuições, registos e documentos.

---

## G

### Geocerca / Raio de registo
Perímetro geográfico circular definido em torno das coordenadas de uma sucursal. Só se aceitam registos efetuados dentro desse perímetro. O raio mede-se em metros e configura-se a partir da ficha de cada sucursal no backoffice.

---

## H

### Herança de configuração
Mecanismo pelo qual os funcionários ou sucursais adotam automaticamente a configuração definida num nível superior da hierarquia (por exemplo, da entidade para a sucursal, ou da sucursal para o funcionário). Se um parâmetro não estiver configurado explicitamente no nível inferior, o sistema utiliza o valor do nível superior.

---

## I

### Índice de eficiência operacional
Indicador que mede o equilíbrio entre o custo real assumido e o custo esperado de acordo com o padrão histórico. A referência é sempre o próprio histórico, não uma escala universal nem uma comparação direta entre pessoas.

### Índice de fiabilidade
Indicador da qualidade do comportamento observado, **separada do tempo durante o qual se mede**: quem está há pouco tempo na empresa não arrasta uma fiabilidade baixa por isso. É um dos três índices principais do painel de Operação, a par do efeito do local e da dependência.

---

## J

### Jornada estrita / flexível
Modalidade de cômputo do calendário. Com **jornada estrita** manda o horário oficial: o que se trabalha antes ou depois não é contabilizado, e atrasos e saídas antecipadas são descontados. Com **jornada flexível** manda o tempo real: o que se trabalha fora da faixa soma-se como extra. Existe a mesma distinção para os descansos.

### Jornada incompleta (`incomplete_workday`)
Jornada de trabalho em que existe uma entrada mas não a saída correspondente, ou vice-versa. O sistema marca-a automaticamente como incompleta e exclui-a do cálculo de horas trabalhadas até que seja completada através de uma jornada manual.

### Jornada manual
Correção retroativa de um registo efetuada por um Owner ou Manager a partir do backoffice. Utiliza-se quando um funcionário se esqueceu de registar, quando o sistema não conseguiu gravar o evento por uma falha técnica pontual ou quando é necessário ajustar dados de assiduidade históricos. Fica registada com o nome do utilizador que a efetuou e a data da modificação.

---

## L

### Local de trabalho (de uma tarefa)
Morada própria de uma tarefa, com uma margem em metros, para trabalhos que não se fazem na sucursal. Iniciá-la ou retomá-la exige estar dentro da margem, e iniciá-la, retomá-la ou concluí-la só pode ser feito a partir da aplicação. Veja [Criar uma tarefa](../06-tarefas/40-criar-uma-tarefa.md#local-de-trabalho-próprio).

---

## M

### Manager
Perfil de utilizador com capacidade para gerir funcionários, sucursais, documentos, relatórios e incidências dentro das sucursais que lhe foram atribuídas. O Manager atua sob a supervisão do Owner e não pode modificar a configuração global da entidade.

### Merlin
Veja *Assistente de IA (Merlin)*.

### Modelo de horário
Cópia guardada de um horário semanal que se aplica depois a outra sucursal, a um funcionário ou à entidade, para não o configurar dia a dia. Antes chamava-se *predefinição de calendário*.

### Módulo documental
Conjunto de funcionalidades do CheckBiz360 que permite carregar, organizar e distribuir documentos laborais (contratos, recibos de vencimento, comunicados, políticas de empresa, protocolos e prevenção de riscos), com visibilidade por perfil e confirmação de leitura do funcionário. Está incluído na subscrição, independentemente do plano. A assinatura eletrónica avançada não faz parte da versão atual: o que existe hoje é a confirmação de leitura.

---

## N

### Notificação push
Mensagem enviada diretamente para o dispositivo móvel de um funcionário através do sistema de notificações do sistema operativo (APNs em iOS, FCM em Android). O CheckBiz360 utiliza notificações push para avisar de novas tarefas, documentos pendentes de confirmação de leitura, alertas de jornada e comunicados do sistema.

---

## O

### Owner
Perfil com acesso completo a todas as funcionalidades de uma entidade no CheckBiz360. O Owner pode gerir funcionários, sucursais, configuração global, faturação e todos os módulos disponíveis no plano contratado. Cada entidade tem pelo menos um Owner.

---

## P

### Painel operacional
Ecrã do backoffice que consolida a atividade do período em três vistas: a comparação entre sucursais, o detalhe por funcionário e a análise do período. É o ponto de entrada para a inteligência operacional e onde surge o relato do assistente de IA.

### Pausa (`restin` / `restout`)
Registo do início (`restin`) e fim (`restout`) de uma pausa dentro da jornada de trabalho. As pausas serão ou não descontadas do tempo trabalhado consoante a configuração da sucursal. Tal como a entrada e a saída, as pausas exigem que o funcionário esteja dentro da geocerca, se assim estiver configurado. Não confundir com a *pausa de uma tarefa*.

### Pausa de uma tarefa
Interrupção de uma tarefa em curso, que se pausa e se retoma tantas vezes quantas forem necessárias. Não é um estado: a tarefa continua *em curso* e mostra a etiqueta *Em pausa*. O tempo em pausa é somado à parte no relatório de tarefas. Veja [Acompanhamento e atualizações](../06-tarefas/43-acompanhamento-e-atualizacoes.md#pausar-e-retomar-uma-tarefa).

### Pedido de férias ou licença
Pedido que uma pessoa faz a partir de **O meu calendário** na aplicação para uns dias de férias, assuntos pessoais, médico ou outra licença. É aprovado ou recusado pelo proprietário e pelos administradores em **Contacto → Pedidos**; ao aprová-lo, os dias ficam como *ausência*. Veja [Férias e licenças a partir da aplicação](../04-calendario-e-horarios/115-ferias-e-licencas-a-partir-da-aplicacao.md).

### Pendente (estado do funcionário)
Estado de uma ficha de funcionário à qual falta algum dado para poder trabalhar, normalmente o correio eletrónico. Não recebe acesso, não é faturada e sai desse estado ao completar o dado.

### Perfil
Nível de acesso e permissões de um utilizador dentro do CheckBiz360. Os perfis disponíveis são: Owner, Manager, Supervisor e Worker. Cada perfil tem um conjunto definido de ações que pode realizar no backoffice e na aplicação móvel.

### Plano de subscrição
Modalidade de contratação do CheckBiz360. Há duas: **Bronze**, 5 €/funcionário por mês (tarifa 2026 de 2 € subscrevendo até 31 de dezembro de 2026 inclusive), e **Empresarial**, com preço à medida, que acrescenta apoio preferencial e integrações. Ambas dão acesso a todos os módulos da plataforma. Veja [Planos, preços e funcionalidades](./91-planos-e-funcionalidades.md).

### Ponto de registo
Dispositivo fixo num local, tablet ou telemóvel, onde cada pessoa regista o ponto com o seu cartão QR ou o seu código de 6 dígitos e o dispositivo tira uma foto. É um complemento pago. Na aplicação chama-se *modo quiosque*. Veja [Ponto de registo](../03-controlo-de-horarios/113-ponto-de-registo.md).

### Pontuação de promoção
Índice único que combinaria fiabilidade, eficiência e avaliações num só valor comparável entre funcionários. **Não existe na versão atual**: o que existe é a *avaliação operacional do funcionário*, um diagnóstico do seu padrão que inclui o sinal de candidato a promoção. Veja [Avaliação operacional do funcionário](../07-inteligencia-operacional/53-pontuacao-de-promocao.md).

---

## R

### RDL 8/2019
Real Decreto-Lei 8/2019, de 8 de março, que estabelece a obrigação de registo de horários para todos os trabalhadores em Espanha. O CheckBiz360 foi concebido para cumprir os requisitos deste decreto, disponibilizando registos imutáveis, com hora exata e disponíveis para inspeção do trabalho.

### Registo / Checklog
Registo individual de uma ação de controlo de horários efetuada por um funcionário. Um checklog inclui: tipo de evento (checkin, checkout, restin, restout), coordenadas GPS, timestamp, dispositivo utilizado e estado de validação. É a unidade mínima de dados do módulo de controlo de horários.

### Registo de jornada
Conjunto de todos os eventos de registo (checkin, restin, restout, checkout) que compõem uma jornada de trabalho completa de um funcionário. O registo de jornada é a unidade de análise para o cálculo de horas, a conformidade legal e a geração de relatórios.

### Responsabilidades (`responsibilities`)
Campo de configuração de um funcionário que define as áreas de trabalho ou funções específicas que lhe estão atribuídas dentro da organização. As responsabilidades podem ser utilizadas para a atribuição de tarefas e como critério de filtragem em relatórios.

---

## S

### Sucursal / Branch
Unidade organizativa dentro de uma entidade que representa um local de trabalho, uma delegação ou qualquer agrupamento geográfico ou funcional de funcionários. Cada sucursal tem as suas próprias coordenadas, raio de registo, horários, calendário efetivo e configuração de controlo de horários.

### Supervisor
Perfil intermédio entre Manager e Worker. O Supervisor pode rever os registos e as tarefas dos funcionários da sua equipa direta se o Manager lhe tiver concedido essa capacidade, mas não tem acesso à configuração global da sucursal nem aos relatórios de custos ou de anomalias.

---

## T

### Tarefa
Unidade de trabalho atribuída a um ou vários funcionários de uma sucursal, com prazo e, opcionalmente, data prevista de início e local de trabalho próprio. Percorre sete estados —rascunho, atribuída, em curso, concluída, validada, recusada e cancelada—, pode ser pausada enquanto está em curso e leva associado um indicador de cumprimento temporal independente do estado.

### Token de validação
Código temporário gerado pelo sistema para verificar a identidade de um utilizador em operações sensíveis, como o primeiro início de sessão, a reposição de palavra-passe ou a autorização de um novo dispositivo. Os tokens de validação caducam ao fim de um determinado tempo; o do funcionário, ao fim de 30 dias.

### Trabalho fora do centro
Configuração que permite a um funcionário efetuar registos a partir de uma localização diferente da geocerca da sua sucursal. Quando está ativa, o sistema aceita registos fora do raio habitual sem gerar o erro `checklog/out_of_radius`. Deve ser ativada explicitamente pelo Owner ou pelo Manager. Antes chamava-se *Trabalho remoto*.

### Turno
Faixa horária atribuída a um funcionário para uma jornada concreta, que define a sua hora de início e de fim de trabalho esperadas. Os turnos configuram-se no backoffice e associam-se ao calendário efetivo do funcionário ou da sucursal. No modo *Calendário*, os turnos carregam-se data a data em vez de se repetirem todas as semanas.

---

## V

### Verificação biométrica obrigatória
Configuração que obriga um funcionário a autenticar-se com impressão digital ou reconhecimento facial antes de completar um registo a partir da aplicação móvel. Quando está ativa, o sistema não aceita o registo se a biometria não for verificada corretamente no dispositivo.

---

## W

### Worker
Perfil de utilizador base no CheckBiz360, correspondente a um funcionário operacional. Os Workers podem registar a partir da aplicação, consultar os seus próprios dados de assiduidade, ver os seus documentos e gerir as suas tarefas. Não têm acesso ao backoffice salvo se lhes for concedido um perfil superior.

---

## Nota de perfil

Este artigo é de consulta livre para todos os perfis da plataforma: Owner, Manager, Supervisor e Worker.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Códigos de erro completos](./90-codigos-de-erro-completos.md) | Referência de todos os códigos de erro do sistema |
| [Planos, preços e funcionalidades](./91-planos-e-funcionalidades.md) | Preço de cada plano, período experimental e módulos incluídos |
| [Perguntas frequentes](./92-perguntas-frequentes.md) | Respostas às dúvidas mais habituais sobre o CheckBiz360 |
| [Controlo de horários: conceitos básicos](../03-controlo-de-horarios/13-como-funciona-o-registo-de-ponto.md) | Introdução ao módulo de controlo de horários |
