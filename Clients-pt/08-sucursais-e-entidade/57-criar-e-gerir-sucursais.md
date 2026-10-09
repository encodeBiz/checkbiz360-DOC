# Criar e gerir sucursais

Uma sucursal no CheckBiz360 representa uma unidade operacional física ou lógica à qual se atribuem funcionários e a partir da qual se controla o registo de ponto. Pode corresponder a uma loja, um escritório, um local de trabalho ou qualquer outra unidade que a empresa precise de gerir de forma independente. Este artigo explica como criar a primeira sucursal, como completar a sua configuração e como editá-la ou desativá-la posteriormente.

## Requisitos prévios

Para criar e gerir sucursais precisa de aceder ao backoffice web com um perfil de **Owner** ou **Manager** com permissões de administração de sucursais. Se não dispuser das permissões necessárias, contacte o Owner da sua entidade.

## Criar uma sucursal

### Campos obrigatórios

Ao criar uma sucursal terá de preencher os seguintes campos:

- **Nome**: identificador visível da sucursal em todo o sistema. Utilize um nome claro e único dentro da sua organização (por exemplo, «Lisboa Centro» ou «Armazém Norte»).
- **Morada**: morada postal completa do local de trabalho, escolhida na pesquisa. O sistema obtém dela as coordenadas GPS que serão utilizadas como ponto central da geocerca de registo, e preenche automaticamente o **país** e o **código postal**. Não há campo de cidade: a morada normalizada já a inclui. É importante que a morada seja precisa para garantir a exatidão das coordenadas.
- **Raio de registo**: distância em metros a partir do ponto central da sucursal dentro da qual o sistema considera válido um registo por geolocalização. Um raio de 100 metros é o valor recomendado para escritórios em ambientes urbanos; pode ser alargado para instalações industriais ou espaços abertos.
- **Fuso horário**: faz parte da morada e determina como se interpretam as horas de registo e como se calculam as jornadas. É especialmente relevante em organizações com locais em diferentes países ou regiões. Se não for indicado, a sucursal herda o fuso horário da entidade.

### Campos opcionais

- **NIF**: identificador fiscal do local, quando difere do da entidade.
- **Estado**: ativa ou inativa. Por omissão, uma sucursal recém-criada fica ativa.
- **Dados adicionais**: campos livres em formato chave/valor para informação própria da sua organização.
- **Calendário**: horário semanal, pausas e modalidade de jornada. Se não for configurado, a sucursal herda o calendário da entidade.

### Passos para criar a primeira sucursal

1. Aceda ao backoffice em `saas.encodebiz.com` e inicie sessão com as suas credenciais.
2. No menu lateral, selecione **Sucursais** (ou o nome que a sua entidade dê aos seus locais).
3. Prima o botão de criar sucursal.
4. Introduza o nome da sucursal no campo correspondente.
5. Escreva a morada postal completa no campo **Morada**. Selecione a sugestão que aparece na lista de preenchimento automático para se assegurar de que o sistema obtém as coordenadas corretas.
6. Verifique que o mapa interativo mostra o marcador na posição correta. Se a posição não for exata, pode arrastar o marcador manualmente para a ajustar.
7. Introduza o raio de registo em metros. Se não tiver um critério definido, comece com 100 metros e ajuste-o após as primeiras semanas de operação.
8. Verifique o fuso horário associado à morada.
9. Complete os campos opcionais se o considerar necessário.
10. Prima **Guardar**. O sistema confirmará a criação com uma mensagem de sucesso e a nova sucursal aparecerá na listagem.

> **Aviso:** se a geocodificação da morada não devolver coordenadas precisas, o sistema indicá-lo-á com uma advertência. Nesse caso, ajuste o marcador manualmente no mapa antes de guardar. Coordenadas incorretas gerarão recusas de registo injustificadas para os funcionários atribuídos.

> **Nota:** o código postal admite letras, espaços e hífenes, de modo que é possível criar locais fora de Espanha («EC2V 8AS», «3512 EN», «K1A 0B1»). O país é retirado da morada escolhida; se o seu local estiver noutro país, procure-o com a morada completa.

> **Nota:** ao ativar o serviço, o CheckBiz360 cria uma primeira sucursal com os dados da empresa. Reveja-a antes de criar outras.

## Editar uma sucursal

Para modificar os dados de uma sucursal existente:

1. Aceda a **Sucursais** no menu lateral.
2. Localize a sucursal que pretende editar e clique no seu nome ou no ícone de edição.
3. Modifique os campos que precisar de atualizar.
4. Se alterar a morada, o sistema geocodificará de novo e atualizará as coordenadas. Verifique o mapa antes de guardar.
5. Prima **Guardar alterações**.

> **Aviso:** as alterações no raio de registo ou nas coordenadas produzem efeito imediato. Os funcionários que estejam a tentar registar nesse momento podem ser afetados transitoriamente.

Editar só altera o que modificar. Em particular, se a sucursal tiver a **zona de verificação desativada**, guardar outras alterações não a volta a ativar.

Se a sucursal tiver sido criada por uma integração (por exemplo, uma montagem importada do Rentman), a sua ficha mostra um distintivo com a origem. Pode editá-la normalmente; os dados de proveniência que a integração guarda não se perdem ao guardar.

## Desativar uma sucursal

Desativar uma sucursal impede que os funcionários atribuídos possam registar a partir dela, mas conserva todo o histórico de dados. Esta operação é reversível.

1. Aceda a **Sucursais**.
2. Prima o ícone de edição da sucursal que pretende desativar.
3. Mude o campo **Estado** para **Inativa**.
4. Prima **Guardar alterações**.

O sistema mostrar-lhe-á um aviso a indicar quantos funcionários estão atribuídos a essa sucursal e serão afetados. Consulte o artigo sobre estados de uma sucursal para compreender o impacto completo desta ação.

---

> **Nota de perfil:** a criação e edição de sucursais está disponível para os perfis **Owner** e **Manager** com permissões de administração de organização. A consulta da listagem de sucursais também está disponível para **Supervisor**.

## Artigos relacionados

- [Configuração avançada de sucursal](58-configuracao-avancada-de-sucursal.md)
- [Estados de uma sucursal](59-estados-de-uma-sucursal.md)
- [Atribuir funcionários a sucursais](60-atribuir-funcionarios-a-sucursais.md)
- [Configuração da entidade](61-configuracao-da-entidade.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)
