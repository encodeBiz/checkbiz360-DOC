# Documentação — CheckBiz360

Bem-vindo à documentação do CheckBiz360, a plataforma de controlo de assiduidade digital da EncodeBiz. Esta documentação reúne todo o material dirigido ao cliente final: proprietários de conta, responsáveis de recursos humanos, gestores de área e supervisores de equipa.

Os artigos estão organizados em 16 secções temáticas. Cada secção cobre um módulo ou área funcional da plataforma e contém artigos independentes que podem ser consultados individualmente ou lidos de forma sequencial.

---

## Estados das funcionalidades

A convenção seguinte identifica o estado de cada funcionalidade na versão atual do CheckBiz360 (V1). Aplica-se a todos os artigos da documentação e às tabelas de cada módulo desta página.

| Estado | Significado |
|---|---|
| **Disponível** | A funcionalidade está ativa na versão atual e pode ser utilizada de imediato. |
| **Parcialmente disponível** | A funcionalidade existe, mas com capacidades limitadas face à descrição completa. |
| **Planeada** | A funcionalidade está planeada e será incluída numa versão futura da plataforma. |
| **Não disponível** | A funcionalidade não está implementada e não tem, de momento, data de entrega planeada. |

---

## Secções

### 01. Primeiros passos

Introdução à plataforma, diferenças face a outros sistemas e guia de arranque inicial.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Registo de conta e configuração da entidade | **Disponível** | Processo completo disponível a partir do backoffice. |
| Configuração de sucursais | **Disponível** | Criação, edição e desativação de sucursais. |
| Guia de início rápido | **Disponível** | Fluxo de 10 passos até ao primeiro registo validado. |
| Guia inicial no backoffice, narrado pelo Merlin | **Disponível** | Cinco passos sobre o estado real da conta: subscrição, horário, local, funcionário e teste de registo. |
| Verificação anti-bots no registo e na recuperação da palavra-passe | **Disponível** | Desafio da Cloudflare integrado no formulário. |
| Hierarquia entidade → sucursal → funcionário | **Disponível** | Totalmente operacional na V1. |

| Artigo | Descrição |
|---|---|
| [O que é o CheckBiz360](01-primeiros-passos/01-o-que-e-o-checkbiz360.md) | Descrição geral da plataforma, componentes e casos de utilização |
| [Diferenças face a outros software](01-primeiros-passos/02-diferencas-face-a-outros-software.md) | Comparação com sistemas tradicionais de controlo de horários |
| [Criar conta e configurar a entidade](01-primeiros-passos/03-criar-conta-e-configurar-a-entidade.md) | Passos desde o registo até à primeira sucursal operacional |
| [Guia de início rápido](01-primeiros-passos/04-guia-de-inicio-rapido.md) | Os 10 passos para ter o primeiro registo validado em 15 minutos |
| [Estrutura da plataforma](01-primeiros-passos/05-estrutura-da-plataforma.md) | Os três níveis hierárquicos: entidade, sucursal e funcionário |

---

### 02. Funcionários

Criação, configuração, perfis e segurança dos funcionários na plataforma.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Criação, edição e desativação de funcionários | **Disponível** | CRUD completo com estados laborais, e estado *pendente* —que não é faturado— para fichas por completar. |
| Tipo de relação: pessoal ou colaborador | **Disponível** | Visível na ficha; os colaboradores ficam de fora do relatório de registo de jornada. |
| Equipas (modelos de pessoas com função e valor) | **Disponível** | Aplicam-se a uma sucursal para adicionar toda a equipa de trabalho de uma vez. Adicionar uma equipa inteira a uma tarefa: planeado. |
| Perfis e níveis de responsabilidade (worker, supervisor, manager, owner) | **Disponível** | Quatro níveis com permissões diferenciadas. |
| Autenticação de dois fatores (2FA) | **Disponível** | Compatível com aplicações TOTP (Google Authenticator, Authy). |
| Verificação biométrica e dispositivos de confiança | **Disponível** | Configurável por funcionário a partir da aplicação. |
| Funcionários atribuídos a várias entidades | **Disponível** | Seletor de entidade no início de sessão. |
| Entrada de sucursais e equipa a partir de Excel | **Disponível** | Um modelo com duas folhas; revê-se o que vai ser criado antes de confirmar; as boas-vindas à aplicação enviam-se no fim, quando decidir. |
| Estado do acesso à aplicação, reenviar acesso e alterar e-mail | **Disponível** | A ficha diz se o correio de acesso foi entregue ou devolvido e se a pessoa já usa a aplicação; a página inicial avisa do que não chegou. |
| Exportação do diretório de funcionários | **Planeada** | A lista consulta-se e filtra-se no ecrã, sem ficheiro descarregável. |

| Artigo | Descrição |
|---|---|
| [Criar e gerir funcionários](02-funcionarios/06-criar-e-gerir-funcionarios.md) | Criação, edição, estados laborais e desativação |
| [Perfis e níveis de responsabilidade](02-funcionarios/07-perfis-e-niveis-de-responsabilidade.md) | Os quatro níveis: worker, supervisor, manager, owner |
| [Matriz de permissões por perfil](02-funcionarios/08-matriz-de-permissoes-por-perfil.md) | Tabela completa do que cada perfil pode fazer |
| [Autenticação de dois fatores (2FA)](02-funcionarios/09-autenticacao-de-dois-fatores.md) | Configuração, aplicações compatíveis e recuperação de acesso |
| [Biometria e dispositivos de confiança](02-funcionarios/10-biometria-e-dispositivos-de-confianca.md) | Verificação biométrica e gestão de dispositivos autorizados |
| [Funcionários multi-entidade](02-funcionarios/11-funcionarios-multi-entidade.md) | Um funcionário em várias organizações, seletor de entidade |
| [Exportar a lista de funcionários](02-funcionarios/12-exportar-lista-de-funcionarios.md) | Estado da funcionalidade, alternativas disponíveis e RGPD |
| [Equipas](02-funcionarios/99-equipas.md) | Criar equipas, aplicá-las a uma sucursal e guardar uma sucursal como equipa |
| [Dar entrada a sucursais e equipa a partir de Excel](02-funcionarios/110-dar-entrada-a-sucursais-e-equipa-a-partir-de-excel.md) | Centros e pessoas de uma vez, com revisão antes de criar o que quer que seja e as boas-vindas à parte |
| [Acesso à aplicação e alteração de e-mail](02-funcionarios/116-acesso-a-aplicacao-e-alteracao-de-email.md) | Saber se o acesso chegou, reenviá-lo, alterar o e-mail e enviar o cartão do ponto de registo |

---

### 03. Controlo de horários

Como funciona o sistema de registo de ponto: validações, tipos de registo, geocercas e gestão de jornadas.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Registo com validação de geocerca, horário e dispositivo | **Disponível** | Três camadas de validação simultâneas em cada registo. |
| Entrada e saída a partir da aplicação móvel | **Disponível** | Processo completo operacional em iOS e Android. |
| Trabalho fora do centro (antes «registo em teletrabalho») | **Disponível** | Ativação por funcionário com validação de fuso horário. |
| Pausas e descansos (restin/restout) | **Disponível** | Desconto automático configurável por sucursal. |
| Validação por QR antes do registo | **Disponível** | Mecanismo configurável por sucursal, não obrigatório. |
| Pedido de jornada manual (Modo A e Modo B) | **Disponível** | Requer aprovação do responsável. |
| Revisão e validação de registos pelo responsável | **Disponível** | Fluxo de aprovação, recusa e resolução; uma correção recusada deixa o registo como estava. |
| Rastreabilidade e histórico de alterações imutável | **Disponível** | Registo de pedidos e alterações com auditoria. |
| Deteção de registo suspeito | **Disponível** | Indicador automático baseado em padrões anómalos. |
| Ponto de registo: dispositivo do local com QR ou código e foto | **Disponível** | Complemento pago. Contrata-se e gere-se no painel; o dispositivo usa a aplicação CheckBiz360. |

| Artigo | Descrição |
|---|---|
| [Como funciona o registo de ponto](03-controlo-de-horarios/13-como-funciona-o-registo-de-ponto.md) | As três camadas de validação: geocerca, horário e dispositivo |
| [Entrada e saída na aplicação](03-controlo-de-horarios/14-entrada-e-saida-na-aplicacao.md) | Passo a passo do registo a partir da aplicação móvel |
| [Trabalho fora do centro](03-controlo-de-horarios/15-registo-em-teletrabalho.md) | Registar sem geocerca: trabalho de campo, teletrabalho, ativação e fuso horário |
| [Geocercas e raio de registo](03-controlo-de-horarios/16-geocercas-e-raio-de-registo.md) | Configuração do raio, desativação e valores recomendados |
| [Pausas e descansos](03-controlo-de-horarios/17-pausas-e-descansos.md) | Restin/restout, desconto automático e configuração por sucursal |
| [Validação do funcionário por QR](03-controlo-de-horarios/18-validacao-do-funcionario-qr.md) | Token QR, fluxo com supervisor e arranque do sistema |
| [Solicitar jornada manual](03-controlo-de-horarios/19-solicitar-jornada-manual.md) | Modo A (jornada completa) e Modo B (apenas saída) |
| [Revisão e validação de registos](03-controlo-de-horarios/20-revisao-e-validacao-de-registos.md) | Fluxo de aprovação, recusa e resolução pelo responsável |
| [Rastreabilidade e histórico de alterações](03-controlo-de-horarios/21-rastreabilidade-e-historico-de-alteracoes.md) | requestUpdates, imutabilidade e utilização em auditorias |
| [Estados e códigos de erro](03-controlo-de-horarios/22-estados-e-codigos-de-erro.md) | Tabelas de estados e códigos de erro com causas e soluções |
| [Ponto de registo](03-controlo-de-horarios/113-ponto-de-registo.md) | Registar o ponto a partir de um tablet do local com QR ou código e uma foto, sem biometria |

---

### 04. Calendário e horários

Configuração de turnos, horários base, calendários laborais e exceções individuais.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Horários base e turnos por sucursal | **Disponível** | Turno único ou vários turnos por dia. |
| Calendário laboral (feriados nacionais e locais) | **Disponível** | Hierarquia de herança: entidade → sucursal → funcionário. |
| Exceções de horário individuais | **Disponível** | Exceções pontuais e periódicas. |
| Jornada estrita ou flexível | **Disponível** | Decide se conta o horário oficial ou o tempo realmente trabalhado. |
| Descanso estrito ou flexível | **Disponível** | Duração fixa descontada, ou pausas marcadas pelo funcionário. |
| Modelos de horário | **Disponível** | Guardar um horário semanal e aplicá-lo a outras sucursais. |
| Ausências de funcionário por intervalo de datas, com marca de remunerada | **Disponível** | Remunerada, não remunerada ou por definir. |
| Quadro de disponibilidade | **Disponível** | Cobertura por sucursal e dia, quem falta e porquê, registo de dias livres a partir do quadro e exportação para Excel. |
| Herança de configuração em cascata | **Disponível** | Algoritmo de prioridade para calcular o calendário efetivo. |
| Turnos rotativos (alternância A/B automática) | **Planeada** | Hoje resolve-se com uma sucursal por turno ou com horário próprio do funcionário. |
| Escala semanal a partir de um modelo de Excel | **Disponível** | A semana de toda uma sucursal num só carregamento, uma folha por pessoa e revisão antes de aplicar; também a de uma pessoa a partir da sua ficha. Conforme o modo de cada pessoa carrega turnos ou tarefas; a quem está em «Semana tipo» não se carrega nada. |
| Três modos do horário: «Semana tipo», «Por turnos» e «Por tarefas» | **Disponível** | O modo é a única fonte do horário de cada pessoa. «Por tarefas» escolhe-se por pessoa na sua ficha. |
| «Por turnos»: turnos carregados por data | **Disponível** | Na empresa, numa sucursal ou numa pessoa; escala de turnos semanal com um ou vários turnos por dia, copiar para a semana seguinte e importar a escala por turnos. Um dia sem turnos é folga. |
| Férias e licenças pedidas a partir da aplicação | **Disponível** | «O meu calendário» na aplicação; aprovam-se em Contacto → Pedidos. |

| Artigo | Descrição |
|---|---|
| [Horários base e turnos](04-calendario-e-horarios/23-horarios-base-e-turnos.md) | Turno único, vários turnos por dia, seleção do turno ativo |
| [Calendário laboral](04-calendario-e-horarios/24-calendario-laboral.md) | Feriados nacionais e locais, hierarquia entity→branch→employee |
| [Exceções de horário](04-calendario-e-horarios/25-excecoes-de-horario.md) | Exceções pontuais e periódicas, jornada reduzida |
| [Herança de configuração](04-calendario-e-horarios/26-heranca-de-configuracao.md) | Algoritmo em cascata e depuração do calendário efetivo |
| [Turnos rotativos](04-calendario-e-horarios/27-turnos-rotativos.md) | Não disponível na V1: como cobrir a rotação com sucursais ou horário do funcionário |
| [Jornada estrita e jornada flexível](04-calendario-e-horarios/28-horario-flexivel.md) | Como se contam as horas e as pausas em cada modalidade |
| [Feriados e dias não úteis](04-calendario-e-horarios/29-feriados-e-dias-nao-uteis.md) | Tipos de feriado, ausências de funcionário, bloqueio de registos, setores que trabalham em feriado |
| [Quadro de disponibilidade](04-calendario-e-horarios/98-quadro-de-disponibilidade.md) | Cobertura por sucursal e dia, detalhe de quem falta e dias livres a partir do quadro |
| [Importar a escala semanal](04-calendario-e-horarios/108-importar-a-escala-semanal.md) | A semana de toda a equipa de uma filial num só carregamento, ou a de uma pessoa a partir da sua ficha |
| [Por turnos: o horário são os turnos que carrega](04-calendario-e-horarios/114-calendario-de-turnos-por-data.md) | Os três modos do horário e a escala de turnos: cada dia com os seus turnos, carregados à mão, copiados ou a partir de Excel |
| [Férias e licenças a partir da aplicação](04-calendario-e-horarios/115-ferias-e-licencas-a-partir-da-aplicacao.md) | «O meu calendário» na aplicação, pedir férias ou licença e aprová-lo no painel |

---

### 05. Gestão documental

Carregamento, organização, confirmação de leitura e controlo de acesso aos documentos laborais.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Carregamento e organização de documentos | **Disponível** | Doze tipos, âmbito entidade/sucursal/funcionário e visibilidade por perfil. Máx. 10 MB por ficheiro. |
| Documentos privados com controlo de acesso por perfil | **Disponível** | Tabela de permissões diferenciada por nível de utilizador. |
| Notificações push ao receber documentos | **Disponível** | Navegação direta para o documento a partir da notificação. |
| Confirmação de leitura | **Disponível** | O funcionário confirma a leitura; fica registado no sistema. |
| Descarga individual de documentos | **Disponível** | Ligação assinada por documento, com expiração. |
| Arquivo lógico de documentos (sem eliminação permanente) | **Disponível** | Os documentos arquivados deixam de estar visíveis mas são conservados. |
| Confirmação assinada no telemóvel | **Disponível** | Ata de assinatura descarregável e PDF assinado para documentos PDF dirigidos a um único funcionário. |
| Histórico automático de versões | **Planeada** | Planeado para uma versão futura. |
| Descarga em massa de documentos (ZIP) | **Planeada** | Planeada para uma versão futura. |

| Artigo | Descrição |
|---|---|
| [O que é o módulo documental](05-gestao-documental/30-o-que-e-o-modulo-documental.md) | Para que serve, tipos de documentos e diferença face a um armazenamento genérico |
| [Carregar e organizar documentos](05-gestao-documental/31-carregar-e-organizar-documentos.md) | Campos, categorias, destinatários e visibilidade |
| [Recibos de vencimento e contratos](05-gestao-documental/32-recibos-de-vencimento-e-contratos.md) | Fluxo mensal, notificação, acesso pela aplicação e conservação legal |
| [Documentos privados](05-gestao-documental/33-documentos-privados.md) | Visibilidade por perfil, tabela de acesso e casos de utilização |
| [Notificações de documentos](05-gestao-documental/34-notificacoes-de-documentos.md) | Payload push, navegação direta para o documento a partir da notificação |
| [Confirmação de leitura e assinatura eletrónica](05-gestao-documental/35-assinatura-eletronica.md) | Confirmação assinada com o telemóvel, ata de assinatura e PDF assinado para documentos de uma pessoa |
| [Histórico de versões](05-gestao-documental/36-historico-de-versoes.md) | Fluxo manual disponível na V1; histórico automático no roadmap |
| [Permissões de acesso documental](05-gestao-documental/37-permissoes-de-acesso-documental.md) | Tabela de permissões por perfil: carregar, ver, confirmar, arquivar |
| [Exportar documentos](05-gestao-documental/38-exportar-documentos.md) | Descarga individual na V1; descarga em massa no roadmap |

---

### 06. Tarefas

Criação, atribuição, acompanhamento e avaliação de tarefas operacionais.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Criar e atribuir tarefas a funcionários | **Disponível** | Atribuição individual e múltipla com notificação push; editar a tarefa atribui e retira funcionários. |
| Local de trabalho próprio por tarefa | **Disponível** | Morada e margem próprias; iniciar exige estar lá, a partir da aplicação. |
| Duplicar uma tarefa | **Disponível** | Copia o trabalho, sem atribuição e em rascunho; pede de novo as datas. |
| Pausar e retomar tarefas | **Disponível** | A partir do backoffice e da aplicação 1.4.0; o tempo em pausa aparece no relatório. |
| Histórico da tarefa | **Disponível** | Quem a criou, iniciou, pausou, concluiu, validou ou cancelou, com data e perfil. |
| Descrição com formatação (listas, checklists, ligações) | **Disponível** | Editor com barra de formatação e pré-visualização. |
| Evidências de foto e vídeo | **Disponível** | Foto (JPG, PNG, WEBP) até 5 MB; vídeo até 25 MB a partir da aplicação. |
| Estados de tarefa: rascunho, atribuída, em curso, concluída, validada, recusada, cancelada | **Disponível** | Sete estados com rastreabilidade completa. |
| Quatro prioridades: baixa, média, alta e crítica | **Disponível** | Com código de cor na listagem. |
| Indicador de cumprimento temporal | **Disponível** | A tempo, em risco, vencida, concluída a tempo ou tarde. |
| Data prevista de início e aviso de início tardio | **Disponível** | Notificação ao fim de 15 minutos, configurável por tarefa. |
| Validação e avaliação de tarefas pelo responsável | **Disponível** | Delegáveis ao supervisor por tarefa; recusa com motivo obrigatório. |
| Notificações push de tarefas | **Disponível** | Atribuição, validação, recusa, início tardio e vencimento. |
| Relatório de tarefas exportável | **Disponível** | Excel (XLSX), filtrável por sucursal, estado e período de vencimento, com tempo investido e em pausa; com o inventário contratado, também o material de cada tarefa. |
| Anexos de tipo documento (PDF, Word, Excel) | **Planeada** | Hoje as evidências admitem foto e vídeo. |
| Estado «vencida» automático ao ultrapassar o prazo | **Planeada** | Hoje o vencimento reflete-se no cumprimento temporal. |
| Configurar a antecedência dos avisos de vencimento | **Planeada** | Os avisos são emitidos; a sua antecedência não é configurável. |
| Métricas agregadas de tarefas (conclusão, tempo médio) | **Planeada** | Calculáveis hoje a partir do relatório em Excel. |
| Calendário semanal de tarefas | **Disponível** | Separador ao lado da lista: a semana por dia e hora, com os buracos, as sobreposições e o que vence; mesmos filtros que a lista. |

| Artigo | Descrição |
|---|---|
| [O que é o módulo de tarefas](06-tarefas/39-o-que-e-o-modulo-de-tarefas.md) | Para que serve e diferença face ao controlo de assiduidade |
| [Criar uma tarefa](06-tarefas/40-criar-uma-tarefa.md) | Campos, local de trabalho próprio, duplicar uma tarefa e anexos de foto/vídeo |
| [Atribuir tarefas a funcionários](06-tarefas/41-atribuir-tarefas-a-funcionarios.md) | Atribuição individual e múltipla, reatribuição, notificação |
| [Estados de uma tarefa](06-tarefas/42-estados-de-uma-tarefa.md) | Ciclo de vida, reabrir uma tarefa, tarefa em pausa e indicador de cumprimento temporal |
| [Acompanhamento e atualizações](06-tarefas/43-acompanhamento-e-atualizacoes.md) | Iniciar, pausar e retomar, notas e histórico da tarefa |
| [Prioridades e prazos](06-tarefas/44-prioridades-e-prazos.md) | Sistema de prioridades e indicador de cumprimento temporal |
| [Validação de tarefas](06-tarefas/45-validacao-de-tarefas.md) | Fluxo de validação, aceitação e recusa com motivo |
| [Avaliação do trabalhador](06-tarefas/46-avaliacao-do-trabalhador.md) | Escala de pontuação e impacto no índice de eficiência |
| [Notificações de tarefas](06-tarefas/47-notificacoes-de-tarefas.md) | Eventos notificados na V1; lembretes no roadmap |
| [Relatórios de tarefas](06-tarefas/48-relatorios-de-tarefas.md) | Métricas no backoffice e relatório em Excel, com as suas colunas de tempo |
| [Calendário semanal de tarefas](06-tarefas/111-calendario-semanal-de-tarefas.md) | A semana num relance: o que há em cada dia, a que hora, em que estado e o que vence |

---

### 07. Inteligência operacional

Análise de padrões de comportamento, índices de desempenho, custos e deteção de anomalias.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Painel de Operação (vista única, por período mensal) | **Disponível** | Lê-se de cima para baixo; três separadores: Sucursais, Funcionários e Análise. |
| Índice de fiabilidade | **Disponível** | Qualidade do comportamento, separada do tempo que se leva a medir. |
| Efeito do local | **Disponível** | Compara cada pessoa consigo própria em locais diferentes. |
| Dependência (concentração da operação) | **Disponível** | Quanto da operação recai sobre poucas pessoas, com substituição por função. |
| Estados de maturidade do dado | **Disponível** | A acumular dados / evidência parcial / sem dados suficientes. |
| Índice de eficiência operacional e custo | **Disponível** | Custo real face ao histórico consolidado; requer tarifa configurada. |
| Avaliação operacional do funcionário | **Disponível** | Diagnóstico automático do padrão, com sinal de candidato a promoção. |
| Deteção de anomalias (registos suspeitos) | **Disponível** | Surge no separador de Análise do painel. |
| Relato do assistente de IA sobre o painel | **Disponível** | Narra e prioriza os números que o ecrã já mostra. |
| Pontuação de promoção como valor único comparável | **Planeada** | Não existe um número único nem um ranking por esse valor. |
| Fluxo de revisão de anomalias (estados pendente/revisto) | **Planeada** | Planeado para uma versão futura. |
| Alertas de excesso de custo configuráveis | **Planeada** | Planeados para uma versão futura. |
| Exportação de dados dos painéis (CSV/PDF) | **Planeada** | Planeada para uma versão futura. |
| Página inicial «Início»: o hoje por centro, alertas, últimas semanas, disponibilidade da semana, equipa ao longo do tempo e custos estimados | **Disponível** | A primeira coisa que se vê ao entrar; atualiza-se sozinha e mostra só o que requer atenção. |

| Artigo | Descrição |
|---|---|
| [O que é a inteligência operacional](07-inteligencia-operacional/49-o-que-e-a-inteligencia-operacional.md) | O módulo diferenciador do CheckBiz360 e o conceito de padrão de comportamento |
| [Padrão de comportamento](07-inteligencia-operacional/50-padrao-de-comportamento.md) | Como se constrói o padrão e porque supera o relatório pontual |
| [Índice de fiabilidade](07-inteligencia-operacional/51-indice-de-fiabilidade.md) | O que mede, intervalos e como melhorá-lo |
| [Índice de eficiência operacional](07-inteligencia-operacional/52-indice-de-eficiencia.md) | Custo real face ao histórico e como interpretá-lo |
| [Avaliação operacional do funcionário](07-inteligencia-operacional/53-pontuacao-de-promocao.md) | Diagnóstico do padrão e sinal de candidato a promoção |
| [Análise de custos](07-inteligencia-operacional/54-analise-de-custos.md) | Tarifa por sucursal, indicadores de custo e alertas no roadmap |
| [Deteção de anomalias](07-inteligencia-operacional/55-detecao-de-anomalias.md) | Indicador automático na V1; fluxo de revisão no roadmap |
| [O painel de Operação](07-inteligencia-operacional/56-paineis-de-controlo.md) | Os três índices, os três separadores e como se lê |
| [A página inicial: o hoje, os alertas e as últimas semanas](07-inteligencia-operacional/112-a-pagina-inicial-o-hoje-os-alertas-e-as-ultimas-semanas.md) | O que vê ao entrar: jornada, tarefas e custo de hoje por centro, alertas, histórico semanal, equipa e custos estimados |

---

### 08. Sucursais e entidade

Criação e configuração de sucursais, atribuição de funcionários e vista global multi-sucursal.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Criar e gerir sucursais | **Disponível** | Criação, edição, geocodificação e desativação. |
| Configuração avançada de sucursal (geocerca, pausas, tolerância) | **Disponível** | Todos os parâmetros operacionais configuráveis. |
| Atribuir funcionários a sucursais com responsabilidades | **Disponível** | Multi-sucursal com calendário efetivo por atribuição. |
| Configuração da entidade (dados fiscais, fuso horário) | **Disponível** | Propagação de alterações às sucursais dependentes. |
| Armazenamento por empresa | **Disponível** | 2 GB incluídos; acima disso, 0,25 € por GB completo se a ampliação estiver ativada. Consulta-se em Entidade → Subscrições. |
| Colaboradores do backoffice (proprietário e administrador) | **Disponível** | Convite, mudança de perfil e remoção; a entidade nunca fica sem proprietário ativo. |
| Vista global multi-sucursal | **Disponível** | A página inicial mostra o hoje por centro e os alertas; o painel de Operação compara os centros por período. |

| Artigo | Descrição |
|---|---|
| [Criar e gerir sucursais](08-sucursais-e-entidade/57-criar-e-gerir-sucursais.md) | Criação, campos obrigatórios, geocodificação e desativação |
| [Configuração avançada de sucursal](08-sucursais-e-entidade/58-configuracao-avancada-de-sucursal.md) | Parâmetros avançados: geocerca, pausas, tolerância, ajuste de timestamp |
| [Estados de uma sucursal](08-sucursais-e-entidade/59-estados-de-uma-sucursal.md) | Ativa/inativa, impacto nos registos e histórico |
| [Atribuir funcionários a sucursais](08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md) | Multi-sucursal, responsabilidades e calendário efetivo |
| [Configuração da entidade](08-sucursais-e-entidade/61-configuracao-da-entidade.md) | Dados fiscais, ambiente de trabalho, colaboradores, fuso horário global e propagação de alterações |
| [Vista global multi-sucursal](08-sucursais-e-entidade/62-vista-global-multi-sucursal.md) | Onde está cada vista de conjunto: a página inicial de hoje por centros, o painel de Operação e a disponibilidade |

---

### 09. Notificações

Tipos de notificação gerados automaticamente pelo sistema para funcionários e responsáveis.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Notificações push por eventos (assiduidade, documentos, tarefas) | **Disponível** | Enviadas automaticamente em cada evento relevante. |
| Alertas para responsáveis (funcionário sem registo, registo suspeito) | **Disponível** | Visíveis no backoffice e na aplicação do supervisor. |
| Centro de notificações na aplicação e no backoffice | **Parcialmente disponível** | Notificações visíveis enquanto não são descartadas; sem histórico persistente. |
| Correio de boas-vindas e reposição de palavra-passe | **Disponível** | Com o estado de entrega na ficha do funcionário e o reenvio do acesso. |
| Avisos de tarefas e horário semanal por correio, para quem não usa a aplicação | **Disponível** | Caixa por pessoa em Horários e feriados; nada do registo de ponto. |
| Preferências de notificação configuráveis por utilizador | **Planeada** | Planeada para uma versão futura. |
| Histórico persistente de notificações | **Planeado** | Planeado para uma versão futura. |
| Alertas operacionais por correio aos responsáveis | **Planeada** | Planeada para uma versão futura. |

| Artigo | Descrição |
|---|---|
| [Tipos de notificação](09-notificacoes/63-tipos-de-notificacao.md) | Assiduidade, documentos, tarefas, segurança e administrativas |
| [Notificações push na aplicação](09-notificacoes/64-notificacoes-push-na-aplicacao.md) | Conteúdo, navegação direta para o recurso e diagnóstico |
| [Configurar preferências de notificação](09-notificacoes/65-configurar-preferencias-de-notificacao.md) | Eventos notificados na V1; preferências configuráveis no roadmap |
| [Alertas para responsáveis](09-notificacoes/66-alertas-para-responsaveis.md) | Funcionário que não registou, registo suspeito, jornada manual pendente |
| [Histórico de notificações](09-notificacoes/67-historico-de-notificacoes.md) | Centro de notificações na V1; histórico persistente no roadmap |
| [Notificações por email](09-notificacoes/68-notificacoes-por-email.md) | Boas-vindas e estado do acesso, avisos de trabalho por correio, aviso de armazenamento; alertas operacionais no roadmap |

---

### 10. Aplicação móvel

Descarga, instalação, navegação e utilização da aplicação CheckBiz360 para funcionários.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Descarga e instalação em iOS e Android | **Disponível** | Disponível na App Store e no Google Play. |
| Registo a partir da aplicação com as três validações | **Disponível** | Geocerca, horário e dispositivo validados em tempo real. |
| Consulta do histórico de assiduidade próprio | **Disponível** | Filtros por período e detalhe de cada registo. |
| Acesso a documentos e tarefas a partir da aplicação | **Disponível** | Navegação da notificação para o recurso; a descrição da tarefa é mostrada com formatação. |
| Pausar e retomar tarefas, tempo investido e histórico na aplicação | **Disponível** | A partir da versão 1.4.0. |
| Local de trabalho da tarefa com ligação ao Maps | **Disponível** | A partir da versão 1.3.2. |
| Configuração de perfil, 2FA e biometria | **Disponível** | Gerível a partir da secção de perfil da aplicação. |
| «O meu calendário»: o mês de cada pessoa e pedir férias ou licença | **Disponível** | A partir da versão 1.10.0, no menu, dentro de **Ferramentas**. |
| Motivo do dia não útil no ecrã de Presença | **Disponível** | A partir da versão 1.10.0: o nome que esse dia livre tem no calendário. |
| Consulta de dados em cache sem ligação | **Parcialmente disponível** | Apenas leitura de dados previamente carregados; registar e atualizar tarefas requer ligação. |
| Modo offline com fila de sincronização de registos | **Planeado** | Planeado para uma versão futura. |

| Artigo | Descrição |
|---|---|
| [Descarga e instalação](10-aplicacao-movel/69-descarga-e-instalacao.md) | iOS e Android, requisitos mínimos e permissões necessárias |
| [Primeiro início de sessão](10-aplicacao-movel/70-primeiro-inicio-de-sessao.md) | Ativação de conta, palavra-passe e seleção de entidade |
| [Navegação principal da aplicação](10-aplicacao-movel/71-navegacao-principal-da-aplicacao.md) | As 5 secções: registo, registos, documentos, tarefas e perfil |
| [Configuração de perfil na aplicação](10-aplicacao-movel/72-configuracao-de-perfil-na-aplicacao.md) | Dados pessoais, palavra-passe, 2FA e biometria a partir da aplicação |
| [Os meus registos de assiduidade](10-aplicacao-movel/73-os-meus-registos-de-assiduidade.md) | Histórico próprio, filtros, detalhe e pedido de correção |
| [Utilização sem ligação](10-aplicacao-movel/74-utilizacao-sem-ligacao.md) | Que dados estão acessíveis sem ligação e o que exige conectividade |
| [Atualizações da aplicação](10-aplicacao-movel/75-atualizacoes-da-aplicacao.md) | Novidades por versão, como atualizar e consequências de versões desatualizadas |

---

### 11. Relatórios e exportação

Geração, filtragem e exportação de relatórios de assiduidade, custos e conformidade.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Relatório de assiduidade em PDF ou Excel (XLSX) | **Disponível** | Geração a pedido, com histórico de relatórios; reúne o pessoal da empresa, não os colaboradores. |
| Relatório de tarefas em Excel (XLSX) | **Disponível** | Filtrável por sucursal, estado e período de vencimento; inclui tempo em pausa e, com o inventário contratado, o material e o seu custo. |
| Exportação do diretório de funcionários | **Planeada** | A lista consulta-se e filtra-se no ecrã, sem ficheiro descarregável. |
| Relatório de conformidade com o RDL 8/2019 para inspeções | **Disponível** | Geração a partir do backoffice. |
| Exportação dos painéis de inteligência operacional | **Planeada** | Custos, anomalias e comparações consultam-se no ecrã. |
| Relatórios automáticos periódicos enviados por email | **Planeados** | Planeados para uma versão futura. |

| Artigo | Descrição |
|---|---|
| [Tipos de relatório](11-relatorios-e-exportacao/76-tipos-de-relatorio.md) | Assiduidade, pontualidade, custos, anomalias e tarefas |
| [Gerar e filtrar relatórios](11-relatorios-e-exportacao/77-gerar-e-filtrar-relatorios.md) | Filtros disponíveis, pré-visualização e configurações guardadas |
| [Exportar dados](11-relatorios-e-exportacao/78-exportar-para-excel-e-csv.md) | Assiduidade em PDF ou Excel e tarefas em Excel |
| [Relatório de conformidade legal](11-relatorios-e-exportacao/79-relatorio-de-conformidade-legal.md) | Relatório para auditorias e inspeções ao abrigo do RDL 8/2019 |
| [Relatórios automáticos](11-relatorios-e-exportacao/80-relatorios-automaticos.md) | Funcionalidade planeada no roadmap; não disponível na V1 |

---

### 12. Conformidade legal

Registo de jornada obrigatório em Espanha, proteção de dados e preparação para inspeções.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Registo de jornada conforme o RDL 8/2019 | **Disponível** | Timestamp imutável com rastreabilidade completa. |
| Relatório de inspeção do trabalho | **Disponível** | Geração a partir do backoffice com todos os dados exigidos. |
| Conservação de dados conforme a LOPD/RGPD | **Disponível** | Base legal, períodos de retenção e direitos dos funcionários. |

| Artigo | Descrição |
|---|---|
| [Registo de horários obrigatório em Espanha](12-conformidade-legal/81-registo-de-horarios-obrigatorio-em-espanha.md) | RDL 8/2019: o que exige, âmbito de aplicação e sanções |
| [Como o CheckBiz360 cumpre o RDL 8/2019](12-conformidade-legal/82-como-o-checkbiz360-cumpre-o-rdl-8-2019.md) | Mecanismos técnicos: timestamp, imutabilidade, rastreabilidade |
| [Conservação e proteção de dados](12-conformidade-legal/83-conservacao-e-protecao-de-dados.md) | LOPD/RGPD: base legal, retenção e direitos dos funcionários |
| [Preparar uma inspeção do trabalho](12-conformidade-legal/84-preparar-uma-inspecao-do-trabalho.md) | Que documentação pedir, que relatório apresentar e recomendações prévias |

---

### 13. Apoio e incidências

Como criar e gerir incidências e como contactar a equipa de apoio.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Criação de incidências a partir do backoffice | **Disponível** | Canal interno da organização: tipo, perfil de origem/destino, sucursal e comentário. Estão em **Contacto**, separador **Incidentes**. |
| Pedidos de férias e licenças em Contacto | **Disponível** | Separador **Pedidos**; só o proprietário e os administradores aprovam ou recusam. |
| Acompanhamento através de um fio de respostas | **Disponível** | Três estados (pendente, em revisão, resolvida); o estado muda ao responder. |
| Contacto com o apoio técnico por email | **Disponível** | Tempos de resposta indicativos, não contratuais. |
| Numeração automática de tickets | **Não disponível** | As incidências não geram número de referência automático. |
| Prioridade e anexos numa incidência | **Não disponível** | O formulário não contempla prioridade nem ficheiros anexos. |
| Reabertura de uma incidência resolvida | **Não disponível** | Uma incidência resolvida não admite mais respostas; cria-se uma nova. |
| Exportação do histórico de incidências | **Não disponível** | Consulta-se e filtra-se no ecrã. |

| Artigo | Descrição |
|---|---|
| [Criar uma incidência](13-apoio-e-incidencias/85-criar-uma-incidencia.md) | Canal interno da organização: tipos, campos e criação |
| [Acompanhamento e resolução de incidências](13-apoio-e-incidencias/86-acompanhamento-e-resolucao-de-incidencias.md) | Os três estados, o fio de respostas e o histórico |
| [Contactar o apoio técnico](13-apoio-e-incidencias/87-contactar-o-apoio-tecnico.md) | Canais, tempos indicativos e que informação incluir |
| [Problemas frequentes e soluções](13-apoio-e-incidencias/88-problemas-frequentes-e-solucoes.md) | As 14 situações mais habituais com passos de diagnóstico |

---

### 14. Referência

Glossário, códigos de erro, planos e perguntas frequentes.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Glossário de termos da plataforma | **Disponível** | Termos principais definidos, incluindo os de tarefas e IA. |
| Tabela completa de códigos de erro | **Disponível** | Todos os códigos do dicionário, por módulo, com causa e solução. |
| Planos e preços (Bronze e Empresarial) | **Disponível** | Preço, período experimental, módulos incluídos, complementos, armazenamento e roadmap. |
| Perguntas frequentes de avaliação | **Disponível** | 20 perguntas e respostas para clientes que avaliam a plataforma. |

| Artigo | Descrição |
|---|---|
| [Glossário](14-referencia/89-glossario.md) | Definições dos termos principais da plataforma |
| [Códigos de erro completos](14-referencia/90-codigos-de-erro-completos.md) | Tabela de todos os códigos de erro com causa e solução |
| [Planos, preços e funcionalidades](14-referencia/91-planos-e-funcionalidades.md) | Preço de cada plano, período experimental, módulos incluídos, complementos, armazenamento e roadmap |
| [Perguntas frequentes](14-referencia/92-perguntas-frequentes.md) | 20 perguntas e respostas para clientes que avaliam a plataforma |

### 15. Integrações

Add-ons que ligam o CheckBiz360 a outros programas que a sua empresa já utiliza, para que a informação viaje sozinha e ninguém escreva a mesma coisa duas vezes.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Catálogo de integrações | **Disponível** | Com descrição, capacidades e estado |
| RentmanBiz — envio de horas para o Rentman | **Disponível** | Automático a cada 15 minutos, ou de imediato |
| RentmanBiz — importação de equipa, centros e tarefas | **Disponível** | O incompleto fica pendente, nunca a meio |
| RentmanBiz — aviso de horas alteradas no Rentman | **Disponível** | O registo de ponto nunca é sobreposto |
| Ecrã de configuração do add-on | **Pendente de desenvolvimento** | Durante a beta configura-o a equipa da Encodebiz |
| Envio de tarefas para o Rentman | **Pendente de desenvolvimento** | Prevista numa versão futura |
| Gestor operacional no Claude ou no ChatGPT | **Disponível** | Ligue a sua empresa ao seu assistente e peça-lhe a semana, as entradas e as alterações nas suas palavras; nada se guarda sem a sua confirmação |

| Artigo | Descrição |
|---|---|
| [O que são as integrações](15-integracoes/93-o-que-sao-as-integracoes.md) | O que é um add-on, como se ativa e o que acontece ao desativá-lo |
| [RentmanBiz](15-integracoes/94-rentmanbiz.md) | O que traz a integração com o Rentman e o que não faz |
| [Ligar o RentmanBiz passo a passo](15-integracoes/95-ligar-o-rentmanbiz.md) | Do token do Rentman à primeira importação |
| [O que se importa e o que fica pendente](15-integracoes/97-importacao-e-pendentes.md) | Pessoas, centros, responsabilidades e tarefas; e o que fazer com o pendente |
| [Horas lançadas e avisos](15-integracoes/96-horas-lancadas-e-avisos.md) | Ler o painel, as divergências e as perguntas frequentes |
| [O seu gestor operacional no Claude ou no ChatGPT](15-integracoes/109-o-seu-gestor-operacional-no-claude-ou-chatgpt.md) | Ligar a sua empresa ao seu assistente e o que lhe pedir: a semana inteira, entradas em bloco, alterações soltas |


---

### 16. Inventário

Complemento pago: o material ligado à tarefa, à pessoa, ao sítio e à hora.

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Armazéns ligados a sucursais | **Disponível** | Todo o armazém serve pelo menos uma sucursal. |
| Artigos consumíveis e operáveis, com exemplares | **Disponível** | O artigo cria-se na sua primeira entrada. |
| Existências com estado, mínimos e discrepâncias | **Disponível** | Aviso aos responsáveis ao descer abaixo do mínimo. |
| Material atribuído ao criar a tarefa e acompanhado no seu detalhe | **Disponível** | Reserva, saída, consumo e acerto ao validar. |
| Saída e consumo na aplicação | **Disponível** | Pré-preenchido com o reservado e o pendente. |
| Calendário de exemplares com aviso de coincidência | **Disponível** | Por exemplar, na ficha do artigo. |
| Relatório de consumo e livro de movimentos | **Disponível** | Agrupado por artigo, tarefa, funcionário, sucursal ou armazém; CSV. |
| Material no relatório de tarefas | **Disponível** | Só com o complemento contratado. |
| Documentos e revisões de cada máquina | **Disponível** | Aviso de caducidade e marca a vermelho, sem bloquear. |
| Entrega de EPI confirmada pelo trabalhador | **Disponível** | Com impressão digital ou rosto na aplicação. |
| Relatório «Equipamentos e EPI» para inspeções | **Disponível** | Registo de entregas e dossiê por máquina. |
| Importação de material a partir de um modelo de Excel | **Disponível** | Por armazém, um para consumíveis e outro para operáveis; revê-se antes de importar e não duplica ao voltar a carregá-lo. |
| Onde está cada equipamento e equipamentos fora da base | **Disponível** | Libertá-lo não o devolve ao armazém: diz-se onde fica e recebe-se no armazém; histórico de onde esteve. |
| Material sem tarefas: para uma pessoa ou uma sucursal | **Disponível** | Dar saída, atribuir dotação, declarar a partir da jornada na app e acertar a partir da ficha; «Fora do armazém» em Existências. |

| Artigo | Descrição |
|---|---|
| [O que é o inventário](16-inventario/100-o-que-e-o-inventario.md) | Que problemas resolve, como funciona e como se contrata |
| [Existências, armazéns e entradas](16-inventario/101-existencias-armazens-e-entradas.md) | Entrada do material e controlo do que há |
| [Material nas tarefas](16-inventario/102-material-nas-tarefas.md) | Reservar, retirar, declarar e acertar |
| [Relatório de consumo e movimentos](16-inventario/103-relatorio-de-consumo-e-movimentos.md) | Para onde vai o material e quanto custa |
| [Equipamentos: documentos, inspeções e entregas](16-inventario/104-equipamentos-documentos-inspecoes-e-entregas.md) | Documentos de cada máquina, entregas de EPI e relatório para a inspeção |
| [Importar material a partir de um modelo](16-inventario/105-importar-material-a-partir-de-um-modelo.md) | Carregar de uma vez tudo o que há num armazém |
| [Onde está cada equipamento](16-inventario/106-onde-esta-cada-equipamento.md) | Equipamentos livres fora do armazém, recolhê-los e recebê-los |
| [Material sem tarefas: pessoas e locais](16-inventario/107-material-sem-tarefas-pessoas-e-locais.md) | Dar material a uma pessoa ou a um local e declará-lo a partir da jornada |

---

## Estrutura de ficheiros

```
DOCS/Clients-pt/
├── README.md                           (este índice)
├── 01-primeiros-passos/                (5 artigos)
├── 02-funcionarios/                    (10 artigos)
├── 03-controlo-de-horarios/            (11 artigos)
├── 04-calendario-e-horarios/           (11 artigos)
├── 05-gestao-documental/               (9 artigos)
├── 06-tarefas/                         (11 artigos)
├── 07-inteligencia-operacional/        (9 artigos)
├── 08-sucursais-e-entidade/            (6 artigos)
├── 09-notificacoes/                    (6 artigos)
├── 10-aplicacao-movel/                 (7 artigos)
├── 11-relatorios-e-exportacao/         (5 artigos)
├── 12-conformidade-legal/              (4 artigos)
├── 13-apoio-e-incidencias/             (4 artigos)
├── 14-referencia/                      (4 artigos)
├── 15-integracoes/                     (6 artigos)
└── 16-inventario/                      (8 artigos)
```

**Total: 116 artigos**
