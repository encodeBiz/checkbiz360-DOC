# Criar conta e configurar a entidade

Antes de qualquer funcionário poder registar entradas e saídas, é preciso montar a estrutura base da sua organização no CheckBiz360. É um processo que se faz uma única vez e que deixa os alicerces em que assenta tudo o resto: horários, sucursais, funcionários e políticas de controlo.

Este artigo percorre o caminho desde o registo até ter a primeira sucursal operacional e o primeiro funcionário convidado.

> **Nota:** quem completa este processo fica como **Owner** da entidade. A gestão da subscrição é exclusiva desse perfil; o resto da configuração pode ser delegado depois num Manager.

---

## Conceitos prévios

Três termos estruturam a plataforma:

- **Entidade**: a sua empresa. Contém a configuração global —dados legais, idioma, morada e fuso horário— que se aplica a toda a organização.
- **Sucursal**: cada unidade operacional (loja, escritório, obra, projeto). Herda a configuração da entidade, mas pode ter o seu próprio fuso horário, zona de verificação, horário e feriados.
- **Funcionário**: é associado a uma ou várias sucursais. Em cada associação define-se a sua responsabilidade, a sua função e a sua tarifa. Herda o calendário da sua sucursal, salvo se tiver um próprio.

---

## Passo 1. Criar a conta

O registo faz-se no próprio backoffice, em `saas.encodebiz.com`.

1. Abra `saas.encodebiz.com` em qualquer navegador.
2. A partir do ecrã de acesso, entre no formulário de registo.
3. Preencha os campos, **todos obrigatórios**:
   - **Nome completo**
   - **Correio eletrónico**
   - **Telefone**
   - **Palavra-passe** e a respetiva **confirmação**
4. Aceite os termos e a política de privacidade.
5. Submeta o formulário.

Não há passo intermédio de verificação por correio: ao completar o registo, o sistema leva-o **diretamente ao ecrã de criação da entidade**.

> **Nota:** utilize um endereço de correio empresarial. Esse endereço fica associado como Owner da conta e é para ele que chegam as comunicações administrativas. Se o correio já estiver em uso, o sistema indica-o com o erro `auth/email-already-in-use`.

---

## Passo 2. Criar a entidade

É o ecrã a que chega imediatamente após o registo. Se já estiver dentro do backoffice, acede-se a partir de **Entidade** no menu lateral.

| Campo | Obrigatório | Descrição |
|---|---|---|
| **Nome da empresa** | Sim | Denominação comercial, a que a sua equipa verá na plataforma |
| **Idioma principal** | — | Espanhol ou inglês. Alemão e português estão em desenvolvimento |
| **Denominação social** | Sim | Denominação legal, a que aparece na documentação |
| **Email de faturação** | — | Endereço para onde são enviadas as faturas; é proposto o do registo |
| **NIF / CIF** | — | Identificação fiscal da entidade |
| **Morada** | Sim | Domicílio da empresa. Ao selecioná-la resolvem-se as coordenadas e o **fuso horário**, que funciona como valor por omissão para as sucursais que não tenham um próprio |

Guarde para continuar.

> **Importante:** a denominação social e os dados fiscais não são uma formalidade opcional. **Sem eles não é possível contratar o plano**: o backoffice bloqueia a subscrição até que os dados legais e um método de pagamento estejam completos.

---

## Passo 3. Ativar o CheckBiz

Com a entidade criada, é preciso ativar o serviço. No menu lateral, entre em **CheckBiz** e reveja os planos disponíveis.

Antes de contratar, o sistema verifica dois requisitos e avisa se faltar algum, com ligação ao ecrã correspondente:

- **Dados da empresa** completos.
- **Método de pagamento** configurado.

Recorde que a primeira subscrição inclui **15 dias de experiência**. Consulte [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md).

---

## Passo 4. Criar a primeira sucursal

No menu lateral, dentro do CheckBiz, entre em **Sucursais** e crie uma.

| Campo | Obrigatório | Descrição |
|---|---|---|
| **Nome** | Sim | Identificador da unidade operacional: «Loja Centro», «Escritório Lisboa» |
| **Morada** | Sim | O sistema geocodifica-a para obter as coordenadas e o fuso horário do local |
| **Zona de verificação em metros** | Sim | O raio dentro do qual se aceita um registo. Entre 50 e 200 metros consoante a dimensão do local |
| **NIF** | — | Apenas se o local tiver identificação fiscal própria |
| **Estado** | — | Ativa por omissão |

> **Nota:** a zona de verificação é o que impede registar a partir de fora do local. Um raio demasiado amplo torna-a inútil; um demasiado estreito gera recusas por imprecisão do GPS. Para a maioria dos escritórios e lojas, **100 metros** é um bom ponto de partida, ajustando-se depois com os dados das primeiras semanas.

Guarde. Depois poderá configurar o seu horário semanal a partir de **Calendário**.

---

## Passo 5. Criar o primeiro funcionário

Em **Funcionários**, crie um novo.

1. Preencha os dados obrigatórios: **nome completo**, **correio eletrónico**, **telefone** e **tipo de relação** (interno ou colaborador).
2. Guarde. O sistema cria o perfil e **envia automaticamente o correio de boas-vindas** com as instruções de ativação.
3. Abra a ficha do funcionário e **associe-o à sucursal** que acabou de criar. É nessa associação que se define a sua **responsabilidade** —worker, supervisor, manager ou owner—, a sua **função** e a sua **tarifa horária**.

> **Importante:** o nível de responsabilidade não se escolhe na criação, mas sim na associação a cada sucursal. A mesma pessoa pode ser worker num local e supervisora noutro.

Se o funcionário não receber o correio, consulte a secção correspondente em [Problemas frequentes e soluções](../13-apoio-e-incidencias/88-problemas-frequentes-e-solucoes.md).

---

## Passo 6. Instalar a aplicação

O funcionário precisa da aplicação CheckBiz360 no seu telemóvel para registar entradas e saídas. Está disponível sem custo para iOS e Android.

Ao abri-la pela primeira vez, iniciará sessão com o correio e a palavra-passe que definiu ao ativar a conta a partir do correio de boas-vindas.

---

## Estado no final

Ao completar estes passos, a sua organização tem:

- Uma entidade com os seus dados legais e o seu fuso horário.
- O serviço CheckBiz ativo.
- Uma sucursal operacional com a sua zona de verificação.
- Um funcionário criado, associado a essa sucursal e com acesso à aplicação.

A partir daqui pode repetir os passos 4 e 5 para os restantes locais e pessoas, ou passar ao guia de início rápido para fazer o primeiro registo de teste.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Guia de início rápido](04-guia-de-inicio-rapido.md) | Da criação ao primeiro registo validado |
| [Estrutura da plataforma](05-estrutura-da-plataforma.md) | Entidade, sucursal e funcionário |
| [Criar e gerir sucursais](../08-sucursais-e-entidade/57-criar-e-gerir-sucursais.md) | Campos, geocodificação e estados |
| [Criar e gerir funcionários](../02-funcionarios/06-criar-e-gerir-funcionarios.md) | Criação, estados laborais e opções de segurança |
| [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md) | Preço, experiência de 15 dias e como contratar |
