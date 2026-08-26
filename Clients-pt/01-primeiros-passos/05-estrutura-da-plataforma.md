# Estrutura da plataforma

O CheckBiz360 organiza a informação em três níveis hierárquicos: entidade, sucursal e funcionário. Esta arquitetura permite que uma empresa com dezenas de locais e centenas de funcionários opere a partir de uma única conta, com configurações diferenciadas por unidade e exceções individuais onde for necessário.

Compreender esta estrutura é fundamental para configurar corretamente os horários, os calendários e as políticas de controlo. Uma configuração bem pensada elimina a necessidade de introduzir dados repetidamente e garante que cada funcionário opera sempre com as regras corretas.

## Os três níveis hierárquicos

### Nível 1: Entidade

A entidade representa a empresa enquanto organização. É o nível mais alto da hierarquia e o contentor de tudo o resto.

A configuração ao nível da entidade estabelece os valores por omissão que se aplicarão a todas as sucursais e funcionários, salvo se algum dos níveis inferiores os substituir explicitamente.

O que se configura ao nível da entidade:

- Dados fiscais e corporativos: nome comercial, denominação social, NIF/CIF e morada.
- Idioma principal e identidade visual.
- Fuso horário por omissão, que resulta da morada da entidade.
- Calendário laboral global: horário semanal base e feriados que afetam toda a organização.
- Faturação e subscrição.

### Nível 2: Sucursal ou projeto

A sucursal é a unidade operacional. Pode representar uma loja, um escritório, uma obra, um departamento ou qualquer outro agrupamento funcional de funcionários.

A sucursal herda toda a configuração da entidade, mas pode substituir os elementos que difiram da configuração global. Isto permite que uma empresa com locais em diferentes regiões tenha calendários de feriados locais distintos sem necessidade de criar contas separadas.

O que se pode configurar ao nível da sucursal:

- Nome, morada e coordenadas GPS.
- Zona de verificação e o respetivo raio em metros.
- Fuso horário próprio, se diferir do da entidade.
- Horário semanal e pausas, que podem diferir dos da entidade.
- Modalidade de jornada e de descanso: estrita ou flexível.
- Calendário de feriados locais.

> **Nota:** uma sucursal não pode ter configurações mais permissivas do que as restrições de segurança definidas ao nível da entidade. Por exemplo, se a entidade exigir 2FA, nenhuma sucursal a pode desativar para os seus funcionários.

### Nível 3: Funcionário

O funcionário é a unidade mínima da hierarquia. É atribuído a uma ou várias sucursais com um perfil determinado e recebe o calendário efetivo resultante da combinação da configuração da entidade com a da sua sucursal.

Em casos específicos —funcionários remotos, trabalhadores com horários irregulares, pessoal em comissão de serviço— é possível definir exceções individuais que substituam os valores da sucursal.

O que se pode configurar ao nível do funcionário:

- Fuso horário próprio (para funcionários remotos noutra região).
- Exceções de horário (alterações pontuais ou periódicas).
- Custo horário (para a análise de custos).
- Documentos associados (contratos, recibos de vencimento, certificados).

## A herança em cascata

O calendário efetivo de um funcionário num dia concreto resolve-se seguindo uma ordem de prioridade clara:

```
Configuração do funcionário  (prioridade máxima)
         |
         v
Configuração da sucursal
         |
         v
Configuração da entidade     (prioridade base)
```

Na prática, isto significa que se a entidade define o horário base como 09:00-17:00, mas a sucursal «Armazém Sul» tem horário 07:00-15:00, e o funcionário Juan García tem uma exceção individual de horário para o turno da tarde (15:00-23:00), o sistema aplicará o horário de Juan García e usará esse como referência para calcular atrasos, ausências e horas extraordinárias.

Esta lógica de herança elimina a necessidade de configurar cada funcionário de raiz e garante que as alterações ao nível da entidade ou da sucursal se propagam automaticamente a todos os funcionários afetados.

## Perfis do backoffice

Os responsáveis que administram a plataforma a partir do backoffice web operam sob um destes três perfis:

| Perfil | Âmbito | Capacidades principais |
|---|---|---|
| Owner | Toda a entidade | Configuração completa, faturação, criação de sucursais, gestão de todos os funcionários, acesso a todos os relatórios |
| Manager | Sucursais atribuídas | Gestão de funcionários e horários nas suas sucursais, acesso a registos e relatórios dos seus locais |
| Supervisor | Sucursais atribuídas | Revisão e validação de registos, gestão de incidências, consulta de relatórios básicos |

> **Nota:** um manager pode gerir várias sucursais em simultâneo. Um funcionário pode ter perfil de manager numa sucursal e perfil de supervisor noutra, se a organização assim o exigir.

## Perfil da aplicação móvel

O perfil **Worker** corresponde ao funcionário que utiliza a aplicação CheckBiz360 para registar entradas e saídas. Este perfil não tem acesso ao backoffice web.

A partir da aplicação, o Worker pode:

- Registar entrada e saída.
- Consultar os seus próprios registos de assiduidade.
- Ver o horário que lhe foi atribuído.
- Receber notificações da plataforma.
- Aceder aos seus documentos laborais (se o módulo documental estiver ativo).
- Consultar e gerir as tarefas atribuídas (se o módulo de tarefas estiver ativo).

## Módulos disponíveis por perfil

| Módulo | Owner | Manager | Supervisor | Worker (aplicação) |
|---|---|---|---|---|
| Controlo de horários e registos | Completo | Por sucursal | Por sucursal | Apenas o próprio |
| Gestão de funcionários | Completo | Por sucursal | Consulta | Não |
| Configuração de horários | Completo | Por sucursal | Não | Não |
| Análise de custos | Completo | Por sucursal | Não | Não |
| Inteligência operacional | Completo | Por sucursal | Resumo | Não |
| Gestão documental | Completo | Por sucursal | Não | Apenas os próprios |
| Tarefas operacionais | Completo | Por sucursal | Por equipa | Apenas as atribuídas |
| Relatórios e exportações | Completo | Por sucursal | Básico | Não |
| Configuração da entidade | Completo | Não | Não | Não |
| Faturação e subscrição | Completo | Não | Não | Não |

> **Nota:** ambos os planos, Bronze e Empresarial, dão acesso a todos os módulos da plataforma; o que muda entre eles é o apoio e as integrações. Consulte [Planos, preços e funcionalidades](../14-referencia/91-planos-e-funcionalidades.md).

## Artigos relacionados

- [O que é o CheckBiz360](01-o-que-e-o-checkbiz360.md)
- [Criar conta e configurar a entidade](03-criar-conta-e-configurar-a-entidade.md)
- [Criar e gerir sucursais](../08-sucursais-e-entidade/57-criar-e-gerir-sucursais.md)
- [Perfis e níveis de responsabilidade](../02-funcionarios/07-perfis-e-niveis-de-responsabilidade.md)
- [Horários base e turnos](../04-calendario-e-horarios/23-horarios-base-e-turnos.md)
