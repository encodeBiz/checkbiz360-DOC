# Registo em teletrabalho

O CheckBiz360 contempla cenários de trabalho fora das instalações físicas da empresa. O modo de trabalho remoto permite que os funcionários registem a sua assiduidade sem necessidade de estarem dentro da geocerca da sucursal, mantendo ao mesmo tempo as validações de autenticação e de horário efetivo.

---

## O que é o modo de trabalho remoto

O trabalho remoto no CheckBiz360 é uma configuração individual por funcionário que desativa a validação de geolocalização durante o registo. Quando este modo está ativo, o sistema não verifica se o dispositivo se encontra dentro do raio da sucursal. As restantes validações (horário, dispositivo de confiança e biometria, se aplicável) continuam a funcionar normalmente.

Este modo destina-se a funcionários que realizam o seu trabalho de forma habitual ou pontual fora das instalações: teletrabalhadores, equipas distribuídas geograficamente, ou funcionários com teletrabalho parcial que alternam entre o escritório e o domicílio.

---

## Como ativar o trabalho remoto para um funcionário

A ativação do trabalho remoto é uma operação realizada por utilizadores com perfil **manager** ou **owner** a partir do painel de configuração do funcionário no backoffice.

1. Aceda ao backoffice do CheckBiz360.
2. Navegue até à secção **Funcionários** e selecione o funcionário correspondente.
3. Abra o separador de configuração de assiduidade ou de dados laborais.
4. Ative o campo **Trabalho remoto**.
5. Guarde as alterações.

A partir desse momento, os registos do funcionário não incluirão a validação de geocerca.

---

## O que muda quando o trabalho remoto está ativo

### Geolocalização desativada

O sistema omite por completo a validação de raio de registo. O funcionário pode registar a sua entrada e saída a partir de qualquer localização sem que o sistema gere erros do tipo `checklog/out_of_radius`.

### Fuso horário do funcionário

Quando o trabalho remoto está ativo, o sistema utiliza o fuso horário do funcionário para as validações de horário, em vez do fuso horário da sucursal. Isto é especialmente relevante para equipas distribuídas por diferentes países ou regiões.

Se o fuso horário do funcionário não estiver configurado, o sistema utiliza por omissão o fuso horário da entidade.

### Autenticação sem alterações

O trabalho remoto não modifica as exigências de autenticação. Se o funcionário tiver a 2FA ativada, tem de continuar a registar a partir de um dispositivo de confiança. Se tiver biometria obrigatória, tem de continuar a verificar a sua identidade biométrica antes de cada registo.

---

## Casos de utilização habituais

**Teletrabalho integral:** o funcionário trabalha inteiramente a partir do seu domicílio. Ativa-se o «trabalho remoto» de forma permanente e configura-se corretamente o seu fuso horário.

**Teletrabalho parcial:** o funcionário alterna entre escritório e domicílio consoante o dia. Neste caso, o responsável pode ativar ou desativar o modo remoto conforme o calendário acordado, ou mantê-lo sempre ativo se o funcionário registar corretamente em ambos os ambientes.

**Equipas distribuídas geograficamente:** empresas com funcionários em diferentes distritos ou países que não estão atribuídos a uma sucursal física concreta. O modo remoto permite centralizar o controlo de assiduidade sem necessidade de criar sucursais virtuais para cada localização.

**Deslocações e trabalho de campo:** funcionários que trabalham em instalações de clientes ou em movimento. Se a geocerca não for aplicável à sua atividade, o modo remoto evita registos falhados desnecessários.

---

## Como se reflete nos relatórios

Os registos efetuados em modo remoto ficam identificados no sistema como registos de trabalho remoto. A partir do backoffice, o responsável pode filtrar os relatórios de assiduidade por tipo de registo para obter uma visão separada das jornadas presenciais e das realizadas em remoto.

Esta distinção é útil para o acompanhamento de acordos de teletrabalho, para o cumprimento dos limites legais de dias de trabalho remoto estabelecidos em convenções ou acordos internos, e para análises de produtividade por modalidade de trabalho.

---

> **Aviso de configuração:** ativar o trabalho remoto sem configurar corretamente o fuso horário do funcionário pode gerar discrepâncias no cálculo de horas se o funcionário se encontrar num fuso horário diferente do da sucursal. Reveja sempre o fuso horário do funcionário antes de ativar este modo.

---

## Perfis com acesso a esta funcionalidade

A ativação do modo de trabalho remoto exige perfil **manager** ou **owner**. O funcionário não pode ativar nem desativar este modo por sua iniciativa.

---

## Artigos relacionados

- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Geocercas e raio de registo](16-geocercas-e-raio-de-registo.md)
- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
