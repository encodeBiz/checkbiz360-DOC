# RentmanBiz — a integração com o Rentman

O **RentmanBiz** é o add-on que liga o CheckBiz360 ao Rentman, o software com que muitas empresas de eventos, audiovisuais e aluguer de material planeiam os seus projetos, as suas equipas e o seu armazém.

## O que falta ao Rentman (e porque isso lhe interessa)

O Rentman sabe **o que está planeado**: que montagem há, que material sai, quem devia ir e durante quantas horas. O que não sabe é **o que aconteceu de facto**: se essa pessoa chegou, a que horas, se estava no pavilhão ou em casa, e quantas horas trabalhou realmente.

Essa lacuna preenche-se hoje à mão. Alguém pergunta, alguém aponta, alguém escreve as horas ao fim da semana. E quando o cliente final contesta uma fatura ou um trabalhador contesta o seu recibo, só existe a palavra de cada um.

O RentmanBiz fecha essa lacuna nos dois sentidos: traz do Rentman **quem trabalha e onde**, e devolve-lhe **as horas efetivamente registadas**.

## O que traz, em concreto

### As horas deixam de se escrever

Quando um trabalhador fecha a sua jornada no CheckBiz360, essas horas aparecem sozinhas no projeto correspondente do Rentman, no quarto de hora seguinte. Sem folhas de cálculo pelo meio, sem lembretes e sem ninguém a transcrever nada.

### Horas verificáveis, não declaradas

É esta a diferença de fundo. Não é o mesmo *"o técnico diz que esteve dez horas"* e *"está registado que entrou às 08:02 dentro do recinto, a partir do seu dispositivo autorizado, e saiu às 18:10 do mesmo sítio"*.

Isso muda duas conversas: a que se tem com o cliente final sobre uma fatura, e a que se tem com um trabalhador sobre o seu recibo.

### O registo legal de horários, que o Rentman não cobre

O Rentman é uma ferramenta de produção, não um sistema de registo de horários. A lei exige um registo diário da jornada, conservado, acessível e não manipulável. O CheckBiz360 fornece-o — com relatórios exportáveis — sem mudar a forma de trabalhar de ninguém: o planeamento continua no Rentman.

### O evento passa a ser um sítio onde se regista o ponto

Cada montagem com pessoas atribuídas passa a ser um centro de trabalho com a sua **geocerca**, obtida a partir da morada do local. Neste setor ninguém regista o ponto no escritório: regista-o no pavilhão, no teatro ou no armazém onde se monta. E ninguém tem de criar centros à mão todas as semanas.

Os **armazéns** entram da mesma forma, como centros permanentes: é onde se regista o ponto todos os dias.

### Cada um sabe o que lhe compete ao chegar

As atribuições do Rentman convertem-se em tarefas dentro do CheckBiz360. O trabalhador abre o telemóvel e vê a que montagem vai, com que função e em que horário, e vai marcando o que completa. Deixa de chegar a perguntar.

### Quem preparou cada pedido, e quanto tempo demorou

É provavelmente o contributo que mais muda o dia a dia de uma empresa de aluguer.

Um aluguer em seco ou uma venda não levam ninguém a um evento, mas alguém tem de preparar esse material antes de o cliente o levantar, e alguém tem de o rever quando volta. Hoje isso combina-se de palavra — *"eu trato disso à tarde"* — e não fica registado em lado nenhum.

Com o RentmanBiz, cada operação gera a sua tarefa no armazém correspondente, com a data de saída do material. A partir daí:

- **Sabe-se quem tem de o fazer**: o responsável distribui essas tarefas pela sua gente do armazém, e cada um vê a sua no telemóvel.
- **Sabe-se quem o fez**, porque a tarefa fica em seu nome e é marcada como concluída.
- **E sabe-se quanto tempo demorou**, porque essa pessoa está com o ponto registado nesse armazém enquanto o prepara.

Isso abre perguntas que até agora nem se podiam formular: quanto custa realmente preparar um pedido tipo, se duas pessoas demoram o mesmo no mesmo trabalho, se os picos do armazém coincidem com os planeados, ou quantas pessoas são precisas na sexta-feira de um fim de semana carregado.

Vem **desativado de fábrica**, porque nem todas as empresas querem gerir o armazém com tarefas e uma empresa de aluguer tem dezenas destas operações por semana.

### Quanto custou de facto uma montagem

As horas lançadas são as **líquidas**, com o intervalo já descontado, e levam associado o custo por hora de cada função que já tem definido no Rentman. A diferença entre o planeado e o real deixa de ser uma intuição.

### E ninguém mexe no registo sem que se saiba

Se alguém alterar no Rentman horas já lançadas, **o ponto do CheckBiz360 não é alterado**. A diferença é detetada, assinalada e mostrada com as duas versões à frente para que decida. O registo legal nunca é sobreposto em silêncio.

## O que NÃO faz

Tão importante como o anterior:

- **Não altera os seus registos de ponto** a partir de dados do Rentman.
- **Não envia jornadas abertas nem incompletas**: sem saída registada não há nada a enviar.
- **Não cria pessoal nem atribuições no Rentman.** A API deles não o permite: as pessoas e as atribuições viajam do Rentman para o CheckBiz360, nunca ao contrário.
- **Não sincroniza material, orçamentos nem faturas.**
- **Não envia as suas tarefas para o Rentman.** Está previsto para mais tarde.

## Estado atual

| Funcionalidade | Estado | Comentário |
|---|---|---|
| Envio de jornadas fechadas para o Rentman | **Disponível** | Automático a cada 15 minutos, ou de imediato |
| Horas líquidas com intervalo e custo por hora | **Disponível** | Mesmo valor do relatório legal |
| Aviso de horas alteradas no Rentman | **Disponível** | Com as duas versões comparadas |
| Importação da equipa | **Disponível** | Emparelha por e-mail; quem não o tiver fica pendente |
| Montagens e armazéns como centros de trabalho | **Disponível** | Nascem inativos até confirmar a geocerca |
| Atribuições convertidas em tarefas | **Disponível** | Uma tarefa por função, com a sua gente |
| Tarefas de armazém (alugueres e vendas) | **Disponível** | Desativado de fábrica |
| Ecrã de configuração no backoffice | **Em desenvolvimento** | Durante a beta configura-o a equipa da Encodebiz |
| Enviar tarefas do CheckBiz360 para o Rentman | **Pendente de desenvolvimento** | Prevista numa versão futura |
| Material, orçamentos e faturas | **Não disponível** | Fora do âmbito |

## O que precisa para começar

Uma conta Rentman com permissão para criar um token de API, o controlo de horários do CheckBiz360 ativo, e algum tempo para rever o que a primeira importação deixar pendente — habitualmente e-mails em falta e geocercas por confirmar.

## Artigos relacionados

- [Ligar o RentmanBiz passo a passo](95-ligar-o-rentmanbiz.md)
- [O que se importa e o que fica pendente](97-importacao-e-pendentes.md)
- [Horas lançadas e avisos](96-horas-lancadas-e-avisos.md)
