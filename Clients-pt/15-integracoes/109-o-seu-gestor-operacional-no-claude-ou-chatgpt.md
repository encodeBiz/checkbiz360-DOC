# O seu gestor operacional no Claude ou no ChatGPT

Montar a semana, dar entrada às pessoas novas, saber quem não picou o ponto esta manhã e quem o pode substituir: é o trabalho que consome as tardes de quem gere a operação. Se já usa o Claude ou o ChatGPT, pode delegar-lho. Ligue o CheckBiz360 ao seu assistente e peça-lhe as coisas nas suas próprias palavras: ele fá-las no CheckBiz360 com as suas permissões, mostra-lhe o que vai fazer e não guarda nada até que diga que sim.

---

## O que resolve

- **«Como está a correr o dia?»** Quem picou o ponto, quem não, quem chegou tarde e que tarefas não começaram à hora, centro a centro, a começar pelo que pede atenção.
- **«A Lúcia não picou o ponto, quem pode cobrir o serviço das dez?»** O assistente diz-lhe quem está livre a essa hora, quem poderia com reservas e quem não está, e faz a mudança quando escolher.
- **«Monta a semana da equipa do Norte igual à anterior, mas a Marta folga na quinta.»** Prepara a semana inteira, mostra-lha e aplica-a quando confirmar.
- **«Dá entrada a estas doze pessoas e a estes três centros.»** Cole a lista que a contabilidade lhe enviou, um Excel ou uma fotografia: o assistente lê-a, diz-lhe o que vai criar e cria.
- **«Estamos melhor ou pior do que no mês passado?»** Compara semanas, custos e alertas, e tira-lhe o relatório de jornada de que precisar.

Faz tudo isto com as permissões de quem liga: nem mais nem menos do que essa pessoa pode fazer no painel.

---

## Como funciona, em três passos

| Passo | O que acontece |
|---|---|
| **1. Ligar** | Uma única vez, com um endereço que serve para todas as suas empresas. Demora dois minutos. |
| **2. Pedir** | No Claude ou no ChatGPT, com as suas palavras: «como está o dia?», «monta», «muda», «dá entrada», «quem…?». |
| **3. Rever e confirmar** | O assistente mostra o que vai fazer. Só o aplica quando diz que sim. |

---

## 1. Ligar

Use este endereço de ligação. É o mesmo para todas as empresas que administra:

```
https://api.checkbiz360.com/api/v1/assistant/mcp
```

**No Claude**

1. Abra **Definições → Conectores** e carregue em **Adicionar conector personalizado**.
2. Escreva um nome (por exemplo, *CheckBiz360*), cole o endereço e carregue em **Adicionar**.
3. Carregue em **Ligar**, entre com o seu utilizador do CheckBiz360 e o seu código de verificação, e autorize o acesso.

**No ChatGPT**

1. Abra **Definições → Aplicações e conectores** e carregue em **Criar**. Se não aparecer, ative antes o modo de programador em **Definições avançadas**.
2. Escreva um nome, cole o endereço como URL do servidor, escolha a autenticação **OAuth** e confirme.
3. Entre com o seu utilizador do CheckBiz360 e o seu código de verificação, e autorize o acesso.

Ao autorizar verá a lista de empresas a que terá acesso: as que administra. Se mais tarde lhe derem acesso a outra, o assistente vê-a sem voltar a ligar; se lho retirarem, deixa de a ver.

> **Se já tinha ligado uma empresa com o seu endereço próprio** (o que aparece em **Ambiente de trabalho**, na configuração da empresa), continua a funcionar para essa empresa. Para trabalhar com todas a partir de um mesmo conector, adicione o endereço acima.

> **Antes de começar:** precisa da verificação em dois passos ativada e de ser proprietário ou administrador de pelo menos uma empresa. Se ao ligar não o deixar entrar, é quase sempre uma dessas duas coisas.

---

## 2. Com que empresa trabalha

Se administra mais do que uma empresa, o assistente pergunta-lhe no início com qual quer trabalhar. A partir daí:

- **Diz sempre a empresa** quando lhe propõe uma mudança, para que não haja dúvidas.
- **Não mistura empresas** numa mesma ação.
- **Para mudar**, diga-lho: «agora na Limpezas Sul». Pode ter duas conversas abertas com empresas diferentes sem que se atrapalhem.

---

## 3. O que lhe pode pedir

Não é preciso aprender nenhum comando. Conte o que precisa como o contaria a alguém da sua equipa.

### Saber como está a correr o dia

Quem está a trabalhar, quem está em pausa, quem não picou o ponto, quem chegou tarde e quanto, jornadas por fechar ou abertas desde ontem, picagens pendentes de validação e tarefas que vencem hoje ou não começaram à hora. São os mesmos dados da página inicial do painel. Se lhe perguntar «o que vejo primeiro?», começa pelos alertas.

O assistente diz o que vê, não o que supõe: «não picou o ponto», nunca «não veio». O CheckBiz360 sabe o primeiro; o segundo só o sabe o senhor.

### Cobrir alguém

Pergunte-lhe quem pode cobrir uma tarefa. Responde com três grupos:

- **Livres:** o seu horário cobre esse intervalo e não têm nada a essa hora.
- **Com reservas:** o turno não cobre o intervalo inteiro, ou já têm outra tarefa a essa hora; diz-lhe qual.
- **Não disponíveis:** de férias, de baixa, num feriado ou sem turno nesse dia, com o motivo.

Se a tarefa for de hoje, diz-lhe também quem picou o ponto. É o senhor que escolhe a pessoa; o assistente faz a mudança com o antes e o depois à frente.

### Ver a disponibilidade

Quantas pessoas tem disponíveis em cada dia e em cada centro, e quem falta num dia concreto e porquê. Serve para ver de relance o dia fraco da próxima semana antes de chegar. Em empresas muito grandes, a consulta vai centro a centro.

### Montar a semana inteira

- **Copiar a semana anterior**, com as mudanças que lhe disser.
- **Do zero**, ditando-lhe os serviços.
- **A partir de um documento**: a escala que o seu programa de gestão imprime, um Excel, uma fotografia do papel. O assistente lê-o, reconhece a sua equipa e converte-o na semana de cada pessoa.

Nos três casos mostra-lhe a proposta pessoa a pessoa, com os avisos que convém ver (dois serviços que se sobrepõem, um dia que é feriado para alguém), e uma ligação a um Excel com tudo para rever com calma. Cada pessoa recebe a sua semana no telemóvel, com os horários e a morada de cada serviço, só quando confirmar.

Não há limite de tarefas: se a escala for muito grande, o assistente carrega-a por partes e o senhor confirma uma única vez no fim. Se a semana mudar, peça-lhe que a proponha outra vez com a versão boa: o que já estava é atualizado e nada se duplica. Os serviços que a pessoa já tinha começado mantêm-se.

### Mudanças pontuais

Criar uma tarefa, mudá-la de dia ou de hora, passá-la a outra pessoa, cancelá-la. Também mudar a semana-tipo de alguém ou passá-lo ao horário por tarefas. Antes de mexer em nada mostra-lhe o antes e o depois e espera pelo seu sim.

### Dar entrada a pessoas e centros

Uma pessoa ou um centro soltos, ou muitos de uma vez a partir da lista da contabilidade, de um Excel ou de um documento. O assistente verifica quem já existe, diz-lhe o que vai criar e que morada entendeu de cada centro, e cria tudo quando confirmar. As boas-vindas à app não são enviadas sozinhas: peça-as quando tiver verificado que está tudo bem.

### Analisar

- **A evolução por semanas:** cobertura de picagens, atrasos, tarefas a tempo, horas e custo, de toda a empresa ou por centro.
- **Os custos do mês** face ao mês anterior. Se faltar a tarifa a alguém, o valor sai como parcial e o assistente diz-lho.
- **Os alertas** que o painel considera importantes, ordenados por gravidade.
- **O relatório de jornada** em PDF ou Excel, da empresa, de um centro ou de uma pessoa, entre as datas que indicar. Dá-lhe uma ligação que expira numa hora, e o relatório fica também no histórico de relatórios do painel.

---

## 4. O que o protege

- **Nada é guardado sem o seu sim.** O que muda a operação é proposto primeiro e aplicado quando confirmar. Se fechar a conversa sem confirmar, não acontece nada.
- **Atua com as suas permissões, verificadas em cada pedido.** Não pode fazer nada que o senhor não possa fazer no painel.
- **Quem deixa de administrar deixa de entrar de imediato.** Se retirar ou desativar um colaborador na empresa, o assistente dele perde o acesso a ela nesse mesmo momento. Se já não administrar nenhuma empresa, a ligação é cortada por completo.
- **Não adivinha a quem se refere.** Se um nome não estiver claro ou houver duas pessoas parecidas, pergunta mostrando o e-mail de cada uma.
- **As horas são as do centro.** «Às dez» é às dez no fuso horário da sucursal, mesmo que o senhor esteja noutro.

---

## Privacidade

Ao ligar, os nomes dos seus funcionários e os dados da operação são enviados para a conta do Claude ou do ChatGPT que usar. Convém que seja uma conta da empresa, não pessoal, e verificar nesse serviço o que faz com os seus dados. Pode retirar o conector quando quiser a partir do Claude ou do ChatGPT: a partir desse momento o assistente deixa de ter acesso.

---

## Problemas frequentes

| O que acontece | O que fazer |
|---|---|
| No ChatGPT não aparece **Criar** | Ative o modo de programador em **Definições avançadas** e volte a **Aplicações e conectores**. |
| Ao ligar não me deixa entrar | Verifique que tem a verificação em dois passos ativada e que é proprietário ou administrador de alguma empresa. |
| Diz que não tem acesso a uma empresa | Não a administra, ou retiraram-lhe o acesso. Peça-lhe que lhe mostre as suas empresas: são as que administra hoje. |
| Não sei com que empresa está a trabalhar | Pergunte-lhe. Diga-lhe a empresa se quiser mudar. |
| Diz que não encontra uma pessoa | Talvez na ficha tenha outro nome. Diga-lhe o e-mail dessa pessoa. |
| Propõe mas não aplica | Diga-lho com clareza: «confirma», «aplica». Não faz mudanças sem um sim explícito. |
| Deixou de funcionar de repente | Volte a ligar a partir do Claude ou do ChatGPT. Se lhe retiraram o acesso às suas empresas, a ligação é cortada e é preciso entrar outra vez. |

---

## Quem pode ligar

Proprietários e administradores com a verificação em dois passos ativada. Cada um vê apenas as empresas que administra.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [A página inicial: o hoje, os alertas e as últimas semanas](../07-inteligencia-operacional/112-a-pagina-inicial-o-hoje-os-alertas-e-as-ultimas-semanas.md) | Os mesmos dados que o assistente lhe conta, no painel |
| [Quadro de disponibilidade](../04-calendario-e-horarios/98-quadro-de-disponibilidade.md) | A disponibilidade que o assistente cruza para cobrir alguém |
| [Importar a escala semanal](../04-calendario-e-horarios/108-importar-a-escala-semanal.md) | O mesmo que pede ao assistente, feito com uma folha de Excel a partir do painel |
| [Dar entrada a sucursais e equipa a partir de Excel](../02-funcionarios/110-dar-entrada-a-sucursais-e-equipa-a-partir-de-excel.md) | As entradas em bloco a partir do painel |
| [Configuração da entidade](../08-sucursais-e-entidade/61-configuracao-da-entidade.md) | Onde está o separador Ambiente de trabalho |
| [Autenticação de dois fatores](../02-funcionarios/09-autenticacao-de-dois-fatores.md) | O segundo fator que a ligação exige |
