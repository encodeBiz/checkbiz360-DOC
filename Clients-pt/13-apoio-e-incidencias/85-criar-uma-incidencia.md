# Criar uma incidência

O módulo de incidências do CheckBiz360 é o canal formal de comunicação **dentro da sua organização** entre quem deteta um problema operacional e quem o pode resolver.

É importante não o confundir com o apoio técnico do CheckBiz360: uma incidência é um reporte interno —«não consegui registar à entrada», «o descanso ficou mal registado», «a geocerca desta sucursal está mal configurada»— dirigido a um responsável da própria empresa. Para problemas da plataforma em si, o canal é o apoio da EncodeBiz, descrito em [Contactar o apoio técnico](./87-contactar-o-apoio-tecnico.md).

---

## Para que serve

O módulo resolve um problema concreto: fazer com que as incidências operacionais deixem de ser resolvidas por WhatsApp ou de viva voz e passem a ficar registadas, com o seu histórico, junto aos dados de registo a que se referem.

Cada incidência reúne quem a reporta, sobre que sucursal, de que tipo é, e mantém um fio de respostas até ser marcada como resolvida.

---

## Campos de uma incidência

| Campo | Descrição |
|---|---|
| **Funcionário** | A pessoa a que a incidência se refere |
| **Sucursal** | O local de trabalho onde ocorreu |
| **Perfil de origem** | A partir de que nível é reportada: trabalhador ou supervisor |
| **Perfil de destino** | A que nível se dirige: trabalhador ou supervisor |
| **Tipo** | Registo de jornada, registo de descanso, configuração ou outro |
| **Estado** | Pendente, em revisão ou resolvida |
| **Comentário** | A descrição do problema |
| **Incluir localização** | Anexa as coordenadas a partir das quais é reportada, útil quando o problema tem a ver com a geocerca |

### Os quatro tipos de incidência

- **Registo de jornada** — problemas com a entrada ou a saída: não ficou registada, foi registada fora de horas, ficou uma jornada por fechar.
- **Registo de descanso** — problemas com o início ou o fim de uma pausa.
- **Configuração** — algo mal configurado que impede trabalhar com normalidade: geocerca demasiado estreita, horário que não corresponde, calendário por resolver.
- **Outro** — qualquer situação que não se enquadre nas anteriores.

---

## Como criar uma incidência a partir do backoffice

1. Aceda a **Incidências** no menu lateral.
2. Prima o botão de criar incidência.
3. Selecione o **funcionário** e a **sucursal** a que se refere.
4. Indique o **perfil de origem** e o **perfil de destino**.
5. Escolha o **tipo** que melhor descreve o problema.
6. Escreva o **comentário** com o detalhe: o que aconteceu, quando e com que frequência se repete. Quanto mais concreto, menos idas e vindas no fio.
7. Ative **incluir localização** se o problema tiver relação com o local onde o funcionário se encontra.
8. Guarde. A incidência nasce **em revisão**.

> **Sugestão:** ao descrever um problema de registo, inclua a data e a hora exatas e, se apareceu um código de erro no ecrã, copie-o literalmente. Com o código, o diagnóstico é imediato: consulte [Códigos de erro completos](../14-referencia/90-codigos-de-erro-completos.md).

---

## O que acontece depois

A incidência fica listada em **Incidências**, filtrável por estado, sucursal e funcionário. O responsável revê-a e **responde** a partir do seu detalhe; cada resposta pode ainda mudar o estado. A troca fica como um fio consultável.

Enquanto a incidência não estiver resolvida, continua a admitir respostas. Consulte [Acompanhamento e resolução de incidências](./86-acompanhamento-e-resolucao-de-incidencias.md).

---

## Nota de perfil

A gestão de incidências a partir do backoffice compete a **Owner** e **Manager**. Os perfis de origem e destino de cada incidência —trabalhador e supervisor— identificam as partes envolvidas no problema operacional, não quem administra o módulo.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Acompanhamento e resolução de incidências](./86-acompanhamento-e-resolucao-de-incidencias.md) | Estados, respostas e histórico de uma incidência |
| [Contactar o apoio técnico](./87-contactar-o-apoio-tecnico.md) | Canal com a equipa da EncodeBiz para problemas da plataforma |
| [Problemas frequentes e soluções](./88-problemas-frequentes-e-solucoes.md) | Diagnóstico das situações mais habituais |
| [Códigos de erro completos](../14-referencia/90-codigos-de-erro-completos.md) | Causa e solução de cada código |
| [Solicitar jornada manual](../03-controlo-de-horarios/19-solicitar-jornada-manual.md) | A via para corrigir um registo que não ficou gravado |
