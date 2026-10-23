# Importar a escala semanal

Quando o trabalho muda todas as semanas —apoio domiciliário, limpeza por locais, manutenção—, escrever a semana de cada pessoa, turno a turno ou trabalho a trabalho, é uma manhã perdida todas as segundas-feiras. Este guia explica como carregar de uma vez a semana de toda a equipa de uma filial a partir de uma folha de Excel, ou a de uma só pessoa a partir da sua ficha.

---

## O que resolve

- **Um carregamento para toda a equipa.** Um ficheiro por filial e semana, com um separador por pessoa. Não é preciso ir ficha a ficha.
- **Cada pessoa recebe a sua semana no telemóvel**: os seus turnos, ou os seus trabalhos com a morada onde tem de registar, conforme a forma como se organiza o seu horário.
- **Nada se guarda sem que o veja antes.** A plataforma mostra o que fará com cada pessoa e só o aplica quando confirma.
- **Corrigir é voltar a carregar.** Se a semana mudar, carregue o ficheiro corrigido: o que já estava é substituído e nada se duplica.

---

## O que se carrega depende do modo de cada pessoa

O tipo de escala não se escolhe: decide-o o [modo do horário](114-calendario-de-turnos-por-data.md) de cada pessoa.

| Modo da pessoa | O que carrega o seu separador | O que acontece às suas tarefas |
|---|---|---|
| **Por turnos** | Os seus turnos dessa semana: data, entrada e saída. Os dias sem linhas são folga. | Nenhuma se cria, se move nem se apaga. |
| **Por tarefas** | Uma tarefa por linha, com a sua morada. As suas tarefas são o seu horário. | Substituem a sua semana: as tarefas da escala anterior que ainda não começou são retiradas e criam-se as do ficheiro. As começadas ficam. |
| **Semana tipo** | Nada. O seu horário é a semana tipo e não se lhe carrega escala. | Não se tocam. |

Se quiser carregar a alguém outro tipo de escala, mude-lhe antes o modo.

---

## Como funciona, em três passos

| Passo | O que acontece |
|---|---|
| **1. Descarregar o modelo** | A partir da filial, para a semana que escolher. Traz um separador por cada pessoa da filial, do tipo que lhe cabe. |
| **2. Preenchê-lo e carregá-lo** | Uma linha por turno ou por trabalho. Ao carregá-lo ainda não se guarda nada. |
| **3. Rever e confirmar** | A plataforma mostra o que fará com cada pessoa. Só ao confirmar se aplica. |

---

## 1. Descarregar o modelo

A escala de toda a equipa carrega-se a partir de uma filial que está **Por turnos**:

1. Vá a **Filiais/Projetos**, abra a ficha da filial e clique em **Editar**.
2. Em **Horários e feriados**, confirme que **Como se organiza o horário** está em **Por turnos**.
3. Em **Importar escala por turnos**, por cima da escala de turnos, clique em **Carregar uma escala**.
4. Escolha a semana e clique em **Descarregar modelo**.

Quem nessa filial estiver **Por tarefas** também leva o seu separador, de tarefas. Se a filial estiver em **Semana tipo**, a escala de quem estiver **Por tarefas** carrega-se a partir da sua ficha (veja «A semana de uma só pessoa», mais abaixo).

O modelo traz uma primeira folha com as instruções e a lista das pessoas, e **um separador por pessoa**, com o seu nome e o tipo que lhe cabe: **Escala por turnos** ou **Escala por tarefas**.

> **Não apague a linha 1 de nenhum separador**: é a que diz de quem é e de que tipo. Pode mudar o nome dos separadores ou reordená-los sem problema.

Cada separador traz **duas linhas de exemplo** que começam pela palavra **EXCLUIR**: pode apagá-las ou deixá-las, porque não se importam.

### Colunas

Numa **escala por turnos**, cada linha é um turno e só são precisas as três primeiras colunas. Um dia partido são duas linhas com a mesma data.

Numa **escala por tarefas**, cada linha é um trabalho:

| Coluna | O que pôr |
|---|---|
| **Data** * | O dia do trabalho: 19/10/2026. |
| **Hora de início** * | A que horas começa: 08:00. |
| **Hora de fim** * | A que horas acaba: 10:00. |
| **Cliente** | Para quem é o trabalho: a pessoa apoiada, o condomínio, a empresa. |
| **Morada** | Onde se faz. É o local onde a pessoa terá de registar. |
| **Trabalho** | O que se faz: limpeza, acompanhamento, revisão. |
| **Deslocação (min)** | Minutos de deslocação até esse trabalho. |

As colunas com asterisco são obrigatórias. Numa escala por tarefas, convém pôr sempre a **morada**: sem ela o trabalho cria-se na mesma, mas poderá ser registado de qualquer sítio.

### O que significa deixar um separador vazio

- **Um separador vazio** deixa essa pessoa como está. Não quer dizer «essa semana não trabalha»: quer dizer que não se diz nada sobre ela.
- **Um separador com linhas** é a semana inteira dessa pessoa: os dias sem nenhuma linha ficam livres.

---

## 2. Carregar o ficheiro

Clique em **Escolher ficheiro**, selecione o modelo preenchido e clique em **Ver a proposta**. Aceita-se Excel (.xlsx) até 2 MB, guardado com o Excel ou com qualquer outro programa de folhas de cálculo. Não se aceita CSV, porque um CSV não tem separadores.

Se carregar um ficheiro que não é o modelo, a plataforma indica-o e não lê nada.

---

## 3. Rever o que se fará

Antes de confirmar, cada pessoa aparece com o seu estado, as suas linhas e as horas da semana. A revisão de cada pessoa faz-se conforme o seu modo: numa escala por turnos não se fala de tarefas nem de moradas.

| Estado | Significa |
|---|---|
| **Pronta** | Tudo foi lido corretamente. Será aplicada ao confirmar. |
| **Bloqueada** | Algo impede aplicá-la: uma linha mal escrita (indica-se qual), trabalhos num dia que para essa pessoa é feriado ou férias, uma pessoa em **Semana tipo**, ou um separador de um tipo que já não corresponde ao seu modo. Essa pessoa não se aplica; as outras, sim. |
| **Sem alterações** | O seu separador está vazio. Não se toca. |
| **Separador não reconhecido** | O separador não corresponde a ninguém da filial. Verifique a linha 1. |
| **Separador repetido** | Há dois separadores para a mesma pessoa e não se sabe qual vale. |

Ao lado de cada pessoa aparecem também os avisos que convém ver. Numa escala por tarefas: dois trabalhos que se sobrepõem, trabalhos sem morada, ou uma deslocação antes do primeiro trabalho mais longa do que a margem que a pessoa tem para registar a entrada; e que tarefas dessa semana são substituídas e quais ficam por já estarem começadas. Numa escala por turnos: se o separador trouxer cliente, morada ou trabalho, avisa-se de que esses dados não se carregam. Duas linhas do mesmo dia que se sobrepõem carregam-se como um só turno.

O que pede atenção aparece primeiro. Para corrigir uma pessoa bloqueada, corrija o ficheiro e clique em **Carregar outro ficheiro**. Se fechar a janela sem confirmar, nada se guarda.

Quando estiver de acordo, clique em **Confirmar**. Com muitas pessoas demora um pouco e vê-se o progresso; pode fechar a janela e a importação continua. No fim, cada pessoa indica quantos dias de turnos lhe foram carregados ou quantas tarefas lhe foram criadas.

---

## O que cada pessoa vê

Na app, a semana importada:

- **Por turnos**: os seus turnos de cada dia, com o lembrete de entrada e de saída. Regista contra a filial, como sempre.
- **Por tarefas**: os seus trabalhos, cada um com a sua hora e a sua morada. Registará na morada de cada trabalho, e o seu horário de cada dia são esses trabalhos.

As datas passadas não se carregam: os dias anteriores a hoje ficam como estavam.

---

## Voltar a carregar a mesma semana

Se a semana mudar, preencha o modelo com a versão certa e carregue-o outra vez:

- **Por turnos**: cada dia que o ficheiro traz substitui o que havia nesse dia. Nada se duplica.
- **Por tarefas**: a semana é substituída. Os trabalhos que já não aparecem **são retirados**, exceto os que a pessoa já tenha começado: esses ficam e a revisão avisa.

---

## A semana de uma só pessoa

Abra a ficha da pessoa e clique em **Editar**. Em **Horários e feriados**, com a pessoa **Por turnos** ou **Por tarefas**, clique em **Carregar uma escala** em **Importar escala por turnos** ou em **Importar escala semanal**. Pode fazer o mesmo só para ela:

- **Descarregar modelo** dá-lhe um modelo com o separador dela.
- Também pode carregar o documento que o seu programa de gestão imprime (PDF, Excel ou CSV). Nesse caso a plataforma mostra o que entendeu de cada coluna para que o confirme antes de continuar, e demora um pouco mais.

A quem está em **Semana tipo** não se carrega escala.

---

## Quem pode importar

As pessoas com acesso de gestão ao painel da empresa.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Por turnos: o horário são os turnos que carrega](./114-calendario-de-turnos-por-data.md) | Os três modos do horário e a escala de turnos |
| [Horários base e turnos](./23-horarios-base-e-turnos.md) | A semana tipo, com um ou vários turnos por dia |
| [Feriados e dias não úteis](./29-feriados-e-dias-nao-uteis.md) | Porque é que um trabalho num dia de férias bloqueia essa pessoa |
