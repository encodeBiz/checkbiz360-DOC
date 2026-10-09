# Trabalho fora do centro

O CheckBiz360 contempla cenários de trabalho fora das instalações da empresa: montagens, serviços em casa do cliente, trabalho de campo ou teletrabalho. A opção **Trabalha fora do centro** permite que um funcionário registe a sua assiduidade sem estar dentro da geocerca de uma sucursal, mantendo as validações de autenticação e de horário efetivo.

> **Nota:** até setembro de 2026 esta opção chamava-se **Trabalho remoto**. Mudou o nome, não o funcionamento: «remoto» sugeria teletrabalho a partir de casa, e a opção serve para qualquer pessoa que não regista num centro.

---

## O que é o trabalho fora do centro

É uma configuração individual por funcionário que desativa a validação de geolocalização durante o registo. Quando está ativa, o sistema não verifica se o dispositivo se encontra dentro do raio da sucursal. As restantes validações (horário, dispositivo de confiança e biometria, se aplicável) continuam a funcionar normalmente.

Destina-se a funcionários que trabalham de forma habitual ou pontual fora das instalações: equipas de campo, técnicos que se deslocam, pessoal de montagem ou de eventos, e também teletrabalhadores.

---

## Como ativá-lo para um funcionário

A ativação é realizada por utilizadores com perfil **manager** ou **owner** a partir da ficha do funcionário no backoffice.

1. Aceda ao backoffice do CheckBiz360.
2. Navegue até à secção **Funcionários** e abra a ficha do funcionário.
3. Prima **Editar**.
4. Ative **Trabalha fora do centro** e complete a morada do funcionário, que passa a ser obrigatória.
5. Guarde as alterações.

A partir desse momento, os registos do funcionário não incluirão a validação de geocerca. Na sua ficha, a situação aparece como **Trabalha fora do centro**; se a opção estiver desativada, como **Pica no centro**.

> **Sugestão:** se o que precisa é de verificar que o funcionário está no local de um trabalho concreto —o domicílio de um cliente, por exemplo—, não desative a geocerca: dê à tarefa o seu próprio local de trabalho. Ver [Local de trabalho próprio](../06-tarefas/40-criar-uma-tarefa.md#local-de-trabalho-próprio).

---

## O que muda quando está ativo

### Geolocalização desativada

O sistema omite por completo a validação de raio de registo. O funcionário pode registar a sua entrada e saída a partir de qualquer localização sem que o sistema gere erros do tipo `checklog/out_of_radius`.

### Fuso horário do funcionário

Quando o trabalho fora do centro está ativo, o sistema utiliza o fuso horário do funcionário para as validações de horário, em vez do fuso horário da sucursal. Isto é especialmente relevante para equipas distribuídas por diferentes países ou regiões.

Se o fuso horário do funcionário não estiver configurado, o sistema utiliza por omissão o fuso horário da entidade.

### Autenticação sem alterações

Trabalhar fora do centro não modifica as exigências de autenticação. Se o funcionário tiver a 2FA ativada, tem de continuar a registar a partir de um dispositivo de confiança. Se tiver biometria obrigatória, tem de continuar a verificar a sua identidade biométrica antes de cada registo.

---

## Casos de utilização habituais

**Deslocações e trabalho de campo:** funcionários que trabalham em instalações de clientes ou em movimento. Se a geocerca não for aplicável à sua atividade, trabalhar fora do centro evita registos falhados desnecessários.

**Equipas distribuídas geograficamente:** empresas com funcionários em diferentes distritos ou países que não estão atribuídos a uma sucursal física concreta. A opção permite centralizar o controlo de assiduidade sem criar sucursais virtuais para cada localização.

**Teletrabalho integral:** o funcionário trabalha inteiramente a partir do seu domicílio. Ativa-se **Trabalha fora do centro** de forma permanente e configura-se corretamente o seu fuso horário.

**Teletrabalho parcial:** o funcionário alterna entre escritório e domicílio consoante o dia. O responsável pode ativar ou desativar a opção conforme o calendário acordado, ou mantê-la sempre ativa se o funcionário registar corretamente em ambos os ambientes.

---

## Como se reflete nos relatórios

Os registos efetuados fora do centro ficam identificados no sistema como tal. A partir do backoffice, o responsável pode filtrar os relatórios de assiduidade por tipo de registo para obter uma visão separada das jornadas no centro e das realizadas fora dele.

Esta distinção é útil para o acompanhamento de acordos de teletrabalho, para o cumprimento dos limites de dias de trabalho à distância estabelecidos em convenções ou acordos internos, e para análises de produtividade por modalidade de trabalho.

---

> **Aviso de configuração:** ativar o trabalho fora do centro sem configurar corretamente o fuso horário do funcionário pode gerar discrepâncias no cálculo de horas se o funcionário se encontrar num fuso horário diferente do da sucursal. Reveja sempre o fuso horário do funcionário antes de ativar este modo.

---

## Perfis com acesso a esta funcionalidade

A ativação do trabalho fora do centro exige perfil **manager** ou **owner**. O funcionário não pode ativar nem desativar este modo por sua iniciativa.

---

## Artigos relacionados

- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Geocercas e raio de registo](16-geocercas-e-raio-de-registo.md)
- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
