# Ligar o RentmanBiz passo a passo

A ligação faz-se uma única vez, em cinco passos. Conte com uns dez minutos, mais o tempo que precisar para emparelhar a sua equipa.

> **Durante a fase beta**, a ativação é feita pela equipa da Encodebiz a partir dos dados que fornecer. O ecrã de autosserviço no backoffice está em desenvolvimento. Os passos são os mesmos e o resultado também.

## Passo 1 — Obter o token do Rentman

O token é a chave que permite ao CheckBiz360 falar com a sua conta Rentman.

1. Entre no Rentman com um utilizador administrador.
2. Vá a **Configuration → Account → Integrations**.
3. Crie um novo token de API e copie-o.

O token tem validade de dez anos. Recomendamos criá-lo a partir de um utilizador dedicado a integrações e não da conta pessoal de um colaborador: se essa pessoa sair, a sincronização deixaria de funcionar.

## Passo 2 — Introduzir o token no CheckBiz360

Cole-o no assistente. Ao guardar, o token é cifrado: a partir desse momento ninguém — nem a nossa equipa — o consegue voltar a ler. Se um dia precisar de o mudar, introduz-se um novo que substitui o anterior.

## Passo 3 — Confirmar a ligação

Antes de enviar seja o que for, a plataforma verifica que o token é válido e que consegue ler a sua equipa. Se algo falhar, verá o motivo exato. Os dois casos habituais:

| Mensagem | O que costuma significar |
|---|---|
| Token inválido | Foi copiado incompleto ou revogado no Rentman |
| Sem acesso aos dados | O utilizador que criou o token não tem permissões suficientes |

Não avance enquanto esta verificação não estiver correta.

## Passo 4 — Emparelhar a sua equipa

É o passo que exige mais atenção, e o que determina se as horas de uma pessoa chegam ou não ao Rentman.

O CheckBiz360 mostra duas listas: os seus colaboradores e os *crew members* do Rentman. Os pares cujo **e-mail coincide** são propostos automaticamente e o utilizador confirma ou corrige. Os restantes emparelham-se à mão.

**Um trabalhador sem emparelhar não gera horas no Rentman.** Não é um erro: simplesmente não há ficha do Rentman a que as lançar. Convém rever sempre que entra alguém novo.

## Passo 5 — Importar o catálogo

Com a ligação testada, a plataforma traz do Rentman a sua equipa, as suas montagens, os seus armazéns e as tarefas de cada função. Antes de escrever seja o que for mostra uma **pré-visualização** do que vai acontecer, e só corre quando o confirmar.

O que chegar incompleto — pessoas sem e-mail, centros sem coordenadas — é importado marcado como pendente e sem poder operar, não é descartado. Explicado em detalhe em [O que se importa e o que fica pendente](97-importacao-e-pendentes.md).

## Depois de ligar

A partir daí, cada jornada que se fecha é enviada para o Rentman no ciclo de sincronização seguinte, que corre a cada 15 minutos. Não espere ver os dados de imediato: se alguém acabou de registar a saída, as horas aparecem no Rentman nos minutos seguintes.

As jornadas **anteriores** à ligação não são enviadas indefinidamente para trás: a sincronização analisa os últimos sete dias. Se precisar de recuperar um período mais antigo, peça-o através de **Apoio**.

## Artigos relacionados

- [O que são as integrações](93-o-que-sao-as-integracoes.md)
- [Horas lançadas e avisos](96-horas-lancadas-e-avisos.md)
