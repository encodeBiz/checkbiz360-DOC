# Importar a escala semanal

Quando o trabalho muda todas as semanas —apoio domiciliário, limpeza por locais, manutenção—, escrever a semana de cada pessoa, trabalho a trabalho, é uma manhã perdida todas as segundas-feiras. Este guia explica como carregar de uma vez a semana de toda a equipa de uma filial a partir de uma folha de Excel, ou a de uma só pessoa a partir da sua ficha.

---

## O que resolve

- **Um carregamento para toda a equipa.** Um ficheiro por filial e semana, com um separador por pessoa. Não é preciso ir ficha a ficha.
- **Cada pessoa recebe a sua semana no telemóvel**: o seu horário de cada dia e um trabalho por cada serviço, com a morada onde tem de registar.
- **Nada se guarda sem que o veja antes.** A plataforma mostra o que fará com cada pessoa e só o aplica quando confirma.
- **Corrigir é voltar a carregar.** Se a semana mudar, carregue o ficheiro corrigido: o que já estava é atualizado e nada se duplica.

---

## Como funciona, em três passos

| Passo | O que acontece |
|---|---|
| **1. Descarregar o modelo** | A partir da filial, para a semana que escolher. Traz um separador por cada pessoa da filial. |
| **2. Preenchê-lo e carregá-lo** | Uma linha por trabalho. Ao carregá-lo ainda não se guarda nada. |
| **3. Rever e confirmar** | A plataforma mostra o que fará com cada pessoa. Só ao confirmar se aplica. |

---

## 1. Descarregar o modelo

1. Vá a **Filiais/Projetos** e abra a ficha da filial.
2. No separador **Horários e feriados**, abra **Escala semanal de toda a equipa** e clique em **Importar escala**.
3. Escolha a semana e clique em **Descarregar modelo**.

O modelo traz uma primeira folha com as instruções e a lista das pessoas, e **um separador por pessoa**, com o seu nome.

> **Não apague a linha 1 de nenhum separador**: é a que diz de quem é. Pode mudar o nome dos separadores ou reordená-los sem problema.

Cada separador traz **duas linhas de exemplo** que começam pela palavra **EXCLUIR**: pode apagá-las ou deixá-las, porque não se importam.

### Colunas

| Coluna | O que pôr |
|---|---|
| **Data** * | O dia do trabalho: 19/10/2026. |
| **Hora de início** * | A que horas começa: 08:00. |
| **Hora de fim** * | A que horas acaba: 10:00. |
| **Cliente** | Para quem é o trabalho: a pessoa apoiada, o condomínio, a empresa. |
| **Morada** | Onde se faz. É o local onde a pessoa terá de registar. |
| **Trabalho** | O que se faz: limpeza, acompanhamento, revisão. |
| **Deslocação (min)** | Minutos de deslocação até esse trabalho. |

As colunas com asterisco são obrigatórias. Convém pôr sempre a **morada**: sem ela o trabalho cria-se na mesma, mas poderá ser registado de qualquer sítio.

### O que significa deixar um separador vazio

- **Um separador vazio** deixa essa pessoa como está. Não quer dizer «essa semana não trabalha»: quer dizer que não se diz nada sobre ela.
- **Um separador com trabalhos** é a semana inteira dessa pessoa: os dias sem nenhuma linha ficam livres.

---

## 2. Carregar o ficheiro

Clique em **Escolher ficheiro**, selecione o modelo preenchido e clique em **Ver a proposta**. Aceita-se Excel (.xlsx) até 2 MB, guardado com o Excel ou com qualquer outro programa de folhas de cálculo. Não se aceita CSV, porque um CSV não tem separadores.

Se carregar um ficheiro que não é o modelo, a plataforma indica-o e não lê nada.

---

## 3. Rever o que se fará

Antes de confirmar, cada pessoa aparece com o seu estado, os seus trabalhos e as horas da semana:

| Estado | Significa |
|---|---|
| **Pronta** | Tudo foi lido corretamente. Será aplicada ao confirmar. |
| **Bloqueada** | Algo impede aplicá-la: uma linha mal escrita (indica-se qual), ou trabalhos num dia que para essa pessoa é feriado ou férias. Essa pessoa não se aplica; as outras, sim. |
| **Sem alterações** | O seu separador está vazio. Não se toca. |
| **Separador não reconhecido** | O separador não corresponde a ninguém da filial. Verifique a linha 1. |
| **Separador repetido** | Há dois separadores para a mesma pessoa e não se sabe qual vale. |

Ao lado de cada pessoa aparecem também os avisos que convém ver: dois trabalhos que se sobrepõem, trabalhos sem morada, ou uma deslocação antes do primeiro trabalho mais longa do que a margem que a pessoa tem para registar a entrada.

O que pede atenção aparece primeiro. Para corrigir uma pessoa bloqueada, corrija o ficheiro e clique em **Carregar outro ficheiro**. Se fechar a janela sem confirmar, nada se guarda.

Quando estiver de acordo, clique em **Confirmar**. Com muitas pessoas demora um pouco e vê-se o progresso; pode fechar a janela e a importação continua.

---

## O que cada pessoa vê

Na app, a semana importada: o seu horário de cada dia e os seus trabalhos, cada um com a sua hora e a sua morada. Registará na morada de cada trabalho.

- Com o horário habitual, a jornada de cada dia vai do início do primeiro trabalho ao fim do último.
- Se a pessoa trabalha com **Horário por tarefas**, o seu horário de cada dia são os seus trabalhos, um atrás do outro, com os intervalos entre eles. Um dia sem trabalhos é um dia livre. Na app vê sempre a semana em curso tal como está nesse momento.

---

## Voltar a carregar a mesma semana

Se a semana mudar, preencha o modelo com a versão certa e carregue-o outra vez:

- O que já estava **é atualizado** e nada se duplica.
- Os trabalhos que já não aparecem **são retirados**, exceto os que a pessoa já tenha começado: esses ficam e a revisão avisa.

---

## A semana de uma só pessoa

Na ficha da pessoa, em **Horários e feriados**, abra **Importar escala semanal** e clique em **Carregar uma escala**. Pode fazer o mesmo só para ela:

- **Descarregar modelo** dá-lhe um modelo com o separador dela.
- Também pode carregar o documento que o seu programa de gestão imprime (PDF, Excel ou CSV). Nesse caso a plataforma mostra o que entendeu de cada coluna para que o confirme antes de continuar, e demora um pouco mais.

---

## Quem pode importar

As pessoas com acesso de gestão ao painel da empresa.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Horários base e turnos](./23-horarios-base-e-turnos.md) | O horário habitual, com um ou vários turnos por dia |
| [Feriados e dias não úteis](./29-feriados-e-dias-nao-uteis.md) | Porque é que um trabalho num dia de férias bloqueia essa pessoa |
