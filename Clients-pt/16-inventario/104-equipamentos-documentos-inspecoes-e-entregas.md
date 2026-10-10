# Equipamentos: documentos, inspeções e entregas

Numa inspeção do trabalho, uma empresa tem de responder com documentos a duas perguntas: **cada trabalhador recebeu o seu equipamento de proteção?** e **a máquina com que trabalha passou as suas inspeções obrigatórias?** O inventário guarda as duas provas junto do próprio equipamento e avisa antes de algo expirar.

Tudo isto aplica-se ao material que se **empresta** (máquinas, veículos, ferramentas, EPI com número de série), não ao que se gasta.

---

## Os documentos de cada equipamento

A ficha de um equipamento (**Inventário → Existências → o equipamento**) tem a secção **Documentos**. Aí guardam-se a propriedade ou fatura, a declaração CE, o manual, o seguro, a inspeção obrigatória que lhe corresponde, as revisões de manutenção e a avaliação de riscos.

Há duas formas de adicionar um:

- **Carregar documento**: escolhe-se o tipo, o título, a data de validade (numa inspeção, a da próxima), o resultado se for uma inspeção e quem a fez.
- **Vincular existente**: se o documento já está na **Gestão documental**, procura-se e vincula-se sem o carregar de novo.

Nos dois casos, **Aplica-se a** decide se o documento é de **todos os exemplares** (um manual, uma declaração CE) ou de **um só** (a inspeção de uma carrinha, o seguro de uma máquina).

Também se pode fazer a partir da **Gestão documental**: ao carregar um documento, com o âmbito **Equipamento**; ou na ficha de um documento que já existe, com **Vincular a um equipamento**. É sempre o mesmo documento: vê-se nos dois sítios, e **desvinculá-lo não o apaga**.

---

## O que está em regra e o que não está

Cada exemplar indica se está em regra segundo os seus documentos:

| Marca | O que significa |
|---|---|
| **Em regra** | Tem documentos e nenhum está expirado |
| **Rever documentos** (âmbar) | Algum documento expira nos próximos 30 dias, ou um documento não obrigatório expirou |
| **Fora de regra** (vermelho) | A inspeção obrigatória expirou ou o resultado foi «não apto» |

Um equipamento sem documentos não tem marca. Se se carregar uma inspeção nova, conta a mais recente: a antiga aparece como **Substituído**.

A marca vê-se na lista de exemplares da ficha, nas **Existências** (quantos estão fora de regra) e ao escolher material para uma tarefa.

**Um equipamento fora de regra não é bloqueado.** Retirá-lo é uma decisão da empresa, não do programa. Mas ao reservá-lo para uma tarefa ou entregá-lo a uma pessoa aparece o aviso com o motivo, e é preciso marcar que se sabe para continuar. Fica registado quem o aceitou.

---

## Avisos antes de expirar

Os responsáveis do armazém do equipamento recebem um aviso quando um dos seus documentos vai expirar em menos de 30 dias, e outro quando expirou ou uma inspeção dá «não apto». Se o documento for de todos os exemplares, o aviso chega aos responsáveis da empresa. Cada aviso chega uma só vez.

---

## Entregar um equipamento a uma pessoa

Na ficha do equipamento ou nas Existências, **Entregar** atribui um exemplar a um trabalhador juntamente com os seus documentos: o manual de uso, o folheto do fabricante ou o compromisso de responsabilidade. Os que o equipamento tem marcados **Com cada entrega** na sua secção de documentos aparecem já marcados, e no momento pode-se desmarcar algum ou carregar outro. Só podem ir com a entrega os documentos visíveis para trabalhadores, que é como nascem os documentos de um equipamento. O trabalhador confirma que recebeu o equipamento e os documentos relacionados e que está de acordo com a entrega; o registo guarda que documentos eram e em que versão. A confirmação vai **assinada com a chave do seu telemóvel** e a plataforma verifica-a, como nos documentos (ver [Confirmação de leitura e assinatura eletrónica](../05-gestao-documental/35-assinatura-eletronica.md)); o relatório «Equipamentos e EPI» diz na coluna «Assinatura» se foi verificada. O trabalhador recebe um aviso no telemóvel e confirma em **O meu material** com a impressão digital, o rosto ou o código de desbloqueio; se o telemóvel não tiver bloqueio, com a palavra-passe da conta. Também pode indicar que não o recebeu ou que não está conforme, e quem gere o armazém recebe o aviso.

Na devolução indica-se como volta: em bom estado, com danos ou não devolvido. Se voltar com danos ou não for devolvido, fica indisponível com esse motivo. O equipamento passa a estar no armazém que o recebe (ver [Onde está cada equipamento](./106-onde-esta-cada-equipamento.md)). O que cada trabalhador tem vê-se também na sua ficha, no separador **Material**.

---

## O relatório «Equipamentos e EPI»

Gera-se em **Relatórios**, em Excel, com duas folhas:

- **Entregas**: o que foi entregue a cada trabalhador, com que documentos e em que versão, por quem, o que confirmou, quando e como, e como o devolveu.
- **Equipamentos e inspeções**: cada exemplar com o seu estado, quem o tem agora e cada documento com tipo, resultado, validade e estado.

É o que se apresenta numa inspeção. Sem o inventário contratado, o relatório aparece a vermelho na lista e explica o que fazer para o ter.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [O que é o inventário](./100-o-que-e-o-inventario.md) | Que problemas resolve |
| [Existências, armazéns e entradas](./101-existencias-armazens-e-entradas.md) | Registo do material e de cada exemplar |
| [Tipos de relatório](../11-relatorios-e-exportacao/76-tipos-de-relatorio.md) | Todos os relatórios da plataforma |
