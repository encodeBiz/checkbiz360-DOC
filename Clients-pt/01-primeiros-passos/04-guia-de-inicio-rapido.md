# Guia de início rápido

Este guia permite-lhe ter o CheckBiz360 completamente operacional —com a primeira sucursal configurada, um funcionário ativo e um registo validado— em menos de quinze minutos. Destina-se ao responsável de conta (perfil Owner) que acabou de se registar e quer verificar que tudo funciona corretamente antes de estender a plataforma ao resto da equipa.

Siga os dez passos por ordem. Cada um assenta no anterior.

**Tempo estimado:** 10-15 minutos.

**Pré-requisitos:**
- Ligação à internet.
- Dispositivo Android (5.0 ou superior) ou iOS (13 ou superior).
- Correio eletrónico empresarial para a conta Owner.

---

## Os 10 passos

### Passo 1. Criar conta e entidade

Aceda a `saas.encodebiz.com` e registe-se com o seu correio empresarial, o seu telefone e uma palavra-passe. Ao submeter o formulário, o sistema leva-o diretamente à criação da entidade: **nome da empresa**, **denominação social** e **morada** são obrigatórios; o NIF e o email de faturação, opcionais.

O fuso horário é resolvido a partir da morada e serve de valor por omissão para as sucursais.

> **Nota:** para poder contratar o plano será necessário ter os dados legais completos e um método de pagamento. Consulte [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md).

### Passo 2. Criar a primeira sucursal com geocerca

Entre em **Sucursais** e crie uma:

- **Nome** da sucursal (por exemplo, «Escritório Principal»).
- **Morada** completa do local; dela saem as coordenadas e o fuso horário.
- **Zona de verificação em metros**: comece por **100** se não tiver uma referência.

Guarde a sucursal.

### Passo 3. Configurar o horário da sucursal

Vá a **Calendário** e coloque-se no separador **Sucursal**:

1. Selecione os dias úteis (por exemplo, de segunda a sexta-feira).
2. Estabeleça a hora de entrada e a de saída de cada dia (por exemplo, 09:00-17:00).
3. Escolha a **modalidade de jornada**: estrita, se manda o horário oficial; flexível, se manda o tempo realmente trabalhado.
4. Guarde o calendário.

Este horário é a referência contra a qual o sistema valida cada registo.

> **Nota:** pode adicionar vários turnos por dia e pausas dentro de cada turno. Para este primeiro arranque, um horário simples é suficiente. A alternância automática de semanas A/B não está disponível; consulte [Turnos rotativos](../04-calendario-e-horarios/27-turnos-rotativos.md).

### Passo 4. Criar o primeiro funcionário

Entre em **Funcionários** e crie um novo com os dados obrigatórios: **nome completo**, **correio eletrónico**, **telefone** e **tipo de relação** (interno ou colaborador).

Guarde. Depois, a partir da ficha do funcionário, **associe-o à sucursal**: é aí que se escolhe a sua responsabilidade —para este arranque, *worker*—, a sua função e a sua tarifa horária.

### Passo 5. O funcionário recebe o correio de boas-vindas

O sistema enviará automaticamente um correio ao funcionário com:

- A ligação para ativar a conta e definir a palavra-passe.
- As instruções para descarregar a aplicação.

> **Nota:** se o correio não chegar em poucos minutos, peça ao funcionário que verifique a pasta de spam e confirme que o endereço está bem escrito na sua ficha. Consulte [Problemas frequentes e soluções](../13-apoio-e-incidencias/88-problemas-frequentes-e-solucoes.md).

### Passo 6. O funcionário descarrega a aplicação CheckBiz360

O funcionário descarrega a aplicação a partir da loja oficial do seu dispositivo:

- **iOS**: App Store — procurar «CheckBiz360».
- **Android**: Google Play — procurar «CheckBiz360».

A instalação demora menos de um minuto na maioria dos dispositivos com ligação WiFi.

### Passo 7. O funcionário inicia sessão na aplicação

Com a aplicação instalada, o funcionário:

1. Abre a aplicação CheckBiz360.
2. Introduz o seu correio eletrónico e a palavra-passe que definiu ao ativar a conta.
3. Seleciona a organização se aparecer mais do que uma (habitual quando um funcionário trabalha para várias empresas).
4. Chega ao ecrã principal de registo.

### Passo 8. O funcionário configura a autenticação de dois fatores (2FA)

Embora opcional, recomenda-se ativar a 2FA no primeiro início de sessão. O funcionário ativa-a a partir da secção de segurança do seu perfil, seguindo as instruções no ecrã para associar a sua conta a uma aplicação de autenticação.

> **Nota:** a 2FA pode ser configurada como obrigatória para todos os funcionários a partir da configuração da entidade no backoffice. Se a sua empresa lida com dados sensíveis ou tem requisitos de auditoria, recomenda-se ativar esta opção.

### Passo 9. Primeiro registo de entrada a partir da aplicação

Com o funcionário já na sucursal ou nas suas proximidades:

1. O funcionário abre a aplicação CheckBiz360.
2. Toca no botão **Registar entrada**.
3. A aplicação valida a localização GPS face à geocerca da sucursal.
4. Se a localização estiver correta, o registo fica gravado e aparece uma mensagem de confirmação.

Se a localização não for válida, a aplicação indicará que o dispositivo está fora do perímetro definido.

### Passo 10. Verificar o registo no backoffice

No backoffice, entre em **Assiduidade**.

Verifique que:

- Aparece o registo do funcionário com estado **válido**.
- A hora coincide com o registo efetuado.

Se o registo aparecer como **falhado**, o detalhe indica o código do motivo —fora da zona de verificação, fora de horário— que pode consultar em [Códigos de erro completos](../14-referencia/90-codigos-de-erro-completos.md).

---

## Resultado ao completar os 10 passos

No final deste guia, a sua conta CheckBiz360 tem:

- Uma entidade e uma sucursal configuradas.
- Um funcionário ativo com acesso à aplicação.
- O primeiro registo de assiduidade validado e visível no backoffice.

A partir deste ponto, pode repetir o processo para as restantes sucursais e funcionários, ou explorar os módulos avançados: análise de custos, relatórios de conformidade legal e gestão documental.

## Artigos relacionados

- [Criar conta e configurar a entidade](03-criar-conta-e-configurar-a-entidade.md)
- [Estrutura da plataforma](05-estrutura-da-plataforma.md)
- [Entrada e saída na aplicação](../03-controlo-de-horarios/14-entrada-e-saida-na-aplicacao.md)
- [Criar e gerir sucursais](../08-sucursais-e-entidade/57-criar-e-gerir-sucursais.md)
