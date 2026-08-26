# Geocercas e raio de registo

A geocerca é o mecanismo através do qual o CheckBiz360 garante que um funcionário se encontra fisicamente no local de trabalho no momento em que regista a sua assiduidade. Este artigo explica o que é uma geocerca, como configurá-la corretamente e o que acontece quando um funcionário tenta registar fora da área permitida.

---

## O que é uma geocerca

Uma geocerca é um perímetro circular definido em torno das coordenadas GPS de uma sucursal. A sua função é estabelecer a área dentro da qual se considera válido um registo presencial. Quando um funcionário prime o botão de registo, a aplicação envia as coordenadas do seu dispositivo e o sistema calcula a distância entre esse ponto e o centro da sucursal. Se a distância ultrapassar o raio configurado, o registo é recusado.

O raio é expresso em metros e pode ser ajustado à superfície e às características físicas de cada instalação.

---

## Como configurar o raio de registo

O raio de registo configura-se ao nível da sucursal, aceitando um valor inteiro em metros.

1. Aceda ao backoffice do CheckBiz360 com perfil **manager** ou **owner**.
2. Navegue até à secção **Sucursais** e selecione a sucursal que pretende configurar.
3. Abra o separador de configuração de assiduidade ou de definições da sucursal.
4. Localize o campo **Raio de registo** e introduza o valor em metros.
5. Certifique-se de que as coordenadas GPS da sucursal estão corretamente definidas. O raio não tem utilidade se o ponto central não estiver bem localizado.
6. Guarde as alterações. A nova configuração aplica-se de imediato aos registos seguintes.

---

## Como desativar a validação de geocerca

Nalgumas situações, a validação de geocerca não é aplicável: sucursais sem morada fixa, ambientes de trabalho de campo ou instalações com coordenadas GPS pouco precisas.

Para desativar a geocerca numa sucursal concreta, ative a opção «desativar validação de geocerca» na configuração dessa sucursal.

1. Aceda à configuração da sucursal como descrito na secção anterior.
2. Ative o campo **Desativar validação de geocerca**.
3. Guarde as alterações.

Com esta opção ativa, o sistema omite a verificação de distância para todos os funcionários atribuídos a essa sucursal. As restantes validações (horário, dispositivo, biometria) continuam a aplicar-se normalmente.

> **Nota:** esta opção é diferente do modo de trabalho remoto por funcionário. «Desativar validação de geocerca» afeta todos os funcionários da sucursal, ao passo que «trabalho remoto» é uma configuração individual.

---

## O que acontece quando o funcionário está fora do raio

Se o funcionário tentar registar a partir de uma localização fora do raio permitido, o sistema:

1. Grava a tentativa de registo com estado `failed`.
2. Atribui o código de erro `checklog/out_of_radius`.
3. Armazena a distância real entre a localização do dispositivo e o centro da geocerca, bem como o raio configurado nesse momento.

Esta informação fica disponível no histórico do funcionário e pode ser consultada pelo responsável a partir do backoffice. Permite identificar se o problema é pontual (o funcionário estava noutro edifício do recinto) ou sistemático (o raio está mal dimensionado).

O funcionário vê na aplicação uma mensagem a indicar que está fora da zona de registo.

---

## Recomendações de raio consoante o tipo de instalação

A escolha do raio adequado depende da dimensão e da distribuição física do local de trabalho. Apresentam-se em seguida valores indicativos:

| Tipo de instalação | Raio recomendado |
|---|---|
| Escritório pequeno ou espaço comercial | 50 – 100 metros |
| Pavilhão industrial ou armazém | 200 – 500 metros |
| Campus universitário ou recinto industrial grande | 500 – 1.000 metros |
| Edifício de escritórios com vários pisos | 100 – 200 metros |

Estes valores são indicativos. Recomenda-se validar o raio no local: peça a um funcionário que faça um registo de teste a partir dos pontos mais afastados do recinto, para verificar que o raio cobre corretamente a área de trabalho.

Um raio excessivamente pequeno gera registos falhados desnecessários. Um raio excessivamente grande reduz a eficácia do controlo de presenças. Procure o equilíbrio que se ajuste à realidade física da instalação.

---

> **Aviso sobre dispositivos GPS:** a precisão da geolocalização depende do dispositivo móvel e das condições do ambiente (interiores, zonas com sinal fraco, dispositivos com GPS desativado). Em ambientes com baixa precisão de GPS, pondere alargar ligeiramente o raio para evitar recusas indevidas.

---

## Perfis com acesso a esta funcionalidade

A configuração de geocercas e do raio de registo exige perfil **manager** ou **owner**. Os funcionários não têm acesso a esta configuração.

---

## Artigos relacionados

- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Registo em teletrabalho](15-registo-em-teletrabalho.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
