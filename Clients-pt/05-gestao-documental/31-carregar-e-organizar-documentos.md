# Carregar e organizar documentos

O backoffice do CheckBiz360 centraliza todo o processo de carregamento e distribuição de documentos laborais. A partir de um único painel pode carregar ficheiros, atribuí-los aos funcionários correspondentes, definir a sua visibilidade e organizar o arquivo documental por categorias e períodos.

## Antes de começar

Para carregar documentos precisa de ter o perfil de Manager ou Owner na entidade. Os supervisores podem ter acesso a esta função se o manager lhes tiver delegado essa permissão. Se não vir a opção de carregamento no seu painel, confirme com o responsável da entidade as suas permissões.

Os formatos aceites são PDF e imagens (JPG, PNG), com um **máximo de 10 MB por ficheiro**. Um ficheiro maior é recusado com o erro `documents/file_too_large`, e um formato não admitido com `documents/invalid_mime_type`.

Recomenda-se o PDF: é o que garante que o documento é visualizado corretamente em qualquer dispositivo, sobretudo na aplicação móvel do funcionário.

## Como carregar um documento

1. Aceda ao backoffice e navegue até à secção **Documentos** do menu principal.
2. Prima o botão **Novo documento**.
3. Preencha os campos do formulário tal como se descreve na secção seguinte.
4. Anexe o ficheiro a partir do seu dispositivo.
5. Reveja os dados e prima **Guardar** ou **Publicar**, consoante o caso.

> **Importante:** se premir **Guardar** sem publicar, o documento ficará em estado de rascunho e o funcionário não o verá nem receberá notificação. Para que o funcionário tenha acesso, o documento tem de estar publicado e com visibilidade ativada.

## Campos do formulário

### Título

O título é o nome com que o funcionário verá o documento na sua aplicação. Seja descritivo e consistente no formato que a sua empresa usa. Um exemplo habitual é: `Recibo de vencimento - Março 2026`.

### Descrição

Campo opcional que permite acrescentar contexto ao documento. Pode usá-lo para indicar o período que abrange, se contém alguma correção face a versões anteriores ou qualquer instrução para o funcionário.

### Tipo de documento

Selecione o tipo que corresponder. Existem doze:

- **Recibo de vencimento**: recibos salariais, acertos, complementos.
- **Contrato**: contratos de trabalho, renovações, alterações de condições.
- **Repreensão** e **Chamada de atenção**: documentação disciplinar.
- **Comprovativo**: comprovativos de ausência e de licenças.
- **Certificado**: certificados de empresa, de carreira contributiva, de retenções.
- **Política**: políticas de empresa, código de conduta.
- **Procedimento**: instruções de trabalho, protocolos operacionais.
- **Prevenção de riscos**: avaliações de riscos, formação em segurança, entrega de EPI.
- **Protocolo de sucursal**: normas específicas de um local.
- **Documento de projeto**: documentação associada a um projeto ou cliente.
- **Outro**: qualquer documento que não se enquadre nos anteriores.

> **Importante:** ao contrário do que acontece com uma simples etiqueta, **alguns tipos estão restritos por perfil**. Quem não tiver nível suficiente para esse tipo recebe o erro `documents/restricted_document_type`. O tipo, portanto, afeta o acesso, além de facilitar a pesquisa.

### Âmbito

Além do tipo, cada documento tem um âmbito que determina a quem se dirige:

- **Funcionário**: um documento pessoal, como um recibo de vencimento ou um contrato.
- **Sucursal**: dirigido a todo o pessoal de um local, como um protocolo de abertura.
- **Entidade**: dirigido a todo o quadro de pessoal, como uma política de empresa.

O âmbito determina também o modo de confirmação de leitura disponível: de um funcionário concreto, dos funcionários de uma sucursal ou de toda a entidade.

### Funcionário ou funcionários destinatários

Pode atribuir o documento a um único funcionário ou a vários de uma só vez. Quando atribui o mesmo documento a vários funcionários —por exemplo, uma circular informativa— o sistema cria uma entrada de documento por cada funcionário, de modo que cada um acede à sua própria cópia e a rastreabilidade fica separada por pessoa.

Para atribuir vários destinatários, use o campo de pesquisa de funcionários e selecione-os um a um ou através dos filtros de sucursal ou departamento, se os tiver configurados.

### Visibilidade: o campo privado

O campo **Privado** controla se o funcionário pode ver o documento a partir da sua aplicação.

- **Privado desativado (público)**: o funcionário pode ver e descarregar o documento a partir do momento em que é publicado.
- **Privado ativado**: o documento só é visível para os gestores com acesso ao backoffice. O funcionário não o verá na sua aplicação ainda que o documento exista no sistema.

Este campo é útil quando precisa de carregar documentação interna de carácter sensível —como notas disciplinares ou avaliações confidenciais— sem que o funcionário lhe aceda até que o decida.

> **Nota:** pode alterar a visibilidade de um documento já carregado a qualquer momento a partir dos detalhes do documento. Consulte o artigo sobre documentos privados para mais informação sobre os casos de utilização deste campo.

## Organizar o arquivo documental

À medida que o volume de documentos cresce, manter o arquivo organizado torna-se fundamental para localizar documentos rapidamente.

Aplique estas convenções desde o início:

- **Título consistente**: use sempre o mesmo formato de nome, por exemplo `[Tipo] - [Funcionário/Período]`.
- **Tipo correto**: não use «Outro» como categoria de recurso. Com doze tipos disponíveis, quase tudo tem o seu lugar, e o tipo condiciona quem pode ver o documento.
- **Períodos claros na descrição**: sobretudo em recibos de vencimento, indique o mês e o ano no título ou na descrição.

Os filtros do painel de documentos permitem-lhe pesquisar por tipo, por âmbito, por funcionário e por data de carregamento, o que facilita a gestão mesmo quando o arquivo contém centenas de documentos.

## Artigos relacionados

- [O que é o módulo documental](30-o-que-e-o-modulo-documental.md)
- [Recibos de vencimento e contratos](32-recibos-de-vencimento-e-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificações de documentos](34-notificacoes-de-documentos.md)
- [Permissões de acesso documental](37-permissoes-de-acesso-documental.md)
- [Exportar documentos](38-exportar-documentos.md)
