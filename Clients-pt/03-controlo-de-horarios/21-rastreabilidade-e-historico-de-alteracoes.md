# Rastreabilidade e histórico de alterações

Cada registo no CheckBiz360 tem associado um registo completo e imutável de todas as modificações que foram efetuadas sobre ele desde a sua criação. Este histórico de alterações é a base do sistema de auditoria do controlo de assiduidade e permite demonstrar, perante qualquer inspeção ou revisão interna, quem realizou cada alteração, quando e sobre que dados.

---

## O que é o histórico de alterações

O histórico de alterações é um registo associado a cada registo de assiduidade que armazena de forma cronológica todas as intervenções que modificaram esse registo. Cada elemento representa uma ação concreta e contém toda a informação necessária para reconstruir o histórico completo do registo.

Ao contrário de outros dados do sistema que podem ser editados, o histórico de alterações é **imutável**. As entradas não podem ser modificadas nem eliminadas depois de gravadas. Isto garante a integridade do histórico e a sua validade como prova documental.

---

## Estrutura de cada entrada do histórico

Cada registo no histórico de alterações contém os seguintes campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único da entrada de auditoria |
| Data e hora | Timestamp exato do momento em que a alteração foi efetuada |
| Ação | Tipo de modificação realizada (ver tabela de ações) |
| UID do utilizador | Identificador do utilizador que executou a ação |
| Estado anterior | Dados do registo antes da alteração |
| Estado novo | Dados do registo após a alteração |

### Tipos de ação registados

| Ação | Significado |
|---|---|
| `created` | Criação do registo original pelo funcionário |
| `updated` | Modificação de um dado do registo por um responsável |
| `edited` | Proposta de correção de um responsável, pendente de que o funcionário a aceite |
| `rejected` | O funcionário recusou uma proposta de correção; inclui o motivo, e o registo conserva os seus dados anteriores |
| `manual_request_created` | Criação de jornada completa manual (Modo A) |
| `manual_checkout_created` | Criação de saída manual sobre entrada em aberto (Modo B) |

---

## Porque é que o histórico é imutável

A imutabilidade do histórico de alterações responde a duas necessidades fundamentais:

**Integridade do dado:** uma vez registada uma ação, não pode ser alterada. Isto significa que o histórico reflete fielmente o que aconteceu, sem possibilidade de reescrita posterior.

**Valor probatório:** no âmbito laboral, os registos de controlo de horários têm valor como prova perante a Inspeção do Trabalho. Um histórico imutável e rastreável é a garantia de que o dado não foi manipulado depois do facto. Se um registo for modificado posteriormente, o histórico mostra tanto o dado original como o modificado, e quem efetuou a alteração.

---

## Como ver o histórico de alterações de um registo

1. Aceda ao backoffice com perfil **manager** ou **owner**.
2. Navegue até à secção **Assiduidade** do funcionário correspondente.
3. Selecione o registo ou jornada cujo histórico pretende rever.
4. Abra o separador ou secção **Histórico de alterações** ou **Auditoria**.
5. O sistema mostrará todas as entradas do histórico de alterações por ordem cronológica, com os detalhes de cada ação.

Cada entrada mostra o nome ou identificador do utilizador que efetuou a alteração, a data e hora exatas, a ação executada e os valores anteriores e posteriores dos campos modificados.

---

## Caso de utilização legal: inspeção do trabalho

Perante uma inspeção do trabalho, a empresa pode precisar de demonstrar que os registos de assiduidade estão íntegros, não foram alterados de forma fraudulenta e refletem fielmente a jornada real dos funcionários.

Com o CheckBiz360, o responsável pode aceder ao histórico de qualquer registo e mostrar:

- Quem registou originalmente e a partir de que dispositivo.
- Se um responsável efetuou alguma modificação posterior, quando e com que motivo.
- Se o funcionário validou ou recusou alguma jornada manual ou alguma correção, e com que motivo.
- Que dados tinha o registo antes e depois de qualquer alteração.

Esta rastreabilidade completa cobre os requisitos de conservação e transparência exigidos pela regulamentação de registo de horários em vigor.

---

## Exportação do histórico para auditorias

O histórico de alterações pode ser exportado a partir do backoffice para utilização em auditorias internas ou perante pedidos da Inspeção do Trabalho.

1. A partir da vista de assiduidade ou do relatório de auditoria, selecione o intervalo de datas e os funcionários a incluir.
2. Escolha o formato de exportação disponível (PDF, CSV ou outros, consoante a configuração da entidade).
3. Descarregue o ficheiro gerado.

O documento exportado inclui, para cada registo, tanto os dados do registo como o histórico completo de intervenções.

---

> **Nota de conformidade:** a legislação espanhola (Real Decreto-Lei 8/2019) obriga as empresas a conservar os registos de jornada durante quatro anos e a colocá-los à disposição da Inspeção do Trabalho quando forem solicitados. O sistema de rastreabilidade do CheckBiz360 foi concebido para dar cumprimento a este requisito.

---

## Perfis com acesso a esta funcionalidade

A consulta do histórico de alterações está disponível para os perfis **manager** e **owner**. Os funcionários não têm acesso direto ao histórico técnico de auditoria, embora possam ver o estado atual dos seus registos e as notificações de alterações que os afetam.

---

## Artigos relacionados

- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
- [Revisão e validação de registos](20-revisao-e-validacao-de-registos.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
