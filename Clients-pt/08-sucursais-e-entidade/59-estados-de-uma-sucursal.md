# Estados de uma sucursal

No CheckBiz360, cada sucursal tem um estado que determina se os funcionários atribuídos podem operar com normalidade ou se o local está temporariamente suspenso. Compreender o significado de cada estado e as consequências de o alterar é fundamental para evitar interrupções não planeadas no registo de assiduidade.

## Estados possíveis

Uma sucursal pode encontrar-se num dos dois estados seguintes:

### Ativa

É o estado normal de operação. Quando uma sucursal está ativa:

- Os funcionários atribuídos podem registar a partir da aplicação sem restrições relacionadas com o estado da sucursal.
- O calendário efetivo e os horários configurados estão em vigor.
- Os relatórios e análises incluem os dados dessa sucursal.
- As notificações e alertas relacionados com a sucursal funcionam normalmente.

Toda a sucursal recém-criada fica no estado ativo por omissão.

### Inativa

Uma sucursal inativa está temporariamente suspensa. Os seus efeitos são os seguintes:

- Os funcionários que tentem registar a partir da aplicação nessa sucursal receberão um erro a indicar que a sucursal não está disponível.
- Não é possível criar novos registos de assiduidade associados a essa sucursal a partir da aplicação.
- Os responsáveis continuam a poder aceder à sucursal a partir do backoffice para consultar dados históricos e modificar a configuração.
- As atribuições de funcionários à sucursal conservam-se intactas.
- O histórico de registos, jornadas e documentos associados à sucursal permanece íntegro e pode ser consultado.

> **Aviso:** desativar uma sucursal produz efeito imediato. Se houver funcionários a tentar registar no momento da alteração, os seus registos serão recusados. Planeie as mudanças de estado fora do horário de trabalho do pessoal afetado ou comunique-as com antecedência.

## Diferença entre desativar e eliminar

Desativar e eliminar são operações distintas com consequências muito diferentes:

| Ação | Efeito sobre os dados | Reversibilidade | Recomendada para |
|---|---|---|---|
| **Desativar** | Os dados históricos conservam-se integralmente | Reversível a qualquer momento | Encerramentos temporários, remodelações, reestruturações |
| **Eliminar** | Os dados da sucursal ficam desassociados da estrutura ativa | Irreversível | Sucursais criadas por erro sem dados associados |

> **Aviso:** o CheckBiz360 não permite eliminar sucursais que tenham registos, jornadas ou documentos associados. Se precisar de encerrar definitivamente uma sucursal com dados históricos, a operação correta é desativá-la e solicitar à equipa de apoio a desassociação definitiva, caso seja necessária para cumprimento da regulamentação de proteção de dados.

Na prática, a grande maioria dos encerramentos de sucursal —temporários ou definitivos— deve ser gerida através da desativação, e não da eliminação.

## Como alterar o estado de uma sucursal

### Desativar uma sucursal ativa

1. Aceda ao backoffice web e navegue até **Sucursais**.
2. Localize a sucursal na listagem. As sucursais ativas são mostradas com um indicador verde.
3. Prima o ícone de edição ou o nome da sucursal para abrir a sua ficha.
4. No campo **Estado**, selecione **Inativa**.
5. O sistema mostrará um aviso com o número de funcionários atribuídos à sucursal que serão afetados.
6. Confirme a operação e prima **Guardar alterações**.

### Reativar uma sucursal inativa

1. Aceda a **Sucursais**.
2. Na listagem, ative o filtro para mostrar sucursais inativas se não aparecerem por omissão.
3. Prima o ícone de edição da sucursal que pretende reativar.
4. No campo **Estado**, selecione **Ativa**.
5. Prima **Guardar alterações**.

A reativação é imediata. Os funcionários atribuídos poderão registar de novo assim que a alteração tiver sido guardada.

## Impacto no histórico de dados

O estado de uma sucursal não altera qualquer dado histórico. Independentemente de uma sucursal estar ativa ou inativa:

- Os registos gravados antes da mudança de estado permanecem no sistema com a sua informação original.
- Os relatórios de períodos anteriores refletem os dados reais desses períodos.
- Os documentos e tarefas associados à sucursal continuam acessíveis aos responsáveis a partir do backoffice.
- Os cálculos de custo e de horas trabalhadas de períodos passados não são afetados.

O estado de uma sucursal é, no essencial, um interruptor operacional que controla se os funcionários podem continuar a gerar novos registos a partir dessa sucursal. Não tem qualquer efeito retroativo.

---

> **Nota de perfil:** a alteração do estado de uma sucursal está disponível para os perfis **Owner** e **Manager** com permissões de administração de organização. O perfil **Supervisor** pode consultar o estado das sucursais a que está atribuído, mas não o pode modificar.

## Artigos relacionados

- [Criar e gerir sucursais](57-criar-e-gerir-sucursais.md)
- [Configuração avançada de sucursal](58-configuracao-avancada-de-sucursal.md)
- [Atribuir funcionários a sucursais](60-atribuir-funcionarios-a-sucursais.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)
