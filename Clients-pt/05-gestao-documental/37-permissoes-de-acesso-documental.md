# Permissões de acesso documental

O módulo documental do CheckBiz360 aplica um modelo de permissões baseado em perfis que determina que ações cada utilizador pode realizar sobre os documentos. Compreender esta estrutura é fundamental para configurar corretamente o acesso, proteger a documentação sensível e garantir que cada pessoa da organização vê apenas o que lhe diz respeito.

## Perfis e permissões gerais

O CheckBiz360 define quatro perfis principais com diferentes níveis de acesso ao módulo documental:

| Ação | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| Ver documentos próprios | Sim (públicos) | Sim (públicos) | Sim (todos) | Sim (todos) |
| Ver documentos de outros funcionários | Não | Só a sua equipa (se tiver permissão) | Sim (a sua entidade) | Sim (toda a entidade) |
| Carregar documentos | Não | Consoante delegação | Sim | Sim |
| Editar documentos | Não | Consoante delegação | Sim | Sim |
| Eliminar documentos | Não | Não | Sim | Sim |
| Solicitar assinatura | Não | Não | Sim | Sim |
| Confirmar leitura | Sim (os próprios) | Sim (os próprios) | Não aplicável | Não aplicável |
| Ver documentos privados | Não | Consoante delegação | Sim | Sim |
| Exportar documentos | Não | Não | Sim | Sim |

> **Nota:** esta tabela reflete as permissões por omissão de cada perfil. As permissões específicas dos supervisores podem ser alargadas ou restringidas através da delegação configurada pelo manager. As permissões do Owner não são modificáveis.

## Visibilidade de recibos de vencimento e contratos

Os recibos de vencimento e os contratos são os tipos de documentos mais habituais e também os que com maior frequência geram dúvidas sobre quem lhes pode aceder.

### Recibos de vencimento

- **Owner e Manager**: podem ver os recibos de todos os funcionários da entidade, independentemente de estarem marcados como privados ou não.
- **Supervisor**: pode ver os recibos dos funcionários da sua equipa unicamente se o manager lhe tiver concedido acesso explícito aos documentos dessa equipa. Por omissão, o supervisor não tem acesso aos recibos.
- **Worker**: pode ver os seus próprios recibos se não estiverem marcados como privados. Não pode ver os recibos de nenhum outro funcionário.

### Contratos

As mesmas regras aplicam-se aos contratos. Um funcionário pode ver o seu próprio contrato se estiver publicado e não for privado. Não pode ver os contratos dos seus colegas.

## Restrições pelo campo privado

Quando um documento tem o campo `private` ativado, as restrições de visibilidade aplicam-se da seguinte forma:

- O documento é invisível para o funcionário (Worker), independentemente de estar publicado.
- O supervisor só pode ver o documento se tiver permissões delegadas para gerir documentos da equipa afetada e se o manager lhe tiver concedido expressamente acesso a documentos privados.
- O Manager e o Owner podem sempre ver todos os documentos, incluindo os privados.

Esta hierarquia garante que a informação sensível —como notas disciplinares, avaliações ou cartas de repreensão— permanece protegida face a acessos não autorizados.

## Delegação de permissões de Manager para Supervisor

O manager pode alargar as permissões de um supervisor para incluir a gestão documental da sua equipa. Isto permite que o supervisor assuma responsabilidades de carregamento e organização de documentos sem necessidade de lhe dar acesso completo de manager.

A delegação pode abranger:

- **Carregamento de documentos**: o supervisor pode criar e publicar documentos para os funcionários da sua equipa.
- **Edição de documentos**: o supervisor pode modificar os metadados de documentos existentes da sua equipa.
- **Visibilidade de documentos privados**: o supervisor pode ver os documentos marcados como privados dos funcionários da sua equipa.

> **Importante:** a delegação de permissões não transforma o supervisor em manager. O supervisor com permissões documentais alargadas só pode atuar sobre os funcionários da sua equipa atribuída. Não tem acesso à configuração global do módulo, aos documentos de outras equipas nem à exportação em massa do arquivo.

Para configurar a delegação de permissões:

1. Aceda ao backoffice como Manager ou Owner.
2. Navegue até à secção de **Gestão de funcionários** ou **Configuração de equipas**.
3. Selecione o supervisor a quem pretende delegar permissões.
4. Na secção de permissões do supervisor, ative as opções documentais correspondentes.
5. Guarde as alterações.

## Permissões de eliminação

A eliminação de documentos é uma ação irreversível que apenas os utilizadores com perfil Manager ou Owner podem realizar. Antes de eliminar um documento, verifique:

- Se o documento tiver assinatura registada, a eliminação apagará também o registo de rastreabilidade da assinatura.
- Se o documento fizer parte de um processo que deve ser conservado por obrigação legal, não o elimine ainda que a sua utilidade operacional imediata tenha terminado.

Recomenda-se marcar os documentos obsoletos como privados em vez de os eliminar, sobretudo em documentos com assinatura ou com relevância laboral, para conservar o histórico sem expor o documento ao funcionário.

## Artigos relacionados

- [O que é o módulo documental](30-o-que-e-o-modulo-documental.md)
- [Documentos privados](33-documentos-privados.md)
- [Confirmação de leitura](35-assinatura-eletronica.md)
- [Exportar documentos](38-exportar-documentos.md)
- [Carregar e organizar documentos](31-carregar-e-organizar-documentos.md)
