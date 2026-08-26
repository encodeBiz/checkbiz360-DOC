# Problemas frequentes e soluções

Este artigo reúne as doze situações técnicas e operacionais mais habituais no CheckBiz360, juntamente com os passos de diagnóstico e resolução recomendados. Consulte este guia antes de abrir uma incidência, uma vez que a maioria destes problemas tem solução direta sem necessidade de intervenção da equipa de apoio.

---

## 1. O funcionário não consegue registar (erro genérico)

**Sintoma:** o funcionário prime o botão de registo na aplicação e aparece uma mensagem de erro sem código específico, ou a operação não se conclui.

**Passos de resolução:**

1. Verifique que o dispositivo tem ligação à internet ativa (Wi-Fi ou dados móveis). Sem ligação, o registo não pode ser processado.
2. Confirme que o GPS do dispositivo está ativado. Aceda às definições do sistema operativo e confirme que a localização está ativada para o CheckBiz360.
3. Verifique que a aplicação tem permissões de localização concedidas: em iOS, vá a **Definições > CheckBiz360 > Localização** e selecione «Ao usar a aplicação». Em Android, aceda a **Definições > Aplicações > CheckBiz360 > Permissões > Localização**.
4. Feche a aplicação completamente e volte a abri-la.
5. Se o problema persistir, atualize a aplicação para a versão mais recente a partir da loja de aplicações.

---

## 2. Erro «Fora de zona» persistente

**Sintoma:** o funcionário recebe o erro `checklog/out_of_radius` de forma repetida mesmo quando se encontra fisicamente no local de trabalho.

**Passos de resolução:**

1. No backoffice, aceda a **Sucursais** e selecione a sucursal afetada.
2. Confirme as coordenadas da sucursal: verifique que a latitude e a longitude registadas correspondem ao ponto exato do estabelecimento e não a uma morada aproximada ou incorreta.
3. Reveja o raio de registo configurado para a sucursal. Se o edifício ou o ambiente tiverem sinal GPS impreciso (pisos interiores, caves, zonas com interferências), pondere alargar o raio.
4. Peça ao funcionário que verifique a precisão de GPS do seu dispositivo: no exterior, a precisão costuma ser de 5 a 15 metros; no interior pode ultrapassar os 50 metros.
5. Se o problema afetar todos os funcionários da sucursal, verifique se as coordenadas foram modificadas recentemente de forma acidental.

---

## 3. O funcionário não recebe o correio de boas-vindas

**Sintoma:** um funcionário recém-criado na plataforma não recebeu o correio de convite com as suas credenciais de acesso.

**Passos de resolução:**

1. Peça ao funcionário que verifique a pasta de correio não solicitado ou spam.
2. Confirme no backoffice, dentro do perfil do funcionário, que o endereço de correio eletrónico está escrito corretamente (sem espaços, sem erros de escrita).
3. Se o endereço estiver correto e o correio não aparecer em nenhuma pasta, aceda ao perfil do funcionário e prima **Reenviar convite**.
4. Se depois de reenviar o correio continuar a não chegar, verifique com o funcionário se a sua empresa tem filtros de correio empresarial que possam estar a bloquear as mensagens de @encodebiz.com. Nesse caso, será necessário adicionar esse domínio à lista de remetentes permitidos.

---

## 4. A aplicação não abre ou fecha sozinha

**Sintoma:** a aplicação CheckBiz360 fecha de forma inesperada ao abrir ou durante a sua utilização normal.

**Passos de resolução:**

1. Verifique que a versão instalada é a mais recente: aceda à App Store ou à Google Play e atualize se houver uma versão disponível.
2. Reinicie o dispositivo completamente e volte a tentar abrir a aplicação.
3. Se o problema persistir após a atualização, desinstale a aplicação e volte a instalá-la a partir da loja oficial.
4. Depois de reinstalar, inicie sessão com as mesmas credenciais. Os dados do servidor não se perdem com a reinstalação.
5. Se a aplicação continuar a fechar, anote o modelo do dispositivo e a versão do sistema operativo e inclua esta informação ao abrir uma incidência.

---

## 5. Erro «Dispositivo não autorizado»

**Sintoma:** o funcionário recebe a mensagem de erro `auth/untrusted_device` ao tentar iniciar sessão ou registar a partir de um dispositivo novo.

**Passos de resolução:**

1. Aceda ao backoffice com a sua conta de Owner ou Manager.
2. Vá ao perfil do funcionário afetado.
3. Na secção **Dispositivos de confiança**, localize o novo dispositivo (aparecerá listado com o seu identificador).
4. Prima **Autorizar dispositivo** para o marcar como de confiança.
5. Informe o funcionário de que pode voltar a tentar iniciar sessão.

> **Aviso:** reveja a lista de dispositivos de confiança do funcionário e retire os que já não usa. Um dispositivo antigo que continua autorizado é uma via aberta para registar em nome dessa pessoa.

---

## 6. O funcionário não consegue ver os seus documentos

**Sintoma:** um funcionário indica que não encontra na aplicação os documentos que deveriam estar disponíveis para ele.

**Passos de resolução:**

1. Aceda ao backoffice e vá ao módulo **Documentos**.
2. Localize o documento em causa e verifique a sua configuração de visibilidade.
3. Reveja a **visibilidade por perfil** do documento: se não incluir o perfil do funcionário, este não o verá.
4. Verifique o **âmbito** e o destinatário: se for de funcionário, que seja o correto; se for de sucursal, que o funcionário lhe pertença —caso contrário o sistema responde `documents/employee_not_in_branch`.
5. Confirme que o documento não está **arquivado**: os arquivados deixam de ser mostrados.
6. Se a configuração estiver correta, peça ao funcionário que termine sessão na aplicação e volte a iniciá-la para forçar a sincronização.

---

## 7. A notificação push não chega

**Sintoma:** o funcionário não recebe notificações de tarefas, documentos ou alertas do sistema no seu dispositivo.

**Passos de resolução:**

1. Verifique que o funcionário concedeu permissões de notificação ao CheckBiz360. Em iOS: **Definições > CheckBiz360 > Notificações** e ativar «Permitir notificações». Em Android: **Definições > Aplicações > CheckBiz360 > Notificações** e ativar.
2. Confirme que o modo «Não incomodar» ou qualquer perfil de silêncio não está ativo no dispositivo.
3. Nalguns dispositivos Android com gestão agressiva de bateria (Xiaomi, Huawei, OnePlus), é necessário excluir o CheckBiz360 da otimização de bateria. Aceda a **Definições > Bateria > Otimização de bateria** e exclua a aplicação.
4. Certifique-se de que a aplicação está atualizada para a última versão.
5. Se o problema persistir, o funcionário pode terminar sessão e voltar a iniciá-la para registar de novo o token de notificações.

---

## 8. O histórico de assiduidade mostra lacunas

**Sintoma:** no histórico de um funcionário aparecem dias ou jornadas sem registos completos, embora o funcionário garanta ter trabalhado nesses dias.

**Passos de resolução:**

1. Aceda ao backoffice e reveja o detalhe de assiduidade do funcionário na data afetada.
2. Verifique se há um registo de entrada sem a saída correspondente. Isto gera uma jornada incompleta (`incomplete_workday`).
3. Se o funcionário se esqueceu de registar a saída, utilize a opção de **Jornada manual** para completar o registo retroativamente.
4. Verifique se o funcionário tem jornadas com pausas (`restin` / `restout`) por fechar, que também podem provocar registos incompletos.
5. Verifique se nessas datas havia jornadas desativadas no calendário efetivo da sucursal.

---

## 9. As horas calculadas não coincidem com as esperadas

**Sintoma:** o total de horas trabalhadas que a plataforma mostra para um funcionário não coincide com o cálculo manual que o manager faz.

**Passos de resolução:**

1. Verifique a **modalidade de jornada** do calendário aplicável. Com jornada estrita, o tempo trabalhado fora da faixa oficial não é contabilizado; com jornada flexível, é somado. É a causa mais frequente de as horas do relatório não baterem certo com as horas brutas dos registos.
2. Verifique se há pausas registadas que estejam a ser descontadas do tempo total.
3. Confirme se alguma jornada está marcada como incompleta, o que pode excluí-la do cálculo total.
4. Verifique o fuso horário configurado na sucursal e confronte-o com o fuso horário do dispositivo do funcionário.
5. Se detetar uma discrepância sistemática, aceda à configuração da sucursal e reveja as regras de cálculo de jornada.

---

## 10. A aplicação mostra «Fora de horário» quando o funcionário está no seu turno

**Sintoma:** o funcionário recebe o erro `checklog/out_of_schedule` embora garanta que está a registar dentro do seu horário habitual.

**Passos de resolução:**

1. Aceda ao backoffice e reveja o **horário efetivo** da sucursal para o dia em causa.
2. Verifique o fuso horário configurado na sucursal. Se o fuso horário estiver incorreto, os limites do turno podem estar a ser calculados com um desfasamento de horas.
3. Confirme que o funcionário tem atribuído o turno correto para esse dia no calendário efetivo.
4. Verifique se existem exceções ou feriados configurados que possam estar a desativar o turno.
5. Se o horário parecer correto, verifique se há uma margem de tolerância de registo configurada e se o funcionário estava a tentar registar mesmo no limite ou fora dele.

---

## 11. O funcionário aparece como inativo no backoffice

**Sintoma:** ao consultar a lista de funcionários, um deles aparece com estado inativo embora devesse estar ativo.

**Passos de resolução:**

1. Aceda ao perfil do funcionário no backoffice.
2. Reveja o campo **Estado do perfil**. Se estiver definido como «Inativo», prima **Reativar funcionário**.
3. Confirme que a conta não foi desativada em consequência de uma baixa temporária ou de um processo de saída iniciado por erro.
4. Verifique que a subscrição da entidade está ativa e sem pagamentos pendentes. Não há limite de funcionários por plano —a faturação é por funcionário e mês—, mas uma subscrição com incidências de cobrança pode bloquear operações.

---

## 12. Não é possível gerar o relatório de um período anterior

**Sintoma:** ao tentar gerar um relatório para um intervalo de datas passado, o sistema devolve um erro ou não mostra dados.

**Passos de resolução:**

1. Verifique que o intervalo de datas selecionado não ultrapassa o período de retenção de dados incluído no seu plano de subscrição.
2. Confirme que o seu perfil tem permissões para gerar relatórios do tipo selecionado. Os relatórios de custos e de anomalias estão restritos a Owner e Manager.
3. Certifique-se de que os filtros aplicados (sucursal, funcionário) não excluem todos os registos disponíveis para esse período.
4. Se o problema persistir com um intervalo de datas que deveria estar dentro do período de retenção, abra uma incidência com o intervalo exato que está a tentar consultar.

---

> **Aviso:** se algum dos passos anteriores não resolver o problema, não repita a mesma ação várias vezes. Recolher evidências (capturas de ecrã, código de erro, data e hora exatas) e abrir uma incidência é sempre mais eficaz do que tentar forçar uma solução que pode agravar o problema.

---

## Nota de perfil

Este artigo dirige-se principalmente a **Owner** e **Manager**, que são os responsáveis por diagnosticar e resolver os problemas operacionais das suas equipas. Os funcionários com perfil Worker que tenham algum destes problemas devem comunicá-lo ao seu Manager.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma incidência](./85-criar-uma-incidencia.md) | Como abrir formalmente um caso de apoio |
| [Contactar o apoio técnico](./87-contactar-o-apoio-tecnico.md) | Canais e tempos de resposta da equipa de apoio |
| [Códigos de erro completos](../14-referencia/90-codigos-de-erro-completos.md) | Referência completa de todos os códigos de erro do sistema |
| [Solicitar jornada manual](../03-controlo-de-horarios/19-solicitar-jornada-manual.md) | Como corrigir um registo incorreto ou em falta |
| [Gestão de dispositivos de confiança](../02-funcionarios/10-biometria-e-dispositivos-de-confianca.md) | Como autorizar novos dispositivos a partir do backoffice |
