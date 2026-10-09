# Autenticação de dois fatores (2FA)

A autenticação de dois fatores (2FA) acrescenta uma camada de segurança adicional ao processo de início de sessão no CheckBiz360. Uma vez ativada, o acesso à conta exige não só a palavra-passe do utilizador, mas também um código de verificação gerado por uma aplicação no seu dispositivo móvel.

Esta medida reduz significativamente o risco de acessos não autorizados, mesmo que a palavra-passe de um funcionário seja comprometida. A sua ativação é especialmente recomendável para perfis com nível de acesso elevado, como managers e owners.

---

## Como funciona a autenticação de dois fatores

Quando o funcionário ativa a 2FA, sempre que inicia sessão no CheckBiz360 tem de completar dois passos:

1. Introduzir o seu email e palavra-passe habituais.
2. Introduzir um código numérico de 6 dígitos gerado pela sua aplicação de autenticação.

O código é válido durante um intervalo de tempo breve (geralmente 30 segundos) e é regenerado automaticamente. Este desenho garante que, ainda que alguém obtenha a palavra-passe, não consiga aceder sem ter também o dispositivo físico do funcionário.

> **Nota:** no backoffice, o ecrã onde é pedido o código tem uma **cruz no canto superior direito** que termina a sessão e volta ao início de sessão. Serve para entrar com outra conta ou para sair se não tiver o telemóvel à mão, sem ficar preso na verificação.

---

## Configurar a 2FA a partir da aplicação

### Passo a passo para o funcionário

1. Inicie sessão com as suas credenciais: na aplicação móvel, a partir da secção de perfil; no backoffice, a partir de **A minha conta**.
2. Localize a secção de **segurança** da sua conta.
3. Ative a opção **Autenticação de dois fatores**.
4. A plataforma gerará um código QR e uma chave secreta manual.
5. Abra a sua aplicação de autenticação (ver opções na secção seguinte) e adicione uma nova conta.
6. Leia o código QR com a câmara do seu dispositivo ou, se preferir introduzi-lo manualmente, copie a chave secreta apresentada no ecrã.
7. A aplicação de autenticação começará a gerar códigos de 6 dígitos de forma automática.
8. Introduza o código atual de 6 dígitos no ecrã de verificação do CheckBiz360 e prima **Confirmar**.

A 2FA ficará ativada a partir desse momento.

---

## Aplicações de autenticação compatíveis

O CheckBiz360 é compatível com qualquer aplicação que implemente a norma TOTP (Time-based One-Time Password). As mais habituais são:

- **Google Authenticator** — Disponível para Android e iOS.
- **Microsoft Authenticator** — Disponível para Android e iOS.
- **Authy** — Disponível para Android, iOS e computador. Permite cópias de segurança cifradas na nuvem.

> **Nota:** recomenda-se utilizar o Authy se o funcionário quiser manter uma cópia de segurança dos seus tokens em caso de perda ou mudança de dispositivo.

---

## Dispositivos de confiança

Durante o processo de verificação com 2FA, a aplicação pode oferecer a opção de marcar o dispositivo atual como **dispositivo de confiança**. Esta opção permite que o sistema não solicite o código 2FA nos próximos inícios de sessão a partir desse mesmo dispositivo, durante um período de tempo configurado.

Os dispositivos de confiança são úteis para funcionários que trabalham habitualmente a partir do mesmo telemóvel ou tablet e não querem introduzir o código em cada acesso.

> **Nota:** não marque um dispositivo como de confiança se não for de uso exclusivamente pessoal. Em dispositivos partilhados, desative esta opção para manter a segurança do acesso.

---

## Ativar ou desativar a 2FA a partir do backoffice

Os responsáveis da empresa podem gerir o estado da 2FA de qualquer funcionário diretamente a partir do backoffice, sem necessidade de intervenção do próprio funcionário:

1. Aceda ao backoffice com credenciais de manager ou owner.
2. Vá a **Funcionários** e abra o perfil do funcionário.
3. Na secção **Segurança**, localize o controlo **Autenticação de dois fatores**.
4. Ative ou desative o interruptor consoante o caso.
5. Guarde as alterações.

> **Nota:** a desativação da 2FA a partir do backoffice elimina de imediato o requisito do segundo fator para esse funcionário. Use esta opção com cautela e apenas quando for estritamente necessário.

---

## Recuperação de acesso em caso de perda do dispositivo

Se um funcionário perder o dispositivo com o qual tinha configurado a 2FA e não conseguir gerar o código de verificação, o processo de recuperação é o seguinte:

1. O funcionário contacta o seu manager ou owner.
2. O responsável acede ao backoffice e desativa temporariamente a 2FA no perfil do funcionário.
3. O funcionário inicia sessão com a sua palavra-passe habitual sem necessidade de código.
4. Uma vez dentro, o funcionário configura de novo a 2FA com o seu novo dispositivo seguindo os passos descritos acima.
5. O manager pode voltar a ativar o requisito de 2FA depois de concluída a reconfiguração.

---

## Quem pode gerir a 2FA de outros funcionários

A ativação e desativação da 2FA a partir do backoffice está disponível para os perfis **manager** (nível 3) e **owner** (nível 4). Os próprios funcionários podem configurar a sua 2FA a partir da aplicação móvel, independentemente do seu perfil.

---

## Artigos relacionados

- [Biometria e dispositivos de confiança](10-biometria-e-dispositivos-de-confianca.md)
- [Criar e gerir funcionários](06-criar-e-gerir-funcionarios.md)
- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Funcionários multi-entidade](11-funcionarios-multi-entidade.md)
