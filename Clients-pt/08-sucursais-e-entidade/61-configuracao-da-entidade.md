# Configuração da entidade

A entidade é o nível organizativo superior do CheckBiz360: representa a empresa que contratou o serviço e engloba sucursais, funcionários e dados. O que aqui se configura funciona como referência para toda a estrutura.

Acede-se a partir de **Entidade** no menu lateral, e o ecrã está organizado em seis separadores.

---

## Os seis separadores

| Separador | O que contém |
|---|---|
| **Dados da Empresa** | Nome comercial, idioma principal, denominação social, NIF/CIF, email de faturação e morada |
| **Ambiente de trabalho** | Como se chamam as coisas na sua organização: por exemplo, se os seus locais se chamam *Sucursal*, *Projeto* ou *Obra* |
| **Configurar Faturação** | Métodos de pagamento da conta |
| **Subscrições** | Plano contratado e o seu estado |
| **Faturas** | Histórico de faturação |
| **Colaboradores** | Utilizadores com acesso ao backoffice desta entidade |

**Dados da Empresa** e **Configurar Faturação** mostram um aviso visual enquanto estiverem incompletos. Não é decorativo: **sem denominação social e sem método de pagamento não é possível contratar o plano**.

---

## Ambiente de trabalho

Antes chamava-se *Identidade visual*. Já não configura cores nem imagens: serve para adaptar o nome dos locais de trabalho ao vocabulário da sua organização. Se os seus locais forem projetos ou obras, o backoffice di-lo-á assim no menu, nas listagens e nas fichas —por exemplo, «Detalhes de Obra»—. Deixar o campo em branco usa o nome por omissão.

Neste mesmo separador está **Ligar ao Claude ou ao ChatGPT**: o endereço de ligação da sua empresa e os passos para o adicionar ao seu assistente, para lhe poder pedir a semana, as entradas e as alterações nas suas próprias palavras. Explica-se em [O seu gestor operacional no Claude ou no ChatGPT](../15-integracoes/109-o-seu-gestor-operacional-no-claude-ou-chatgpt.md).

---

## Colaboradores

Os colaboradores são as pessoas com acesso ao backoffice da entidade, cada uma com o seu perfil: **Proprietário** ou **Administrador**. São convidados por correio a partir do separador **Colaboradores**.

- **Convite.** Enquanto a pessoa não entra, o seu convite figura como *Aceitação pendente*. Dá-se por aceite assim que inicia sessão com a entidade atribuída; não depende de premir nada nas boas-vindas.
- **Quem gere.** Convidar, mudar o perfil ou retirar colaboradores cabe a proprietários e administradores com acesso **ativo**; um convite por aceitar ou um acesso desativado não permitem gerir ninguém.
- **O escalão de proprietário.** Só um proprietário pode nomear outro proprietário ou retirá-lo.
- **Nunca sem proprietário.** Não é possível retirar o **único proprietário ativo** da entidade: adicione antes outro proprietário.

Retirar um colaborador elimina as suas permissões sobre a entidade e não pode ser desfeito; para lhe devolver o acesso é preciso convidá-lo de novo.

---

## Dados da empresa

| Campo | Obrigatório | Para que serve |
|---|---|---|
| **Nome da empresa** | Sim | Denominação comercial, a que a sua equipa vê na plataforma |
| **Idioma principal** | — | Espanhol ou inglês. Alemão e português estão em desenvolvimento |
| **Denominação social** | Sim | Denominação legal. Necessária para contratar e para a documentação |
| **NIF / CIF** | — | Identificação fiscal da entidade |
| **Email de faturação** | — | Endereço para onde chegam as faturas |
| **Morada** | Sim | Domicílio da empresa, escolhido na pesquisa de moradas. Dela saem as coordenadas e o **fuso horário**. Não há campo de cidade à parte: a morada normalizada já a inclui |

Não existe um campo de «setor de atividade»: a plataforma não classifica a entidade por setor nem ajusta nada em função dele.

---

## Fuso horário

O fuso horário da entidade é retirado da sua morada e funciona como **valor por omissão** para as sucursais que não tenham um próprio. Se toda a sua organização operar no mesmo fuso, basta deixar que as sucursais o herdem.

> **Aviso:** ao mudar a morada da entidade, o novo fuso horário só afeta as sucursais que não tenham um configurado. As que têm o seu não são alteradas.

---

## Segurança

A verificação em dois passos ativa-se **por utilizador e por funcionário**, não como política global da entidade: cada ficha de funcionário tem a sua própria opção de 2FA, e cada utilizador pode ativá-la a partir da secção de segurança da sua conta.

> **Estado: Não disponível**
> Uma política de 2FA obrigatória para toda a entidade, que force todos os utilizadores do backoffice a configurá-la, não está implementada na versão atual.

Se a sua organização precisar de 2FA generalizada, ative-a funcionário a funcionário na sua ficha. Consulte [Autenticação de dois fatores](../02-funcionarios/09-autenticacao-de-dois-fatores.md).

---

## Faturação e subscrição

A partir de **Subscrições** o Owner consulta o plano contratado e o seu estado, e a partir de **Faturas** o histórico. Os métodos de pagamento são geridos em **Configurar Faturação**.

A faturação do plano Bronze é **por funcionário e mês**: não há uma quota de funcionários incluídos que se possa esgotar. Consulte [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md).

---

## Como a configuração se propaga às sucursais

Os valores da entidade são a referência que as sucursais herdam ou substituem:

1. **Entidade**: define o valor global por omissão.
2. **Sucursal**: se definir o seu, tem prioridade.
3. **Funcionário**: se definir o seu, tem prioridade sobre o da sua sucursal.

Por exemplo, com a entidade em `Europe/Madrid` e uma sucursal nas Canárias com `Atlantic/Canary`, essa sucursal usa o seu e as restantes herdam Madrid. O mesmo acontece com o calendário: horário semanal, pausas e modalidade de jornada descem em cascata por esses três níveis.

Os dados fiscais e a faturação não têm equivalente na sucursal: são estritamente globais.

---

## Diferença entre configuração de entidade e de sucursal

| Aspeto | Entidade | Sucursal |
|---|---|---|
| Âmbito | Toda a organização | Um único local de trabalho |
| Acesso | Owner | Owner e Manager |
| Parâmetros exclusivos | Dados fiscais, ambiente de trabalho, colaboradores, faturação e subscrição | Zona de verificação e o seu raio |
| Herança | Valor por omissão | Substitui o da entidade |
| Impacto de uma alteração | Toda a organização | Apenas esse local e os seus funcionários |

A regra é simples: o que afeta a empresa como um todo configura-se na entidade; o que é próprio de um local, na sucursal.

---

## Como aceder

1. Inicie sessão no backoffice com uma conta **Owner**.
2. No menu lateral, selecione **Entidade**.
3. Coloque-se no separador de que precisa e modifique os parâmetros.
4. Guarde.

> **Aviso:** as alterações nos dados fiscais afetam a documentação gerada a partir desse momento; não alteram faturas nem relatórios já emitidos.

---

> **Nota de perfil:** a configuração da entidade, e em particular a subscrição, compete ao **Owner**. Para delegar a gestão do dia a dia —sucursais, funcionários, tarefas e documentos— use o perfil **Manager**.

---

## Assinatura eletrónica

No separador **Ambiente de trabalho** há uma secção **Assinatura eletrónica** com o certificado do CheckBiz360 e os passos para o instalar no Acrobat Reader, para que os PDF assinados pelos seus trabalhadores apareçam a verde. Explica-se em [Confirmação de leitura e assinatura eletrónica](../05-gestao-documental/35-assinatura-eletronica.md).

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar conta e configurar a entidade](../01-primeiros-passos/03-criar-conta-e-configurar-a-entidade.md) | O processo completo de registo |
| [Criar e gerir sucursais](./57-criar-e-gerir-sucursais.md) | Campos, geocodificação e estados |
| [Configuração avançada de sucursal](./58-configuracao-avancada-de-sucursal.md) | Zona de verificação, horário e modalidade de jornada |
| [Herança de configuração](../04-calendario-e-horarios/26-heranca-de-configuracao.md) | Como se resolve o calendário efetivo |
| [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md) | Preço, experiência de 15 dias e como contratar |
