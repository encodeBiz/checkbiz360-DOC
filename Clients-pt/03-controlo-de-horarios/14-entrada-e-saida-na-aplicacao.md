# Entrada e saída na aplicação

A aplicação móvel do CheckBiz360 é o ponto de entrada principal para o registo de assiduidade. Este artigo explica passo a passo como efetuar um registo de entrada e um registo de saída a partir da aplicação, que informação mostra o ecrã principal de assiduidade e como interpretar as mensagens de erro mais habituais.

Se parte da sua equipa não quer registar o ponto com o telemóvel, o [ponto de registo](113-ponto-de-registo.md) é um dispositivo fixo no local onde cada pessoa regista com o seu QR ou o seu código.

---

## O ecrã principal de assiduidade

Ao abrir a aplicação e selecionar a entidade de trabalho, o funcionário acede ao ecrã de assiduidade. Este ecrã mostra em tempo real:

- **Estado atual:** se o funcionário está dentro ou fora da sua jornada ativa.
- **Hora do último registo:** a hora exata do último evento registado (entrada, saída ou pausa).
- **Sucursal ativa:** o nome e a localização da sucursal atribuída a esse turno.
- **Tipo de registo disponível:** a aplicação mostra apenas a ação que corresponde ao estado atual. Se o funcionário não registou a entrada, aparece o botão de entrada. Se já registou a entrada, aparece o botão de saída ou de pausa consoante o caso.

Este ecrã atualiza-se automaticamente sempre que ocorre uma mudança de estado.

---

## Como efetuar um registo de entrada

1. Abra a aplicação CheckBiz360 no seu dispositivo móvel.
2. Inicie sessão com as suas credenciais, se ainda não o tiver feito.
3. Selecione a entidade de trabalho correspondente.
4. No ecrã de assiduidade, prima o botão **Registar entrada**.
5. Se o seu dispositivo exigir verificação biométrica, confirme a sua identidade com impressão digital ou reconhecimento facial quando o sistema o solicitar.
6. A aplicação pedirá permissão de localização se ainda não a tiver concedido. Tem de conceder esta permissão para que a validação de geocerca funcione corretamente.
7. O sistema processa o registo. Em poucos segundos, o ecrã mostrará a confirmação da entrada com a hora gravada.

Se o registo estiver correto, o estado do ecrã muda para «Dentro da jornada» e é apresentada a hora de entrada.

---

## Como efetuar um registo de saída

1. No ecrã de assiduidade, prima o botão **Registar saída**.
2. Confirme a ação, se o sistema o solicitar.
3. Se tiver a verificação biométrica ativada, complete a autenticação.
4. O sistema processa o registo de saída. O ecrã mostrará a confirmação com a hora de saída e o tempo total trabalhado na jornada.

### Avisos antes de fechar a jornada

**A partir da versão 1.6.0 da aplicação**, se algo não bater certo a aplicação di-lo antes de registar e deixa a pessoa decidir. O aviso aparece logo no início, antes de pedir localização ou biometria, e sempre com duas saídas: **Cancelar** ou **Terminar jornada**.

Avisa em dois casos:

- **O turno ainda não terminou.** Aparece quando faltam mais de 30 minutos para o fim do turno que está a ser feito. Em jornada partida mede-se contra o turno atual, não contra o fim do dia: sair às 13:00 com turno das 9 às 13 não avisa. Sem horário configurado para esse dia, também não.
- **Participa em tarefas que continuam em curso.** Só contam as tarefas próprias, não as da equipa. A aplicação não as pausa nem as fecha: uma tarefa pode ter vários atribuídos e os restantes podem continuar a trabalhar nela.

Nenhum dos dois impede o registo. Estão lá para que ninguém feche a jornada sem querer, não para bloquear quem sabe o que está a fazer.

> **Importante:** o registo de saída fecha a jornada ativa. Se se esquecer de registar a saída, a jornada ficará no estado `incomplete_workday` até que um responsável a corrija manualmente ou o funcionário a resolva a partir do ecrã de notificações.

---

## Mensagens de erro no ecrã

A aplicação mostra mensagens específicas quando o registo não pode ser processado corretamente. Descrevem-se em seguida as mais habituais:

### Fora de zona

Aparece quando o dispositivo está fora do raio de registo definido para a sucursal. A aplicação pode mostrar a distância aproximada ao ponto de registo autorizado.

**O que fazer:** verifique que se encontra nas instalações corretas. Se trabalha habitualmente nessa localização e o erro se repete, comunique-o ao seu responsável para que reveja a configuração do raio.

### Fora de horário

Aparece quando a tentativa de registo é feita fora do turno ativo do funcionário.

**O que fazer:** reveja o turno que lhe foi atribuído na secção de horários da aplicação. Se considerar que o registo está correto, solicite ao seu responsável uma jornada manual.

### Dispositivo não autorizado

Aparece quando o dispositivo a partir do qual se tenta registar não está registado como dispositivo de confiança e o funcionário tem ativada a autenticação de duplo fator.

**O que fazer:** contacte o seu responsável ou o administrador do sistema para registar o dispositivo atual como dispositivo de confiança.

---

## Disponibilidade do registo no backoffice

O registo fica disponível no backoffice de imediato, sem necessidade de sincronização manual. O responsável pode ver o registo em tempo real a partir do painel de assiduidade.

Tanto os registos válidos como os falhados ficam guardados e são visíveis no histórico de assiduidade do funcionário. Os registos falhados incluem o código de erro e os dados técnicos da tentativa (hora, coordenadas, distância ao raio).

---

> **Nota para responsáveis:** se um funcionário reportar um erro persistente ao registar, aceda ao histórico de assiduidade a partir do backoffice e reveja o código de erro do registo falhado. Isto permitir-lhe-á identificar se o problema é de configuração (raio, horário, dispositivo) ou se exige uma correção manual.

---

## Perfis com acesso a esta funcionalidade

O registo de entrada e saída a partir da aplicação é uma ação disponível para todos os utilizadores com perfil **funcionário**. A revisão de registos no backoffice está disponível para os perfis **manager** e **owner**.

---

## Artigos relacionados

- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Pausas e descansos](17-pausas-e-descansos.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Ponto de registo](113-ponto-de-registo.md) — para quem não regista o ponto com o telemóvel
