# Navegação principal da aplicação

Depois de iniciar sessão no CheckBiz360, encontrará uma interface organizada em secções bem diferenciadas. Este artigo descreve a estrutura geral da aplicação, para que possa localizar com facilidade cada função e aproveitar ao máximo as ferramentas disponíveis.

---

## Estrutura geral da aplicação

A navegação principal do CheckBiz360 organiza-se através de uma barra de navegação inferior que agrupa as cinco áreas fundamentais da experiência do funcionário:

1. **Registo** — ecrã inicial e centro da experiência.
2. **Os meus registos** — histórico pessoal de assiduidade.
3. **Documentos** — documentos laborais do funcionário.
4. **Tarefas** — tarefas atribuídas pelo manager.
5. **Perfil** — configuração pessoal e segurança.

Pode deslocar-se entre estas secções tocando no ícone correspondente na barra inferior a qualquer momento.

---

## Secção Registo

O ecrã de registo é o primeiro que aparece ao iniciar sessão e constitui o núcleo da aplicação. A partir dele pode:

- Registar a sua entrada no início da jornada.
- Registar pausas intermédias quando for o caso.
- Registar a sua saída no fim da jornada.
- Consultar o estado do seu registo atual (dentro ou fora do turno).

O ecrã mostra a hora atual, a sucursal ou ponto de trabalho associado e, caso seja exigida validação por GPS, o estado da sua localização em relação ao raio permitido.

A partir da versão 1.3.2, o ecrã organiza-se em cartões:

- **Cartão de controlo**, com o botão de registo que corresponde a cada momento e dois cronómetros: o da **jornada**, que começa com a entrada e não para durante as pausas, e o de **descanso**, que soma todas as pausas do dia. São calculados a partir dos registos válidos, pelo que refletem também as correções feitas a partir do backoffice.
- **Informação laboral**: sucursal, horário do dia —um turno por linha— e descanso. Com descanso estrito são mostrados os minutos; com descanso flexível, «Flexível».
- **Tarefas de hoje**.

Se hoje não for dia útil para o funcionário, o cartão indica-o —distinguindo um feriado de um dia livre— e o registo explica porque não é possível registar e que, se trabalhou, pode pedir uma jornada manual. **A partir da versão 1.10.0**, a casa do horário diz **Dia não útil** e o motivo aparece por baixo dos números do dia numa etiqueta destacada: o tipo de férias ou licença, ou o nome do feriado, tal como esse dia se chama no calendário. Ver [Feriados e dias não úteis](../04-calendario-e-horarios/29-feriados-e-dias-nao-uteis.md).

### O meu calendário

**A partir da versão 1.10.0**, o menu lateral tem, dentro de **Ferramentas**, a opção **O meu calendário**: o mês da pessoa, com os dias de trabalho, as folgas, os feriados e as suas ausências. A partir daí pede férias ou uma licença, e recebe um aviso quando a empresa a aprova ou a recusa. Ver [Férias e licenças a partir da aplicação](../04-calendario-e-horarios/115-ferias-e-licencas-a-partir-da-aplicacao.md).

> **Aviso:** para efetuar um registo é imprescindível ter ligação à internet ativa e o GPS ativado. Sem estes elementos, o registo não poderá ser concluído.

---

## Secção Os meus registos

Nesta secção encontrará o histórico completo dos seus registos gravados na plataforma. A partir daqui pode:

- Consultar entradas, saídas e pausas por data.
- Filtrar os registos por sucursal ou por tipo de evento.
- Ver o detalhe de cada registo: hora exata, estado (válido ou falhado), distância ao raio da sucursal e método de validação utilizado.
- Solicitar a correção de um registo ou a criação de uma jornada manual, se for o caso.

---

## Secção Documentos

A secção de documentos centraliza todos os ficheiros laborais que a sua organização lhe partilhou através do CheckBiz360. Aqui encontrará:

- Recibos de vencimento, contratos, comunicados internos e qualquer outro documento que o administrador tenha publicado para si.
- A possibilidade de consultar os documentos diretamente na aplicação ou descarregá-los para o seu dispositivo.
- O estado de confirmação de leitura de cada documento, quando aplicável.

---

## Secção Tarefas

A secção de tarefas mostra as atividades que lhe foram atribuídas pelo seu manager ou administrador. A partir daqui pode:

- Consultar a lista de tarefas atribuídas com o seu estado e a sua prioridade.
- Ver o detalhe de cada tarefa: descrição, prazo, data prevista de início e evidências.
- Ver o **local de trabalho**, se a tarefa tiver um próprio, e abri-lo com **Ver no Maps**. Antes de iniciar, a aplicação calcula a distância e avisa se estiver longe; quem decide é o servidor.
- Iniciar uma tarefa, **pausá-la e retomá-la** (a partir da versão 1.4.0), acrescentar notas de progresso, carregar evidências em foto ou vídeo e marcá-la como concluída. Iniciar, retomar e concluir requerem ter a jornada registada.
- **A partir da versão 1.6.0**, iniciar, pausar, retomar e concluir estão também no próprio cartão da lista e no cartão **Tarefas de hoje** do ecrã de assiduidade, sem entrar no detalhe. Só aparecem nas tarefas próprias, e concluir pede confirmação.
- **Procurar por sucursal ou por funcionário** nos filtros: os campos de procura mostram opções mal lhes toca, sem escrever nada.
- Consultar o **tempo investido**, o total de pausas e o **histórico** da tarefa (a partir da versão 1.4.0).

A **descrição é mostrada com a sua formatação**: os títulos, as listas e as listas de verificação que o responsável escreveu a partir do backoffice veem-se como tal, e não como texto simples com símbolos. As caixas de uma lista de verificação são um guia de trabalho: leem-se, mas não se marcam a partir da aplicação, porque fazem parte do texto da tarefa e não do seu estado. As ligações abrem-se no navegador do dispositivo.

### O que vê um supervisor na lista

Quem tem pessoas a seu cargo vê na mesma lista as suas tarefas e as da equipa. **A partir da versão 1.6.0** aparecem separadas: em cima **As minhas tarefas**, numa secção que se pode fechar, e por baixo **Tarefas da equipa**. As próprias levam ainda uma marca junto ao título, e são as únicas com botões de ação no cartão. Em **Tarefas de hoje**, as próprias aparecem primeiro.

Um funcionário sem pessoas a cargo não vê nenhuma destas separações: todas as tarefas da sua lista são suas.

> **Aviso:** atualizar o estado de uma tarefa exige ligação à internet.

---

## Secção Perfil

A secção de perfil permite-lhe gerir a sua informação pessoal e as preferências de segurança da sua conta. A partir daqui pode:

- Consultar e atualizar os seus dados de contacto.
- Alterar a sua palavra-passe de acesso.
- Configurar a autenticação em dois passos (2FA).
- Ativar o acesso biométrico (impressão digital ou reconhecimento facial), se o seu dispositivo e a configuração da sua organização o permitirem.
- Gerir as preferências de notificações push.

---

## Ecrã de notificações

O CheckBiz360 inclui um centro de notificações acessível a partir do ícone de sino ou aviso que aparece na parte superior do ecrã. Neste espaço encontrará:

- Alertas sobre novos documentos publicados.
- Notificações de tarefas atribuídas ou próximas do prazo.
- Comunicados do sistema ou da sua organização.

As notificações não lidas são indicadas com um contador numérico sobre o ícone. Toque em qualquer notificação para aceder diretamente ao conteúdo relacionado.

---

## Navegação entre secções

Para se mover entre as diferentes áreas da aplicação:

1. Localize a barra de navegação inferior do ecrã.
2. Toque no ícone da secção a que pretende aceder.
3. A secção carregará de imediato, conservando a sua posição na secção anterior para que possa regressar com facilidade.

A partir de qualquer secção pode voltar ao ecrã de registo tocando no ícone central da barra de navegação, que funciona como atalho prioritário.

---

## Nota de perfil

Este artigo dirige-se a **funcionários** que utilizam a aplicação CheckBiz360 no seu dia a dia. A estrutura e as secções descritas são as que correspondem ao perfil de funcionário padrão; os perfis de manager ou administrador podem ter acesso a secções adicionais no portal web.

---

## Artigos relacionados

- [Primeiro início de sessão](70-primeiro-inicio-de-sessao.md)
- [Configuração de perfil na aplicação](72-configuracao-de-perfil-na-aplicacao.md)
- [Os meus registos de assiduidade](73-os-meus-registos-de-assiduidade.md)
- [Utilização sem ligação](74-utilizacao-sem-ligacao.md)
