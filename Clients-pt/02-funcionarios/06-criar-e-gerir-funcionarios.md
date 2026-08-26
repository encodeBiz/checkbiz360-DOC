# Criar e gerir funcionários

A gestão da equipa é o ponto de partida de qualquer operação no CheckBiz360. A partir do backoffice, os responsáveis da empresa podem integrar novos funcionários, atualizar a sua informação a qualquer momento e controlar o seu estado laboral ao longo do tempo.

Este artigo explica como criar um funcionário de raiz, que campos são obrigatórios e quais são opcionais, e como gerir os estados que uma pessoa pode atravessar durante a sua relação laboral com a organização.

---

## Criar um novo funcionário

### Campos obrigatórios

- **Nome completo** — Nome e apelidos tal como devem aparecer nos registos.
- **Correio eletrónico** — Endereço único na plataforma. É o identificador do funcionário e o endereço para onde é enviado o acesso inicial. **Não pode ser alterado depois de criado o perfil.**
- **Telefone** — Número de contacto, com indicativo internacional.
- **Tipo de relação** — *Interno* (quadro de pessoal) ou *Colaborador* (externo, freelancer ou prestador de serviços).

> **Importante:** o nível de responsabilidade —worker, supervisor, manager ou owner— **não é atribuído na criação**. Define-se ao associar o funcionário a uma sucursal, porque a mesma pessoa pode ter responsabilidades distintas em cada local. Consulte [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md).

### Passos para criar um funcionário

1. Aceda ao backoffice com credenciais de manager ou owner.
2. No menu lateral, selecione **Funcionários** e prima o botão de novo funcionário.
3. Complete os dados pessoais obrigatórios.
4. Ajuste as opções de segurança e os dados adicionais de que precise.
5. Configure o calendário do funcionário se diferir do da sua sucursal.
6. Guarde. O sistema cria o perfil e envia o correio de boas-vindas.
7. Associe o funcionário à sua sucursal e atribua-lhe aí a sua responsabilidade e a sua função.

### Email de boas-vindas automático

Ao guardar o perfil, o CheckBiz360 envia automaticamente um correio ao funcionário com as instruções para ativar a sua conta e aceder à aplicação móvel. Não exige qualquer ação adicional do administrador.

---

## Opções de segurança e de trabalho

Três opções ativam-se ou desativam-se por funcionário:

| Opção | O que faz |
|---|---|
| **Verificação em dois passos (2FA)** | Exige um código temporário além da palavra-passe |
| **Biometria obrigatória** | O funcionário tem de se autenticar com impressão digital ou reconhecimento facial antes de o seu registo ser aceite |
| **Trabalho remoto** | Permite registar fora da geocerca da sucursal. Ao ativá-lo, **a morada do funcionário passa a ser obrigatória**, porque é a referência com que se valida o registo remoto |

---

## Outros campos

- **Documento de identificação** — Útil para auditorias e exportações de recursos humanos.
- **Morada** — Opcional, salvo se o trabalho remoto for ativado.
- **Calendário do funcionário** — Horário próprio e exceções, quando diferem dos da sua sucursal. Se não for configurado, o funcionário herda o calendário da sucursal.
- **Dados adicionais** — Campos livres em formato chave/valor para informação própria da sua organização (número de funcionário, convenção coletiva, centro de custo…).

Ao associar o funcionário a uma sucursal definem-se ainda a sua **responsabilidade** nesse local, a sua **função** e a sua **tarifa horária**, sendo esta última a que alimenta a análise de custos.

---

## Estados do funcionário

O CheckBiz360 contempla sete estados laborais:

| Estado | Descrição |
|---|---|
| **Ativo** | O funcionário trabalha com normalidade e tem acesso à plataforma. |
| **Inativo** | O funcionário não está operacional. É o estado usado ao terminar a relação laboral: o perfil e o seu histórico são conservados. |
| **Férias** | O funcionário encontra-se de férias. |
| **Baixa médica** | O funcionário está de baixa por doença. |
| **Licença sem vencimento** | O funcionário goza de uma licença sem vencimento. |
| **Licença de paternidade** | O funcionário está em licença de paternidade. |
| **Licença de maternidade** | A funcionária está em licença de maternidade. |

Para alterar o estado, abra o perfil do funcionário, prima **Editar** e selecione o novo estado.

> **Nota:** os estados de ausência (férias, baixas, licença sem vencimento) também podem ser geridos como **ausências com datas** a partir do calendário, o que permite planeá-las com antecedência em vez de mudar o estado à mão no dia em que começam.

---

## Editar os dados de um funcionário

1. Aceda a **Funcionários** no menu lateral.
2. Localize o funcionário com a pesquisa ou os filtros.
3. Clique no seu nome para abrir o perfil.
4. Selecione **Editar** e efetue as alterações.
5. Guarde.

As alterações produzem efeito de imediato. O correio eletrónico é o único dado que não pode ser alterado.

---

## Desativar face a eliminar um funcionário

Estas duas ações têm consequências muito distintas:

- **Desativar** (estado *Inativo*): o funcionário perde o acesso à plataforma, mas todo o seu histórico —registos, documentos, tarefas, incidências— é conservado integralmente. É a opção correta quando termina a relação laboral ou quando é preciso suspender o acesso temporariamente.
- **Eliminar**: apaga o perfil de forma permanente. É irreversível. Reserve esta ação para casos excecionais, como um perfil criado por erro ou duplicado.

> **Importante:** o registo de jornada deve ser conservado durante quatro anos ao abrigo do RDL 8/2019. Desativar, e não eliminar, é o que permite cumprir essa obrigação.

---

## Quem pode realizar estas ações

A gestão de perfis está disponível para **manager** (nível 3) e **owner** (nível 4). Supervisores e workers não têm acesso à gestão de perfis de outros funcionários.

---

## Artigos relacionados

- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Matriz de permissões por perfil](08-matriz-de-permissoes-por-perfil.md)
- [Autenticação de dois fatores](09-autenticacao-de-dois-fatores.md)
- [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md)
- [Exportar a lista de funcionários](12-exportar-lista-de-funcionarios.md)
