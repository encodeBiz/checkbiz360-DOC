# O que é o módulo documental

O módulo documental do CheckBiz360 permite às empresas gerir, distribuir e arquivar documentos laborais diretamente na plataforma. Ao contrário de um repositório genérico de ficheiros, cada documento fica associado a um funcionário concreto e à sua relação laboral com a entidade, o que transforma o sistema num processo digital de pessoal estruturado e rastreável.

O módulo faz parte da subscrição: está disponível em **Documentos**, no menu lateral do backoffice, independentemente do plano contratado.

## Para que serve

A gestão documental no CheckBiz360 responde a uma necessidade habitual nos departamentos de recursos humanos: distribuir documentos laborais de forma ordenada, garantir que o funcionário os recebe e os pode consultar, e manter um arquivo digital organizado por tipo de documento e período.

Com o módulo documental pode:

- Carregar recibos de vencimento, contratos, certificados e outros documentos laborais a partir do backoffice.
- Dirigir cada documento a um funcionário concreto, a toda uma sucursal ou a toda a entidade.
- Enviar uma notificação push ao funcionário no momento da publicação.
- Controlar que perfis podem ver cada documento.
- Exigir **confirmação de leitura** e verificar quem a deu e quem não.
- Arquivar um documento quando deixa de estar em vigor, sem o perder.

## Tipos de documentos que se podem gerir

O módulo classifica os documentos em doze tipos:

| Tipo | Exemplos habituais |
|---|---|
| Recibo de vencimento | Recibo salarial mensal, acerto final |
| Contrato | Contrato inicial, renovações, alterações de condições |
| Repreensão | Carta de repreensão disciplinar |
| Chamada de atenção | Aviso prévio, advertência formal |
| Comprovativo | Comprovativos de ausência e de licenças |
| Certificado | Certificado de empresa, de carreira contributiva, de retenções |
| Política | Política de empresa, código de conduta |
| Procedimento | Instrução de trabalho, protocolo operacional |
| Prevenção de riscos | Avaliação de riscos, formação em segurança, entrega de EPI |
| Protocolo de sucursal | Normas específicas de um local de trabalho |
| Documento de projeto | Documentação associada a um projeto ou cliente |
| Outro | Qualquer documento que não se enquadre nos anteriores |

O tipo é atribuído ao carregar o documento e facilita os filtros de pesquisa, tanto para os gestores como para o funcionário a partir da aplicação.

### Âmbito do documento

Além do tipo, cada documento tem um **âmbito** que determina a quem se dirige:

- **Funcionário** — um documento pessoal, como um recibo de vencimento ou um contrato.
- **Sucursal** — dirigido a todo o pessoal de um local, como um protocolo de abertura.
- **Entidade** — dirigido a todo o quadro de pessoal, como uma política de empresa.

## Diferença face a um sistema de armazenamento genérico

Um serviço de armazenamento genérico —como uma pasta partilhada na nuvem— guarda ficheiros sem contexto. O CheckBiz360 não é isso.

No CheckBiz360, cada documento sabe a quem pertence, a que relação laboral corresponde, que perfil o pode ver e se o funcionário confirmou a leitura ou não. Isto permite, por exemplo, que quando um funcionário abre a aplicação veja apenas os seus próprios documentos e não os do resto da equipa, ou que um manager possa filtrar todos os contratos em vigor da sua sucursal sem ter de organizar pastas manualmente.

Esta associação ao funcionário e à sua relação laboral é o que faz do módulo um processo de pessoal e não um armazém de ficheiros.

## Casos de utilização por perfil

### Responsável de recursos humanos ou Manager

Todos os meses, o responsável carrega os recibos de vencimento dos funcionários a partir do backoffice. Seleciona o ficheiro, indica a categoria, o período e o funcionário destinatário, e marca se pretende enviar uma notificação push. O funcionário recebe a notificação no seu dispositivo e, ao tocar nela, acede diretamente ao documento na aplicação.

Se o documento exigir **confirmação de leitura**, o responsável ativa essa opção antes de publicar. O sistema regista a data e a hora em que o funcionário confirma a leitura, e sobre que versão do documento o fez.

### Supervisor

O supervisor pode consultar os documentos dos funcionários da sua equipa cuja visibilidade o permita. O carregamento e a configuração de visibilidade reservam-se habitualmente ao nível de manager ou superior; alguns tipos de documento estão ainda restritos por perfil e devolvem o erro `documents/restricted_document_type` a quem não tem nível suficiente.

### Funcionário (Worker)

O funcionário acede aos seus documentos a partir da aplicação móvel, na secção de documentos. Só vê os que lhe foram atribuídos e cuja visibilidade o alcança. Pode descarregá-los e, se lhe for solicitado, **confirmar a leitura** a partir do próprio dispositivo.

> **Nota:** a confirmação de leitura não é uma assinatura eletrónica. Comprova que o funcionário acedeu ao documento e quando, mas não incorpora certificação qualificada. A assinatura eletrónica avançada (eIDAS) está no roadmap.

> **Nota:** os documentos marcados como privados pelo gestor não são visíveis para o funcionário até que o responsável decida publicá-los ou altere o seu estado de visibilidade. Consulte o artigo sobre documentos privados para mais detalhe.

## Artigos relacionados

- [Carregar e organizar documentos](31-carregar-e-organizar-documentos.md)
- [Recibos de vencimento e contratos](32-recibos-de-vencimento-e-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificações de documentos](34-notificacoes-de-documentos.md)
- [Confirmação de leitura](35-assinatura-eletronica.md)
- [Histórico de versões](36-historico-de-versoes.md)
- [Permissões de acesso documental](37-permissoes-de-acesso-documental.md)
- [Exportar documentos](38-exportar-documentos.md)
