# Documentos privados

O campo **Privado** de um documento no CheckBiz360 controla se o funcionário pode ver esse documento a partir da sua aplicação móvel. Quando um documento está marcado como privado, existe no sistema e é acessível aos gestores com as permissões adequadas, mas o funcionário não o verá nem receberá notificações sobre ele.

Este mecanismo permite gerir documentação de carácter sensível —como avaliações de desempenho, cartas de repreensão ou documentos de natureza disciplinar— sem que o funcionário lhe aceda antes de o responsável o considerar oportuno.

## O que significa um documento ser privado

Quando o campo `private` de um documento está ativado:

- O documento **não aparece** na lista de documentos do funcionário na aplicação móvel.
- Não é enviada notificação push ao funcionário, ainda que a opção de notificação esteja marcada.
- O documento **é visível** para os gestores (Manager, Owner) no backoffice.
- O documento pode ser consultado, editado ou eliminado a partir do backoffice pelos utilizadores com permissões suficientes.

Quando o campo `private` está desativado e o documento está publicado:

- O funcionário pode ver e descarregar o documento a partir da aplicação.
- Se a notificação foi ativada ao publicar, o funcionário recebe um aviso push no seu dispositivo.

## Tabela de visibilidade por perfil

A tabela seguinte mostra o que cada perfil pode ver consoante o estado de visibilidade do documento:

| Perfil | Documento privado | Documento não privado (publicado) |
|---|---|---|
| Owner | Visível no backoffice | Visível no backoffice |
| Manager | Visível no backoffice | Visível no backoffice |
| Supervisor | Consoante permissões delegadas | Visível no backoffice (se tiver acesso) |
| Worker (funcionário) | Não visível | Visível na aplicação móvel |

> **Nota:** um supervisor só tem acesso aos documentos dos funcionários da sua equipa e apenas se o manager lhe tiver concedido essa permissão explícita. Consulte o artigo sobre permissões de acesso documental para o detalhe completo.

## Casos de utilização habituais

### Documentos disciplinares

As cartas de repreensão, advertências e outros documentos de natureza disciplinar costumam ser preparados antes de serem entregues formalmente ao funcionário. Carregá-los com visibilidade privada permite tê-los prontos no sistema sem que o funcionário tenha acesso até ao momento em que ocorre a comunicação oficial.

Feita a notificação formal, o responsável altera a visibilidade para pública e o funcionário pode aceder ao documento a partir da aplicação e confirmar a leitura, se lhe for solicitado.

### Avaliações de desempenho

As avaliações de desempenho são documentos confidenciais que devem ser revistos e validados internamente antes de serem partilhados com o funcionário. Mantê-las privadas durante o processo de revisão garante que o funcionário só acede ao resultado final depois de o responsável o ter aprovado.

### Documentação interna de recursos humanos

Alguns documentos são de uso exclusivo do departamento de recursos humanos e não se destinam ao funcionário em momento algum: notas internas, relatórios de acompanhamento ou documentação de natureza administrativa. Nestes casos, o campo privado funciona como controlo permanente de acesso.

## Como alterar a visibilidade de um documento existente

Pode modificar o estado de privacidade de um documento já carregado a qualquer momento. O processo é o seguinte:

1. Aceda à secção **Documentos** do backoffice.
2. Localize o documento que pretende modificar usando os filtros de pesquisa.
3. Abra o detalhe do documento clicando nele.
4. Edite o documento e altere o valor do campo **Privado**.
5. Guarde as alterações.

Se alterar um documento de privado para público, o funcionário poderá vê-lo imediatamente a partir da sua aplicação. Se quiser que receba também uma notificação, terá de a enviar manualmente a partir do painel do documento, pois a mudança de visibilidade por si só não gera uma notificação automática.

> **Importante:** a mudança de visibilidade de privado para público é imediata. Certifique-se de que o documento está no seu estado definitivo antes de o tornar visível para o funcionário, dado que não existe um período de tolerância nem uma confirmação adicional.

Se alterar um documento de público para privado, o funcionário deixará de o ver na sua aplicação de imediato, ainda que já o tivesse consultado ou descarregado.

## Considerações sobre notificações e privacidade

Quando carrega um documento marcado como privado, o sistema não enviará a notificação push ao funcionário ainda que a opção esteja ativada. A notificação só é enviada no momento da publicação se o documento não for privado.

Se carregar um documento como privado, trabalhar nele internamente e posteriormente o tornar público, o fluxo de notificação é gerido manualmente: terá de iniciar a notificação a partir do detalhe do documento se quiser informar o funcionário.

## Artigos relacionados

- [O que é o módulo documental](30-o-que-e-o-modulo-documental.md)
- [Carregar e organizar documentos](31-carregar-e-organizar-documentos.md)
- [Notificações de documentos](34-notificacoes-de-documentos.md)
- [Permissões de acesso documental](37-permissoes-de-acesso-documental.md)
- [Confirmação de leitura](35-assinatura-eletronica.md)
