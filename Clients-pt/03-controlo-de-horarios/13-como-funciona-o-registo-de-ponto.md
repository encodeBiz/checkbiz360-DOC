# Como funciona o registo de ponto no CheckBiz360

O registo de ponto no CheckBiz360 não é uma simples marcação de hora. Sempre que um funcionário regista a sua entrada ou saída, o sistema executa um processo de validação em três camadas que garante a integridade do dado, a coerência com o turno ativo e a identidade do dispositivo utilizado. Este artigo explica como funciona esse processo do princípio ao fim.

---

## As três camadas de validação

Quando um funcionário prime o botão de registo, o sistema avalia de forma sequencial três condições. Se alguma delas não se cumprir, o registo fica gravado como falhado com um código de erro específico que indica a causa exata.

### Camada 1 — Geolocalização

O sistema obtém as coordenadas GPS do dispositivo no momento do registo e compara-as com a localização da sucursal atribuída ao funcionário. Cada sucursal tem configurado um raio de registo (expresso em metros). Se o funcionário se encontrar fora desse raio, o registo é recusado com o código `checklog/out_of_radius`.

A distância real entre o funcionário e o centro da geocerca fica gravada no sistema para análise posterior. Isto permite ao responsável verificar se o raio está bem dimensionado ou se existe um padrão de tentativas de registo a partir de localizações incorretas.

Se o funcionário trabalhar em regime de teletrabalho e tiver ativado o campo «trabalho remoto», esta camada de validação é omitida por completo. A geocerca não se aplica em ambientes de trabalho remoto.

### Camada 2 — Horário efetivo

Validada a localização, o sistema verifica que o registo é efetuado dentro do turno ativo do funcionário para esse dia, de acordo com o seu calendário efetivo.

O registo guarda sempre a **hora real**. O que decide se o tempo trabalhado fora da faixa oficial conta ou não é a **modalidade de jornada** do calendário: com jornada estrita não é contabilizado; com jornada flexível é somado como tempo extra. Consulte [Jornada estrita e jornada flexível](../04-calendario-e-horarios/28-horario-flexivel.md).

Se o registo for efetuado fora do turno ativo, o sistema recusa-o com o código `checklog/out_of_schedule`.

### Camada 3 — Dispositivo e biometria

A terceira camada verifica a identidade do dispositivo e, se aplicável, a biometria do funcionário.

Se o funcionário tiver ativada a autenticação de duplo fator (2FA), só pode registar a partir de dispositivos que tenham sido previamente registados como dispositivos de confiança. Tentar registar a partir de um dispositivo não registado gera o erro `auth/untrusted_device`.

Se a configuração do funcionário ou da sucursal tiver ativa a verificação biométrica, o funcionário tem de completar a verificação biométrica (impressão digital ou reconhecimento facial consoante o dispositivo) antes de o registo ser processado.

---

## Resultado do registo

Uma vez ultrapassadas as três camadas de validação, o registo fica gravado com estado `valid`. Este estado indica que o registo é correto, coerente com o turno e autenticado.

Se alguma camada falhar, o registo é gravado com estado `failed` e o código de erro correspondente. Um ponto importante: **os registos falhados também são guardados no sistema**. Não são descartados. Ficam disponíveis para auditoria, análise de incidências e revisão por parte do responsável.

| Estado após o registo | Significado |
|---|---|
| `valid` | Todas as validações ultrapassadas. Jornada ativa. |
| `failed` | Uma ou mais validações falharam. Código de erro disponível. |

---

## Diferença entre registo válido e registo falhado

A distinção é importante para a gestão salarial e para a conformidade legal. Um registo válido conta como tempo trabalhado dentro da jornada. Um registo falhado fica gravado para auditoria mas não conta horas.

Quando um funcionário acumula registos falhados reiterados, o responsável pode rever o padrão a partir do backoffice e determinar se se trata de um problema de configuração (raio demasiado pequeno, horário mal atribuído) ou de uma incidência que exige atenção.

Se um funcionário não conseguiu registar por causas justificadas, o responsável pode criar um pedido de jornada manual para registar a assiduidade de forma retroativa.

---

> **Nota sobre auditoria:** todos os registos, válidos e falhados, ficam guardados com o seu timestamp original, os dados de validação (coordenadas, distância, dispositivo) e o resultado de cada camada. Este registo é imutável e pode ser consultado perante inspeções do trabalho.

---

## Perfis com acesso a esta funcionalidade

A configuração das camadas de validação (zona de verificação, biometria, 2FA) é gerida por utilizadores com perfil **owner** ou **manager**. Os funcionários interagem com o sistema de registo a partir da aplicação móvel sem necessidade de configurar nada.

---

## Artigos relacionados

- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
- [Registo em teletrabalho](15-registo-em-teletrabalho.md)
- [Geocercas e raio de registo](16-geocercas-e-raio-de-registo.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
