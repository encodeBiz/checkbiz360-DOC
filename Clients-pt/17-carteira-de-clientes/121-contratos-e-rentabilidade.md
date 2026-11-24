# Contratos e rentabilidade

Um contrato com um cliente fixa um montante e, muitas vezes, umas horas. O difícil é saber, enquanto se trabalha, se vai ser cumprido: se as horas chegam, se o custo come a margem. No CheckBiz360 cada contrato junta o seu montante com as tarefas que se fazem para ele e com o que se paga fora, e mostra a margem enquanto ainda é possível fazer alguma coisa.

Os contratos estão na ficha de cada cliente, separador **Detalhe**, bloco **Contratos**.

---

## O que resolve

- **Saber se um contrato deixa dinheiro**, com as horas e as despesas reais, não com uma estimativa de memória.
- **Ver o problema a chegar.** As horas feitas face às previstas, a vermelho quando se ultrapassam, e a data aproximada em que o custo ultrapassaria o montante.
- **Não escrever o contrato à mão.** A IA lê o PDF e propõe montante, datas e horas, com a frase de onde sai cada dado.
- **Ir do contrato às suas tarefas e voltar.** Cada contrato lista as suas tarefas e cada tarefa liga ao seu contrato.
- **Prever o seguinte.** Com os contratos fechados, a plataforma estima horas, custo e margem dos novos.

---

## Antes de começar

- A rentabilidade precisa de que as pessoas tenham a sua **tarifa horária** na sucursal. Sem ela, as suas horas contam-se mas não custam, e o contrato avisa que o custo fica curto. Ver [O que é a carteira de clientes](./117-o-que-e-a-carteira-de-clientes.md#antes-de-começar-o-preço-dos-postos).
- Criar, editar, fechar e apagar contratos, e ver montantes, custos e margens, compete ao **proprietário e aos administradores**. Managers e supervisores veem os contratos dos seus clientes com as suas horas e as suas tarefas, sem dinheiro.

---

## Criar um contrato

Um cliente pode ter **vários contratos ao mesmo tempo** (por exemplo, a manutenção anual e um trabalho pontual).

1. Na ficha do cliente, bloco **Contratos**, prima **Novo contrato**.
2. Em **Documento do cliente**, escolha o PDF do contrato ou do orçamento se já o carregou em **Documentos**; ou prima **Carregar PDF** para o carregar agora (só PDF, até 10 MB). O documento fica guardado como contrato do cliente, visível só para a Administração. Se não tiver PDF, deixe **Sem PDF**.
3. Com um PDF escolhido, pode premir **Ler o PDF** (ver mais abaixo).
4. Preencha ou reveja:
   - **Nome do contrato** (obrigatório).
   - **Começa** e **Termina**. Deixe **Termina** vazio se for por tempo indeterminado.
   - **Montante (€)**: o preço acordado com o cliente, **sem IVA**.
   - **Horas estimadas**: horas de trabalho, não dias.
   - **Complexidade**, de *1 · Simples* a *5 · Muito complexo*. Serve para comparar com contratos semelhantes ao prever.
   - **Notas**.
5. Guarde.

### Ler o PDF com IA

**Ler o PDF** lê o documento e preenche o montante, as datas, as horas e a complexidade. Por baixo de cada dado aparece a frase de onde sai, *Do documento: «…»*, ou *Não está no documento*. **Reveja o que foi lido antes de guardar**: a IA propõe, o senhor decide.

Se o documento não parecer um contrato nem um orçamento, o formulário avisa. Um PDF digitalizado como imagem, sem texto, não pode ser lido: preencha os dados à mão.

> **Privacidade.** Antes de o ler com IA, retiram-se do documento os nomes de pessoas e empresas, documentos de identificação e NIF, moradas, telefones, e-mails e contas bancárias: ao modelo só chega o resto. Mesmo assim, carregue só o que for preciso ler e nunca dados de saúde. O aviso aparece no próprio formulário.

---

## Que tarefas são de um contrato

Cada tarefa indica de que contrato é na sua lista **Contrato** (ver [O cliente na tarefa](./119-o-cliente-na-tarefa.md#o-contrato-da-tarefa)):

- Ao criar uma tarefa, se o cliente tiver um único contrato em vigor, vem proposto.
- **Sem contrato** deixa-a fora de todos, e é respeitado.
- Criar um contrato, mudar as suas datas ou reabri-lo **não leva tarefas**: uma tarefa só muda de contrato quando se escolhe nela.

---

## O cartão do contrato

Cada contrato é um cartão com o seu nome, o seu período (*De … a …* ou *Indeterminado*) e o seu estado (**Em curso** ou **Fechado em …**). Se algo não bater certo, uma marca de **avisos**. Prima **Expandir** para ver o detalhe.

| Número | O que é |
|---|---|
| **Montante** | O preço do contrato, sem IVA. |
| **Horas planeadas / feitas / previstas** | *Planeadas*: as que somam as suas tarefas, do início previsto ao vencimento, por cada pessoa atribuída. *Feitas*: as trabalhadas, segundo os registos das suas tarefas ou, se não os houver, quando foram iniciadas e terminadas. *Previstas*: as **Horas estimadas** do contrato (se não as indicou, só aparecem as duas primeiras). A vermelho se as feitas ultrapassarem as previstas. |
| **Custo bruto** | As horas feitas pela tarifa de cada pessoa (sem encargos sociais) com o posto com que trabalhou de cada vez, mais os **complementos** que recebeu nessas tarefas, mais o material consumido nas suas tarefas se tiver inventário, mais as despesas aprovadas do contrato. A vermelho se já ultrapassar o montante. É o mesmo número que dá o [relatório de tarefas](../06-tarefas/48-relatorios-de-tarefas.md#o-que-contém) para essas tarefas. |
| **Margem** | O que sobra do montante depois do custo, em euros e em percentagem. |

Por baixo:

- **Tarefas (n)**: cada tarefa do contrato com o seu estado, a sua data e as suas pessoas, da mais recente para a mais antiga, de 5 em 5 com **Carregar mais**. O nome da tarefa leva à sua ficha; a partir da ficha da tarefa, o contrato traz de volta aqui.
- O custo do material, os complementos e que parte das horas tem tarifa, se não a tiverem todas.
- **Despesas por aprovar** e **Despesas externas**. Ver [Despesas do contrato e da tarefa](./122-despesas-do-contrato-e-da-tarefa.md).
- **Previsão** (ver mais abaixo).

Por cima dos cartões, **Total do cliente**: o contratado, o custo e a margem de todos os seus contratos.

### Os avisos

| Aviso | O que fazer |
|---|---|
| *Ainda nenhuma tarefa pertence a este contrato.* | Escolha o contrato nas tarefas que lhe correspondam. |
| *Há horas sem tarifa: o custo fica curto.* | Indique a tarifa horária dessas pessoas na sua sucursal. |
| *Há material sem custo unitário: conta em quantidade, não em montante.* | Indique o custo na ficha do artigo de inventário. |
| *Há jornadas sem marcação de saída: não são valorizadas.* | Corrija essas jornadas para que contem. |
| *Algumas tarefas não têm marcações: as horas saem de quando foram iniciadas e terminadas.* | É informativo: essas horas são aproximadas. |

---

## A previsão

Com os contratos já **fechados** como referência, cada contrato em curso com horas estimadas mostra:

- **Horas previstas**: um intervalo, com o valor mais provável.
- **Custo previsto** e **Margem prevista**.
- Se a este ritmo o custo ultrapassar o montante, **por volta de que data**.

Compara-se com contratos semelhantes (da mesma complexidade quando os há). Enquanto não houver contratos fechados suficientes, indica-o: *Ainda não há contratos fechados suficientes para prever*. Sem horas estimadas: *Indique as horas estimadas para ter previsão*.

---

## Editar, fechar, reabrir e apagar

- **Editar** altera os dados do contrato e permite acrescentar ou retirar despesas externas.
- **Fechar contrato**: quando o trabalho termina. Os seus números passam para o histórico com que se preveem os seguintes. Pode **Reabrir**.
- **Apagar**: só se nenhuma tarefa for desse contrato. Se já tiver tarefas, feche-o.

As tarefas de um contrato fechado continuam a ser suas e podem ser editadas. O que não é possível é escolher um contrato fechado para uma tarefa nova.

---

## Problemas frequentes

**A margem sai muito alta ou o custo sai vazio.** Faltam tarifas horárias: o contrato avisa. Indique-as na associação de cada pessoa à sua sucursal.

**As horas feitas são zero embora se tenha trabalhado.** As tarefas não são desse contrato: abra-as e escolha-o em **Contrato**.

**«Ler o PDF» não preenche nada.** O PDF é uma imagem digitalizada ou não é um contrato. Preencha os dados à mão.

**Não vejo o montante nem o botão Novo contrato.** Só os veem proprietários e administradores.

**Não me deixa apagar um contrato.** Tem tarefas. Feche-o em vez disso.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [O cliente na tarefa](./119-o-cliente-na-tarefa.md) | A lista de contrato na tarefa |
| [Despesas do contrato e da tarefa](./122-despesas-do-contrato-e-da-tarefa.md) | O que se paga fora e conta no custo |
| [Documentos do cliente](./120-documentos-do-cliente.md) | O PDF do contrato e quem o vê |
| [O cliente nas análises](./123-o-cliente-nas-analises.md) | A rentabilidade do cliente mês a mês e os alertas de contrato |
| [Criar e gerir funcionários](../02-funcionarios/06-criar-e-gerir-funcionarios.md) | Onde se indica a tarifa horária |
| [Vários postos para a mesma pessoa](../02-funcionarios/140-varios-postos-para-a-mesma-pessoa.md) | Com que preço se valoriza cada tarefa |
| [Complementos](../02-funcionarios/141-complementos.md) | O que se recebe à parte e entra no custo |
