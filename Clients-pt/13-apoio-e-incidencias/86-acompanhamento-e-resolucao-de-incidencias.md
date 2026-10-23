# Acompanhamento e resolução de incidências

Depois de criada, a incidência vive em **Contacto**, separador **Incidentes**, do backoffice até ser resolvida. Este artigo descreve os seus estados, como se responde e o que fica registado.

Recorde que as incidências são um canal **interno da sua organização**. Para problemas da plataforma, o canal é o apoio da EncodeBiz: consulte [Contactar o apoio técnico](./87-contactar-o-apoio-tecnico.md).

---

## Estados de uma incidência

| Estado | Significado |
|---|---|
| **Pendente** | Registada, à espera de que alguém a assuma |
| **Em revisão** | Alguém está a investigar o problema. É o estado com que nasce uma incidência criada a partir do backoffice |
| **Resolvida** | O problema foi solucionado. A incidência deixa de admitir respostas |

Não há um estado «encerrada» nem um encerramento automático por tempo: uma incidência permanece aberta até que alguém a marque como resolvida.

### Quem pode alterar o estado

O estado é alterado de duas formas: editando a incidência, ou **ao responder** no seu fio, onde cada resposta pode levar associada uma mudança de estado. Ambas as ações competem aos perfis com acesso ao backoffice: **Owner** e **Manager**.

---

## Responder a uma incidência

O acompanhamento faz-se através de respostas. Cada resposta fica no fio, com o seu autor e a sua data, e pode ainda mover o estado.

1. Aceda a **Contacto** no menu lateral e fique no separador **Incidentes**.
2. Localize a incidência com os filtros de estado, sucursal ou funcionário.
3. Abra o seu detalhe.
4. Prima **Responder**.
5. Escreva a mensagem e, se for o caso, selecione o novo **estado**.
6. Confirme.

> **Importante:** uma incidência no estado *Resolvida* já não admite respostas. Se o problema voltar a surgir, crie uma incidência nova e faça referência à anterior no comentário.

> **Aviso:** não abra uma incidência nova para acrescentar informação a um caso que continua aberto. Use o fio de respostas para manter o contexto agrupado.

---

## Histórico do caso

O detalhe da incidência mostra a exposição inicial e, por baixo, todas as respostas por ordem cronológica, cada uma com o seu autor, a data e a mudança de estado que produziu. A listagem indica também quantas respostas cada incidência acumula, o que permite localizar num relance as que têm mais idas e vindas.

---

## Quando marcar uma incidência como resolvida

Marque-a como resolvida quando tiver verificado que o problema desapareceu e a operação voltou à normalidade. Convém deixar uma última resposta a explicar **o que o causava e o que foi feito**: é isso que transforma o histórico de incidências em algo consultável quando o mesmo sintoma reaparecer meses depois.

Se o mesmo sintoma gerar incidências repetidas, é sinal de uma causa de fundo —uma geocerca mal dimensionada, um calendário que não cobre um turno— que convém atacar na configuração em vez de resolver caso a caso.

---

## Exportar o histórico de incidências

> **Estado: Não disponível**
> A exportação da listagem de incidências para CSV ou PDF não está implementada na versão atual e não tem data planeada.

As incidências consultam-se e filtram-se no ecrã. Se precisar do histórico para uma auditoria, solicite-o ao apoio em hola@encodebiz.com.

---

## Nota de perfil

Este artigo dirige-se a **Owner** e **Manager**, os únicos perfis com acesso ao módulo de incidências no backoffice.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar uma incidência](./85-criar-uma-incidencia.md) | Campos, tipos e criação de uma incidência |
| [Contactar o apoio técnico](./87-contactar-o-apoio-tecnico.md) | Canal com a equipa da EncodeBiz |
| [Problemas frequentes e soluções](./88-problemas-frequentes-e-solucoes.md) | Diagnóstico das situações mais habituais |
| [Códigos de erro completos](../14-referencia/90-codigos-de-erro-completos.md) | Causa e solução de cada código |
