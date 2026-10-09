# Pausas e descansos

O CheckBiz360 permite registar os períodos de descanso dentro da jornada de trabalho de forma precisa. As pausas distinguem-se do fim de jornada porque não fecham o turno ativo: o funcionário continua em jornada, mas o tempo de pausa é descontado do cômputo de horas trabalhadas. Este artigo explica como funcionam as pausas, como registá-las e como configurá-las por sucursal.

---

## Tipos de evento de pausa

O sistema utiliza dois tipos de registo específicos para gerir as pausas:

- **Restin (`restin`):** marca o início de uma pausa. O funcionário abandona temporariamente o seu posto de trabalho.
- **Restout (`restout`):** marca o fim da pausa. O funcionário retoma a sua atividade.

Ambos os eventos ficam gravados no histórico de assiduidade do funcionário com o respetivo timestamp, tal como os eventos de entrada e saída.

---

## Diferença entre pausa e fim de jornada

A distinção é importante para o cálculo de horas:

| Evento | Efeito na jornada |
|---|---|
| `restin` (início de pausa) | A jornada mantém-se aberta. O tempo de pausa começa a ser contabilizado. |
| `restout` (fim de pausa) | A jornada continua. O tempo de pausa é fechado e descontado. |
| `checkout` (saída) | A jornada é fechada definitivamente. |

Se o funcionário registar um `checkout` sem ter fechado uma pausa ativa com `restout`, o sistema pode marcar a jornada como incompleta ou com incidência, consoante a configuração da sucursal.

As pausas e a saída pertencem à **jornada aberta**, e uma jornada não se reparte entre locais: iniciar uma pausa ou registar a saída numa sucursal diferente da da entrada é recusado com `checklog/different_branches`. Se o funcionário mudar de local a meio do dia, deve fechar a jornada no primeiro e abrir outra no segundo.

> **Nota:** as pausas deste artigo são as da **jornada** (controlo de horários). As pausas de uma **tarefa** são outra coisa: são explicadas em [Acompanhamento e atualizações de tarefas](../06-tarefas/43-acompanhamento-e-atualizacoes.md#pausar-e-retomar-uma-tarefa).

---

## Como registar uma pausa a partir da aplicação

### Iniciar uma pausa (restin)

1. No ecrã de assiduidade, prima o botão **Iniciar pausa**.
2. Confirme a ação, se o sistema o solicitar.
3. A aplicação mostrará que o funcionário está em pausa e registará a hora de início.

### Terminar uma pausa (restout)

1. No ecrã de assiduidade, prima o botão **Terminar pausa**.
2. A aplicação confirmará a retoma da jornada e mostrará o tempo de pausa decorrido.

O ecrã principal de assiduidade reflete a todo o momento se o funcionário está em jornada ativa ou em pausa.

No cartão de informação laboral, o descanso é mostrado consoante a modalidade: com **descanso estrito** aparecem os minutos que são descontados; com **descanso flexível** aparece «Flexível», porque se contabiliza o que o funcionário marcar (a partir da versão 1.3.2 da aplicação).

---

## As pausas no histórico de assiduidade

Cada evento de pausa fica guardado no histórico de assiduidade do funcionário com:

- Tipo de evento (`restin` ou `restout`).
- Timestamp exato do registo.
- Estado de validação (válido ou falhado).
- Dados de geolocalização, se se aplicar a validação de geocerca.

O responsável pode consultar o detalhe de pausas de qualquer funcionário a partir do backoffice, incluindo a duração total de pausas por jornada.

---

## Configuração de pausas por sucursal

As pausas podem ser configuradas com diferentes parâmetros ao nível da sucursal:

### Desativar pausas

Se a operação da sucursal não contemplar pausas registadas, é possível desativar esta funcionalidade através da opção «desativar pausas». Quando está ativa, os botões de pausa não aparecem na aplicação para os funcionários dessa sucursal e os eventos `restin`/`restout` não são processados.

### Duração padrão de pausa

O campo «duração padrão de pausa» permite definir uma duração padrão de pausa em minutos. Este valor é utilizado como referência para o cálculo automático de pausas e pode ser usado nos relatórios para comparar a duração real dos descansos face ao tempo padrão estabelecido.

Para configurar estes parâmetros:

1. Aceda ao backoffice com perfil **manager** ou **owner**.
2. Navegue até **Sucursais** e selecione a sucursal correspondente.
3. Abra a secção de configuração de assiduidade.
4. Ajuste os campos «desativar pausas» e «duração padrão de pausa» consoante as suas necessidades.
5. Guarde as alterações.

---

## Desconto automático de pausas no cálculo de horas

O sistema desconta automaticamente o tempo de pausa do total de horas trabalhadas na jornada. O cálculo é o seguinte:

**Horas trabalhadas = (hora de saída - hora de entrada) - tempo total de pausas**

Se o funcionário tiver feito várias pausas durante a jornada, o sistema soma a duração de todas elas e desconta-as do total. Este cálculo fica disponível nos relatórios de assiduidade e no resumo de jornada do funcionário.

> **Aviso:** se um funcionário iniciar uma pausa com `restin` mas não a fechar com `restout` antes de registar a saída, o sistema pode gravar a pausa como não terminada. Nestes casos, o responsável deve rever e corrigir manualmente a jornada a partir do backoffice.

---

## Perfis com acesso a esta funcionalidade

O registo de pausas a partir da aplicação é uma ação disponível para todos os utilizadores com perfil **funcionário**. A configuração de pausas por sucursal («desativar pausas», «duração padrão de pausa») exige perfil **manager** ou **owner**.

---

## Artigos relacionados

- [Entrada e saída na aplicação](14-entrada-e-saida-na-aplicacao.md)
- [Como funciona o registo de ponto](13-como-funciona-o-registo-de-ponto.md)
- [Estados e códigos de erro](22-estados-e-codigos-de-erro.md)
- [Solicitar jornada manual](19-solicitar-jornada-manual.md)
