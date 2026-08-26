# O que se importa e o que fica pendente

Ao ligar o RentmanBiz, a plataforma traz do Rentman o necessário para que a sua equipa possa registar o ponto. Este artigo explica o que entra, o que fica de fora de propósito e porque algumas coisas nascem **pendentes de completar**.

## Antes de importar: a pré-visualização

A importação nunca começa às cegas. Primeiro gera-se uma **pré-visualização** que não escreve nada e responde à pergunta razoável: *o que é que isto vai meter na minha plataforma?*

Verá quantas montagens se converteriam em centros de trabalho, quantas são descartadas, quantas pessoas se podem criar e quantas não, e quantas tarefas sairiam. Só quando o resultado lhe parecer correto é que se executa a sério.

## O que se importa

### As pessoas

Cada pessoa da sua equipa no Rentman é procurada primeiro entre os seus colaboradores do CheckBiz360 **por e-mail**. Se já existir, é associada — nunca duplicada, porque partir o histórico de alguém em dois é pior do que não o importar.

Se não existir e trouxer e-mail, é criada com o seu acesso e recebe o e-mail de boas-vindas.

### Os centros de trabalho

Entram dois tipos:

- **As montagens**: cada projeto do Rentman **que tenha pessoas atribuídas**. É esse o critério, não o tipo de projeto: se ninguém está atribuído, ninguém vai registar o ponto ali.
- **Os armazéns**: as suas localizações de material, que são centros permanentes onde se regista o ponto todos os dias.

De ambos se retira a morada e calculam-se as coordenadas para propor a geocerca.

### As responsabilidades

Cada pessoa fica associada aos centros onde trabalha: ao armazém que tem atribuído na sua ficha do Rentman, e às montagens em que esteja atribuída. Com a sua função como cargo — técnico, rigger, stagehand — e com o custo por hora que já tem definido lá.

**Todos entram como trabalhador.** A função do Rentman é um ofício, não um nível de permissões: montar luzes num evento não transforma ninguém em responsável de um centro. Para promover alguém, faz-se à mão e de forma consciente.

### As tarefas

Uma tarefa por função de cada montagem, com todas as pessoas dessa função. E, se o ativar, as tarefas de armazém de alugueres e vendas: preparar o material antes da saída e revê-lo à chegada.

## O que se descarta, e porquê

| Descarta-se | Motivo |
|---|---|
| Projetos sem pessoas atribuídas | Vendas e alugueres em seco: ninguém pisa um sítio, não há onde registar o ponto |
| Projetos fora da janela | Só se trazem os do último mês e os três seguintes, para não arrastar o histórico |
| Material, orçamentos, faturas | Fora do âmbito da integração |

## O que fica pendente de completar

O Rentman não guarda tudo o que o CheckBiz360 precisa. Em vez de o inventar ou de descartar o dado, a plataforma importa-o marcado como **pendente**, com o motivo, e mostra um aviso com ligação direta à ficha onde se resolve.

| Pendente | O que significa | O que fazer |
|---|---|---|
| **Sem e-mail** | O Rentman raramente o guarda, e no CheckBiz360 é o acesso do colaborador | Adicionar o e-mail na ficha. Ao fazê-lo recebe acesso e boas-vindas |
| **Falta confirmar a geocerca** | O Rentman não dá coordenadas: foram calculadas a partir da morada | Rever o ponto no centro e ativá-lo |
| **Sem morada** | Essa montagem não traz morada no Rentman | Completá-la ou deixar o centro sem uso |
| **Sem custo por hora** | Essa função não tem tarifa definida no Rentman | Defini-la, ou as jornadas sairão a custo zero nos relatórios |

Duas coisas importantes sobre o que fica pendente:

**Nada pendente pode fazer estragos enquanto o estiver.** Um centro sem geocerca confirmada nasce **inativo**: existe, mas não valida nem invalida o ponto de ninguém. Uma pessoa sem e-mail nasce **inativa e sem acesso**.

**E nada pendente lhe é faturado.** Como a faturação é por colaborador ativo, quem ainda não pode trabalhar não conta. Passa a contar quando completar o seu e-mail e ficar ativo, que é quando pode registar o ponto de facto.

O aviso desaparece sozinho quando não houver nada por completar.

## Voltar a importar

A importação pode repetir-se sem receio: o que já existe não é duplicado, e o que tiver configurado à mão — geocercas, horários, intervalos — **nunca é sobreposto**. Só se acrescenta o que for novo no Rentman.

## Artigos relacionados

- [RentmanBiz](94-rentmanbiz.md)
- [Ligar o RentmanBiz passo a passo](95-ligar-o-rentmanbiz.md)
