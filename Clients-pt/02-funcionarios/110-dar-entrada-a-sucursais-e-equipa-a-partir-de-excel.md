# Dar entrada a sucursais e equipa a partir de Excel

O primeiro dia com o CheckBiz360 costuma começar com uma lista: a contabilidade envia a equipa, tem os centros numa folha, e criar quarenta fichas e seis sucursais uma a uma é uma tarde inteira. Não é preciso. Um modelo de Excel, um carregamento e uma revisão chegam para dar entrada a toda a empresa de uma vez, sem que nada se crie até confirmar.

---

## O que resolve

- **Toda a equipa e todos os centros de uma vez**, a partir de uma folha com dois separadores.
- **Vê antes de criar o que quer que seja.** Cada sucursal e cada pessoa aparece com o que vai acontecer: nova, já existe, acrescentam-se sucursais, sem alterações ou com erro.
- **Um erro não o trava.** As linhas com erro ficam de fora; as restantes são criadas. Corrija o ficheiro e volte a carregá-lo: o que já foi criado não se duplica.
- **As boas-vindas, quando decidir.** Ao importar não se envia nenhum e-mail. Quando tiver verificado que está tudo bem, um botão envia as boas-vindas à aplicação às pessoas novas.
- **Serve para crescer, não só para começar.** Carregue-o outra vez com as pessoas novas: quem já existe é reconhecido pelo e-mail, e as sucursais pelo nome.

---

## Como funciona, em três passos

| Passo | O que acontece |
|---|---|
| **1. Descarregar o modelo** | A partir da lista de funcionários ou da de sucursais, com o botão **Importar**. |
| **2. Preenchê-lo e carregá-lo** | Um separador para as sucursais e outro para as pessoas. Ao carregar não se cria nada ainda. |
| **3. Rever e confirmar** | A plataforma mostra o que fará com cada linha. Só ao confirmar se cria. |

---

## 1. Descarregar o modelo

1. Vá a **Funcionários** (ou a **Sucursais**) e carregue em **Importar**.
2. Na janela **Importar sucursais e equipa**, carregue em **Descarregar modelo**.

O modelo traz dois separadores, **Sucursais** e **Funcionários**, com **linhas de exemplo que começam por ELIMINAR**: pode apagá-las ou deixá-las, não se importam.

> Se uma sucursal já existe no CheckBiz360, não é preciso repeti-la no separador Sucursais: basta escrever o seu nome na linha de cada pessoa.

### Separador Sucursais

| Coluna | O que escrever |
|---|---|
| **Nome** * | Como chama ao centro. É o nome que usará no separador Funcionários. |
| **Morada** * | Rua e número. É onde a sua equipa vai picar o ponto. |
| **Código postal**, **País** | Se não os indicar, completam-se a partir da morada. |
| **NIF** | O desse centro, se tiver um próprio. |
| **Raio de picagem (m)** | Até que distância do centro se admite a picagem. Em branco, o raio habitual. |

Uma morada sem número de porta não chega: se só se localizar de forma aproximada, a linha sai com erro e pede rua e número.

### Separador Funcionários

| Coluna | O que escrever |
|---|---|
| **Nome completo** * | Nome e apelidos. |
| **Email** * | Com ele entra na aplicação e recebe as boas-vindas. É o que identifica a pessoa: se já existir, não se cria outra. |
| **Telefone**, **NIF/CC** | Opcionais. |
| **Cargo** | A sua ocupação. Se ainda não existir no seu catálogo de cargos, é adicionada; a revisão avisa quais são novos. |
| **Tipo** | **Pessoal** ou **Colaborador**. Em branco, pessoal. |
| **Sucursal** * | O nome do seu centro, tal como está no separador Sucursais ou como já se chama no CheckBiz360. Se trabalha em várias, separe-as com ponto e vírgula. |
| **Responsabilidade** | **Trabalhador**, **Supervisor** ou **Gerente** nesse centro. Em branco, trabalhador. |
| **Preço hora** | O que alimenta a análise de custos. Em branco, o do cargo, se já existir. |
| **Horário** | **Semanal** (o habitual) ou **Por tarefas**. Em branco, semanal. |

As colunas com asterisco são obrigatórias.

---

## 2. Carregar o ficheiro

Carregue em **Escolher ficheiro**, selecione o modelo preenchido e carregue em **Rever**. Aceita-se Excel (.xlsx) até 2 MB e 2.000 pessoas. Se carregar um ficheiro que não é o modelo, a plataforma di-lo e não lê nada.

Enquanto lê o ficheiro verifica as moradas, por isso com muitos centros demora uns segundos.

---

## 3. Rever o que se vai fazer

Antes de confirmar vê duas tabelas, **Sucursais** e **Pessoas**, cada linha com o seu estado:

| Estado | Significa |
|---|---|
| **Nova** | Vai ser criada. Nas sucursais, com a morada tal como foi localizada (exata ou aproximada na rua). |
| **Já existe** | Não se toca. |
| **Acrescentam-se sucursais** | A pessoa já existia e ganha os centros novos da sua linha. |
| **Atualiza-se o horário** | Só muda o seu modo de horário. |
| **Sem alterações** | Nada a fazer com essa linha. |
| **Erro** | Essa linha não se importa: a observação diz porquê (uma morada imprecisa, um e-mail mal escrito, uma sucursal que não existe). As restantes linhas importam-se. |

Em cima, um resumo: quantas sucursais e pessoas novas, quantas já existiam, quantas com erro, e quantas pessoas ativas se acrescentam à sua fatura.

Se quiser corrigir algo, corrija o ficheiro e carregue em **Carregar outro ficheiro**. Se fechar a janela sem confirmar, não se cria nada.

Quando estiver conforme, carregue em **Confirmar e importar**. Vê-se o progresso; pode fechar a janela e a importação continua. Se não terminar, **Tentar de novo** continua onde ficou sem duplicar nada.

---

## 4. Enviar as boas-vindas

Ao terminar, a janela diz quantas pessoas novas ainda não receberam as boas-vindas à aplicação. Quando tiver verificado que as suas fichas estão bem, carregue em **Enviar boas-vindas**: cada pessoa recebe o e-mail com que entra pela primeira vez na aplicação. Se preferir enviá-las mais tarde, feche a janela: as pessoas ficam criadas na mesma.

---

## Quem pode importar

Proprietários e administradores da empresa. Cada pessoa ativa criada conta na fatura a partir desse momento, tal como se lhe tivesse dado entrada à mão.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar e gerir funcionários](./06-criar-e-gerir-funcionarios.md) | A entrada de uma só pessoa e os estados da ficha |
| [Criar e gerir sucursais](../08-sucursais-e-entidade/57-criar-e-gerir-sucursais.md) | A entrada de um centro e a sua morada |
| [Perfis e níveis de responsabilidade](./07-perfis-e-niveis-de-responsabilidade.md) | O que pode fazer um trabalhador, um supervisor e um gerente |
| [O seu gestor operacional no Claude ou no ChatGPT](../15-integracoes/109-o-seu-gestor-operacional-no-claude-ou-chatgpt.md) | As mesmas entradas, pedidas ao seu assistente a partir da lista da contabilidade |
