# O que diz o contrato de trabalho: ofício, horário e preço por hora

Ao carregar o contrato de trabalho de uma pessoa, o CheckBiz360 lê-o e propõe-lhe o que precisa para que essa pessoa conte bem nos custos: o seu **ofício**, o seu **horário**, a sua **convenção** e o seu **preço por hora**. Cada dado vem com a frase do contrato de onde sai, e nada muda na ficha até que o aplique.

Isto faz-se na ficha do documento, bloco **O que diz o contrato**. Só o veem e o usam o **proprietário e os administradores**.

---

## O que resolve

- **Não teclar o contrato.** Ofício, categoria, horário, modalidade, datas e salário saem lidos, com a sua citação.
- **Um preço por hora com fundamento.** Se o contrato indica o salário, converte-se em preço por hora com o horário anual que marca a convenção; se o contrato diz «segundo tabelas», o salário sai da tabela da convenção. Esse preço é o que usam os relatórios de custos e a rentabilidade dos clientes.
- **Ver o que não bate certo.** Um salário abaixo do mínimo para esse horário, uma convenção que não se identifica ou umas tabelas de um ano anterior saem como aviso, para que o reveja antes de aplicar.

---

## Antes de começar

- O documento tem de ser do tipo **Contrato**, estar atribuído a **uma pessoa** (âmbito *Funcionário*) e ser um **PDF com texto**. Um PDF digitalizado como imagem não pode ser lido: o bloco di-lo e é preciso preencher a ficha à mão.
- Para que proponha a convenção, a empresa precisa de ter a sua **atividade** indicada (menu **Entidade**, *A que se dedica a sua empresa*) e, se for o caso, a convenção no catálogo. Ver [Convenções coletivas](139-convencoes-coletivas.md).
- Se o ofício da pessoa já estiver no seu **catálogo de postos**, a leitura faz a correspondência com ele. A partir daqui não se criam postos novos.

---

## Carregar o contrato

1. Em **Gestão documental**, carregue o PDF com o tipo **Contrato** e o âmbito **Funcionário**, como qualquer contrato (ver [Recibos de vencimento e contratos](32-recibos-de-vencimento-e-contratos.md)).
2. Se souber por que convenção vai a pessoa, escolha-a em **Convenção coletiva (opcional)**. Se a deixar em *Sem indicar*, procura-se no catálogo ao ler o contrato.
3. Publique. A leitura começa sozinha. Pode ficar na ficha ou continuar a trabalhar: quando terminar, vê-o em **Início** e recebe um e-mail.

Na ficha do documento, o bloco **O que diz o contrato** passa de *Estamos a ler o contrato* para os dados lidos. Se quiser repetir a leitura (por exemplo, depois de referenciar uma convenção nova), prima **Voltar a ler**.

---

## O que propõe

Cada dado tem **De onde vem**, que abre a frase do contrato: *Do contrato: «…»*. O que o contrato não diz aparece como *Não está no contrato*.

| Dado | O que é |
|---|---|
| **Ofício** | O nome curto do posto («auxiliar de apoio domiciliário», «empregado de mesa») e, se o contrato o trouxer, o código de ocupação. |
| **Convenção** | A convenção que o contrato cita e o seu âmbito (estatal, autonómico, provincial ou de empresa). |
| **Categoria** | O grupo e o nível profissional, tal como o contrato os escreve. |
| **Horário semanal** | As horas por semana. |
| **Modalidade** | Sem termo, temporário, formativo ou fixo descontínuo. |
| **Datas** | Desde quando e, se a tiver, até quando. |
| **Salário** | O salário base bruto com o seu período, os pagamentos e se os extraordinários vão rateados ou à parte. |
| **Preço por hora proposto** | Euros brutos por hora, **sem a Segurança Social a cargo da empresa**, e por baixo **Cálculo**: de que valor e de que horário sai. Leva a marca **Estimado** quando o salário vem das tabelas ou quando não há convenção e se usa o horário máximo legal. |

Por baixo, os **avisos**: só o que lhe muda uma decisão. Por exemplo, que o salário do contrato fica abaixo do mínimo para esse horário, que um complemento não entra no salário base, que as tabelas guardadas da convenção são de um ano anterior ou que a data de fim foi calculada a partir de uma duração.

> **O preço por hora é um custo bruto.** Não inclui a Segurança Social da empresa nem outros custos. Se na sua empresa contam os custos de outra maneira, corrija-o ao aplicar.

---

## O bloco Convenção

A convenção decide o **horário anual** com que se passa de salário a preço por hora e, se o contrato remeter para as tabelas, o **salário**. O bloco **Convenção** diz o que se usou:

- **Este contrato vai por «…» · tabelas de 2025**, com **Ver documento** para abrir o boletim de onde saem as tabelas.
- **Linha usada**: a categoria da tabela, o seu montante e os seus pagamentos («Auxiliar de apoio domiciliário: 1.145,81 € × 14 pagamentos»). Se a convenção tiver várias tabelas (uma por âmbito, por zona ou por tipo de estabelecimento), a linha traz o seu bloco entre parêntesis: «Auxiliar Administrativo (Residências)».
- **Sem linha da tabela**: o salário é o que diz o contrato e da convenção toma-se só o horário.

O que pode fazer:

| Botão | Para quê |
|---|---|
| **Mudar convenção** | Escolher outra da lista da sua empresa. As que ainda não têm tabelas não podem ser escolhidas. |
| **Mudar linha** / **Escolher linha** | Escolher a categoria da tabela se a proposta não for a desta pessoa, ou se a leitura não soube qual era. A janela mostra cada linha com o seu grupo, o seu nível, o seu bloco e, se a tiver, o horário completo desse bloco. |
| **Escrever o preço à mão** | Deixar a convenção de fora e teclar o preço por hora. |
| **Voltar à convenção proposta** | Desfazer as alterações. |

Se mudar a convenção ou a linha, o preço por hora proposto deixa de valer: **recalcula-se ao aplicar**, com a tabela escolhida, e o bloco avisa.

Quando o catálogo não tem convenção para este contrato, o bloco di-lo (*Não há convenção para este contrato no catálogo*) e oferece-lhe **Escolher convenção** ou **Referenciar outra convenção**. Se houver várias possíveis, pede-lhe que escolha a que se aplica. Enquanto não houver convenção, o preço calcula-se com o horário máximo legal e fica marcado como estimado.

---

## Aplicar à ficha

O bloco **Aplicar à ficha do funcionário** passa o que foi lido para a ficha da pessoa:

1. **Posto do catálogo.** Se o ofício corresponder a um posto do seu catálogo, vem proposto. Se não, escolha um ou deixe **Manter o posto que já tem**.
2. **Preço por hora (€).** Vem proposto; pode corrigi-lo. Se for pela convenção, aparece *segundo a convenção*: calcula-o o servidor ao aplicar.
3. **Sucursais onde se aplica.** Se a pessoa estiver em várias, marque em quais. Cada linha mostra *o que tem agora → o que vai ter*.
4. Prima **Aplicar à ficha** e confirme. A janela mostra **Antes** e **Depois**. O catálogo de postos não é alterado.

A partir daí, essa pessoa conta nos custos com o seu novo posto e o seu preço por hora nessas sucursais.

---

## Problemas frequentes

**O bloco diz que o PDF não tem texto.** Está digitalizado como imagem. Peça o contrato em PDF com texto ou preencha o posto e o preço à mão na ficha da pessoa.

**Diz que não parece um contrato de trabalho.** Confirme que carregou o documento correto. Um anexo, um recibo de vencimento ou um contrato com um cliente não se leem aqui.

**Diz que o contrato parece de outra pessoa.** O nome do contrato não é o da pessoa a quem carregou o documento. Reveja-o antes de aplicar o que for.

**O preço por hora sai «Estimado» e não me bate certo.** Veja **Cálculo**: diz que salário e que horário foram usados. Se a convenção não for a correta, mude-a; se a categoria não for a dela, mude a linha; se preferir o seu valor, **Escrever o preço à mão**.

**Não há convenção para este contrato.** A sua empresa não tem a atividade indicada, ou a convenção não está no catálogo. Indique a atividade em **Entidade** ou referencie a convenção com a ligação ao boletim. Ver [Convenções coletivas](139-convencoes-coletivas.md).

**As tabelas são de um ano anterior.** O catálogo tem a tabela de 2025 e o contrato começa em 2026. Usa-se a mais recente que há e avisa-se. Quando as novas forem publicadas, referencie-as com o ano novo.

---

## Artigos relacionados

- [Convenções coletivas](139-convencoes-coletivas.md)
- [Recibos de vencimento e contratos](32-recibos-de-vencimento-e-contratos.md)
- [Quem vê cada documento](136-quem-ve-cada-documento.md)
- [Criar e gerir funcionários](../02-funcionarios/06-criar-e-gerir-funcionarios.md)
- [Análise de custos](../07-inteligencia-operacional/54-analise-de-custos.md)
