# Solicitar jornada manual

Há situações em que um funcionário não consegue registar a sua assiduidade através da aplicação no momento habitual: uma falha pontual do dispositivo, uma emergência, a ausência de cobertura ou qualquer outra circunstância justificada. Nestes casos, um manager ou supervisor pode criar um registo de assiduidade de forma manual para o funcionário afetado. Este artigo explica como funciona este processo e o que acontece depois de o pedido ser criado.

---

## O que é um pedido de jornada manual

Uma jornada manual é um registo de assiduidade criado por um responsável em nome de um funcionário, com carácter retroativo ou diferido. Ao contrário do registo comum, não exige que o funcionário esteja presente com o seu dispositivo no momento do registo.

O sistema distingue dois modos de criação de jornada manual consoante o contexto em que se encontra a jornada do funcionário:

---

## Modo A — Jornada completa

Utiliza-se quando o funcionário não registou qualquer evento durante a jornada: nem entrada nem saída.

Neste modo, o responsável cria em simultâneo uma **entrada** e uma **saída** para uma data específica. Se o responsável não indicar as horas concretas, o sistema preenche-as automaticamente utilizando as horas do turno do calendário efetivo atribuído ao funcionário para esse dia.

Este modo é adequado para situações como:

- O funcionário trabalhou mas esqueceu-se ou não conseguiu registar em momento algum.
- Regista-se uma assiduidade correspondente a um dia anterior.
- O funcionário esteve presente mas o seu dispositivo não funcionou durante toda a jornada.

---

## Modo B — Apenas saída

Utiliza-se quando o funcionário já tem uma **entrada válida em aberto**: entrou e foi registado corretamente, mas não registou a saída.

Neste modo, o responsável cria apenas a **saída** correspondente para fechar a jornada. A entrada existente não é modificada.

Este modo é o adequado para situações como:

- O funcionário esqueceu-se de registar a saída no fim do turno.
- O funcionário não conseguiu registar a saída por um problema técnico no fim da jornada.
- A jornada aparece no estado `incomplete_workday` e tem de ser fechada.

---

## Como criar uma jornada manual

1. Aceda ao backoffice com perfil **manager** ou **owner**.
2. Navegue até à secção **Assiduidade** ou até ao perfil do funcionário.
3. Selecione a opção **Nova jornada manual** ou **Solicitar jornada manual**.
4. Escolha o funcionário, a sucursal e a data da jornada.
5. Selecione o modo correspondente (jornada completa ou apenas saída).
6. Introduza as horas se quiser especificá-las manualmente, ou deixe que o sistema as complete de acordo com o turno.
7. Indique o motivo do pedido. Este campo é obrigatório e ficará gravado no histórico de auditoria.
8. Confirme o pedido.

---

## O que acontece depois de criar o pedido

Uma vez criada a jornada manual, o sistema realiza automaticamente as seguintes ações:

### Estado inicial: pendente de validação

A jornada manual fica no estado `pending-employee-validation`. Isto significa que o registo existe no sistema mas **não conta como horas trabalhadas até que o funcionário o aceite**. Este mecanismo protege o funcionário face a modificações não autorizadas do seu registo de assiduidade.

### Notificação push ao funcionário

O funcionário recebe uma notificação push no seu dispositivo a informá-lo de que foi criada uma jornada manual em seu nome. A notificação convida-o a rever e a validar ou recusar o registo.

### Validação ou recusa pelo funcionário

O funcionário acede ao ecrã de notificações da aplicação e revê os detalhes da jornada proposta: data, horas, sucursal e motivo indicado pelo responsável.

- Se o funcionário **aceitar**, a jornada passa ao estado `valid` e começa a contar como horas trabalhadas.
- Se o funcionário **recusar**, a jornada fica marcada como `failed` com o motivo da recusa.

---

## Rastreabilidade da jornada manual

Cada pedido de jornada manual fica gravado no histórico de alterações com a seguinte informação:

- Identificador único da entrada.
- Data e hora em que o pedido foi efetuado.
- Ação realizada (`manual_request_created` ou `manual_checkout_created`, consoante o modo).
- UID do utilizador responsável que criou o pedido.
- Dados do estado anterior e do novo estado da jornada.

Este registo é imutável. Não pode ser modificado nem eliminado, o que garante a integridade do histórico perante inspeções do trabalho ou auditorias internas.

---

> **Aviso:** o campo de motivo é obrigatório e fica permanentemente associado ao registo. Indique sempre uma descrição clara e verdadeira da razão que justifica a jornada manual. Este dado pode ser exigido em caso de inspeção do trabalho.

---

## Perfis com acesso a esta funcionalidade

A criação de jornadas manuais está restrita a utilizadores com perfil **manager** ou **owner**. Os funcionários com perfil **funcionário** só podem validar ou recusar as jornadas manuais que lhes sejam atribuídas.

---

## Artigos relacionados

- [Revisão e validação de registos](20-revisao-e-validacao-de-registos.md)
- [Rastreabilidade e histórico de alterações](21-rastreabilidade-e-historico-de-alteracoes.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
