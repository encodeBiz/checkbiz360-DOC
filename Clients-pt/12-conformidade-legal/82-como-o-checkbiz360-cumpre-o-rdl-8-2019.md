# Como o CheckBiz360 cumpre o RDL 8/2019

## Porque a tecnologia importa na conformidade legal

O RDL 8/2019 não exige um sistema tecnológico concreto, mas estabelece requisitos que na prática só podem ser garantidos com ferramentas digitais: registo diário com timestamp preciso, conservação durante quatro anos, acesso do trabalhador aos seus próprios dados e rastreabilidade completa de qualquer correção.

Um registo em papel pode perder-se, ser modificado sem deixar rasto ou não estar disponível quando um inspetor o solicitar. Uma folha de cálculo pode ser editada retroativamente sem que ninguém o detete. O CheckBiz360 foi concebido para que nenhuma dessas situações seja possível.

Este guia explica os mecanismos técnicos concretos com que a plataforma garante o cumprimento.

---

## Registo automático de timestamp

Sempre que um funcionário regista entrada ou saída a partir da aplicação do CheckBiz360, o sistema grava um **timestamp imediato com precisão ao segundo** nos servidores da plataforma. Este registo não exige qualquer ação adicional do manager nem do funcionário para além do próprio registo.

O timestamp gravado inclui:

- Data e hora exatas do evento.
- Identificação do funcionário.
- Tipo de evento (entrada, saída, pausa, retoma).
- Identificação do dispositivo a partir do qual o registo foi efetuado.
- Coordenadas GPS no momento do registo, se a geocerca estiver configurada.

Este registo é produzido no momento do registo e não pode ser modificado depois de criado.

---

## Armazenamento imutável do histórico

O CheckBiz360 garante a **imutabilidade do histórico de registos**. Isto significa que:

- Nenhum utilizador da plataforma, independentemente do seu perfil, pode eliminar um registo do histórico.
- Nenhum utilizador pode modificar os dados originais de um registo (hora, data, tipo de evento) sem que essa modificação fique gravada como uma correção manual separada.
- O histórico original é sempre conservado, mesmo quando se efetuam correções.

Este desenho é fundamental para a conformidade legal: se um inspetor solicitar os registos de um período, a empresa pode demonstrar não só que registos ocorreram, mas também se algum foi corrigido e por que razão.

---

## Rastreabilidade completa das correções manuais

Na operação diária, é habitual que os managers precisem de corrigir registos errados: um funcionário esqueceu-se de registar a saída, ocorreu um erro técnico pontual ou um registo de uma jornada especial exige ajuste.

O CheckBiz360 permite efetuar estas correções, mas com uma condição: **toda a correção manual fica gravada com plena rastreabilidade**. Para cada correção, o sistema armazena:

- O valor original do registo antes da correção.
- O novo valor introduzido pelo responsável.
- A identidade do utilizador que efetuou a correção (nome e perfil).
- A data e hora em que a correção foi efetuada.
- O motivo da correção, que o responsável tem obrigatoriamente de introduzir.

Além disso, uma correção sobre um registo existente **não é aplicada até que o funcionário a aceite**. Se a aceitar, a hora corrigida é a que figura no relatório de registo de jornada. Se a recusar, o registo conserva o seu valor original —continua a contar no registo de jornada— e a recusa fica anotada com o seu motivo. Nenhuma correção pode ter uma data ou hora futura.

Esta rastreabilidade satisfaz o requisito de integridade do registo que a regulamentação exige e que a Inspeção do Trabalho verifica nas suas atuações.

---

## Acesso do funcionário ao seu próprio histórico

O RDL 8/2019 estabelece o direito do trabalhador a consultar os seus próprios registos. No CheckBiz360, este direito é satisfeito de forma direta: **cada funcionário pode consultar o seu histórico completo de registos a partir da aplicação móvel**, sem necessidade de o solicitar a qualquer responsável.

O funcionário vê na sua aplicação:

- Todos os seus registos de entrada e saída, com timestamp exato.
- O estado de validação de cada registo.
- As correções que tenham sido efetuadas sobre os seus registos, com a data da correção.

Este acesso é permanente e em tempo real. Não exige que o manager exporte qualquer ficheiro nem faça qualquer gestão.

---

## Porque o registo em papel e as folhas de cálculo não oferecem as mesmas garantias

A Inspeção do Trabalho questionou em múltiplas atuações a validade de sistemas de registo baseados em papel ou em folhas de cálculo editáveis. As razões são técnicas e jurídicas:

| Aspeto | Registo em papel | Folha de cálculo | CheckBiz360 |
|---|---|---|---|
| Imutabilidade | Não garantida | Não garantida | Garantida por conceção |
| Rastreabilidade de correções | Impossível | Impossível sem auditoria ativa | Automática e íntegra |
| Acesso do trabalhador | Depende de processo manual | Depende de processo manual | Acesso direto a partir da aplicação |
| Conservação por quatro anos | Risco de perda ou deterioração | Risco de perda ou eliminação | Conservação em servidores geridos |
| Timestamp preciso | Exige disciplina manual | Exige disciplina manual | Automático no momento do registo |

Quando a ITSS deteta que uma empresa usa folhas de cálculo editáveis como único sistema de registo, pode considerar que não existe um sistema de registo fiável e levantar auto de infração ainda que os dados pareçam completos.

---

## Período de conservação garantido

O CheckBiz360 conserva todos os registos de jornada durante o período mínimo exigido pelo RDL 8/2019 (**quatro anos**). A empresa não precisa de efetuar qualquer gestão para cumprir este requisito enquanto mantiver a conta ativa.

> **Aviso:** se a empresa decidir cancelar a sua conta no CheckBiz360, deve exportar todos os registos históricos antes do encerramento. A obrigação de conservação durante quatro anos recai sobre a empresa, não sobre o fornecedor. O CheckBiz360 não pode ser considerado responsável pela perda de registos históricos se a empresa não exportar os seus dados antes de encerrar a conta.

---

> **Nota:** este artigo descreve os mecanismos técnicos da plataforma em relação à conformidade legal. Para aconselhamento jurídico específico sobre a situação da sua empresa, consulte a sua consultoria laboral.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Registo de horários obrigatório em Espanha](./81-registo-de-horarios-obrigatorio-em-espanha.md) | O que exige o RDL 8/2019 e a quem se aplica |
| [Relatório de conformidade legal](../11-relatorios-e-exportacao/79-relatorio-de-conformidade-legal.md) | Como gerar o relatório para a Inspeção do Trabalho |
| [Conservação e proteção de dados](./83-conservacao-e-protecao-de-dados.md) | Bases legais do tratamento de dados de funcionários |
| [Preparar uma inspeção do trabalho](./84-preparar-uma-inspecao-do-trabalho.md) | Guia prático perante uma visita da ITSS |
| [Deteção de anomalias](../07-inteligencia-operacional/55-detecao-de-anomalias.md) | Como o sistema deteta padrões irregulares de registo |
