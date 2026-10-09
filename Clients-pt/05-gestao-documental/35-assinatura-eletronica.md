# Confirmação de leitura e assinatura eletrónica

Um documento pode pedir que o funcionário confirme que o recebeu. Essa confirmação faz-se na aplicação e, desde outubro de 2026, **assina-se com o telemóvel**: o funcionário confirma com a impressão digital, o rosto ou o código de desbloqueio, e a plataforma guarda uma assinatura eletrónica que pode ser verificada fora do CheckBiz360. Nos documentos dirigidos a uma só pessoa, como um recibo de vencimento ou uma advertência, a assinatura **fica dentro do próprio PDF**.

---

## O que vê o funcionário

Quando um documento pede confirmação de leitura, o funcionário abre-o na aplicação, lê-o e toca em **Confirmar**. A aplicação pede a impressão digital ou o rosto; se o telemóvel não tiver biometria, o código de desbloqueio; e se não tiver bloqueio de ecrã, a palavra-passe da conta. Não tem de desenhar nada nem instalar nada.

Se o documento for um PDF dirigido só a ele, ao confirmar recebe o **PDF assinado**, que substitui o anterior na sua lista. Leva na margem inferior de cada página, em letra pequena, quem assinou, quando e as referências para o verificar.

> **Nota:** se o funcionário fechar o documento sem confirmar, continua na sua lista de pendentes.

## O que vê a empresa

Na ficha do documento, na secção de confirmação de leitura, cada confirmação diz como foi feita:

| Marca | O que significa |
|---|---|
| **Assinada e verificada (impressão digital ou rosto)** | o funcionário confirmou com biometria e a plataforma verificou a assinatura com a chave do seu telemóvel |
| **Assinada e verificada (desbloqueio do telemóvel)** | o mesmo, com o código, padrão ou PIN do telemóvel |
| **Confirmada com palavra-passe** | o telemóvel não tem bloqueio de ecrã; confirmou voltando a escrever a palavra-passe |
| **Confirmada com um toque** | confirmações anteriores à assinatura, ou de uma aplicação não atualizada |

Junto a cada confirmação assinada há **Descarregar a ata de assinatura**: um PDF de uma página com quem assinou, quando, de que telemóvel, que documento e em que versão, a assinatura, a chave com que se verificou e as instruções para repetir a verificação com uma ferramenta padrão. É o que se entrega a uma inspeção ou a um perito.

Se o documento era um PDF para uma só pessoa, a descarga do documento entrega já o **PDF assinado**. O original conserva-se na plataforma.

## Que documentos se assinam dentro do PDF

Só os dirigidos a **um único funcionário**: recibos de vencimento, advertências, comunicações individuais. Um documento para toda uma sucursal ou para toda a empresa, por exemplo uma política interna, é confirmado por muitas pessoas: cada confirmação fica assinada e com a sua ata, mas o ficheiro não se altera. O mesmo acontece com um documento que não seja PDF.

## O que vale esta assinatura

É uma **assinatura eletrónica avançada** segundo o Regulamento eIDAS: está ligada ao signatário, sob o seu controlo e vinculada ao conteúdo exato que assinou. Não é uma assinatura qualificada, que exige um certificado emitido por um prestador reconhecido; se um procedimento a exigir, use um serviço externo.

Duas coisas que a empresa deve fazer para que a assinatura tenha pleno valor:

- **Recolher o consentimento do trabalhador.** Para que confirmar com a impressão digital valha como assinatura, o funcionário tem de ter aceitado esse meio. É responsabilidade da empresa, não da plataforma; como fazê-lo com a própria plataforma, na secção seguinte.
- **Instalar o certificado do CheckBiz360**, se quiser que os leitores de PDF mostrem a assinatura a verde. Sem o instalar, o leitor dirá que a assinatura é válida mas de confiança desconhecida; a verificação é a mesma. O certificado descarrega-se no backoffice, na ficha da empresa, separador **Ambiente de trabalho**, secção **Assinatura eletrónica**, onde estão também os passos para o instalar no Acrobat Reader.

## Verificar uma assinatura sem a plataforma (para peritos)

A ata de assinatura leva tudo o que é preciso para repetir a verificação com o OpenSSL, uma ferramenta padrão que vem em qualquer Linux ou Mac e se instala no Windows. Não é preciso confiar no CheckBiz360 nem em nenhum certificado: só matemática.

Da ata copiam-se três coisas: a **cadeia assinada** (o bloco «tal qual» da secção 2), a **assinatura** em base64 (secção 3) e a **chave pública** em PEM (secção 3). Depois, numa pasta vazia:

1. Guarde a cadeia assinada num ficheiro `payload.txt`, exatamente como aparece, sem acrescentar uma quebra de linha no fim.
2. Guarde a assinatura em `sig.b64` e descodifique-a: `base64 -d sig.b64 > sig.der`
3. Guarde a chave pública, com as linhas `BEGIN PUBLIC KEY` e `END PUBLIC KEY`, em `key.pem`.
4. Verifique a assinatura: `openssl dgst -sha256 -verify key.pem -signature sig.der payload.txt` → deve responder **Verified OK**.
5. Verifique que a chave é a que consta na ata: `openssl pkey -pubin -in key.pem -outform DER | openssl dgst -sha256` → deve coincidir com a **impressão digital da chave pública (keyId)** da ata.

Fica assim demonstrado que **essa chave assinou exatamente essa cadeia**, e a cadeia leva dentro o documento, a versão e o hash do conteúdo (ou a entrega e os seus documentos). Para ligar a chave à pessoa, a ata indica quando foi registada e de que telemóvel, e o consentimento do trabalhador fecha o círculo.

Se o perito preferir o ficheiro de evidência original em JSON, com os mesmos dados e o seu próprio SHA-256, o suporte pode facultá-lo a partir do número da ata.

## Recolher o consentimento com a própria plataforma

O consentimento não precisa de papel: recolhe-se como qualquer outra confirmação de leitura, e assim fica datado, assinado e com a sua ata.

1. Redija um documento breve, **«Condições da assinatura eletrónica»**, que diga: que confirmar um documento ou uma entrega na aplicação CheckBiz360 com a impressão digital, o rosto ou o código do telemóvel é a assinatura eletrónica do trabalhador e tem o mesmo valor que a sua assinatura manuscrita para efeitos internos; que a chave se cria no seu telemóvel e não sai dele; que se o telemóvel não tiver bloqueio de ecrã confirmará com a palavra-passe da conta; que pode pedir a qualquer momento uma cópia do que assinou e da ata; e a quem se dirigir com dúvidas. Convém que a sua assessoria o reveja.
2. Carregue-o **em cada sucursal** com **Requer confirmação de leitura** ativado, visível para todos os perfis. A confirmação de leitura pede-se por sucursal ou por funcionário, não a toda a empresa de uma vez.
3. Cada trabalhador confirma-o na aplicação. Essa confirmação é o registo do consentimento: quem, quando e sobre que texto, com a sua ata se o fez com a aplicação atualizada.
4. A quem entrar depois, inclua-o no contrato ou carregue-lho individualmente ao registá-lo.

Até um trabalhador o ter confirmado, trate-o como se confirmasse com um toque: a plataforma regista na mesma, mas a empresa não terá o consentimento que sustenta a assinatura.

## Descarregar e instalar o certificado do CheckBiz360

Só é necessário se quiser que o Acrobat Reader mostre as assinaturas **a verde**. Sem o instalar, o leitor diz que o documento não foi alterado e que a assinatura é válida, mas que a identidade do signatário é «desconhecida» porque o CheckBiz360 não está na sua lista de confiança. A verificação é a mesma nos dois casos.

**Descarregar:** no backoffice, abra a ficha da empresa, separador **Ambiente de trabalho**, secção **Assinatura eletrónica**, e clique em **Descarregar o certificado (.zip)**. Descomprima o zip: contém o mesmo certificado em dois formatos, **checkbiz360-firma-ca.cer** para o Acrobat e o Windows e **checkbiz360-firma-ca.crt** em texto para o porta-chaves do Mac ou Linux, e um ficheiro com estas instruções.

**Instalar no Acrobat Reader:**

1. Abra **Editar → Preferências → Assinaturas**.
2. Em **Identidades e certificados de confiança**, clique em **Mais**.
3. Entre em **Certificados de confiança** e clique em **Importar**.
4. Escolha o ficheiro **.cer** e, nas opções do certificado, marque **Utilizar este certificado como raiz de confiança**. Confirme.
5. Feche o PDF assinado e volte a abri-lo: a assinatura aparece a verde.

**Se a empresa tiver vários computadores (Windows):** o informático pode instalá-lo uma vez em cada equipamento, ou por política, no repositório de certificados do Windows, em **Autoridades de certificação de raiz fidedignas**, e no Acrobat, em **Preferências → Assinaturas → Verificação → Mais**, marcar que confie nos certificados de raiz do repositório do Windows.

> **Nota:** no Mac, a Pré-visualização não verifica assinaturas; use o Acrobat Reader, onde os passos são os mesmos.

**Outros leitores e validadores.** O Acrobat não é obrigatório: a assinatura é PAdES, o padrão europeu, e o Foxit, o PDF-XChange ou o LibreOffice também a validam, cada um com a sua forma de importar o certificado. O AutoFirma é uma ferramenta para assinar com certificados reconhecidos, não para validar; o validador da Administração espanhola, VALIDe, confirmará que o documento não foi alterado, mas assinalará o certificado do signatário como não reconhecido, porque o CheckBiz360 não é um prestador qualificado. Para demonstrar a assinatura perante um perito basta a ata, que se verifica sem qualquer lista de confiança.

## Como ativar a confirmação de leitura

1. Ao carregar ou editar o documento, ative **Requer confirmação de leitura**.
2. Para um recibo de vencimento ou uma advertência, carregue o documento **ao funcionário** (âmbito funcionário): é o que permite assiná-lo dentro do PDF.
3. Verifique que o documento é visível para o destinatário.

Se tiver ativas as notificações do módulo documental, o funcionário recebe um aviso com o documento pendente.

---

## Artigos relacionados

- [O que é o módulo documental](30-o-que-e-o-modulo-documental.md)
- [Carregar e organizar documentos](31-carregar-e-organizar-documentos.md)
- [Recibos de vencimento e contratos](32-recibos-de-vencimento-e-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificações de documentos](34-notificacoes-de-documentos.md)
- [Primeiro início de sessão na aplicação](../10-aplicacao-movel/70-primeiro-inicio-de-sessao.md)
