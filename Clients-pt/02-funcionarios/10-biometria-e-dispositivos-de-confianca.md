# Biometria e dispositivos de confiança

O CheckBiz360 integra um sistema de verificação biométrica que permite garantir que o registo é feito pela pessoa certa a partir do dispositivo certo. Esta camada de segurança é especialmente relevante em ambientes onde a presença física e a identidade do funcionário têm de ficar comprovadas de forma inequívoca.

Este artigo explica como funciona a validação biométrica, o que é um dispositivo de confiança e como gerir ambos a partir do backoffice.

---

## Validação biométrica no CheckBiz360

A validação biométrica é um passo de verificação que o CheckBiz360 pode exigir ao funcionário antes de registar uma entrada ou saída. Consoante o dispositivo do funcionário, esta verificação é feita através de:

- **Reconhecimento facial (Face ID)** — Disponível em dispositivos iOS compatíveis e alguns modelos Android.
- **Impressão digital** — Disponível em dispositivos com sensor de impressões digitais integrado (Touch ID ou equivalentes Android).

Quando a validação biométrica está ativada para um funcionário, a aplicação solicita a autenticação biométrica no momento do registo. Só se a verificação for bem-sucedida é que a entrada ou saída fica registada.

---

## Verificação biométrica obrigatória

Cada perfil de funcionário inclui a opção **verificação biométrica obrigatória**, que determina se a autenticação biométrica é obrigatória para esse utilizador ao efetuar registos.

- **Ativa** — O funcionário tem de verificar a sua identidade biométrica antes de cada registo. Este é o valor por omissão para todos os funcionários novos.
- **Inativa** — O funcionário pode registar sem verificação biométrica adicional.

> **Nota:** por razões de segurança, a verificação biométrica obrigatória está ativada por predefinição em todos os perfis criados de novo. Desativá-la exige uma decisão explícita por parte do manager ou do owner.

---

## Como desativar a biometria para um funcionário específico

Há situações em que pode ser necessário desativar a verificação biométrica para um funcionário concreto, por exemplo quando o dispositivo do funcionário não dispõe de sensor biométrico ou quando existe uma avaria técnica pontual.

Para desativar este requisito:

1. Aceda ao backoffice com credenciais de manager ou owner.
2. Vá a **Funcionários** e abra o perfil do funcionário.
3. Na secção **Segurança**, localize o controlo **Verificação biométrica obrigatória**.
4. Desative o interruptor.
5. Guarde as alterações.

A alteração produz efeito imediato. O funcionário poderá registar no seu próximo acesso sem necessidade de verificação biométrica.

---

## Dispositivos de confiança

O CheckBiz360 controla a partir de que dispositivos cada funcionário pode registar através de um sistema de dispositivos de confiança. Quando um funcionário inicia sessão e completa o processo de verificação (incluindo a 2FA, se estiver ativa), o sistema regista o identificador único do dispositivo (UUID).

Só os dispositivos registados como de confiança podem efetuar registos. Se um funcionário tentar registar a partir de um dispositivo que não está registado, a aplicação mostrará o erro:

```
Untrusted device
```

Este comportamento protege a integridade do controlo de horários, impedindo que um terceiro se faça passar pelo funcionário a partir de um dispositivo não autorizado.

---

## Como registar um novo dispositivo

Se um funcionário mudar de dispositivo ou precisar de adicionar um novo telemóvel como dispositivo de confiança, o processo é o seguinte:

1. O funcionário instala a aplicação do CheckBiz360 no seu novo dispositivo.
2. Inicia sessão com as suas credenciais (email e palavra-passe).
3. Se a 2FA estiver ativa, introduz o código de verificação gerado pela sua aplicação de autenticação.
4. Concluído o processo de autenticação, o sistema regista automaticamente o novo dispositivo como de confiança.

A partir desse momento, o funcionário pode registar a partir do novo dispositivo.

---

## Gestão de dispositivos a partir do backoffice

Os managers e owners podem consultar e gerir os dispositivos de confiança associados a cada funcionário:

### Ver os dispositivos registados

1. Aceda ao perfil do funcionário no backoffice.
2. Aceda à secção **Segurança e dispositivos**.
3. Será apresentada a lista de dispositivos de confiança registados, com informação sobre o modelo, o sistema operativo e a data do último acesso.

### Revogar o acesso a um dispositivo perdido ou roubado

Se um funcionário perder o seu dispositivo ou este for furtado, é fundamental revogar o seu acesso de imediato para evitar registos fraudulentos:

1. Aceda ao perfil do funcionário no backoffice.
2. Vá à secção **Segurança e dispositivos**.
3. Localize o dispositivo que pretende revogar e prima **Eliminar**.
4. Confirme a ação.

O dispositivo fica desassociado de imediato. Qualquer tentativa de registo a partir desse dispositivo será recusada com o erro «Untrusted device».

> **Nota:** depois de revogar um dispositivo, informe o funcionário para que registe o seu novo dispositivo seguindo o processo descrito acima. Se o funcionário ainda não dispuser de um dispositivo de substituição, pode ser necessário desativar temporariamente o requisito de dispositivo de confiança até que a situação se resolva.

---

## Quem pode gerir estas opções

A gestão da verificação biométrica e dos dispositivos de confiança a partir do backoffice está disponível para os perfis **manager** (nível 3) e **owner** (nível 4).

---

## Artigos relacionados

- [Autenticação de dois fatores](09-autenticacao-de-dois-fatores.md)
- [Criar e gerir funcionários](06-criar-e-gerir-funcionarios.md)
- [Perfis e níveis de responsabilidade](07-perfis-e-niveis-de-responsabilidade.md)
- [Funcionários multi-entidade](11-funcionarios-multi-entidade.md)
