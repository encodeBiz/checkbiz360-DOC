# Criar e gerir funcionários

A gestão da equipa é o ponto de partida de qualquer operação no CheckBiz360. A partir do backoffice, os responsáveis da empresa podem integrar novos funcionários, atualizar a sua informação a qualquer momento e controlar o seu estado laboral ao longo do tempo.

Este artigo explica como criar um funcionário de raiz, que campos são obrigatórios e quais são opcionais, e como gerir os estados que uma pessoa pode atravessar durante a sua relação laboral com a organização.

---

## Criar um novo funcionário

### Campos obrigatórios

- **Nome completo** — Nome e apelidos tal como devem aparecer nos registos.
- **Correio eletrónico** — Endereço único na plataforma. É o identificador do funcionário e o endereço para onde é enviado o acesso inicial. **Não pode ser alterado depois de criado o perfil.**
- **Telefone** — Número de contacto, com indicativo internacional.
- **Tipo de relação** — *Pessoal* (quadro de pessoal da empresa) ou *Colaborador* (externo, freelancer ou prestador de serviços). Aparece na ficha junto ao estado, e não é um dado menor: os colaboradores **não são incluídos no relatório de registo de jornada**, que é obrigatório para a relação laboral. Ver [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md#tipo-de-relação-interno-face-a-colaborador).

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
| **Trabalha fora do centro** | Permite registar fora da geocerca da sucursal (antes chamava-se *Trabalho remoto*). Ao ativá-lo, **a morada do funcionário passa a ser obrigatória**, porque é a referência com que se valida o registo. Ver [Trabalho fora do centro](../03-controlo-de-horarios/15-registo-em-teletrabalho.md) |

---

## Outros campos

- **Documento de identificação** — Útil para auditorias e exportações de recursos humanos.
- **Morada** — Opcional, salvo se o trabalho fora do centro for ativado. Escolhe-se na pesquisa de moradas; não há campo de cidade à parte, porque a morada normalizada já a inclui.
- **Calendário do funcionário** — Horário próprio e exceções, quando diferem dos da sua sucursal. Se não for configurado, o funcionário herda o calendário da sucursal.
- **Dados adicionais** — Campos livres em formato chave/valor para informação própria da sua organização (número de funcionário, convenção coletiva, centro de custo…).

Ao associar o funcionário a uma sucursal definem-se ainda a sua **responsabilidade** nesse local, a sua **função** e a sua **tarifa horária**, sendo esta última a que alimenta a análise de custos.

---

## Estados do funcionário

O CheckBiz360 contempla sete estados laborais, mais o estado **Pendente** para as fichas por completar:

| Estado | Descrição |
|---|---|
| **Pendente** | A ficha existe mas ainda não pode trabalhar, normalmente porque lhe falta o correio eletrónico (é habitual em fichas importadas a partir de uma integração). Não recebe acesso nem correio de boas-vindas, e **não é faturada**. Sai deste estado ao completar o correio. Não se atribui à mão. |
| **Ativo** | O funcionário trabalha com normalidade e tem acesso à plataforma. |
| **Inativo** | O funcionário não está operacional. É o estado usado ao terminar a relação laboral: o perfil e o seu histórico são conservados. |
| **Férias** | O funcionário encontra-se de férias. |
| **Baixa médica** | O funcionário está de baixa por doença. |
| **Licença sem vencimento** | O funcionário goza de uma licença sem vencimento. |
| **Licença de paternidade** | O funcionário está em licença de paternidade. |
| **Licença de maternidade** | A funcionária está em licença de maternidade. |

Para alterar o estado, abra o perfil do funcionário, prima **Editar** e selecione o novo estado. O filtro de estado da listagem de funcionários inclui **Pendente**, para localizar as fichas que falta completar.

> **Importante:** para efeitos de faturação, conta todo o funcionário que não esteja pendente nem eliminado. Um funcionário **Inativo** ou de baixa continua a fazer parte do quadro de pessoal e **é faturado**.

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

## Dar entrada a muitas pessoas de uma vez

Se começa com uma equipa de trinta ou quarenta pessoas, não é preciso criá-las uma a uma. Na lista de funcionários, **Importar** descarrega um modelo de Excel com uma folha para as sucursais e outra para as pessoas; preenche-o, carrega-o e, antes de se criar o que quer que seja, vê o que vai acontecer com cada linha. As boas-vindas à aplicação enviam-se no fim, quando decidir. Explica-se em [Dar entrada a sucursais e equipa a partir de Excel](./110-dar-entrada-a-sucursais-e-equipa-a-partir-de-excel.md).

---

## Artigos relacionados

- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Matriz de permissões por perfil](08-matriz-de-permissoes-por-perfil.md)
- [Autenticação de dois fatores](09-autenticacao-de-dois-fatores.md)
- [Atribuir funcionários a sucursais](../08-sucursais-e-entidade/60-atribuir-funcionarios-a-sucursais.md)
- [Exportar a lista de funcionários](12-exportar-lista-de-funcionarios.md)
- [Equipas](99-equipas.md)
