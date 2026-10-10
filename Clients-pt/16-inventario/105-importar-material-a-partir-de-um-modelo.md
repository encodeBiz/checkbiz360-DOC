# Importar material a partir de um modelo

Registar o material artigo a artigo custa quando são dezenas ou centenas. Este guia explica como carregar de uma vez tudo o que há num armazém com uma folha de Excel. Requer o complemento de inventário contratado ou em período de experiência.

---

## Como funciona, em três passos

| Passo | O que acontece |
|---|---|
| **1. Descarregar o modelo** | A partir da ficha do armazém. Há um para consumíveis e outro para operáveis. |
| **2. Preenchê-lo e carregá-lo** | Uma linha por artigo, ou por exemplar se for um operável. Ao carregá-lo ainda não se guarda nada. |
| **3. Rever e importar** | A plataforma mostra o que fará com cada linha. Só ao clicar em **Importar** se regista. |

O modelo está sempre ligado ao armazém a partir do qual se descarrega: tudo o que se importa entra nesse armazém.

---

## 1. Descarregar o modelo

1. Vá a **Inventário → Armazéns** e abra a ficha do armazém.
2. Clique em **Importar** e escolha **Consumíveis** ou **Operáveis**.
3. Clique em **Descarregar modelo**.

São dois modelos porque um consumível e um operável não se descrevem da mesma forma: o primeiro tem quantidade e mínimo; o segundo, identificador do exemplar e unidade de uso. O que se importar com qualquer um dos dois aparece depois na mesma lista de **Existências**.

Cada modelo traz o cabeçalho e **duas linhas de exemplo**. As duas começam pela palavra **EXCLUIR**: pode apagá-las ou deixá-las, porque não são importadas.

### Colunas do modelo de consumíveis

| Coluna | O que pôr |
|---|---|
| **Nome** * | O nome do artigo: «Toalhas», «Desengordurante». |
| **Referência** | O seu código. É o que identifica o artigo se voltar a carregar o ficheiro. |
| **Categoria** | Para o agrupar: limpeza, EPI, papelaria. |
| **Unidade** | Como se conta: unidade, litro, caixa, metro. |
| **Custo unitário** | Quanto custa cada unidade. Usa-se nos relatórios de custo. |
| **Quantidade inicial** | O que há agora no armazém. |
| **Mínimo** | O nível abaixo do qual se avisa os responsáveis. |

### Colunas do modelo de operáveis

| Coluna | O que pôr |
|---|---|
| **Nome** * | O nome do artigo: «Lavadora de pisos industrial». |
| **Referência** | O código do modelo. |
| **Categoria** | Para o agrupar: maquinaria, veículos. |
| **Unidade de uso** * | Horas, km ou dias. O modelo traz uma lista para escolher. |
| **Custo unitário** | Quanto custa cada exemplar. |
| **Identificador** * | O da sua etiqueta: número de série, matrícula. |
| **Etiqueta** | Um nome curto: «a lavadora vermelha». |
| **Leitura do contador** | Horas, km ou dias que tem agora. |

Nos operáveis, **cada linha é um exemplar**. Três lavadoras do mesmo modelo são três linhas com o mesmo nome e referência e três identificadores diferentes. Os dois exemplos do modelo são exatamente isso.

As colunas com asterisco são obrigatórias. Os números podem escrever-se com vírgula ou ponto decimal.

---

## 2. Carregar o ficheiro

Clique em **Escolher ficheiro**, selecione o modelo preenchido e clique em **Rever**. Aceita-se Excel (.xlsx) ou CSV, até 2 MB. Um CSV guardado a partir do Excel com ponto e vírgula também se lê bem.

Se carregar o modelo errado —o de operáveis a partir de **Consumíveis**, ou ao contrário—, a plataforma di-lo e não lê nada.

---

## 3. Rever o que se fará

Antes de importar, cada linha diz o que vai acontecer:

| O que diz | Significa |
|---|---|
| **Novo** | O artigo não existe e será criado. |
| **Atualizado** | O artigo já existe e mudam os seus dados: nome, categoria, unidade ou custo. |
| **Reativado** | O artigo estava arquivado e volta a estar ativo. |
| **Sem alterações** | O artigo já existe e o ficheiro não muda nada. |
| **Exemplar novo** / **Exemplar atualizado** | Nos operáveis, o mesmo para cada exemplar. |
| **Quantidade inicial** | A quantidade entra no armazém. |
| **Já tem existências: a quantidade não se aplica** | Ver mais abaixo. |
| **Exemplo: não é importado** | Uma das linhas que começam por EXCLUIR. |
| **Não é importado** | A linha tem um erro, que se explica ao lado. |

O que pede atenção aparece primeiro: as linhas com erro, e as que se parecem com um artigo que já existe («Parece-se com «Toalha»: confirme que não é o mesmo»).

As linhas com erro não são importadas; as restantes sim. Se as quiser incluir, corrija o ficheiro e clique em **Carregar outro ficheiro**. Se fechar a janela sem importar, não se guarda nada.

Quando estiver de acordo, clique em **Importar**. Com muitas linhas demora um pouco e vê-se o avanço; pode fechar a janela e a importação continua.

---

## Como sabe se um artigo já existe

1. **Pela referência.** Se a linha traz uma referência que um artigo já tem, é esse artigo.
2. **Pelo nome**, se a linha não traz referência ou traz uma que não existe: «Toalhas» e «toalhas» são o mesmo artigo; «Toalhas» e «Toalhas pequenas», não.
3. Se não coincidir com nada, é **novo**.

Por isso convém pôr a referência: assim pode voltar a carregar o mesmo ficheiro, corrigido ou ampliado, e o que já existe é atualizado em vez de duplicado.

### A quantidade inicial só entra uma vez

A **quantidade inicial** só se soma se o artigo não tiver existências nesse armazém. Se já tiver, é ignorada e a revisão di-lo. Mudar o que há num armazém que já funciona é uma **contagem**, com o seu motivo, e faz-se a partir da linha do artigo em **Existências**.

---

## Quem pode importar

Quem pode registar artigos e entradas: **Manager** e **Owner**.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Existências, armazéns e entradas](./101-existencias-armazens-e-entradas.md) | O registo artigo a artigo e o controlo do que há |
| [O que é o inventário](./100-o-que-e-o-inventario.md) | Que problemas resolve e como se contrata |
