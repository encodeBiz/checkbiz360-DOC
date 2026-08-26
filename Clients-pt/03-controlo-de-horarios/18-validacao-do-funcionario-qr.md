# Validação do funcionário através de QR

O CheckBiz360 oferece um mecanismo opcional de verificação de identidade prévio ao registo, designado validação do funcionário. Quando está ativado na configuração da sucursal, utiliza um código QR gerado na aplicação do funcionário que o supervisor lê para confirmar que a pessoa presente é quem diz ser. Este artigo explica como funciona este mecanismo, quando se aplica e o que representa do ponto de vista técnico.

> **Nota:** a validação QR é um mecanismo configurável por sucursal, não um requisito universal do sistema. Independentemente de a validação QR estar ativada ou não, o processo de registo valida sempre de forma automática o dispositivo de confiança, a geolocalização dentro da geocerca e o horário do turno ativo do funcionário.

---

## O que é a validação do funcionário

A validação do funcionário é um mecanismo de verificação presencial de identidade que pode ser ativado como passo prévio ao primeiro registo da jornada. O seu propósito é acrescentar uma camada adicional de segurança face ao registo delegado ou fraudulento, sobretudo em ambientes onde a identidade do funcionário tem de ser confirmada presencialmente.

Este mecanismo é totalmente configurável por sucursal: nem todas as sucursais ou entidades o exigem. Quando está ativado, o funcionário não pode completar o registo até que o supervisor tenha lido e validado o seu código. Nas sucursais onde não está ativado, o funcionário pode registar diretamente; o sistema valida igualmente nesse momento o dispositivo de confiança, a geolocalização e o turno ativo.

---

## O token de validação

Quando o funcionário inicia sessão na aplicação e seleciona a sua entidade de trabalho, o sistema gera um **código de verificação**. Este código é uma cadeia em formato base64 que contém o identificador do funcionário e o identificador da entidade.

O código de verificação tem uma validade limitada e é utilizado exclusivamente para o processo de validação QR. Não é reutilizável entre sessões nem transferível entre dispositivos.

---

## O código QR

A partir do código de verificação, a aplicação gera um código QR visível no ecrã do dispositivo do funcionário. Este código contém a informação necessária para que o sistema identifique o funcionário de forma inequívoca.

O supervisor, utilizando o seu próprio dispositivo com a aplicação do CheckBiz360, lê este código QR. O sistema verifica o código de verificação, confirma a identidade do funcionário e marca a validação como concluída.

---

## Fluxo do processo quando a validação QR está ativada na sucursal

1. O funcionário abre a aplicação do CheckBiz360 e inicia sessão com as suas credenciais.
2. Seleciona a entidade de trabalho correspondente.
3. A aplicação deteta que a sucursal tem a validação QR ativada e mostra o ecrã de validação com o código QR gerado a partir do código de verificação.
4. O supervisor dirige-se ao funcionário e lê o QR a partir do seu dispositivo.
5. O sistema verifica o token e regista a validação de identidade.
6. A aplicação do funcionário passa automaticamente ao ecrã de registo.
7. O funcionário regista a sua entrada; o sistema valida nesse momento o dispositivo de confiança, a geolocalização e o turno ativo.

Quando a validação QR não está ativada na sucursal, o processo começa diretamente no passo 7: o funcionário acede ao ecrã de registo e o sistema aplica igualmente as validações automáticas de dispositivo, geolocalização e horário.

---

## Preparação prévia do sistema de registo

Quando o supervisor lê o código QR e completa a validação, o sistema executa de forma automática e transparente um processo de preparação prévia (*warm-up*) do ambiente de registo. Este processo prepara e verifica em segundo plano todos os parâmetros necessários para que o registo seja processado de imediato: turno ativo, geocerca, configuração do dispositivo e estado do funcionário.

O funcionário não se apercebe deste processo. Da sua perspetiva, passa simplesmente do ecrã de validação para o ecrã de registo. Ainda assim, este mecanismo melhora a rapidez e a fiabilidade do registo, sobretudo em ambientes com muitos funcionários a registar no mesmo intervalo de tempo.

---

## Quando é necessária a validação QR

A validação QR ativa-se consoante a configuração da sucursal. Alguns cenários habituais em que é utilizada:

- Ambientes com elevada rotação de pessoal ou contratações temporárias em que a identidade do funcionário pode não ser conhecida do supervisor.
- Instalações com controlo de acesso estrito onde se exige verificação dupla.
- Setores com obrigações legais de identificação presencial (segurança, saúde, alimentação).
- Empresas que pretendem acrescentar uma camada adicional de controlo sem necessidade de leitores biométricos físicos.

---

> **Aviso de privacidade:** o código QR contém apenas o identificador do funcionário e o da entidade, ambos em formato cifrado. Não inclui dados pessoais em texto simples. O código de verificação expira após a sua utilização ou ao terminar a sessão do funcionário.

---

## Perfis com acesso a esta funcionalidade

O funcionário com perfil **funcionário** gera o QR a partir da sua aplicação. A leitura e validação do código compete a utilizadores com perfil **supervisor**, **manager** ou **owner**. A ativação da validação QR como requisito prévio ao registo é configurável pelos perfis **manager** ou **owner**.

---

## Artigos relacionados

- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Revisão e validação de registos](20-revisao-e-validacao-de-registos.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
