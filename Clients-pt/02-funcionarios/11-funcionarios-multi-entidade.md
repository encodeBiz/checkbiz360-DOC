# Funcionários multi-entidade

O CheckBiz360 permite que a mesma pessoa esteja associada a várias empresas dentro da plataforma utilizando um único acesso. Este modelo, designado multi-entidade, é habitual em grupos empresariais, organizações com várias denominações sociais ou prestadores de serviços que trabalham em simultâneo para diferentes clientes da plataforma.

O desenho multi-entidade garante que cada empresa mantém a sua informação completamente isolada das restantes, enquanto o funcionário pode mudar de contexto de trabalho com facilidade a partir da mesma aplicação.

---

## Como funciona o modelo multi-entidade

No CheckBiz360, a identidade de um utilizador assenta no seu endereço de correio eletrónico e no seu identificador único (UID). Quando esse email é adicionado como funcionário em mais do que uma entidade (empresa), o sistema reconhece-o como um único utilizador com vários contextos de trabalho.

Cada entidade em que o utilizador está registado tem o seu próprio espaço independente:

- Horários e turnos próprios.
- Sucursais distintas.
- Documentos, contratos e recibos de vencimento separados.
- Tarefas e incidências específicas.
- Perfis e níveis de acesso que podem diferir entre entidades.

Um funcionário pode ser worker numa empresa e supervisor noutra, sem que as permissões de uma se transfiram para a outra.

---

## Fluxo de acesso com várias entidades

Quando um utilizador com acesso a várias entidades inicia sessão no CheckBiz360, o processo é o seguinte:

1. O utilizador introduz o seu email e palavra-passe no ecrã de início de sessão.
2. Se tiver a 2FA ativada, completa a verificação com o código da sua aplicação de autenticação.
3. Após a autenticação, a plataforma deteta que o utilizador pertence a mais do que uma entidade e mostra um **seletor de entidade**.
4. O utilizador seleciona a empresa com a qual pretende trabalhar nessa sessão.
5. A aplicação carrega o contexto completo da entidade selecionada: sucursais, horários, tarefas, documentos e configuração própria.

Se o utilizador pertencer apenas a uma entidade, o seletor não aparece e o acesso é direto.

---

## Token de sessão específico por entidade

Sempre que o utilizador seleciona uma entidade, o sistema gera um token de sessão associado exclusivamente a essa empresa. Este desenho garante que:

- As operações que o utilizador realiza (registos, validações, visualização de documentos) correspondem apenas à entidade ativa.
- Não é possível aceder acidentalmente a dados de outra empresa sem mudar explicitamente de contexto.
- As auditorias de acesso e os rastos de atividade ficam corretamente separados por entidade.

Para mudar de entidade durante o mesmo dia, o utilizador tem de encerrar a sessão ativa e voltar a iniciar sessão, repetindo o processo de seleção de entidade.

---

## Casos de utilização habituais

### Prestadores de serviços externos

Um consultor, técnico de manutenção ou profissional independente pode prestar serviços a vários clientes que utilizam o CheckBiz360. Cada cliente tem a sua própria entidade na plataforma, e o prestador aparece como colaborador em cada uma delas. A partir de uma única aplicação, o prestador pode registar na empresa A de manhã e na empresa B à tarde, com registos completamente independentes.

### Grupos empresariais com várias denominações sociais

Uma corporação pode gerir várias empresas sob diferentes denominações legais, cada uma como entidade distinta no CheckBiz360. Um diretor de recursos humanos corporativo pode estar registado como manager em todas elas, acedendo ao contexto de cada empresa para rever registos, gerir funcionários ou gerar relatórios, sem misturar os dados das diferentes organizações.

### Funcionários com duplo contrato

Nalguns casos, um funcionário pode ter contratos em simultâneo com duas empresas do mesmo grupo. O modelo multi-entidade permite-lhe registar a sua atividade em cada empresa de forma separada, com registos de horário e documentação independentes para cada relação laboral.

---

## Registo de um funcionário em várias entidades

Para que um utilizador apareça em várias entidades, o processo é independente em cada empresa:

1. O manager ou owner de cada entidade tem de criar o perfil do funcionário de forma separada na sua própria empresa, utilizando o mesmo email do utilizador.
2. A plataforma associa automaticamente os perfis ao mesmo UID quando deteta que o email já existe no sistema.
3. Cada entidade pode atribuir ao utilizador o perfil e as sucursais que considerar oportuno, independentemente do que esteja configurado noutras entidades.

> **Nota:** o facto de um utilizador estar registado em várias entidades não implica que possa ver a informação das outras. Cada entidade é um espaço completamente isolado. O utilizador só vê os dados da entidade em que tem a sessão ativa nesse momento.

---

## Quem pode gerir estas configurações

A criação e gestão de perfis de funcionários em cada entidade é da responsabilidade do **manager** (nível 3) ou do **owner** (nível 4) dessa entidade concreta. Não é possível que o responsável de uma empresa faça a gestão de funcionários noutra empresa, ainda que partilhem utilizadores.

---

## Artigos relacionados

- [Criar e gerir funcionários](06-criar-e-gerir-funcionarios.md)
- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Autenticação de dois fatores](09-autenticacao-de-dois-fatores.md)
- [Biometria e dispositivos de confiança](10-biometria-e-dispositivos-de-confianca.md)
