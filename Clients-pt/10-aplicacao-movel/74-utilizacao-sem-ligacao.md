# Utilização sem ligação

O CheckBiz360 foi concebido para funcionar com ligação à internet ativa. As operações críticas da plataforma — em especial o registo de ponto — exigem validação em tempo real com os servidores e não podem ser realizadas sem conectividade. Sem ligação, a aplicação tem uma funcionalidade muito limitada: permite apenas consultar os dados que já estavam carregados na cache do dispositivo durante sessões anteriores.

Este artigo explica o que está disponível sem ligação, o que exige obrigatoriamente conectividade e o que está previsto para versões futuras.

---

## O que funciona sem ligação (apenas consulta de dados em cache)

Quando não há ligação disponível, a aplicação permite consultar a informação que foi descarregada durante sessões anteriores com ligação ativa. Esta informação não é atualizada até que a conectividade seja restabelecida.

### Consultar registos de assiduidade já descarregados

Pode rever o histórico de registos que foi carregado na última sessão com ligação. A informação mostrada corresponde ao último estado sincronizado; não verá alterações posteriores a essa sincronização.

### Consultar documentos previamente descarregados

Os documentos laborais que já abriu ou descarregou enquanto tinha ligação (recibos de vencimento, contratos ou outros ficheiros da secção de documentos) permanecem disponíveis para consulta sem ligação.

### Consultar tarefas descarregadas

As tarefas que foram carregadas durante a última sessão com ligação podem ser consultadas. Poderá ver o detalhe de cada tarefa, os seus anexos descarregados e o seu estado no momento da última sincronização.

---

## O que NÃO funciona sem ligação

As seguintes funções exigem obrigatoriamente ligação à internet e não estão disponíveis em modo sem ligação:

### Efetuar registos

O registo (entrada, saída e pausas) exige ligação no momento em que é executado. O sistema precisa de validar em tempo real a sua identidade, a sua localização GPS em relação à geocerca do local, o estado do seu turno ativo e as regras de dispositivo autorizado. Nenhuma destas validações pode ser feita sem conectividade.

> **Aviso:** se tentar efetuar um registo sem ligação, a aplicação informá-lo-á de que não é possível concluir a operação. Não existe uma fila de registos pendentes: a marca temporal do registo deve corresponder ao momento real em que ocorre, e as validações não podem ser adiadas.

### Descarregar novos documentos

Se a sua organização publicar um documento enquanto não tem ligação, não o poderá descarregar nem visualizar até recuperar o acesso à internet.

### Sincronizar alterações em tarefas

As mudanças de estado de tarefas (marcar como concluída, atualizar progresso) exigem ligação para serem transmitidas ao servidor. Se atualizar uma tarefa sem ligação, a alteração pode ficar guardada localmente mas não será visível para o seu manager até que sincronize.

### Iniciar sessão pela primeira vez no dispositivo

O processo de autenticação inicial exige sempre ligação para verificar as credenciais. Se nunca tiver iniciado sessão nesse dispositivo, não poderá aceder à aplicação sem conectividade.

---

## Modo offline com fila de sincronização

> **Estado: Planeado**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

Numa versão futura, o CheckBiz360 incorporará um modo offline robusto com fila de sincronização que permitirá registar entradas e saídas sem ligação para as enviar ao servidor assim que a conectividade for restabelecida. Este modo incluirá a validação diferida das condições do registo (geocerca, dispositivo, horário) e mecanismos de resolução de conflitos. Por agora, o registo exige ligação ativa no momento em que é executado.

---

## Sincronização ao recuperar a ligação

Quando o CheckBiz360 deteta que a ligação foi restabelecida, realiza automaticamente uma sincronização em segundo plano para atualizar os dados em cache. Não é necessária qualquer ação manual; a aplicação fá-lo assim que deteta conectividade.

---

## Recomendações para ambientes com conectividade intermitente

Se trabalha em ambientes onde a ligação não é estável, tenha em conta o seguinte:

1. **Efetue os seus registos assim que tiver ligação.** Não espere: se tiver sinal suficiente, registe de imediato.
2. **Abra os documentos com antecedência.** Se souber que precisará de consultar um documento, abra-o quando tiver ligação para que fique em cache.
3. **Reveja as tarefas antes de perder a ligação.** Carregue a listagem quando tiver ligação para ter a informação disponível depois.
4. **Ative o WiFi quando estiver disponível.** Uma ligação WiFi estável é preferível a dados móveis em ambientes com cobertura flutuante.
5. **Comunique os problemas de conectividade ao seu manager.** Se os problemas de ligação afetarem de forma recorrente os seus registos, informe o seu manager para que fique constância e possa gerir os registos manualmente.

> **Aviso:** se num dia não conseguiu efetuar qualquer registo por problemas de conectividade, deve informar o seu manager e solicitar a criação de uma jornada manual a partir da secção «Os meus registos». Consulte o artigo sobre registos de assiduidade para conhecer o procedimento completo.

---

## Nota de perfil

Este artigo dirige-se a **funcionários** que utilizam a aplicação em ambientes onde a conectividade pode ser limitada ou intermitente.

---

## Artigos relacionados

- [Os meus registos de assiduidade](73-os-meus-registos-de-assiduidade.md)
- [Navegação principal da aplicação](71-navegacao-principal-da-aplicacao.md)
- [Atualizações da aplicação](75-atualizacoes-da-aplicacao.md)
