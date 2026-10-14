# Existências, armazéns e entradas

Este guia explica como pôr o inventário a funcionar e como controlar o que há. Requer o complemento de inventário contratado ou em experiência.

---

## 1. Criar os armazéns

Um armazém é o sítio de onde sai o material: uma arrecadação de limpeza, um pavilhão, uma carrinha. **Todo o armazém serve pelo menos uma sucursal**, e uma sucursal pode ter vários armazéns.

1. Vá a **Inventário → Armazéns**.
2. Clique em **Novo armazém**, dê-lhe um nome e escolha as sucursais que serve.

Quando uma tarefa dessa sucursal precisar de material, a plataforma só oferece os seus armazéns. Se houver só um, escolhe-o sozinha.

Cada armazém tem a sua **ficha**, com um resumo —artigos, exemplares livres, existências abaixo do mínimo e discrepâncias—, o que contém e os seus movimentos recentes.

---

## 2. Registar a primeira entrada

O material entra sempre por **Nova entrada**, em **Inventário → Existências**. Não é preciso criar o artigo antes:

1. Clique em **Nova entrada**.
2. Em **Artigo**, escreva para o procurar. Se não existir, escolha **＋ Novo artigo** e preencha a sua ficha: tipo, nome e unidade de medida (ou unidade de uso, se for um operável), referência, custo unitário e categoria.
3. Escolha o **armazém**.
4. Se for um **consumível**, indique a **quantidade**. Se for um **operável**, a entrada é um **exemplar novo**: dê-lhe o identificador da etiqueta (matrícula, número de série) e, se quiser, um nome curto («a lavadora vermelha»).
5. Clique em **Registar entrada**.

> **Dica:** a pesquisa começa a partir da terceira letra, como as restantes pesquisas do backoffice.

Se tiver muitos artigos para registar, carregue-os de uma vez a partir da ficha do armazém com **Importar**: explica-se em [Importar material a partir de um modelo](./105-importar-material-a-partir-de-um-modelo.md).

---

## 3. Existências: o que há, artigo a artigo

**Existências** é o centro de comando do inventário. Cada linha é um artigo num armazém:

- Um **consumível** mostra o disponível, o que há em armazém, o comprometido por tarefas e o seu mínimo.
- Um **operável** mostra quantos exemplares estão livres agora, quantos ocupados e quantos indisponíveis. Se algum tiver documentos expirados, a linha diz quantos estão **fora de regra** ou **a rever**.

A coluna **Estado** resume se é preciso fazer alguma coisa:

| Estado | Significa |
|---|---|
| **Correto** | Um consumível sem avisos: nem abaixo do mínimo nem com discrepância. |
| **Disponível** | Um operável com algum exemplar livre agora. |
| **Abaixo do mínimo** | Há menos do que o mínimo de aviso fixado para esse armazém. |
| **Discrepância** | O saldo ficou negativo: saiu mais do que o registado. É preciso recontar. |
| **Todos ocupados** | Nenhum exemplar livre neste momento. |
| **Sem exemplares** | Operável registado sem nenhum exemplar ainda. |

Pode filtrar por texto, tipo, armazém e estado. Se houver discrepâncias, um aviso no topo permite vê-las com um clique. O estado **Fora da base** deixa só os equipamentos livres que não estão no seu armazém: o que há para recolher (ver [Onde está cada equipamento](./106-onde-esta-cada-equipamento.md)).

---

## 4. Ações sobre o material

A partir de cada linha, ou da ficha do artigo:

| Ação | Para quê |
|---|---|
| **Entrada** | Material que chega: uma compra, uma devolução de fornecedor, um exemplar novo. |
| **Transferência** | Mover quantidade de um armazém para outro, ou mudar o armazém base de um exemplar. |
| **Contagem** | Fixar o que há de facto depois de contar, com um motivo. Só consumíveis. |
| **Mínimo** | Fixar o nível abaixo do qual os responsáveis são avisados. Só consumíveis. |
| **Editar** | Alterar os dados da ficha. O tipo não se altera. |
| **Dar saída** | Entregar material do armazém a uma tarefa, a uma pessoa ou a uma sucursal. É opcional: se ninguém a der, regista-a o consumo. Ver [Material sem tarefas](./107-material-sem-tarefas-pessoas-e-locais.md). |
| **Entregar** | Dar um exemplar a uma pessoa, que o confirma no telemóvel. Ver [Equipamentos: documentos, inspeções e entregas](./104-equipamentos-documentos-inspecoes-e-entregas.md). |
| **Arquivar** | Deixar de oferecer um artigo. Se tiver histórico, conserva-se. |

---

## 5. A ficha do artigo

Todos os artigos têm a mesma ficha: os seus dados, o que há em cada armazém e o seu histórico.

- Num **consumível**: existências por armazém e movimentos dos últimos 30 dias, com descarga do ano em CSV.
- Num **operável**: quantos exemplares estão livres; cada exemplar com o seu estado (livre, reservado, em uso, entregue, indisponível ou retirado), o seu uso atual e **onde está**; um **calendário** onde cada reserva é uma barra com o seu horário, em períodos de 7, 14 ou 30 dias; e os seus **documentos** (inspeção, seguro, revisões, manual), com a marca de se cada exemplar está em regra.

---

## Quem pode fazer o quê

| Perfil | Pode |
|---|---|
| Worker | Ver o material dos armazéns das suas sucursais, declarar o consumo nas suas tarefas e confirmar os equipamentos que lhe são entregues |
| Supervisor | Além disso, reservar material e exemplares para tarefas |
| Manager, Owner | Além disso, criar artigos, armazéns e exemplares, e registar entradas, contagens e transferências |

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [O que é o inventário](./100-o-que-e-o-inventario.md) | Que problemas resolve e como se contrata |
| [Material nas tarefas](./102-material-nas-tarefas.md) | Como se atribui e acompanha o material de cada tarefa |
| [Importar material a partir de um modelo](./105-importar-material-a-partir-de-um-modelo.md) | Carregar de uma vez tudo o que há num armazém |
| [Onde está cada equipamento](./106-onde-esta-cada-equipamento.md) | Equipamentos livres fora do armazém e como se recebem |
