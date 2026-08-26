# Configuração da entidade

A entidade é o nível organizativo superior do CheckBiz360: representa a empresa que contratou o serviço e engloba sucursais, funcionários e dados. O que aqui se configura funciona como referência para toda a estrutura.

Acede-se a partir de **Entidade** no menu lateral, e o ecrã está organizado em seis separadores.

---

## Os seis separadores

| Separador | O que contém |
|---|---|
| **Dados da Empresa** | Nome comercial, idioma principal, denominação social, NIF/CIF, email de faturação e morada |
| **Identidade visual** | Logótipo e cores de marca da entidade |
| **Configurar Faturação** | Métodos de pagamento da conta |
| **Subscrições** | Plano contratado e o seu estado |
| **Faturas** | Histórico de faturação |
| **Colaboradores** | Utilizadores com acesso ao backoffice desta entidade |

Os três primeiros mostram um aviso visual enquanto estiverem incompletos. Não é decorativo: **sem denominação social e sem método de pagamento não é possível contratar o plano**.

---

## Dados da empresa

| Campo | Obrigatório | Para que serve |
|---|---|---|
| **Nome da empresa** | Sim | Denominação comercial, a que a sua equipa vê na plataforma |
| **Idioma principal** | — | Espanhol ou inglês. Alemão e português estão em desenvolvimento |
| **Denominação social** | Sim | Denominação legal. Necessária para contratar e para a documentação |
| **NIF / CIF** | — | Identificação fiscal da entidade |
| **Email de faturação** | — | Endereço para onde chegam as faturas |
| **Morada** | Sim | Domicílio da empresa. Dela saem as coordenadas e o **fuso horário** |

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
| Parâmetros exclusivos | Dados fiscais, identidade visual, faturação e subscrição | Zona de verificação e o seu raio |
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

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Criar conta e configurar a entidade](../01-primeiros-passos/03-criar-conta-e-configurar-a-entidade.md) | O processo completo de registo |
| [Criar e gerir sucursais](./57-criar-e-gerir-sucursais.md) | Campos, geocodificação e estados |
| [Configuração avançada de sucursal](./58-configuracao-avancada-de-sucursal.md) | Zona de verificação, horário e modalidade de jornada |
| [Herança de configuração](../04-calendario-e-horarios/26-heranca-de-configuracao.md) | Como se resolve o calendário efetivo |
| [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md) | Preço, experiência de 45 dias e como contratar |
