# Notificações de documentos

Quando se publica um documento no CheckBiz360, o sistema pode enviar automaticamente uma notificação push ao funcionário destinatário. Esta notificação informa o funcionário de que tem um novo documento disponível na aplicação e, ao tocar nela, leva-o diretamente ao ecrã de detalhe do documento correspondente.

As notificações documentais fazem parte do sistema de comunicação do CheckBiz360 e utilizam o mesmo canal de notificações push que o resto da plataforma.

## Como funciona a notificação ao carregar um documento

Quando o responsável publica um documento, pode ativar o envio de notificação push no próprio formulário de carregamento. Se a opção estiver marcada e o documento não estiver configurado como privado, o sistema envia a notificação de forma automática no momento da publicação.

O fluxo completo é:

1. O gestor carrega o documento e ativa a opção de notificação.
2. O sistema verifica que o documento não está marcado como privado.
3. É gerada e enviada uma notificação push para o dispositivo do funcionário.
4. O funcionário vê a notificação no ecrã de bloqueio ou no centro de notificações do seu dispositivo.
5. Ao tocar na notificação, a aplicação do CheckBiz360 abre diretamente no detalhe do documento.

> **Importante:** se o documento estiver marcado como privado, não será enviada notificação push ao funcionário, ainda que a opção de notificação esteja ativa. A notificação só é enviada para documentos com visibilidade pública.

## O que contém a notificação

A notificação que o funcionário recebe inclui a informação necessária para que a aplicação navegue diretamente para o documento correto. Do ponto de vista do funcionário, a notificação mostra o título do documento e o nome da empresa, de forma semelhante a outras notificações da plataforma.

## O que vê o funcionário ao receber a notificação

No dispositivo do funcionário, a notificação aparece com o título do documento como assunto principal. Ao tocar nela, a aplicação abre —ou desperta a partir do segundo plano se já estava instalada— e navega diretamente para o detalhe do documento.

A partir desse ecrã, o funcionário pode:

- Ler o documento completo.
- Descarregá-lo para o seu dispositivo.
- Confirmar a leitura se o documento o exigir.

Se o funcionário não tiver a aplicação instalada ou as notificações push desativadas no seu dispositivo, não receberá o aviso. Nesse caso, o documento continuará disponível na aplicação, na secção de documentos, mas sem o aviso proativo.

## Configurar que documentos geram notificação

A decisão de gerar ou não uma notificação toma-se no momento de carregar o documento, marcando ou desmarcando a opção correspondente no formulário. Não existe uma regra global que ative ou desative as notificações para todos os carregamentos; a escolha é por documento.

Isto permite gerir casos distintos:

- **Documentos que devem notificar sempre**: recibos de vencimento mensais, contratos novos, certificados solicitados pelo funcionário. Ative sempre a notificação para este tipo de documentos.
- **Documentos de arquivo interno que não exigem aviso**: versões corrigidas de documentos já notificados, cópias de segurança ou documentos administrativos que o funcionário pode consultar quando quiser. Nestes casos pode carregar o documento sem notificação.

> **Nota:** se publicar um documento sem notificação e posteriormente quiser informar o funcionário, pode enviar a notificação manualmente a partir do detalhe do documento no backoffice. Isto é útil quando se deteta um erro na notificação original ou quando se pretende reenviar o aviso a um funcionário que não abriu o documento.

## Considerações sobre dispositivos e permissões

Para que o funcionário receba notificações push, é necessário que:

1. Tenha a aplicação do CheckBiz360 instalada no seu dispositivo (iOS ou Android).
2. Tenha concedido permissões de notificação à aplicação durante o processo de instalação ou na configuração do sistema operativo.
3. O dispositivo tenha ligação à internet no momento do envio ou nos momentos posteriores em que o sistema operativo tente a entrega.

Se um funcionário indicar que não recebe notificações, verifique primeiro que as permissões de notificação estão ativadas para a aplicação CheckBiz360 nas definições do seu dispositivo, antes de rever a configuração no backoffice.

## Artigos relacionados

- [O que é o módulo documental](30-o-que-e-o-modulo-documental.md)
- [Carregar e organizar documentos](31-carregar-e-organizar-documentos.md)
- [Documentos privados](33-documentos-privados.md)
- [Confirmação de leitura](35-assinatura-eletronica.md)
- [Permissões de acesso documental](37-permissoes-de-acesso-documental.md)
