# Planos, preços e funcionalidades do CheckBiz360

O CheckBiz360 é contratado como subscrição a partir do backoffice. Este artigo descreve os planos disponíveis, o preço de cada um, o período experimental e que funcionalidades a plataforma inclui na versão atual.

---

## Planos disponíveis

O CheckBiz360 é oferecido em dois planos:

| Plano | Preço | Para quem |
|---|---|---|
| **Bronze** | **Desde 2 €/funcionário por mês** | Empresas que precisam de cumprir o registo de horários e gerir a sua operação diária. É o plano completo da plataforma. |
| **Empresarial** | **Preço à medida** | Organizações grandes (indicativamente, a partir de 100 funcionários) ou que precisam de integrações com os seus próprios sistemas e de apoio preferencial. |

O preço do plano Bronze é **por funcionário e mês**: é faturado consoante os funcionários registados, sem quota fixa de entrada nem custo de implementação. O plano Empresarial é acordado com a equipa comercial em função do volume e das integrações necessárias.

> **Período experimental:** a primeira subscrição inclui **45 dias de experiência**. A experiência não se aplica a subscrições posteriores da mesma entidade.

Para condições concretas (volume, faturação anual, integrações à medida, períodos de fidelização associados a um desenvolvimento específico), escreva para **hola@encodebiz.com**.

---

## O que a subscrição inclui

Ambos os planos dão acesso à plataforma completa: os módulos descritos em seguida estão disponíveis no backoffice e na aplicação móvel desde o primeiro dia.

### Controlo de horários e registos

- Registo de entrada e saída a partir da aplicação móvel (iOS e Android), com validação de geolocalização (geocerca configurável por sucursal), horário e dispositivo.
- Verificação biométrica e dispositivos de confiança, configuráveis por funcionário.
- Pausas e descansos (`restin` / `restout`) com desconto automático configurável.
- Registo em teletrabalho.
- Validação do funcionário através de QR, configurável por sucursal.
- Pedido de jornada manual com aprovação do responsável, e histórico de alterações imutável.

### Gestão de funcionários

- Criação, edição e desativação de funcionários, com estados laborais: ativo, inativo, férias, baixa médica, licença sem vencimento, licença de paternidade e licença de maternidade.
- Quatro níveis de responsabilidade: Owner, Manager, Supervisor e Worker.
- Funcionários internos e colaboradores externos.
- Verificação em dois passos (2FA), biometria e gestão de dispositivos de confiança.
- Funcionários atribuídos a várias entidades, com seletor de entidade ao iniciar sessão.
- Importação de funcionários a partir de CSV no arranque.

### Sucursais e entidade

- Criação e configuração de sucursais com coordenadas, raio de registo e fuso horário próprio.
- Configuração por sucursal: zona de verificação, horário semanal, pausas e modalidade de jornada.
- Herança de configuração em cascata: entidade → sucursal → funcionário.
- Gestão de várias entidades a partir da mesma conta.

### Calendário e horários

- Horários base com um ou vários turnos por dia e descansos dentro do turno.
- Calendário laboral com feriados, ausências e exceções, aplicáveis a entidade, sucursal ou funcionário.
- Jornada estrita ou flexível e descanso estrito ou flexível, que decidem como se contabilizam horas e pausas.
- Predefinições de calendário para replicar um horário em várias sucursais.

### Tarefas

- Criação, atribuição e acompanhamento de tarefas operacionais, com sucursal, prazo e data prevista de início.
- Descrição com formatação: listas, listas de tarefas (checklists), títulos e ligações.
- Quatro prioridades: baixa, média, alta e crítica.
- Evidências de foto e vídeo, notas tipificadas, validação e avaliação pelo responsável.
- Aviso automático se uma tarefa não tiver sido iniciada a tempo.

### Documentos

- Carregamento de documentos laborais (recibos de vencimento, contratos, comunicados, políticas, protocolos, prevenção de riscos e outros tipos).
- Âmbito por entidade, sucursal ou funcionário, e visibilidade por perfil.
- Confirmação de leitura do funcionário, com controlo de versão do documento.
- Arquivo lógico: os documentos arquivados deixam de ser mostrados mas são conservados.

### Incidências

- Abertura e acompanhamento de incidências a partir do backoffice e da aplicação.
- Tipos: registo de jornada, registo de descansos, configuração e outros.
- Estados: pendente, em revisão e resolvida, com fio de respostas.

### Relatórios

- Relatório de assiduidade em **PDF ou Excel (XLSX)**, filtrável por sucursal, funcionário e período.
- Relatório de tarefas em **Excel (XLSX)**, filtrável por sucursal, estado e período de vencimento.
- Relatório de conformidade com o RDL 8/2019 para inspeções.

### Inteligência operacional

- Painel de Operação por período mensal, com três vistas: sucursais, funcionários e análise.
- Três índices sobre o histórico: fiabilidade, efeito do local e dependência da operação.
- Avaliação operacional por funcionário, com sinal de candidato a promoção.
- Análise de custos a partir da tarifa horária configurada por funcionário.
- Deteção de registos com padrões anómalos.

### Assistente de IA (Merlin)

O CheckBiz360 inclui um assistente de inteligência artificial que interpreta os dados operacionais e os converte num relato acionável. Está disponível no painel operacional, no detalhe de sucursal e no detalhe de funcionário.

O assistente **narra e prioriza sobre os números que o ecrã já mostra**: não recalcula nem gera dados próprios, de forma que a sua leitura nunca pode contradizer os painéis.

---

## Diferenças entre Bronze e Empresarial

O plano Empresarial inclui tudo o do plano Bronze e acrescenta:

| | Bronze | Empresarial |
|---|---|---|
| Módulos da plataforma | Todos | Todos |
| Apoio | Padrão, com tempos de resposta definidos | Preferencial, por canais prioritários |
| Integrações por webhook | — | Incluídas |
| Integrações com ERP/CRM e desenvolvimentos à medida | — | Sob acordo |
| Preço | Desde 2 €/funcionário por mês | À medida |

> **Nota:** as integrações à medida são orçamentadas à parte e podem ter associado um período de fidelização pelo trabalho de arranque. A equipa comercial detalha-o em cada caso.

---

## Funcionalidades em desenvolvimento (roadmap)

As seguintes funcionalidades estão planeadas e **não** estão disponíveis na versão atual:

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

- **Assinatura eletrónica** de documentos a partir da aplicação móvel.
- **Histórico automático de versões** de documentos.
- **Descarga em massa de documentos** num único ficheiro.
- **Relatórios automáticos por email**: envio programado dos relatórios já disponíveis.
- **Preferências de notificação configuráveis** por funcionário ou sucursal.
- **Estado «vencida» automático em tarefas**: hoje o vencimento reflete-se no indicador de cumprimento temporal, e não como mudança de estado da tarefa.
- **Turnos rotativos com alternância automática**: hoje cobrem-se com uma sucursal por turno ou com horário próprio do funcionário.
- **Exportação do diretório de funcionários**: a importação a partir de CSV está disponível.
- **Modo offline com sincronização**: registar entradas e saídas sem ligação e sincronizá-las ao recuperá-la.
- **Alertas de custo configuráveis** por limiar.
- **Anexos de tipo documento em tarefas** (PDF, Word, Excel): hoje as evidências admitem foto e vídeo.

---

## Como contratar ou mudar de plano

Antes de contratar, a entidade deve ter completos os **dados legais** e um **método de pagamento**. O backoffice avisa se faltar algum dos dois e liga diretamente ao ecrã correspondente.

1. Inicie sessão no backoffice com a sua conta de Owner.
2. Aceda a **Entidade** no menu lateral e complete os **Dados da Empresa** e os **Métodos de pagamento**.
3. Vá ao ecrã de planos do CheckBiz.
4. Reveja o plano atual e as opções disponíveis.
5. Selecione o plano e complete o processo de pagamento.
6. Os módulos ficam disponíveis de imediato ao concluir o processo.

Para **cancelar**, use a opção de cancelar subscrição no cartão do plano ativo. A subscrição permanece ativa até à data de cancelamento que o próprio cartão mostra; o serviço não é interrompido no momento em que o cancelamento é pedido.

> **Aviso:** a mudança para um plano superior é aplicada de imediato. Os dados gerados não são eliminados ao mudar de plano.

---

## Nota de perfil

A gestão da subscrição é exclusiva do **Owner** da entidade. Os Managers e os restantes perfis não têm acesso ao ecrã de subscrição.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Perguntas frequentes](./92-perguntas-frequentes.md) | Respostas às dúvidas mais habituais sobre o CheckBiz360 |
| [Glossário](./89-glossario.md) | Definição dos termos utilizados na plataforma |
| [Relatório de conformidade legal](../11-relatorios-e-exportacao/79-relatorio-de-conformidade-legal.md) | O relatório para o RDL 8/2019 e a Inspeção do Trabalho |
| [O que é o módulo documental](../05-gestao-documental/30-o-que-e-o-modulo-documental.md) | Primeiros passos no módulo de documentos |
| [O que é a inteligência operacional](../07-inteligencia-operacional/49-o-que-e-a-inteligencia-operacional.md) | Como funciona o módulo de análise |
