# Códigos de erro completos

Este artigo é a referência dos códigos de erro que podem aparecer na aplicação móvel ou no backoffice do CheckBiz360. Quando o sistema mostra uma mensagem de erro, o código que a acompanha permite identificar a causa exata e a ação corretiva.

Os códigos seguem sempre o formato `módulo/motivo`. Em seguida agrupam-se por módulo.

> **Nota:** se no ecrã aparecer um código que não consta deste artigo, significa que provém de um serviço que ainda não tem uma mensagem traduzida. Anote o código literal e abra-o como incidência: é informação suficiente para o apoio o identificar.

---

## Registo e jornada (`checklog`)

Os erros mais frequentes na utilização diária. Salvo indicação em contrário, são vistos pelo **funcionário na aplicação**.

| Código | O que significa | O que fazer |
|---|---|---|
| `checklog/out_of_radius` | O funcionário não está dentro do raio de registo da sucursal selecionada | Verificar que está fisicamente no local de trabalho e que o GPS tem boa precisão. Se se repetir, rever coordenadas e raio da sucursal |
| `checklog/out_of_schedule` | O registo cai fora do horário do turno atribuído | Rever o horário efetivo e o fuso horário da sucursal, e o turno atribuído ao funcionário |
| `checklog/day_disabled` | O dia está desativado no calendário efetivo (feriado ou dia não útil) | Se o dia devia ser útil, corrigir o calendário. Caso contrário, registar as horas através de jornada manual |
| `checklog/calendar_not_resolved` | Não há calendário efetivo resolvido para essa data | Rever o calendário da entidade, da sucursal e do funcionário para essa data. Entretanto, introduzir as horas manualmente |
| `checklog/branch_geo_required` | A sucursal não tem localização configurada | O Owner ou Manager deve acrescentar as coordenadas da sucursal no backoffice |
| `checklog/two_type_followed` | Tentou-se iniciar a jornada duas vezes seguidas | Fechar a jornada aberta antes de iniciar uma nova |
| `checklog/overlap_detected` | Já existe uma jornada válida que se sobrepõe a esse horário | Rever o histórico do funcionário e corrigir o registo sobreposto antes de tentar de novo |
| `checklog/duplicate_pending` | Já há um pedido pendente para esse funcionário nessa data | Aguardar que o responsável resolva o pedido existente em vez de criar outro |
| `checklog/checkin_not_found` | Não se encontra a entrada de referência para a operação | Verificar que existe o registo de entrada ao qual se pretende associar a saída |
| `checklog/checkin_not_open` | A entrada não pode ser fechada manualmente devido ao seu estado atual | Rever o estado do registo; se já estiver fechado ou anulado, não admite fecho manual |
| `checklog/checkout_already_exists` | Já existe um fecho pendente ou válido para essa entrada | Rever o registo: a jornada já tem saída |
| `checklog/invalid_checki` | Registo de entrada inválido | Tentar de novo o registo. Se persistir, atualizar a aplicação |
| `checklog/invalid_checkout` | Registo de saída inválido | Verificar que há uma entrada aberta para fechar |
| `checklog/invalid_restin` / `checklog/invalid_restout` | Início ou fim de pausa inválido | Verificar a ordem dos registos: a pausa deve abrir-se e fechar-se dentro de uma jornada ativa |
| `checklog/unknown_type` | Tipo de registo desconhecido | Atualizar a aplicação para a última versão |
| `checklog/invalid` | Não se encontra o registo relacionado | Atualizar o ecrã e tentar de novo |
| `checklog/bad_request` | Os dados do registo não estão corretos ou estão incompletos | Atualizar a aplicação; se continuar, reinstalar e iniciar sessão de novo |
| `checklog/internal_error` | Erro interno do servidor ao processar o registo | Tentar de novo passados alguns minutos. Se durar mais de 30 minutos, abrir incidência com a hora exata e o funcionário afetado |

> `checklog/manual_request_created` não é um erro: confirma que o pedido de jornada manual foi enviado corretamente e está pendente de aprovação.

---

## Acesso e sessão (`auth`)

| Código | O que significa | O que fazer |
|---|---|---|
| `auth/invalid-credential` | Credenciais incorretas | Rever correio e palavra-passe; usar a recuperação de palavra-passe se necessário |
| `auth/invalid-email` | O endereço de correio não tem um formato válido | Corrigir o correio introduzido |
| `auth/missing-email` / `auth/missing-password` | Falta o correio ou a palavra-passe | Preencher o campo em falta |
| `auth/email-already-exists` / `auth/email-already-in-use` | Esse correio já está em uso | Iniciar sessão com essa conta ou usar outro correio |
| `auth/weak-password` | A palavra-passe não cumpre os requisitos mínimos | Escolher uma palavra-passe mais segura |
| `auth/too-many-requests` | Demasiadas tentativas em pouco tempo | Aguardar alguns minutos antes de tentar de novo |
| `auth/user-disabled` | A conta está desativada | Contactar o Owner da entidade ou o apoio |
| `auth/operation-not-allowed` | O acesso por correio e palavra-passe não está ativado | Contactar o apoio |
| `auth/network-request-failed` | Erro de rede | Verificar a ligação à internet e tentar de novo |
| `auth/unauthorized` | Acesso não autorizado ao recurso, ou sessão caducada | Terminar sessão e voltar a entrar. Se a conta foi desativada, contactar o Owner |
| `auth/untrusted_device` | O dispositivo não está autorizado e exige verificação adicional | O Owner ou Manager deve autorizar o dispositivo a partir do perfil do funcionário |

---

## Verificação em dois passos (`twofactor`)

| Código | O que significa | O que fazer |
|---|---|---|
| `twofactor/invalid_code` | O código TOTP introduzido não é válido | Verificar que a hora do dispositivo está correta e gerar um código novo |
| `twofactor/invalid_token` | A sessão expirou | Voltar a iniciar sessão |
| `twofactor/not_activated` | O funcionário não tem a verificação em dois passos ativada | Ativá-la a partir do perfil do funcionário |
| `twofactor/user_not_activated` | A conta de utilizador não tem 2FA ativada | Ativar a 2FA a partir do perfil de utilizador |
| `twofactor/unauthorized` | A operação exige um token 2FA | Completar a verificação em dois passos para continuar |
| `twofactor/internal` | Erro interno ao processar a verificação | Tentar de novo; se persistir, abrir incidência |

---

## Funcionários (`employee`) e sucursais (`branch`)

| Código | O que significa | O que fazer |
|---|---|---|
| `employee/not_found` | O funcionário indicado não existe na entidade | Verificar que o funcionário continua registado |
| `employee/exist_employee` | Já existe um funcionário com esse correio ou telefone | Procurar o funcionário existente em vez de criar um novo |
| `employee/branchId_required` | Falta a sucursal, que é obrigatória | Atribuir pelo menos uma sucursal antes de guardar |
| `employee/bad_request` | Falta o identificador do funcionário na operação | Repetir a ação a partir da ficha do funcionário |
| `branch/not_found` | A sucursal indicada não existe | Verificar que a sucursal existe e não foi eliminada |

---

## Documentos (`documents`)

| Código | O que significa | O que fazer |
|---|---|---|
| `documents/unauthorized` | Sem permissões para aceder ao documento | Rever a visibilidade por perfil do documento |
| `documents/not_found` | O documento não existe ou não é visível para esse utilizador | Verificar que não está arquivado e que o perfil tem visibilidade |
| `documents/file_required` | Não foi anexado qualquer ficheiro | Anexar o ficheiro antes de guardar |
| `documents/file_too_large` | O ficheiro ultrapassa o máximo permitido de 10 MB | Comprimir o documento ou dividi-lo |
| `documents/invalid_mime_type` | Formato de ficheiro não permitido | Converter o documento para um formato admitido |
| `documents/invalid_visibility_roles` | A configuração de visibilidade não é válida | Rever os perfis selecionados |
| `documents/invalid_acknowledgement_mode` | A configuração de confirmação de leitura não é válida | Rever o modo de confirmação escolhido face ao âmbito do documento |
| `documents/acknowledgement_not_required` | O documento não exige confirmação de leitura | Não é necessária qualquer ação |
| `documents/acknowledgement_not_allowed` | Esse utilizador não pode confirmar a leitura do documento | Verificar que o documento se dirige a esse funcionário |
| `documents/restricted_document_type` | Sem permissões para esse tipo de documento | Rever o perfil necessário para esse tipo |
| `documents/already_archived` | O documento já está arquivado | Não é necessária qualquer ação |
| `documents/branch_not_found` | A sucursal ou projeto indicado não é válido | Selecionar uma sucursal existente |
| `documents/employee_not_found` | O funcionário indicado não é válido | Selecionar um funcionário existente |
| `documents/employee_not_in_branch` | O funcionário não pertence à sucursal selecionada | Corrigir a sucursal ou a atribuição do funcionário |
| `documents/bad_request` | Os dados do documento não são válidos | Rever os campos obrigatórios do formulário |

---

## Tarefas (`task`)

| Código | O que significa | O que fazer |
|---|---|---|
| `task/not_found` | A tarefa não existe ou foi eliminada | Atualizar a listagem de tarefas |
| `task/evidence_required` | A tarefa exige carregar evidência antes de a concluir | Anexar pelo menos uma foto ou vídeo e voltar a concluir |
| `task/forbidden` | Sem permissões para essa ação sobre a tarefa | Rever o nível de responsabilidade exigido |
| `task/unauthorized` | Sem permissões para realizar a ação | Solicitar a ação a um responsável com nível suficiente |
| `task/invalid_mime_type` | O formato do ficheiro anexado não é permitido | Carregar a evidência como foto ou vídeo num formato padrão |
| `task/file_too_large` | O ficheiro ultrapassa o tamanho máximo permitido | Reduzir a resolução ou a duração do ficheiro |
| `task/bad_request` | A informação da tarefa não é válida | Rever os campos obrigatórios: título, sucursal e prazo |

---

## Subscrição e faturação

| Código | O que significa | O que fazer |
|---|---|---|
| `subscription/limit_off` | O plano atingiu o limite de operações permitidas | Rever o estado da subscrição ou contactar o apoio |
| `suscription/entity_not_configured` | A entidade não tem a configuração necessária para contratar | Completar os dados legais e o método de pagamento em **Entidade** |
| `suscription_checkinbiz/entity_legal_not_configured` | Faltam os dados legais da entidade para o CheckBiz | Completar os dados da empresa antes de contratar |
| `suscription/already_subscribed_into_plan` | A entidade já está subscrita a esse plano | Não é necessária qualquer ação |
| `suscription/ko` | A subscrição não pôde ser concluída | Rever o método de pagamento e tentar de novo |
| `subscribe/not_found` | O serviço indicado não existe | Tentar de novo a partir do ecrã de planos |
| `subscribe/invalid_entity_service` | A entidade ou o serviço não estão corretos | Verificar a entidade selecionada |
| `subscribe/internal` | Erro interno do serviço de subscrições | Tentar mais tarde; se persistir, abrir incidência |
| `sub/bad_request` | Os dados enviados não são válidos | Rever o formulário e tentar de novo |
| `sub/entity_not_found` | A entidade não existe | Verificar a entidade selecionada |
| `payment/pending` | Há pagamentos pendentes na conta | Regularizar o pagamento a partir da secção de faturação |

---

## Outros módulos

| Código | O que significa | O que fazer |
|---|---|---|
| `entity/not_found` | A entidade não existe | Verificar a entidade selecionada no backoffice |
| `user/not_found` | Não há qualquer utilizador com esse correio | Rever o correio introduzido |
| `user/internal` | Erro interno do serviço de utilizadores | Tentar de novo; se persistir, abrir incidência |
| `report/internal_error` | Erro interno ao gerar o relatório | Tentar de novo com um intervalo de datas menor; se persistir, abrir incidência |
| `stats/range_and_groupBy_tolong` | O intervalo de datas ou o agrupamento produzem demasiados dados para representar | Selecionar um intervalo menor ou outro agrupamento |
| `analyze/insufficient_data` | Não há dados suficientes para calcular os indicadores | Aguardar a acumulação de mais histórico de registos e tarefas |
| `media/not_found` | O ficheiro não existe | Voltar a carregar o ficheiro |
| `media/invalid_meda_type` | Tipo de ficheiro não permitido | Usar um formato admitido |
| `media/invalid_dimesions` | As dimensões da imagem não são válidas | Ajustar o tamanho da imagem |
| `media/error` | Erro interno de armazenamento | Tentar de novo; se persistir, abrir incidência |
| `internal` | Erro interno do servidor | Tentar de novo; se persistir, abrir incidência com a hora exata |
| `unavailable` | Serviço temporariamente indisponível | Tentar de novo passados alguns minutos |

---

> **Aviso:** se um mesmo código reaparecer de forma sistemática depois de aplicar a ação corretiva, abra uma incidência no backoffice incluindo o código exato, a hora da falha e o funcionário afetado.

---

## Nota de perfil

Este artigo é de consulta para **Owner** e **Manager**, responsáveis por diagnosticar e resolver erros operacionais. Os funcionários com perfil Worker que vejam um código de erro na aplicação devem comunicá-lo ao seu responsável com o código exato que aparece no ecrã.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Problemas frequentes e soluções](../13-apoio-e-incidencias/88-problemas-frequentes-e-solucoes.md) | Guia prático de diagnóstico para as situações mais habituais |
| [Criar uma incidência](../13-apoio-e-incidencias/85-criar-uma-incidencia.md) | Como abrir um caso de apoio quando o erro não tem solução direta |
| [Glossário](./89-glossario.md) | Definição dos termos técnicos utilizados na plataforma |
| [Contactar o apoio técnico](../13-apoio-e-incidencias/87-contactar-o-apoio-tecnico.md) | Canais e tempos de resposta da equipa de apoio |
